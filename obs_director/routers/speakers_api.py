"""Speaker roster CRUD (prep). Persisted via storage.py; independent of live state,
except that deleting a speaker currently showing clears that side (Deep Dive Q6)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import state as state_module
from .. import storage
from ..effects.speaker import apply_speaker_clear
from ..models import BannerStyle, Speaker

router = APIRouter(prefix="/api/speakers", tags=["speakers"])


class SpeakerCreate(BaseModel):
    name: str
    description: str | None = None
    banner_style: BannerStyle = "classic"
    image_path: str | None = None


class SpeakerUpdate(BaseModel):
    name: str
    description: str | None = None
    banner_style: BannerStyle = "classic"
    image_path: str | None = None


@router.get("", response_model=list[Speaker])
async def list_speakers() -> list[Speaker]:
    return storage.list_speakers()


@router.post("", response_model=Speaker, status_code=201)
async def create_speaker(payload: SpeakerCreate) -> Speaker:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    return storage.create_speaker(
        name, payload.description, banner_style=payload.banner_style, image_path=payload.image_path
    )


@router.put("/{speaker_id}", response_model=Speaker)
async def update_speaker(speaker_id: str, payload: SpeakerUpdate) -> Speaker:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    speaker = storage.update_speaker(
        speaker_id, name, payload.description, banner_style=payload.banner_style, image_path=payload.image_path
    )
    if speaker is None:
        raise HTTPException(status_code=404, detail="speaker not found")
    # Deep Dive Q6: editing does not live-update an already-showing banner.
    return speaker


@router.delete("/{speaker_id}", status_code=204)
async def delete_speaker(speaker_id: str) -> None:
    ok = storage.delete_speaker(speaker_id)
    if not ok:
        raise HTTPException(status_code=404, detail="speaker not found")

    # Deep Dive Q6: a speaker deleted while live on screen clears that side.
    changed = False
    if state_module.state.speaker_left is not None and state_module.state.speaker_left.speaker_id == speaker_id:
        apply_speaker_clear(state_module.state, "left")
        changed = True
    if state_module.state.speaker_right is not None and state_module.state.speaker_right.speaker_id == speaker_id:
        apply_speaker_clear(state_module.state, "right")
        changed = True
    if changed:
        await state_module.broadcast_state()
