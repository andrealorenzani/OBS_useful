"""Server-rendered HTML pages: prep pages, the single live-control page, and screen."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .. import storage
from ..templating import templates

router = APIRouter()


@router.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(url="/admin/live")


@router.get("/admin/live", response_class=HTMLResponse)
async def admin_live(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "admin/live.html",
        {
            "speakers": storage.list_speakers(),
            "conversations": storage.list_conversations(),
            "alarm_presets": storage.list_alarm_presets(),
            "platforms": ["x", "discord", "facebook", "whatsapp"],
        },
    )


@router.get("/admin/speakers", response_class=HTMLResponse)
async def admin_speakers(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "admin/speakers.html",
        {"speakers": storage.list_speakers()},
    )


@router.get("/admin/whatsapp", response_class=HTMLResponse)
async def admin_whatsapp(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "admin/whatsapp.html",
        {"conversations": storage.list_conversations()},
    )


@router.get("/admin/alarms", response_class=HTMLResponse)
async def admin_alarms(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "admin/alarms.html",
        {"alarm_presets": storage.list_alarm_presets()},
    )


@router.get("/screen", response_class=HTMLResponse)
async def screen_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "screen/screen.html", {})
