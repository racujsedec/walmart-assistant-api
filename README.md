# Walmart Claude GCP Interview Lab — synthetic educational project

## Read first
See **[docs/ARCHITECTURE_AND_INTERVIEW.md](docs/ARCHITECTURE_AND_INTERVIEW.md)** for an exact 13-step request trace, component explanations, MCP, Kafka, streaming, LangSmith, Prometheus, security, testing, deployment, and role ownership.

The running core is a small end-to-end app: React → FastAPI → LangGraph → Anthropic Claude → Python tool → HTTPX → Order REST API → SQLAlchemy DB → tool result → Claude → React. Prompt is a real file at `backend/app/prompts/system.txt`.

## Local startup
Python 3.11 recommended.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Terminal 1
uvicorn order_service.main:app --port 8001
# Terminal 2
export PYTHONPATH=backend
export ANTHROPIC_API_KEY='YOUR_KEY'
uvicorn app.main:app --port 8000
# Terminal 3
cd frontend && npm install && npm run dev
```

Open Vite's URL; API docs: http://localhost:8000/docs and http://localhost:8001/docs. Local auth is a **stub**, not secure enterprise OIDC. See `.env.example` for config. Requires a real Anthropic key for live Claude calls.

## Tests
`PYTHONPATH=backend pytest -q` (requires dependencies).

## Scope
See the architecture guide for the difference between **implemented**, **optional sample code**, and **planned production integrations**. The refund/approval and hybrid Vertex retrieval workflows are documented designs, not runnable here.
