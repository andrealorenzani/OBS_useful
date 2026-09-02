"""FastAPI app factory: mounts static files, includes every router."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import (
    alarm_presets_api,
    community_api,
    live_api,
    pages,
    screen_ws,
    speakers_api,
    whatsapp_api,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    app = FastAPI(title="OBS_director")

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app.include_router(pages.router)
    app.include_router(speakers_api.router)
    app.include_router(whatsapp_api.router)
    app.include_router(alarm_presets_api.router)
    app.include_router(community_api.router)
    app.include_router(live_api.router)
    app.include_router(screen_ws.router)

    return app


app = create_app()
