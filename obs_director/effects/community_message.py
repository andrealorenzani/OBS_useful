"""Community message effect.

Both authoring paths (free-text + platform style, or provider search-import —
the latter a v1 no-op stub per Deep Dive Q2) converge on the same
``CommunityMessageSlot`` shape and therefore the same rendering/animation
pathway on ``screen``.
"""

from __future__ import annotations

from pydantic import BaseModel

from ..models import CommunityMessageSlot, Platform
from ..state import ScreenState

PLATFORMS: tuple[str, ...] = ("x", "discord", "facebook", "whatsapp")


class CommunityMessagePayload(BaseModel):
    platform: Platform
    text: str
    author: str = "You"


def apply_community_message(
    state: ScreenState,
    platform: str,
    text: str,
    author: str = "You",
    avatar_url: str | None = None,
    timestamp_label: str | None = None,
) -> ScreenState:
    if platform not in PLATFORMS:
        raise ValueError(f"unsupported platform: {platform!r}")
    text = (text or "").strip()
    if not text:
        raise ValueError("community message text must not be empty")
    state.community_message = CommunityMessageSlot(
        platform=platform,
        author=author or "You",
        avatar_url=avatar_url,
        text=text,
        timestamp_label=timestamp_label,
    )
    return state


def apply_community_message_clear(state: ScreenState) -> ScreenState:
    state.community_message = None
    return state
