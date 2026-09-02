from __future__ import annotations

from obs_director.effects.alarm import apply_alarm_dismiss, apply_alarm_trigger
from obs_director.state import ScreenState


def test_trigger_sets_alarm_slot():
    state = ScreenState()
    apply_alarm_trigger(state, "TECHNICAL ISSUE", "top")
    assert state.alarm is not None
    assert state.alarm.label == "TECHNICAL ISSUE"
    assert state.alarm.position == "top"


def test_trigger_with_no_label_uses_default_none():
    state = ScreenState()
    apply_alarm_trigger(state, None, "bottom")
    assert state.alarm.label is None
    assert state.alarm.position == "bottom"


def test_dismiss_clears_slot():
    state = ScreenState()
    apply_alarm_trigger(state, "x", "top")
    apply_alarm_dismiss(state)
    assert state.alarm is None


def test_triggering_while_already_active_is_idempotent_no_duplication():
    state = ScreenState()
    apply_alarm_trigger(state, "first", "top")
    apply_alarm_trigger(state, "first", "top")
    # A single slot can never hold two alarms; re-triggering just replaces
    # the one slot, which is what "never duplicates itself" means server-side.
    assert state.alarm.label == "first"
