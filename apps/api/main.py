from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from packages.neelastack.api.auth import router as auth_router
from packages.neelastack.api.chat import router as chat_router
from packages.neelastack.api.history import router as history_router
from packages.neelastack.api.conversations import router as conversations_router
from packages.neelastack.api.projects import router as projects_router
from packages.neelastack.api.workflows import router as workflows_router
from packages.neelastack.api.tools import router as tools_router
from packages.neelastack.api.mcp import router as mcp_router
from packages.neelastack.api.agents import router as agents_router

app = FastAPI(
    title="NEELASTACK API",
    version="0.1.0",
    description="Local-first AI platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=str)
@app.get("/api/v1/health", response_model=str)
def health():
    return "ok"


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
