"""Big red alarm effect.

Presence/absence of ``ScreenState.alarm`` is the active/dismissed toggle.
Audio (looping siren, Deep Dive Q3) is entirely a client concern —
``static/screen/effects/alarm.js`` starts/stops playback keyed off this
slot appearing/disappearing.
"""

from __future__ import annotations

from pydantic import BaseModel

from ..models import AlarmPosition, AlarmSlot
from ..state import ScreenState


class AlarmTriggerPayload(BaseModel):
    label: str | None = None
    position: AlarmPosition = "top"


def apply_alarm_trigger(state: ScreenState, label: str | None, position: str) -> ScreenState:
    state.alarm = AlarmSlot(label=label or None, position=position)
    return state


def apply_alarm_dismiss(state: ScreenState) -> ScreenState:
    state.alarm = None
    return state
