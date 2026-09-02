"""Preset export/import as a single YAML file (Code changes §4)."""

from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from .. import presets_io
from .. import state as state_module

router = APIRouter(prefix="/api/presets", tags=["presets"])


@router.get("/export")
async def export_presets() -> Response:
    yaml_text = presets_io.export_presets()
    return Response(
        content=yaml_text,
        media_type="text/yaml",
        headers={"Content-Disposition": 'attachment; filename="obs_director_presets.yaml"'},
    )


@router.post("/import", response_model=presets_io.ImportSummary)
async def import_presets(file: UploadFile = File(...)) -> presets_io.ImportSummary:
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"file is not valid UTF-8 text: {exc}") from exc

    try:
        summary = presets_io.import_presets(text)
    except presets_io.PresetImportError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    await state_module.broadcast_state()
    return summary
