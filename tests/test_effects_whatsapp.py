"""Pure calculation tests for the WhatsApp reveal-count-from-elapsed-time
math (Deep Dive Q11), plus apply_whatsapp_play/stop state-transition tests."""

from __future__ import annotations

from obs_director.effects.whatsapp import (
    DEFAULT_MESSAGE_INTERVAL_MS,
    apply_whatsapp_play,
    apply_whatsapp_stop,
    reveal_count,
)
from obs_director.models import WhatsAppConversation, WhatsAppMessage
from obs_director.state import ScreenState


def _conversation(n_messages=3):
    messages = [
        WhatsAppMessage(id=f"m{i}", order_index=i, direction="left" if i % 2 == 0 else "right", body=f"msg {i}")
        for i in range(n_messages)
    ]
    return WhatsAppConversation(id="c1", name="Convo", created_at="now", messages=messages)


def test_reveal_count_at_time_zero_shows_first_message():
    assert reveal_count(0, 1500, total_messages=5) == 1


def test_reveal_count_advances_one_per_interval():
    assert reveal_count(1499, 1500, total_messages=5) == 1
    assert reveal_count(1500, 1500, total_messages=5) == 2
    assert reveal_count(3000, 1500, total_messages=5) == 3


def test_reveal_count_clamped_at_total():
    assert reveal_count(999_999, 1500, total_messages=5) == 5


def test_reveal_count_empty_conversation_is_zero():
    assert reveal_count(999_999, 1500, total_messages=0) == 0


def test_reveal_count_negative_elapsed_treated_as_zero():
    assert reveal_count(-500, 1500, total_messages=5) == 1


def test_apply_whatsapp_play_snapshots_messages_in_authored_order():
    state = ScreenState()
    convo = _conversation(3)
    apply_whatsapp_play(state, convo, now_ms=12345)

    assert state.whatsapp.conversation_id == "c1"
    assert state.whatsapp.started_at_epoch_ms == 12345
    assert state.whatsapp.message_interval_ms == DEFAULT_MESSAGE_INTERVAL_MS
    assert [m.body for m in state.whatsapp.messages] == ["msg 0", "msg 1", "msg 2"]
    assert state.whatsapp.messages[0].direction == "left"
    assert state.whatsapp.messages[1].direction == "right"


def test_apply_whatsapp_play_sorts_by_order_index_even_if_stored_out_of_order():
    state = ScreenState()
    messages = [
        WhatsAppMessage(id="b", order_index=1, direction="right", body="second"),
        WhatsAppMessage(id="a", order_index=0, direction="left", body="first"),
    ]
    convo = WhatsAppConversation(id="c2", name="Out of order", created_at="now", messages=messages)
    apply_whatsapp_play(state, convo, now_ms=0)
    assert [m.body for m in state.whatsapp.messages] == ["first", "second"]


def test_apply_whatsapp_stop_clears_slot():
    state = ScreenState()
    apply_whatsapp_play(state, _conversation(1), now_ms=0)
    assert state.whatsapp is not None
    apply_whatsapp_stop(state)
    assert state.whatsapp is None


def test_empty_conversation_does_not_crash():
    state = ScreenState()
    convo = _conversation(0)
    apply_whatsapp_play(state, convo, now_ms=0)
    assert state.whatsapp.messages == []
    assert reveal_count(5000, 1500, total_messages=len(state.whatsapp.messages)) == 0
