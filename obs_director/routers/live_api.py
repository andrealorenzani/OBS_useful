"""The live-control action endpoints — one explicit route per action (Deep Dive Q10).

Every route here: (1) validates/looks up whatever it needs, (2) calls the
corresponding effect module's ``apply_*`` function against the single
module-level ``state.state``, then (3) broadcasts the resulting full state to
every connected screen client. All of ``admin/live.html``'s controls talk to
routes in this file exclusively.
"""

from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException

from .. import state as state_module
from .. import storage
from ..effects.alarm import AlarmTriggerPayload, apply_alarm_dismiss, apply_alarm_trigger
from ..effects.community_message import (
    CommunityMessagePayload,
    apply_community_message,
    apply_community_message_clear,
)
from ..effects.speaker import SpeakerSelectPayload, apply_speaker_clear, apply_speaker_select
from ..effects.timer import (
    TimerStartPayload,
    apply_timer_clear,
    apply_timer_pause,
    apply_timer_reset,
    apply_timer_start,
)
from ..effects.whatsapp import WhatsAppPlayPayload, apply_whatsapp_play, apply_whatsapp_stop
from ..models import Side, TimerSlotName

router = APIRouter(prefix="/api/live", tags=["live"])


def _now_ms() -> int:
    return int(time.time() * 1000)


# --- Speaker -----------------------------------------------------------------


@router.post("/speaker/{side}", status_code=204)
async def select_speaker(side: Side, payload: SpeakerSelectPayload) -> None:
    speaker = storage.get_speaker(payload.speaker_id)
    if speaker is None:
        raise HTTPException(status_code=404, detail="speaker not found")
    apply_speaker_select(state_module.state, side, speaker)
    await state_module.broadcast_state()


@router.delete("/speaker/{side}", status_code=204)
async def clear_speaker(side: Side) -> None:
    apply_speaker_clear(state_module.state, side)
    await state_module.broadcast_state()


# --- Community message ---------------------------------------------------------


@router.post("/community-message", status_code=204)
async def post_community_message(payload: CommunityMessagePayload) -> None:
    try:
        apply_community_message(state_module.state, payload.platform, payload.text, payload.author)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await state_module.broadcast_state()


@router.delete("/community-message", status_code=204)
async def clear_community_message() -> None:
    apply_community_message_clear(state_module.state)
    await state_module.broadcast_state()


# --- WhatsApp ------------------------------------------------------------------


@router.post("/whatsapp/play", status_code=204)
async def play_whatsapp(payload: WhatsAppPlayPayload) -> None:
    conversation = storage.get_conversation(payload.conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    apply_whatsapp_play(state_module.state, conversation, _now_ms())
    await state_module.broadcast_state()


@router.post("/whatsapp/stop", status_code=204)
async def stop_whatsapp() -> None:
    apply_whatsapp_stop(state_module.state)
    await state_module.broadcast_state()


# --- Timers ----------------------------------------------------------------------


@router.post("/timer/{which}/start", status_code=204)
async def start_timer(which: TimerSlotName, payload: TimerStartPayload) -> None:
    apply_timer_start(
        state_module.state,
        which,
        payload.start_seconds,
        payload.end_seconds,
        payload.position,
        _now_ms(),
        style=payload.style,
    )
    await state_module.broadcast_state()


@router.post("/timer/{which}/pause", status_code=204)
async def pause_timer(which: TimerSlotName) -> None:
    apply_timer_pause(state_module.state, which, _now_ms())
    await state_module.broadcast_state()


@router.post("/timer/{which}/reset", status_code=204)
async def reset_timer(which: TimerSlotName) -> None:
    apply_timer_reset(state_module.state, which, _now_ms())
    await state_module.broadcast_state()


@router.delete("/timer/{which}", status_code=204)
async def clear_timer(which: TimerSlotName) -> None:
    apply_timer_clear(state_module.state, which)
    await state_module.broadcast_state()


# --- Alarm -----------------------------------------------------------------------


@router.post("/alarm/trigger", status_code=204)
async def trigger_alarm(payload: AlarmTriggerPayload) -> None:
    apply_alarm_trigger(state_module.state, payload.label, payload.position)
    await state_module.broadcast_state()


@router.post("/alarm/dismiss", status_code=204)
async def dismiss_alarm() -> None:
    apply_alarm_dismiss(state_module.state)
    await state_module.broadcast_state()
