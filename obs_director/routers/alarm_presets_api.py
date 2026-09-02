"""Alarm preset CRUD (prep, optional — Deep Dive Q9)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import storage
from ..models import AlarmPreset

router = APIRouter(prefix="/api/alarm-presets", tags=["alarm-presets"])


class AlarmPresetCreate(BaseModel):
    label: str


@router.get("", response_model=list[AlarmPreset])
async def list_alarm_presets() -> list[AlarmPreset]:
    return storage.list_alarm_presets()


@router.post("", response_model=AlarmPreset, status_code=201)
async def create_alarm_preset(payload: AlarmPresetCreate) -> AlarmPreset:
    label = payload.label.strip()
    if not label:
        raise HTTPException(status_code=400, detail="label is required")
    return storage.create_alarm_preset(label)


@router.delete("/{preset_id}", status_code=204)
async def delete_alarm_preset(preset_id: str) -> None:
    ok = storage.delete_alarm_preset(preset_id)
    if not ok:
        raise HTTPException(status_code=404, detail="alarm preset not found")
