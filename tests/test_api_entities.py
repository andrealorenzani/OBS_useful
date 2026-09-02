"""HTTP-level CRUD tests for the prep-page REST endpoints (speakers,
whatsapp conversations/messages, alarm presets) — proves the routers wire
correctly onto storage.py, on top of the storage-level tests in
test_storage.py."""

from __future__ import annotations


def test_speaker_crud_roundtrip(client):
    res = client.post("/api/speakers", json={"name": "Ada", "description": "Mathematician"})
    assert res.status_code == 201
    speaker = res.json()

    listing = client.get("/api/speakers").json()
    assert any(s["id"] == speaker["id"] for s in listing)

    res = client.put(f"/api/speakers/{speaker['id']}", json={"name": "Ada L.", "description": None})
    assert res.status_code == 200
    assert res.json()["name"] == "Ada L."

    res = client.delete(f"/api/speakers/{speaker['id']}")
    assert res.status_code == 204
    assert client.delete(f"/api/speakers/{speaker['id']}").status_code == 404


def test_speaker_create_rejects_empty_name(client):
    res = client.post("/api/speakers", json={"name": "   "})
    assert res.status_code == 400


def test_whatsapp_conversation_and_message_crud(client):
    res = client.post("/api/whatsapp/conversations", json={"name": "Interview"})
    assert res.status_code == 201
    convo = res.json()

    res = client.post(
        f"/api/whatsapp/conversations/{convo['id']}/messages",
        json={"direction": "left", "sender_name": "Alex", "body": "Hi!", "timestamp_label": None},
    )
    assert res.status_code == 201
    convo = res.json()
    assert len(convo["messages"]) == 1
    message_id = convo["messages"][0]["id"]

    res = client.put(
        f"/api/whatsapp/conversations/{convo['id']}/messages/{message_id}",
        json={"direction": "left", "sender_name": "Alex", "body": "Hi there!", "timestamp_label": None},
    )
    assert res.status_code == 200
    assert res.json()["messages"][0]["body"] == "Hi there!"

    res = client.delete(f"/api/whatsapp/conversations/{convo['id']}/messages/{message_id}")
    assert res.status_code == 200
    assert res.json()["messages"] == []

    res = client.delete(f"/api/whatsapp/conversations/{convo['id']}")
    assert res.status_code == 204


def test_whatsapp_message_rejects_empty_body(client):
    convo = client.post("/api/whatsapp/conversations", json={"name": "X"}).json()
    res = client.post(
        f"/api/whatsapp/conversations/{convo['id']}/messages",
        json={"direction": "left", "sender_name": None, "body": "   ", "timestamp_label": None},
    )
    assert res.status_code == 400


def test_alarm_preset_crud(client):
    res = client.post("/api/alarm-presets", json={"label": "TECHNICAL ISSUE"})
    assert res.status_code == 201
    preset = res.json()

    listing = client.get("/api/alarm-presets").json()
    assert any(p["id"] == preset["id"] for p in listing)

    assert client.delete(f"/api/alarm-presets/{preset['id']}").status_code == 204
    assert client.delete(f"/api/alarm-presets/{preset['id']}").status_code == 404


def test_community_search_returns_empty_without_error(client):
    # Deep Dive Q2: v1 ships no concrete provider.
    res = client.get("/api/community/search", params={"platform": "x", "q": "hello"})
    assert res.status_code == 200
    assert res.json() == []
