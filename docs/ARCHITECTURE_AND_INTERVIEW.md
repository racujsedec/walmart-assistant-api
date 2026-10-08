# Architecture, interfaces, and interview prep

## Explicitly implemented vs extension
- **Working core source**: React → Vite proxy → FastAPI/Pydantic → LangGraph → Anthropic Messages API → Python tool → HTTPX → separate FastAPI Order Service → SQLAlchemy → SQLite locally/PostgreSQL with DATABASE_URL → JSON → Claude second call → React. Requires Anthropic API key for live LLM test.
- **Examples/optional integrations**: prompt files, Kafka publisher, MCP server, OpenTelemetry configuration, SSE progress helper, local lexical policy search. These are deliberately not claimed as fully integrated production flows.
- **Production designs not implemented here**: enterprise OIDC/JWT verification, Cloud SQL IAM/connectors, Firestore LangGraph checkpointer, Vertex AI embeddings/vector search, true hybrid BM25 and reranking, Redis cache, refunds/approval execution, durable Kafka outbox, GKE Helm/Terraform, production secret management, actual monitoring dashboards.

## One request, exact boundaries
1. `frontend/src/main.tsx` React `fetch` sends `POST /api/v1/chat` with `message` and `conversation_id`.
2. `frontend/vite.config.ts` forwards `/api` to `http://localhost:8000`. Production uses ingress/reverse proxy.
3. `backend/app/main.py` receives `ChatRequest` validated by `schemas.py`; `auth.py` is a local-demo token stub, NOT production security.
4. `main.py` imports compiled `graph` from `graph.py`, calls `await graph.ainvoke(...)`.
5. `graph.py` agent calls `claude_client.ask_claude(messages)`. `claude_client.py` loads `prompts/system.txt`, passes `TOOLS` JSON schemas and `messages` to Anthropic SDK.
6. Claude returns a `tool_use` block with `id`, `name`, `input`; it has NOT executed Python or SQL.
7. Graph conditional edge routes to tools node, which extracts `input.order_id` and calls imported `order_tool.get_order_status`.
8. `order_tool.py` enforces `orders:read`, validates numeric ID with Pydantic, calls `order_client.fetch_order`.
9. `order_client.py` uses HTTPX GET to `ORDER_API_URL/orders/{id}`.
10. `order_service/main.py` defines `GET /orders/{order_id}`, uses SQLAlchemy `select(Order).where(Order.order_id == order_id)` with bound parameter; database URL chooses local SQLite or Cloud SQL PostgreSQL.
11. Domain API returns a broad JSON contract, including demo name/address. `order_tool.py` constructs `OrderResult` from ONLY order_id/status/estimated_delivery. This explicit allow-list drops other fields BEFORE they enter Claude context. Prefer narrower domain API in real production.
12. Graph appends Claude assistant `tool_use` and user `tool_result` messages (matching `tool_use_id`), routes back to agent; Claude returns grounded answer; graph ends.
13. FastAPI returns JSON; React updates state and displays answer.

## What React is / alternatives
React is a JavaScript UI library. A component is a function returning UI; state triggers re-render; `useState` tracks input and messages; event handlers submit; `fetch` invokes HTTP API. TypeScript adds compile-time type checking. Alternatives Vue, Angular, Svelte. React is NOT the Python backend or LLM.

## What MCP is / where it fits
Model Context Protocol standardizes discovery and invocation of tools/resources/prompts between an MCP client and MCP server. In this lab direct Python function calls are simplest. `mcp_server/server.py` illustrates wrapping the same authorized tool in an MCP server. For production, add per-user identity propagation, policy enforcement, transport authentication, input validation, network allowlists and audit logs; do NOT use the demo fixed permission. MCP does not replace Claude, LangGraph, HTTP, or authorization. Alternatives: direct Python functions, OpenAPI generated clients, custom RPC/gRPC.

## LangGraph vs LangSmith vs LangGraph Studio
LangGraph = workflow library (state, nodes, conditional edges, checkpoints). LangSmith = tracing/evaluation/datasets and debugging product. LangGraph Studio = developer graph inspection/debugging interface in the LangSmith tooling ecosystem. None is the LLM itself. Alternatives for workflow: Temporal, custom state machine, Prefect; tracing: OpenTelemetry/Cloud Trace, Langfuse, Phoenix.

## Prometheus and PromQL
Prometheus scrapes numeric time-series metrics, e.g. requests_total and latency histograms. PromQL queries those metrics, e.g. `sum(rate(http_requests_total[5m]))`. Grafana visualizes dashboards. GCP Cloud Monitoring can serve as managed monitoring; Managed Service for Prometheus supports Prometheus metrics. Do not conflate Prometheus with prompts or LangSmith.

## Kafka
Kafka is an event streaming platform. The user-facing request does NOT have to pass through Kafka. A successful synchronous chat can publish a sanitized `assistant.audit.v1` event after a tool action, consumed asynchronously by audit/analytics. For guaranteed delivery use a transactional outbox or durable publish/retry strategy; simple `produce`+`flush` alone is not exactly-once delivery. Alternatives Pub/Sub (GCP-native), RabbitMQ, Cloud Tasks; choose by semantics and operating cost.

## Streaming
Two distinct concepts: (1) Claude token streaming (Anthropic streaming API) and (2) server-to-browser streaming via SSE or WebSockets. `streaming.py` illustrates SSE **progress and final** events, NOT Anthropic token streaming. Production should propagate cancellation, auth, backpressure, proxies/timeouts, errors and reconnection. For one-way chat updates SSE is often simpler than WebSockets.

## Agents and tools
The implemented graph has one Claude agent and one tool executor, not five independent agents. Order, shipment, inventory, policy and case management are capabilities/tools; multiple specialized agents are an optional design, not automatic. A supervisor agent adds cost and complexity. Prefer deterministic routing for high-risk actions and simple tasks.

## Security interview checks
- Verify OIDC JWT issuer, audience, expiry and JWKS signature; never trust role from browser payload.
- Enforce row-level order entitlement in the domain API, not only `orders:read`.
- Validate schema and allowlist tools; prohibit arbitrary SQL execution.
- Treat tool/RAG text as untrusted prompt-injection surfaces.
- Minimize data returned to Claude; redact logs and traces; define retention policies.
- Require approval and server-side eligibility checks for refunds, cancellation and case updates; use idempotency keys.
- Store secrets in Secret Manager; use workload identity, least-privilege IAM and private network access.
- Validate output claims/citations and abstain when evidence is missing.

## QA and evaluation
Unit: Pydantic schema and transformation; integration: HTTPX-to-domain API; contract: JSON shape; functional: correct tool chosen; E2E: React-to-response; regression: golden set; negative: missing/bad ID; security: prompt injection/PII/IDOR; resilience: 404/timeout/429; performance: p95 latency and concurrent users; UAT: associate approval. LLM evaluation: tool accuracy, argument accuracy, retrieval recall, faithfulness, citation precision, task completion, abstention, latency, cost. Tools: pytest, respx, Postman/Newman, Playwright, Locust, Ragas, LangSmith.

## Claude Code in SDLC
Use Claude Code for codebase navigation, test generation, refactoring and PR assistance. Store scoped repo instructions in `CLAUDE.md`, review diffs, keep least-privilege command access, run CI, and do not give it production credentials. Claude Code is a coding assistant, not the runtime serving end-user chat.

## GCP deployment route
GitHub/GitLab PR → tests/quality/secret scan → Cloud Build → Docker → Artifact Registry → Helm deployment on GKE → readiness/liveness probes → smoke/UAT → progressive rollout → Cloud Logging/Monitoring/Trace. Terraform provisions GKE, Cloud SQL, IAM, Artifact Registry, Secret Manager, networking. Infrastructure templates in this lab are sketches, not a deployable secure cluster.

## Team responsibilities (illustrative, verify against real experience)
GenAI engineer: FastAPI contract, LangGraph state/tool nodes, Claude prompts, MCP wrapper, RAG integration, evaluation, observability. Domain teams: Order/Shipment/Returns services, PostgreSQL schema and row-level permissions. Frontend: React UI, accessibility, SSE progress. Security: IAM/OIDC/privacy reviews. Platform: GKE, CI/CD, network/secrets/alerts. Product/QA: acceptance criteria, golden cases, UAT. Never imply you personally owned a domain DB or platform unless you did.

## Advisory decision framework
For each use case: business value, deterministic vs GenAI necessity, data availability, privacy classification, allowed actions, required approvals, latency/cost targets, evaluation plan, rollback/owner. Recommend search/standard API instead of agentic LLM if deterministic lookup fully solves the problem.
