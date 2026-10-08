# Walmart Assistant API — educational two-repository code

This is **synthetic interview learning code**, not Walmart proprietary code and not a verified enterprise deployment. The uploaded study document describes a richer architecture; this repository implements a local runnable slice and marks production adapters explicitly.

## Local run (3 terminals)
From this directory:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DEMO_MODE=true LLM_MODE=mock
uvicorn order_service.main:app --port 8001 --reload
```
In a second terminal (same virtual environment and directory):
```bash
export DEMO_MODE=true LLM_MODE=mock
uvicorn app.main:app --port 8000 --reload
```
In frontend repo: `npm install && npm run dev`; open http://localhost:5173.
Run `pytest -q` from backend root.

## Follow the code like Cmd-click / Go to Definition
React `ChatWindow.tsx` → `useChatStream.ts` → HTTP `POST /api/v1/chat/stream` → `app/api/routes/chat.py:chat_stream` → `process` → `app/agents/graph.py:graph` → `app/agents/nodes/supervisor.py:call_claude` → `app/llm/claude_client.py:ask_claude` → `app/prompts/system.md` → Claude tool calls → `app/agents/nodes/execute_tools.py:execute_tools` → `app/tools/order.py:get_order_status` → `app/clients/order_api.py:fetch_order` → HTTP `GET /orders/12345` → `order_service/main.py:get_order` → SQLAlchemy → database. The return travels back through JSON, tool_result, supervisor, route, SSE and React.

Policy path: `execute_tools.py` → `tools/policy.py` → `rag/retrieve.py` → `rag/ingest.py` + `rag/keyword.py` + `rag/fusion.py` + `rag/rerank.py` + `rag/citations.py`. This is a **lexical local demonstration**, not live Vertex AI embedding/vector search.

Approval path: React `ApprovalCard.tsx` → HTTP `/api/v1/approvals/{id}/confirm` → `app/api/routes/chat.py:confirm` → `app/approvals/service.py:confirm_refund`. This marks a **demo-only approval** and does not move money.

## Important limitations
- Demo bearer token, synthetic data, SQLite, and deterministic mock Claude; **not production authentication**.
- Real Anthropic API optional: set `LLM_MODE=anthropic` and `ANTHROPIC_API_KEY`; model name must be one available to your account. Requires internet and credits.
- SSE sends progress + final, **not live token deltas**.
- Real MCP client, Kafka outbox/consumer, Redis integration, GCS/Vertex AI indexing, model-based reranking, Firestore checkpoints, GKE/Terraform deployment, and LangSmith/Ragas evaluations **are not fully integrated**. Files mark boundaries, not imaginary implementations.
- The Order Service is a local synthetic mock and does not enforce real service-to-service authentication. Do not expose publicly.
