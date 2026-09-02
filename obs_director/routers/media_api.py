"""Serves an arbitrary local filesystem path as an HTTP response, so images
referenced by absolute path (a speaker's banner image, the community logo)
can be loaded into an `<img src>` on `screen` without exposing a raw
`file://` path to the browser.

**Deliberate, user-accepted security/trust tradeoff** (Architectural Impact,
Deep Dive Q16): this app's default bind is ``0.0.0.0`` (LAN-reachable), and
this endpoint will read and stream back *any* file on disk that exists, is a
regular file, and has an allow-listed image extension — with no additional
access restriction (no localhost-only check, no directory allow-list). Any
device on the same local network as the operator's machine could potentially
read arbitrary image-extension files off that machine by knowing/guessing
paths, and could probe path existence via 200 vs 404 responses. This matches
the app's existing "single local operator tool" trust model (see
``docs/architecture.md``'s security/trust-model note) and is not to be
"fixed" by adding restrictions later without an explicit product decision.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

router = APIRouter(tags=["media"])

# Conservative allow-list: only image extensions are ever served.
_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}


@router.get("/media")
async def get_media(path: str = Query(...)) -> FileResponse:
    candidate = Path(path)
    if candidate.suffix.lower() not in _ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=404, detail="unsupported file type")
    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(str(candidate))
