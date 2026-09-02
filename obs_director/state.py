"""The single authoritative live-screen state and its WebSocket broadcast channel.

``ScreenState`` is the flat, in-memory (not persisted) object describing exactly
what is currently showing on ``screen`` — one independent slot per effect family,
per the architecture's Deep Dive Q12 reconciliation. Every admin "live action"
mutates one slot (via the corresponding ``effects.*`` ``apply_*`` function) and
then the *entire* state is broadcast to every connected screen client, so a
reconnecting OBS Browser Source (or a fresh test tab) always resyncs correctly.

Implementation note (minor, documented deviation from the plan's literal
``@dataclass`` sketch): ``ScreenState`` is a Pydantic ``BaseModel`` rather than a
``dataclasses.dataclass``. Field shape and semantics are identical; the only
difference is a ``BaseModel`` gives us `.model_dump_json()` for free, which is
exactly what the WebSocket broadcaster needs, and avoids hand-writing a JSON
encoder for nested slot models.
"""

from __future__ import annotations

from fastapi import WebSocket
from pydantic import BaseModel

from .models import AlarmSlot, CommunityMessageSlot, SpeakerSlot, TimerSlot, WhatsAppSlot


class ScreenState(BaseModel):
    speaker_left: SpeakerSlot | None = None
    speaker_right: SpeakerSlot | None = None
    community_message: CommunityMessageSlot | None = None
    whatsapp: WhatsAppSlot | None = None
    timer_big: TimerSlot | None = None
    timer_corner: TimerSlot | None = None
    alarm: AlarmSlot | None = None


class ConnectionManager:
    """Tracks connected /ws/screen sockets and broadcasts full-state snapshots."""

    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, screen_state: ScreenState) -> None:
        payload = screen_state.model_dump_json()
        still_connected: list[WebSocket] = []
        for websocket in self.active:
            try:
                await websocket.send_text(payload)
                still_connected.append(websocket)
            except Exception:
                # Client went away without a clean disconnect handshake; drop it.
                pass
        self.active = still_connected


# Single process, single worker (per architecture): one module-level instance
# of the live state and its connection manager is the whole "server-side
# source of truth" the product spec calls for.
state = ScreenState()
manager = ConnectionManager()


async def broadcast_state() -> None:
    await manager.broadcast(state)


def reset_state() -> None:
    """Reset live state to a fresh, empty snapshot. Used by tests."""
    global state
    state = ScreenState()
