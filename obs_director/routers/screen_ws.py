"""GET /screen is served from pages.py; this module owns the push channel itself."""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .. import state as state_module

router = APIRouter()


@router.websocket("/ws/screen")
async def ws_screen(websocket: WebSocket) -> None:
    await state_module.manager.connect(websocket)
    try:
        # New connections (including a reconnecting/reloaded OBS Browser
        # Source) get the full current state immediately, not just future
        # deltas.
        await websocket.send_text(state_module.state.model_dump_json())
        while True:
            # screen clients are receive-only from the app's point of view;
            # just block until the socket closes.
            await websocket.receive_text()
    except WebSocketDisconnect:
        state_module.manager.disconnect(websocket)
