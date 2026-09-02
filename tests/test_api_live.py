"""HTTP-level tests for the live-control action endpoints (/api/live/...)."""

from __future__ import annotations

from obs_director import state as state_module


def test_speaker_select_and_clear_per_side(client):
    speaker = client.post("/api/speakers", json={"name": "Ada"}).json()

    res = client.post("/api/live/speaker/left", json={"speaker_id": speaker["id"]})
    assert res.status_code == 204
    assert state_module.state.speaker_left.name == "Ada"
    assert state_module.state.speaker_right is None

    res = client.delete("/api/live/speaker/left")
    assert res.status_code == 204
    assert state_module.state.speaker_left is None


def test_speaker_select_unknown_id_is_404(client):
    res = client.post("/api/live/speaker/left", json={"speaker_id": "does-not-exist"})
    assert res.status_code == 404


def test_deleting_a_speaker_currently_live_clears_that_side(client):
    speaker = client.post("/api/speakers", json={"name": "Ada"}).json()
    client.post("/api/live/speaker/right", json={"speaker_id": speaker["id"]})
    assert state_module.state.speaker_right is not None

    res = client.delete(f"/api/speakers/{speaker['id']}")
    assert res.status_code == 204
    assert state_module.state.speaker_right is None


def test_editing_a_live_speaker_does_not_retroactively_change_screen(client):
    speaker = client.post("/api/speakers", json={"name": "Ada", "description": "Old title"}).json()
    client.post("/api/live/speaker/left", json={"speaker_id": speaker["id"]})

    client.put(f"/api/speakers/{speaker['id']}", json={"name": "Ada", "description": "New title"})

    # The already-showing banner keeps its snapshot from selection time.
    assert state_module.state.speaker_left.description == "Old title"


def test_community_message_post_and_clear(client):
    res = client.post(
        "/api/live/community-message", json={"platform": "discord", "text": "hello!", "author": "Op"}
    )
    assert res.status_code == 204
    assert state_module.state.community_message.text == "hello!"

    res = client.delete("/api/live/community-message")
    assert res.status_code == 204
    assert state_module.state.community_message is None


def test_community_message_rejects_empty_text(client):
    res = client.post("/api/live/community-message", json={"platform": "x", "text": "  ", "author": "Op"})
    assert res.status_code == 400


def test_whatsapp_play_and_stop(client):
    convo = client.post("/api/whatsapp/conversations", json={"name": "C"}).json()
    client.post(
        f"/api/whatsapp/conversations/{convo['id']}/messages",
        json={"direction": "left", "sender_name": "A", "body": "hi", "timestamp_label": None},
    )

    res = client.post("/api/live/whatsapp/play", json={"conversation_id": convo["id"]})
    assert res.status_code == 204
    assert state_module.state.whatsapp is not None
    assert state_module.state.whatsapp.conversation_id == convo["id"]

    res = client.post("/api/live/whatsapp/stop")
    assert res.status_code == 204
    assert state_module.state.whatsapp is None


def test_whatsapp_play_unknown_conversation_is_404(client):
    res = client.post("/api/live/whatsapp/play", json={"conversation_id": "nope"})
    assert res.status_code == 404


def test_timer_start_pause_reset_clear(client):
    res = client.post("/api/live/timer/big/start", json={"start_seconds": 60, "end_seconds": 0, "position": "center"})
    assert res.status_code == 204
    assert state_module.state.timer_big is not None
    assert state_module.state.timer_big.running is True

    res = client.post("/api/live/timer/big/pause")
    assert res.status_code == 204
    assert state_module.state.timer_big.running is False

    res = client.post("/api/live/timer/big/reset")
    assert res.status_code == 204
    assert state_module.state.timer_big.paused_offset_seconds == 0

    res = client.delete("/api/live/timer/big")
    assert res.status_code == 204
    assert state_module.state.timer_big is None


def test_big_and_corner_timers_run_independently(client):
    client.post("/api/live/timer/big/start", json={"start_seconds": 60, "end_seconds": 0, "position": "center"})
    client.post(
        "/api/live/timer/corner/start",
        json={"start_seconds": 0, "end_seconds": 300, "position": "top-right"},
    )
    assert state_module.state.timer_big.start_seconds == 60
    assert state_module.state.timer_corner.start_seconds == 0
    assert state_module.state.timer_corner.position == "top-right"

    client.delete("/api/live/timer/corner")
    assert state_module.state.timer_corner is None
    assert state_module.state.timer_big is not None  # untouched


def test_alarm_trigger_and_dismiss(client):
    res = client.post("/api/live/alarm/trigger", json={"label": "ISSUE", "position": "bottom"})
    assert res.status_code == 204
    assert state_module.state.alarm.label == "ISSUE"
    assert state_module.state.alarm.position == "bottom"

    res = client.post("/api/live/alarm/dismiss")
    assert res.status_code == 204
    assert state_module.state.alarm is None


def test_alarm_trigger_twice_does_not_duplicate(client):
    client.post("/api/live/alarm/trigger", json={"label": "A", "position": "top"})
    client.post("/api/live/alarm/trigger", json={"label": "A", "position": "top"})
    assert state_module.state.alarm.label == "A"  # single slot, no stacking possible
