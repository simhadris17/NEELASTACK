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
5. If you started the API with Docker Compose, do not start a second local API on port 8000. Otherwise run: `python -m uvicorn apps.api.main:app --reload --port 8000` (or use `scripts\dev.cmd`, which detects an already-running API).
6. Open http://127.0.0.1:8000/docs
7. Run the web app from `frontend/web`.

No paid API is required for the default Ollama path.

## Providers and voice

Chat uses the configured provider and retries/falls back through `PROVIDER_FALLBACKS`. OpenAI and Groq use their OpenAI-compatible chat APIs when keys are supplied. Without a reachable Ollama server or hosted keys, chat returns an explicit provider error rather than pretending to work.

Voice is server-side at `/api/v1/voice/transcribe` and `/api/v1/voice/synthesize`. OpenAI/Groq STT require their respective keys. Offline STT requires a `whisper` executable (or `WHISPER_COMMAND`); offline TTS requires `espeak`/`espeak-ng` or optional `pyttsx3`. Browser speech remains a client fallback.

## Jobs, load tests, and mobile

`POST /api/v1/jobs` queues durable `echo`, `chat`, `stt`, and `tts` jobs in the database; run `python -m apps.worker.main` to process them. Jobs expose status, progress, retries, cancellation, and results. Redis is optional for the queue and is used for shared rate limiting when reachable.

Measure, rather than assume, capacity with `python tests/load/run_load_test.py --connections 1000`. Reports explicitly record observations and make no 1000-connection capacity claim. The Expo scaffold is in `frontend/mobile`; set `EXPO_PUBLIC_API_URL` before starting it.