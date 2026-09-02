"""Pydantic models for OBS_director.

Two families of models live here:

- **Persisted entities** (``Speaker``, ``WhatsAppConversation``, ``WhatsAppMessage``,
  ``AlarmPreset``) — round-tripped to/from the JSON files in ``data/`` by ``storage.py``.
- **Live slot payloads** (``SpeakerSlot``, ``CommunityMessageSlot``, ``WhatsAppSlot``,
  ``TimerSlot``, ``AlarmSlot``) — the values held by ``ScreenState`` (see ``state.py``) and
  broadcast verbatim to every connected ``screen`` client.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Side = Literal["left", "right"]
TimerSlotName = Literal["big", "corner"]
TimerPosition = Literal["center", "top-right", "bottom-right"]
AlarmPosition = Literal["top", "bottom"]
Platform = Literal["x", "discord", "facebook", "whatsapp"]
MessageDirection = Literal["left", "right"]
BannerStyle = Literal["classic", "minimal", "glass", "bold", "outline"]
TimerStyle = Literal["solid", "glass", "outline", "text-only"]


# ---------------------------------------------------------------------------
# Persisted entities (data/*.json)
# ---------------------------------------------------------------------------


class Speaker(BaseModel):
    id: str
    name: str
    description: str | None = None
    created_at: str
    banner_style: BannerStyle = "classic"
    image_path: str | None = None


class WhatsAppMessage(BaseModel):
    id: str
    order_index: int
    direction: MessageDirection
    sender_name: str | None = None
    body: str
    timestamp_label: str | None = None


class WhatsAppConversation(BaseModel):
    id: str
    name: str
    created_at: str
    messages: list[WhatsAppMessage] = Field(default_factory=list)


class AlarmPreset(BaseModel):
    id: str
    label: str
    created_at: str


class CommunityBranding(BaseModel):
    """Global, persisted community-message branding (Deep Dive Q5/Q9): one
    logo + accent color shared by every community message, not per-message."""

    logo_path: str | None = None
    accent_color: str = "#5b8def"


# ---------------------------------------------------------------------------
# Live slot payloads (ScreenState)
# ---------------------------------------------------------------------------


class SpeakerSlot(BaseModel):
    speaker_id: str
    name: str
    description: str | None = None
    side: Side
    banner_style: BannerStyle = "classic"
    image_url: str | None = None


class CommunityMessageSlot(BaseModel):
    platform: Platform
    author: str
    avatar_url: str | None = None
    text: str
    timestamp_label: str | None = None
    logo_url: str | None = None
    accent_color: str = "#5b8def"


class WhatsAppMessageView(BaseModel):
    direction: MessageDirection
    sender_name: str | None = None
    body: str
    timestamp_label: str | None = None


class WhatsAppSlot(BaseModel):
    conversation_id: str
    messages: list[WhatsAppMessageView]
    started_at_epoch_ms: int
    message_interval_ms: int = 1500


class TimerSlot(BaseModel):
    start_seconds: float
    end_seconds: float
    anchor_epoch_ms: int
    paused_offset_seconds: float = 0
    running: bool = False
    position: TimerPosition = "center"
    style: TimerStyle = "solid"


class AlarmSlot(BaseModel):
    label: str | None = None
    position: AlarmPosition = "top"
