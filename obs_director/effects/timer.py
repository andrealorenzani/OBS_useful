"""Timer effect: a single generalized "range timer" model.

One model covers both plain countdown-to-zero (``start=N, end=0``) and
counting between an arbitrary configured start/end (in either direction),
per the product acceptance criteria. ``value_at`` is a pure function
(independent of FastAPI/storage) so it's directly unit-testable, and the
same formula is mirrored client-side in ``static/screen/effects/timer.js``
for smooth per-frame ticking without the server pushing every second.
"""

from __future__ import annotations

from pydantic import BaseModel

from ..models import TimerPosition, TimerSlot, TimerSlotName
from ..state import ScreenState

_EPSILON = 1e-9


class TimerStartPayload(BaseModel):
    start_seconds: float
    end_seconds: float
    position: TimerPosition = "center"


def _direction(slot: TimerSlot) -> int:
    return 1 if slot.end_seconds >= slot.start_seconds else -1


def value_at(now_ms: int | float, slot: TimerSlot) -> float:
    """The timer's displayed value at wall-clock time ``now_ms``.

    ``displayed(now) = start + direction * elapsed``, clamped so it never
    passes ``end_seconds``. Elapsed time only accrues while ``running`` is
    True; ``paused_offset_seconds`` is however much elapsed time had already
    accrued as of the last pause/reset.
    """

    direction = _direction(slot)
    if slot.running:
        elapsed = slot.paused_offset_seconds + max(0.0, (now_ms - slot.anchor_epoch_ms) / 1000.0)
    else:
        elapsed = slot.paused_offset_seconds

    value = slot.start_seconds + direction * elapsed
    if direction == 1:
        value = min(value, slot.end_seconds)
    else:
        value = max(value, slot.end_seconds)
    return value


def is_complete(now_ms: int | float, slot: TimerSlot) -> bool:
    return abs(value_at(now_ms, slot) - slot.end_seconds) < _EPSILON


def _slot_attr(which: TimerSlotName) -> str:
    return f"timer_{which}"


def apply_timer_start(
    state: ScreenState,
    which: TimerSlotName,
    start_seconds: float,
    end_seconds: float,
    position: str,
    now_ms: int,
) -> ScreenState:
    slot = TimerSlot(
        start_seconds=start_seconds,
        end_seconds=end_seconds,
        anchor_epoch_ms=now_ms,
        paused_offset_seconds=0,
        running=True,
        position=position,
    )
    setattr(state, _slot_attr(which), slot)
    return state


def apply_timer_pause(state: ScreenState, which: TimerSlotName, now_ms: int) -> ScreenState:
    slot: TimerSlot | None = getattr(state, _slot_attr(which))
    if slot is not None and slot.running:
        elapsed = max(0.0, (now_ms - slot.anchor_epoch_ms) / 1000.0)
        slot.paused_offset_seconds += elapsed
        slot.running = False
        slot.anchor_epoch_ms = now_ms
    return state


def apply_timer_reset(state: ScreenState, which: TimerSlotName, now_ms: int) -> ScreenState:
    slot: TimerSlot | None = getattr(state, _slot_attr(which))
    if slot is not None:
        slot.paused_offset_seconds = 0
        slot.anchor_epoch_ms = now_ms
        slot.running = False
    return state


def apply_timer_clear(state: ScreenState, which: TimerSlotName) -> ScreenState:
    setattr(state, _slot_attr(which), None)
    return state
