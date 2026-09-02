"""Shared helper for translating a raw local filesystem path into the HTTP
URL that ``screen`` can put straight into an ``<img src>``.

Per Code changes §3: raw filesystem paths must never be exposed to the
browser as a ``file://`` src, and must never be broadcast over the WebSocket
as a bare path either. Both ``effects/speaker.py`` (speaker banner image) and
``effects/community_message.py`` (community logo) funnel through this one
function so the translation rule lives in exactly one place.
"""

from __future__ import annotations

from urllib.parse import quote


def media_url(path: str | None) -> str | None:
    """``None`` in, ``None`` out. Otherwise, ``/media?path=<urlencoded path>``,
    served by ``routers/media_api.py``."""

    if not path:
        return None
    return f"/media?path={quote(path, safe='')}"
