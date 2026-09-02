"""YAML export/import of "all presets" (Code changes §4).

Per explicit user decisions (Deep Dives Q1/Q2): export is a **full backup**
of every persisted entity family (speaker roster, WhatsApp conversations,
alarm presets, community branding), and import is a **full replace** of each
included category, always preceded by an automatic timestamped backup of the
current ``data/`` directory.

No new generic "Preset" entity is introduced (Deep Dive Q11) — existing
entities are simply bundled together for transfer. Any file reference inside
a bundled entity (a speaker's ``image_path``, the branding ``logo_path``) is
carried as the same full, absolute filesystem path it was exported with; this
module never copies or relocates the referenced file (Deep Dive Q7/Q12/Q13).
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from . import state as state_module
from . import storage
from .effects.speaker import apply_speaker_clear
from .effects.whatsapp import apply_whatsapp_stop
from .models import AlarmPreset, CommunityBranding, Speaker, WhatsAppConversation

SCHEMA_VERSION = 1


class PresetImportError(ValueError):
    """Raised on any malformed/invalid import input; routers turn this into
    an HTTP 400 with the message as the detail, rather than letting a raw
    parsing/validation exception leak."""


class PresetBundle(BaseModel):
    # Unknown top-level keys are rejected explicitly (Testing information:
    # "unknown top-level keys" must raise a clear validation error).
    model_config = ConfigDict(extra="forbid")

    schema_version: int = SCHEMA_VERSION
    speakers: list[Speaker] = Field(default_factory=list)
    whatsapp_conversations: list[WhatsAppConversation] = Field(default_factory=list)
    alarm_presets: list[AlarmPreset] = Field(default_factory=list)
    community_branding: CommunityBranding = Field(default_factory=CommunityBranding)


class ImportSummary(BaseModel):
    speakers: int
    whatsapp_conversations: int
    alarm_presets: int
    backup_dir: str
    cleared_live_slots: list[str] = Field(default_factory=list)


def export_presets(data_dir: Path | str | None = None) -> str:
    bundle = PresetBundle(
        schema_version=SCHEMA_VERSION,
        speakers=storage.list_speakers(data_dir),
        whatsapp_conversations=storage.list_conversations(data_dir),
        alarm_presets=storage.list_alarm_presets(data_dir),
        community_branding=storage.get_community_branding(data_dir),
    )
    return yaml.safe_dump(bundle.model_dump(mode="json"), sort_keys=False, allow_unicode=True)


def _backup_data_dir(data_dir: Path | str | None) -> Path:
    directory = storage._resolve_dir(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_dir = directory / "backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    for filename in (
        storage.SPEAKERS_FILE,
        storage.CONVERSATIONS_FILE,
        storage.ALARM_PRESETS_FILE,
        storage.COMMUNITY_BRANDING_FILE,
    ):
        src = directory / filename
        if src.exists():
            shutil.copy2(src, backup_dir / filename)
    return backup_dir


def _clear_stale_live_slots(bundle: PresetBundle) -> list[str]:
    """Per Acceptance criteria: because importing is a full replace, a
    currently-live speaker/conversation whose underlying id no longer exists
    post-import is cleared from the live screen. Purely additive/defensive —
    does not touch slots that still reference a surviving id."""

    speaker_ids = {s.id for s in bundle.speakers}
    conversation_ids = {c.id for c in bundle.whatsapp_conversations}
    cleared: list[str] = []
    state = state_module.state

    if state.speaker_left is not None and state.speaker_left.speaker_id not in speaker_ids:
        apply_speaker_clear(state, "left")
        cleared.append("speaker_left")

    if state.speaker_right is not None and state.speaker_right.speaker_id not in speaker_ids:
        apply_speaker_clear(state, "right")
        cleared.append("speaker_right")

    if state.whatsapp is not None and state.whatsapp.conversation_id not in conversation_ids:
        apply_whatsapp_stop(state)
        cleared.append("whatsapp")

    return cleared


def import_presets(yaml_text: str, data_dir: Path | str | None = None) -> ImportSummary:
    try:
        raw = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise PresetImportError(f"invalid YAML: {exc}") from exc

    if not isinstance(raw, dict):
        raise PresetImportError("preset file must be a YAML mapping at the top level")

    try:
        bundle = PresetBundle(**raw)
    except ValidationError as exc:
        raise PresetImportError(f"invalid preset file: {exc}") from exc

    # Validation succeeded: only now do we touch disk (backup, then replace).
    backup_dir = _backup_data_dir(data_dir)

    storage._save_raw(data_dir, storage.SPEAKERS_FILE, [s.model_dump() for s in bundle.speakers])
    storage._save_raw(
        data_dir, storage.CONVERSATIONS_FILE, [c.model_dump() for c in bundle.whatsapp_conversations]
    )
    storage._save_raw(data_dir, storage.ALARM_PRESETS_FILE, [p.model_dump() for p in bundle.alarm_presets])
    storage.save_community_branding(
        bundle.community_branding.logo_path, bundle.community_branding.accent_color, data_dir
    )

    cleared = _clear_stale_live_slots(bundle)

    return ImportSummary(
        speakers=len(bundle.speakers),
        whatsapp_conversations=len(bundle.whatsapp_conversations),
        alarm_presets=len(bundle.alarm_presets),
        backup_dir=str(backup_dir),
        cleared_live_slots=cleared,
    )
