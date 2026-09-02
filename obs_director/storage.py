"""JSON-file persistence for OBS_director.

Per the architect's decision (this repo has no concurrent-writer contention —
a single local operator tool), each entity family is a flat JSON file under
``data/``, loaded and rewritten in full on every prep-page edit. Every public
function takes an optional ``data_dir`` override so tests can point them at a
temporary directory instead of the real ``data/`` folder.

Kept as plain functions (not classes) per the architecture doc.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings
from .models import AlarmPreset, CommunityBranding, Speaker, WhatsAppConversation, WhatsAppMessage

SPEAKERS_FILE = "speakers.json"
CONVERSATIONS_FILE = "conversations.json"
ALARM_PRESETS_FILE = "alarm_presets.json"
COMMUNITY_BRANDING_FILE = "community_branding.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid.uuid4().hex


def _resolve_dir(data_dir: Path | str | None) -> Path:
    return Path(data_dir) if data_dir is not None else settings.data_dir


def _load_raw(data_dir: Path | str | None, filename: str) -> list[dict]:
    path = _resolve_dir(data_dir) / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return []
    return json.loads(content)


def _save_raw(data_dir: Path | str | None, filename: str, items: list[dict]) -> None:
    directory = _resolve_dir(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ---------------------------------------------------------------------------
# Speakers
# ---------------------------------------------------------------------------


def list_speakers(data_dir: Path | str | None = None) -> list[Speaker]:
    return [Speaker(**raw) for raw in _load_raw(data_dir, SPEAKERS_FILE)]


def get_speaker(speaker_id: str, data_dir: Path | str | None = None) -> Speaker | None:
    for speaker in list_speakers(data_dir):
        if speaker.id == speaker_id:
            return speaker
    return None


def create_speaker(
    name: str,
    description: str | None = None,
    data_dir: Path | str | None = None,
    banner_style: str = "classic",
    image_path: str | None = None,
) -> Speaker:
    speaker = Speaker(
        id=_new_id(),
        name=name,
        description=description or None,
        created_at=_now_iso(),
        banner_style=banner_style,
        image_path=image_path or None,
    )
    items = _load_raw(data_dir, SPEAKERS_FILE)
    items.append(speaker.model_dump())
    _save_raw(data_dir, SPEAKERS_FILE, items)
    return speaker


def update_speaker(
    speaker_id: str,
    name: str,
    description: str | None = None,
    data_dir: Path | str | None = None,
    banner_style: str = "classic",
    image_path: str | None = None,
) -> Speaker | None:
    items = _load_raw(data_dir, SPEAKERS_FILE)
    updated: Speaker | None = None
    for raw in items:
        if raw["id"] == speaker_id:
            raw["name"] = name
            raw["description"] = description or None
            raw["banner_style"] = banner_style
            raw["image_path"] = image_path or None
            updated = Speaker(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, SPEAKERS_FILE, items)
    return updated


def delete_speaker(speaker_id: str, data_dir: Path | str | None = None) -> bool:
    items = _load_raw(data_dir, SPEAKERS_FILE)
    remaining = [raw for raw in items if raw["id"] != speaker_id]
    if len(remaining) == len(items):
        return False
    _save_raw(data_dir, SPEAKERS_FILE, remaining)
    return True


# ---------------------------------------------------------------------------
# WhatsApp conversations
# ---------------------------------------------------------------------------


def list_conversations(data_dir: Path | str | None = None) -> list[WhatsAppConversation]:
    return [WhatsAppConversation(**raw) for raw in _load_raw(data_dir, CONVERSATIONS_FILE)]


def get_conversation(conversation_id: str, data_dir: Path | str | None = None) -> WhatsAppConversation | None:
    for convo in list_conversations(data_dir):
        if convo.id == conversation_id:
            return convo
    return None


def create_conversation(name: str, data_dir: Path | str | None = None) -> WhatsAppConversation:
    convo = WhatsAppConversation(id=_new_id(), name=name, created_at=_now_iso(), messages=[])
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    items.append(convo.model_dump())
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return convo


def rename_conversation(conversation_id: str, name: str, data_dir: Path | str | None = None) -> WhatsAppConversation | None:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    updated: WhatsAppConversation | None = None
    for raw in items:
        if raw["id"] == conversation_id:
            raw["name"] = name
            updated = WhatsAppConversation(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return updated


def delete_conversation(conversation_id: str, data_dir: Path | str | None = None) -> bool:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    remaining = [raw for raw in items if raw["id"] != conversation_id]
    if len(remaining) == len(items):
        return False
    _save_raw(data_dir, CONVERSATIONS_FILE, remaining)
    return True


def add_message(
    conversation_id: str,
    direction: str,
    sender_name: str | None,
    body: str,
    timestamp_label: str | None,
    data_dir: Path | str | None = None,
) -> WhatsAppConversation | None:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    updated: WhatsAppConversation | None = None
    for raw in items:
        if raw["id"] == conversation_id:
            next_index = len(raw.get("messages", []))
            message = WhatsAppMessage(
                id=_new_id(),
                order_index=next_index,
                direction=direction,
                sender_name=sender_name or None,
                body=body,
                timestamp_label=timestamp_label or None,
            )
            raw.setdefault("messages", []).append(message.model_dump())
            updated = WhatsAppConversation(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return updated


def update_message(
    conversation_id: str,
    message_id: str,
    direction: str,
    sender_name: str | None,
    body: str,
    timestamp_label: str | None,
    data_dir: Path | str | None = None,
) -> WhatsAppConversation | None:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    updated: WhatsAppConversation | None = None
    for raw in items:
        if raw["id"] == conversation_id:
            found = False
            for msg in raw.get("messages", []):
                if msg["id"] == message_id:
                    msg["direction"] = direction
                    msg["sender_name"] = sender_name or None
                    msg["body"] = body
                    msg["timestamp_label"] = timestamp_label or None
                    found = True
                    break
            if found:
                updated = WhatsAppConversation(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return updated


def delete_message(conversation_id: str, message_id: str, data_dir: Path | str | None = None) -> WhatsAppConversation | None:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    updated: WhatsAppConversation | None = None
    for raw in items:
        if raw["id"] == conversation_id:
            before = len(raw.get("messages", []))
            raw["messages"] = [m for m in raw.get("messages", []) if m["id"] != message_id]
            if len(raw["messages"]) == before:
                break
            # Re-normalize order_index to stay contiguous after a deletion.
            for idx, msg in enumerate(raw["messages"]):
                msg["order_index"] = idx
            updated = WhatsAppConversation(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return updated


def reorder_messages(
    conversation_id: str,
    message_id_order: list[str],
    data_dir: Path | str | None = None,
) -> WhatsAppConversation | None:
    items = _load_raw(data_dir, CONVERSATIONS_FILE)
    updated: WhatsAppConversation | None = None
    for raw in items:
        if raw["id"] == conversation_id:
            by_id = {m["id"]: m for m in raw.get("messages", [])}
            if set(by_id.keys()) != set(message_id_order):
                # Reorder payload must reference exactly the existing messages.
                return None
            reordered = []
            for idx, message_id in enumerate(message_id_order):
                msg = by_id[message_id]
                msg["order_index"] = idx
                reordered.append(msg)
            raw["messages"] = reordered
            updated = WhatsAppConversation(**raw)
            break
    if updated is None:
        return None
    _save_raw(data_dir, CONVERSATIONS_FILE, items)
    return updated


# ---------------------------------------------------------------------------
# Alarm presets
# ---------------------------------------------------------------------------


def list_alarm_presets(data_dir: Path | str | None = None) -> list[AlarmPreset]:
    return [AlarmPreset(**raw) for raw in _load_raw(data_dir, ALARM_PRESETS_FILE)]


def get_alarm_preset(preset_id: str, data_dir: Path | str | None = None) -> AlarmPreset | None:
    for preset in list_alarm_presets(data_dir):
        if preset.id == preset_id:
            return preset
    return None


def create_alarm_preset(label: str, data_dir: Path | str | None = None) -> AlarmPreset:
    preset = AlarmPreset(id=_new_id(), label=label, created_at=_now_iso())
    items = _load_raw(data_dir, ALARM_PRESETS_FILE)
    items.append(preset.model_dump())
    _save_raw(data_dir, ALARM_PRESETS_FILE, items)
    return preset


def delete_alarm_preset(preset_id: str, data_dir: Path | str | None = None) -> bool:
    items = _load_raw(data_dir, ALARM_PRESETS_FILE)
    remaining = [raw for raw in items if raw["id"] != preset_id]
    if len(remaining) == len(items):
        return False
    _save_raw(data_dir, ALARM_PRESETS_FILE, remaining)
    return True


# ---------------------------------------------------------------------------
# Community branding (singleton)
# ---------------------------------------------------------------------------


def get_community_branding(data_dir: Path | str | None = None) -> CommunityBranding:
    """Returns the persisted branding singleton, or defaults when absent
    (Deep Dive Q5/Q9: one global logo + accent color, not per-message)."""

    path = _resolve_dir(data_dir) / COMMUNITY_BRANDING_FILE
    if not path.exists():
        return CommunityBranding()
    with path.open("r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return CommunityBranding()
    return CommunityBranding(**json.loads(content))


def save_community_branding(
    logo_path: str | None,
    accent_color: str,
    data_dir: Path | str | None = None,
) -> CommunityBranding:
    branding = CommunityBranding(logo_path=logo_path or None, accent_color=accent_color)
    directory = _resolve_dir(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / COMMUNITY_BRANDING_FILE
    with path.open("w", encoding="utf-8") as f:
        json.dump(branding.model_dump(), f, indent=2, ensure_ascii=False)
        f.write("\n")
    return branding
