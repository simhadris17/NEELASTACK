# NEELASTACK

Free-first, local-first AI engineering platform.

## Local stack
- Python 3.12 + FastAPI
- PostgreSQL + Redis
- Ollama (no mandatory hosted API key)
- React + TypeScript + Vite
- MCP-style local tool server/client
- RAG with local embeddings
- Docker Compose
- pytest / ruff
- Kubernetes / Terraform manifests

## Start
1. Install Python 3.12, Docker Desktop, Node.js and Ollama.
2. Copy `.env.example` to `.env`.
3. Run `docker compose up -d`.
4. Pull a local model: `ollama pull llama3.2`
5. Run: `python -m uvicorn apps.api.main:app --reload --port 8000`
6. Open http://127.0.0.1:8000/docs
7. Run the web app from `frontend/web`.

No paid API is required for the default Ollama path.
