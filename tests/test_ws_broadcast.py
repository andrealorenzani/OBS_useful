"""Push-channel correctness: an admin action becomes visible to a screen
client promptly, a fresh/reloaded screen client gets the full current state
on connect (not just future deltas), and two simultaneous screen clients
stay in sync (multi-client consistency)."""

from __future__ import annotations


def test_fresh_connection_receives_full_current_state_on_connect(client):
    speaker = client.post("/api/speakers", json={"name": "Ada"}).json()
    client.post("/api/live/speaker/left", json={"speaker_id": speaker["id"]})

    with client.websocket_connect("/ws/screen") as ws:
        snapshot = ws.receive_json()
        assert snapshot["speaker_left"]["name"] == "Ada"


def test_action_after_connect_is_broadcast_to_open_socket(client):
    speaker = client.post("/api/speakers", json={"name": "Alan"}).json()

    with client.websocket_connect("/ws/screen") as ws:
        initial = ws.receive_json()
        assert initial["speaker_right"] is None

        client.post("/api/live/speaker/right", json={"speaker_id": speaker["id"]})

        update = ws.receive_json()
        assert update["speaker_right"]["name"] == "Alan"


def test_two_simultaneous_clients_receive_identical_state(client):
    speaker = client.post("/api/speakers", json={"name": "Grace"}).json()

    with client.websocket_connect("/ws/screen") as ws_a, client.websocket_connect("/ws/screen") as ws_b:
        initial_a = ws_a.receive_json()
        initial_b = ws_b.receive_json()
        assert initial_a == initial_b

        client.post("/api/live/speaker/left", json={"speaker_id": speaker["id"]})

        update_a = ws_a.receive_json()
        update_b = ws_b.receive_json()
        assert update_a == update_b
        assert update_a["speaker_left"]["name"] == "Grace"
