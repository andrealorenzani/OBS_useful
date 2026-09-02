"""Community message effect.

Both authoring paths (free-text + platform style, or provider search-import —
the latter a v1 no-op stub per Deep Dive Q2) converge on the same
``CommunityMessageSlot`` shape and therefore the same rendering/animation
pathway on ``screen``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from .. import storage
from ..media import media_url
from ..models import CommunityBranding, CommunityMessageSlot, Platform
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
    branding: CommunityBranding | None = None,
    data_dir: Path | str | None = None,
) -> ScreenState:
    """``branding`` is read at post-time and baked into the slot (Code
    changes §2b) rather than broadcast on a separate channel. Pass an
    explicit ``branding`` in tests; callers going through the live-control
    router leave it ``None`` and it's loaded from ``storage`` (optionally
    scoped to ``data_dir``, e.g. for tests using an isolated data directory)."""

    if platform not in PLATFORMS:
        raise ValueError(f"unsupported platform: {platform!r}")
    text = (text or "").strip()
    if not text:
        raise ValueError("community message text must not be empty")
    if branding is None:
        branding = storage.get_community_branding(data_dir)
    state.community_message = CommunityMessageSlot(
        platform=platform,
        author=author or "You",
        avatar_url=avatar_url,
        text=text,
        timestamp_label=timestamp_label,
        logo_url=media_url(branding.logo_path),
        accent_color=branding.accent_color,
    )
    return state


def apply_community_message_clear(state: ScreenState) -> ScreenState:
    state.community_message = None
    return state
