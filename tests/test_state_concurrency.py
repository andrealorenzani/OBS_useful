"""Cross-cutting concurrency scenario: at minimum, speaker banner(s),
community message, timer(s) and alarm can all be visible at the same time
as independent, non-interfering slots — with the WhatsApp simulator's
full-screen takeover preserving (not clearing) everything underneath it
(Deep Dive Q8)."""

from __future__ import annotations

from obs_director.effects.alarm import apply_alarm_trigger
from obs_director.effects.community_message import apply_community_message
from obs_director.effects.speaker import apply_speaker_select
from obs_director.effects.timer import apply_timer_start
from obs_director.effects.whatsapp import apply_whatsapp_play, apply_whatsapp_stop
from obs_director.models import Speaker, WhatsAppConversation, WhatsAppMessage
from obs_director.state import ScreenState


def _fully_loaded_state() -> ScreenState:
    state = ScreenState()
    apply_speaker_select(state, "left", Speaker(id="a", name="Ada", created_at="now"))
    apply_speaker_select(state, "right", Speaker(id="b", name="Alan", created_at="now"))
    apply_community_message(state, "x", "hello world", author="Someone")
    apply_timer_start(state, "big", 60, 0, "center", now_ms=0)
    apply_timer_start(state, "corner", 0, 300, "top-right", now_ms=0)
    apply_alarm_trigger(state, "ATTENTION", "top")
    return state


def test_all_five_families_can_be_active_simultaneously():
    state = _fully_loaded_state()
    assert state.speaker_left is not None
    assert state.speaker_right is not None
    assert state.community_message is not None
    assert state.timer_big is not None
    assert state.timer_corner is not None
    assert state.alarm is not None


def test_mutating_one_slot_does_not_affect_others():
    state = _fully_loaded_state()
    apply_speaker_select(state, "left", Speaker(id="c", name="Grace", created_at="now"))
    assert state.speaker_left.name == "Grace"
    # Nothing else moved.
    assert state.speaker_right.name == "Alan"
    assert state.community_message.text == "hello world"
    assert state.timer_big.start_seconds == 60
    assert state.timer_corner.start_seconds == 0
    assert state.alarm.label == "ATTENTION"


def test_whatsapp_takeover_preserves_other_effects_underneath():
    state = _fully_loaded_state()
    convo = WhatsAppConversation(
        id="c1",
        name="Chat",
        created_at="now",
        messages=[WhatsAppMessage(id="m1", order_index=0, direction="left", body="hi")],
    )
    apply_whatsapp_play(state, convo, now_ms=0)

    assert state.whatsapp is not None
    # Per Deep Dive Q8: other slots' state is preserved, only visually
    # covered by the client's z-index stack — not cleared server-side.
    assert state.speaker_left.name == "Ada"
    assert state.speaker_right.name == "Alan"
    assert state.community_message.text == "hello world"
    assert state.timer_big is not None
    assert state.timer_corner is not None
    assert state.alarm is not None


def test_stopping_whatsapp_reveals_everything_still_active_underneath():
    state = _fully_loaded_state()
    convo = WhatsAppConversation(id="c1", name="Chat", created_at="now", messages=[])
    apply_whatsapp_play(state, convo, now_ms=0)
    apply_whatsapp_stop(state)

    assert state.whatsapp is None
    assert state.speaker_left.name == "Ada"
    assert state.speaker_right.name == "Alan"
    assert state.community_message.text == "hello world"
    assert state.timer_big is not None
    assert state.timer_corner is not None
    assert state.alarm is not None
