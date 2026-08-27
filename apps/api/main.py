from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.middleware.trustedhost import TrustedHostMiddleware

from packages.neelastack.api.agents import router as agents_router
from packages.neelastack.api.auth import router as auth_router
from packages.neelastack.api.chat import router as chat_router
from packages.neelastack.api.conversations import router as conversations_router
from packages.neelastack.api.evaluations import router as evaluations_router
from packages.neelastack.api.files import router as files_router
from packages.neelastack.api.history import router as history_router
from packages.neelastack.api.jobs import router as jobs_router
from packages.neelastack.api.mcp import router as mcp_router
from packages.neelastack.api.observability import router as observability_router
from packages.neelastack.api.projects import router as projects_router
from packages.neelastack.api.rag import router as rag_router
from packages.neelastack.api.security import router as security_router
from packages.neelastack.api.tools import router as tools_router
from packages.neelastack.api.voice import router as voice_router
from packages.neelastack.api.workflows import router as workflows_router
from packages.neelastack.core.config import settings
from packages.neelastack.database.session import SessionLocal
from packages.neelastack.observability.state import metrics
from packages.neelastack.security.rate_limit import rate_limit_middleware

app = FastAPI(
    title="NEELASTACK API",
    version="0.1.0",
    description="Local-first AI platform API",
)
if settings.allowed_hosts != "*":
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_host_list)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(rate_limit_middleware)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            too_large = int(content_length) > settings.max_request_body_bytes
        except ValueError:
            too_large = False
        if too_large:
            return JSONResponse(status_code=413, content={"detail": "Request body is too large"})
    started = perf_counter()
    response = await call_next(request)
    metrics.observe(request.method, request.url.path, response.status_code, started)
    if settings.security_headers_enabled:
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(self), geolocation=()")
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
        if settings.hsts_enabled:
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    return response


@app.get("/health", response_model=str)
@app.get("/api/v1/health", response_model=str)
def health():
    return "ok"


@app.get("/health/ready")
@app.get("/api/v1/health/ready")
def readiness():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc
    finally:
        db.close()
    return {"status": "ready"}


def include_router_flat(router):
    for route in router.routes:
        app.router.routes.append(route)


include_router_flat(auth_router)
include_router_flat(chat_router)
include_router_flat(history_router)
include_router_flat(conversations_router)
include_router_flat(projects_router)
include_router_flat(agents_router)
include_router_flat(workflows_router)
include_router_flat(tools_router)
include_router_flat(mcp_router)
include_router_flat(files_router)
include_router_flat(rag_router)
include_router_flat(evaluations_router)
include_router_flat(observability_router)
include_router_flat(security_router)
include_router_flat(jobs_router)
include_router_flat(voice_router)

# Keep the original flat paths for compatibility while exposing a conventional
# versioned namespace for API clients.
for versioned_router in (
    auth_router,
    history_router,
    conversations_router,
    projects_router,
    agents_router,
    workflows_router,
    tools_router,
    mcp_router,
    files_router,
    rag_router,
    evaluations_router,
    observability_router,
    security_router,
    jobs_router,
    voice_router,
):
    app.include_router(versioned_router, prefix="/api/v1")
