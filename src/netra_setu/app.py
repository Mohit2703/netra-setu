"""FastAPI app factory — ADR 0010. Mounts each workstream's API router."""

from __future__ import annotations

from fastapi import FastAPI

from netra_setu.registry.api import router as registry_router
from netra_setu.security.api import router as security_router


def create_app() -> FastAPI:
    app = FastAPI(title="netra-setu", version="0.1.0")
    app.include_router(registry_router)
    app.include_router(security_router)
    return app


app = create_app()
