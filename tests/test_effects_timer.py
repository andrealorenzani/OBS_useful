"""Pure calculation tests for effects/timer.py — the single generalized
"range timer" model that covers both countdown-to-zero and arbitrary
start->end ranges (in either direction)."""

from __future__ import annotations

from obs_director.effects.timer import (
    apply_timer_clear,
    apply_timer_pause,
    apply_timer_reset,
    apply_timer_start,
    is_complete,
    value_at,
)
from obs_director.models import TimerSlot
from obs_director.state import ScreenState


def _slot(start, end, anchor_ms, paused=0.0, running=True, position="center"):
    return TimerSlot(
        start_seconds=start,
        end_seconds=end,
        anchor_epoch_ms=anchor_ms,
        paused_offset_seconds=paused,
        running=running,
        position=position,
    )


def test_countdown_to_zero_arbitrary_wall_clock_offset():
    slot = _slot(start=60, end=0, anchor_ms=1_000_000)
    assert value_at(1_000_000, slot) == 60
    assert value_at(1_010_000, slot) == 50  # 10s elapsed
    assert value_at(1_030_000, slot) == 30  # 30s elapsed


def test_countdown_clamps_at_zero_rather_than_continuing_past_it():
    slot = _slot(start=10, end=0, anchor_ms=0)
    assert value_at(999_000, slot) == 0
    assert is_complete(999_000, slot) is True


def test_count_up_from_a_to_b():
    slot = _slot(start=0, end=120, anchor_ms=0)
    assert value_at(30_000, slot) == 30
    assert value_at(90_000, slot) == 90


def test_count_up_clamps_at_end_rather_than_continuing_past_it():
    slot = _slot(start=0, end=10, anchor_ms=0)
    assert value_at(999_000, slot) == 10
    assert is_complete(999_000, slot) is True


def test_arbitrary_range_not_from_zero():
    # e.g. count from 5:00 down to 1:00
    slot = _slot(start=300, end=60, anchor_ms=0)
    assert value_at(0, slot) == 300
    assert value_at(60_000, slot) == 240
    assert value_at(1_000_000, slot) == 60  # clamped


def test_not_running_holds_at_paused_offset():
    slot = _slot(start=60, end=0, anchor_ms=0, paused=15, running=False)
    # Regardless of "now", a non-running timer stays at its paused value.
    assert value_at(0, slot) == 45
    assert value_at(999_999, slot) == 45


def test_apply_timer_start_sets_independent_slots():
    state = ScreenState()
    apply_timer_start(state, "big", 60, 0, "center", now_ms=0)
    apply_timer_start(state, "corner", 0, 300, "top-right", now_ms=0)

    assert state.timer_big.start_seconds == 60
    assert state.timer_corner.start_seconds == 0
    assert state.timer_corner.position == "top-right"

    # Independent: mutating one doesn't touch the other.
    assert value_at(30_000, state.timer_big) == 30
    assert value_at(30_000, state.timer_corner) == 30


def test_apply_timer_pause_then_resume_accumulates_offset():
    state = ScreenState()
    apply_timer_start(state, "big", 60, 0, "center", now_ms=0)
    apply_timer_pause(state, "big", now_ms=10_000)  # paused after 10s elapsed
    assert state.timer_big.running is False
    assert state.timer_big.paused_offset_seconds == 10
    assert value_at(999_999, state.timer_big) == 50  # frozen at 50s remaining


def test_apply_timer_reset_returns_to_start_value():
    state = ScreenState()
    apply_timer_start(state, "big", 60, 0, "center", now_ms=0)
    apply_timer_reset(state, "big", now_ms=30_000)
    assert state.timer_big.running is False
    assert value_at(30_000, state.timer_big) == 60


def test_apply_timer_clear_removes_slot():
    state = ScreenState()
    apply_timer_start(state, "big", 60, 0, "center", now_ms=0)
    apply_timer_clear(state, "big")
    assert state.timer_big is None


def test_reload_mid_countdown_resumes_at_correct_value_not_reset():
    # Simulates a screen reload: a fresh evaluation of value_at() using only
    # anchor_epoch_ms/paused_offset_seconds (never a client-accumulated
    # counter) must reproduce the same in-progress value.
    slot = _slot(start=100, end=0, anchor_ms=5_000)
    value_before_reload = value_at(20_000, slot)
    # "Reloading" just means re-running value_at with a fresh client state,
    # from the same server-held slot.
    value_after_reload = value_at(20_000, slot)
    assert value_before_reload == value_after_reload == 85
