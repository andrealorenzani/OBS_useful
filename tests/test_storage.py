"""Persistence / CRUD tests for the JSON-file repositories in storage.py.

Every test uses tmp_path (via pytest's built-in fixture) directly as the
data_dir override, so nothing touches the real ./data/ directory
(Testing information: "Persistence isolation").
"""

from __future__ import annotations

from obs_director import storage


# --- Speakers ------------------------------------------------------------


def test_create_and_list_speakers(tmp_path):
    storage.create_speaker("Ada Lovelace", "Mathematician", data_dir=tmp_path)
    storage.create_speaker("Alan Turing", None, data_dir=tmp_path)

    speakers = storage.list_speakers(data_dir=tmp_path)
    names = {s.name for s in speakers}
    assert names == {"Ada Lovelace", "Alan Turing"}
    turing = next(s for s in speakers if s.name == "Alan Turing")
    assert turing.description is None


def test_speaker_persists_across_simulated_restart(tmp_path):
    created = storage.create_speaker("Grace Hopper", "Rear Admiral", data_dir=tmp_path)

    # A "restart" just means calling the repository functions again with no
    # in-memory cache to fall back on — storage.py holds no module-level
    # state, so this genuinely proves durability.
    reloaded = storage.get_speaker(created.id, data_dir=tmp_path)
    assert reloaded is not None
    assert reloaded.name == "Grace Hopper"
    assert reloaded.description == "Rear Admiral"


def test_update_speaker(tmp_path):
    speaker = storage.create_speaker("Name", "Desc", data_dir=tmp_path)
    updated = storage.update_speaker(speaker.id, "New Name", None, data_dir=tmp_path)
    assert updated.name == "New Name"
    assert updated.description is None

    reloaded = storage.get_speaker(speaker.id, data_dir=tmp_path)
    assert reloaded.name == "New Name"


def test_update_missing_speaker_returns_none(tmp_path):
    assert storage.update_speaker("nonexistent", "x", None, data_dir=tmp_path) is None


def test_delete_speaker(tmp_path):
    speaker = storage.create_speaker("Delete me", None, data_dir=tmp_path)
    assert storage.delete_speaker(speaker.id, data_dir=tmp_path) is True
    assert storage.get_speaker(speaker.id, data_dir=tmp_path) is None
    assert storage.delete_speaker(speaker.id, data_dir=tmp_path) is False


def test_speaker_isolated_between_data_dirs(tmp_path):
    dir_a = tmp_path / "a"
    dir_b = tmp_path / "b"
    dir_a.mkdir()
    dir_b.mkdir()

    storage.create_speaker("Only in A", None, data_dir=dir_a)

    assert len(storage.list_speakers(data_dir=dir_a)) == 1
    assert len(storage.list_speakers(data_dir=dir_b)) == 0


# --- WhatsApp conversations ------------------------------------------------


def test_create_conversation_and_add_messages(tmp_path):
    convo = storage.create_conversation("Interview prep", data_dir=tmp_path)
    storage.add_message(convo.id, "left", "Alex", "Hi there!", None, data_dir=tmp_path)
    storage.add_message(convo.id, "right", None, "Hello!", "10:42", data_dir=tmp_path)

    reloaded = storage.get_conversation(convo.id, data_dir=tmp_path)
    assert len(reloaded.messages) == 2
    assert reloaded.messages[0].direction == "left"
    assert reloaded.messages[0].sender_name == "Alex"
    assert reloaded.messages[1].direction == "right"
    assert reloaded.messages[1].timestamp_label == "10:42"
    # order_index tracks authoring order
    assert [m.order_index for m in reloaded.messages] == [0, 1]


def test_conversation_persists_across_simulated_restart(tmp_path):
    convo = storage.create_conversation("Persisted", data_dir=tmp_path)
    storage.add_message(convo.id, "left", "A", "msg one", None, data_dir=tmp_path)

    reloaded = storage.get_conversation(convo.id, data_dir=tmp_path)
    assert reloaded.name == "Persisted"
    assert len(reloaded.messages) == 1


def test_reorder_messages(tmp_path):
    convo = storage.create_conversation("Order test", data_dir=tmp_path)
    convo = storage.add_message(convo.id, "left", "A", "first", None, data_dir=tmp_path)
    convo = storage.add_message(convo.id, "right", None, "second", None, data_dir=tmp_path)
    ids = [m.id for m in convo.messages]

    reordered = storage.reorder_messages(convo.id, list(reversed(ids)), data_dir=tmp_path)
    assert [m.body for m in reordered.messages] == ["second", "first"]
    assert [m.order_index for m in reordered.messages] == [0, 1]


def test_reorder_rejects_mismatched_ids(tmp_path):
    convo = storage.create_conversation("Order test", data_dir=tmp_path)
    storage.add_message(convo.id, "left", "A", "first", None, data_dir=tmp_path)
    assert storage.reorder_messages(convo.id, ["not-a-real-id"], data_dir=tmp_path) is None


def test_delete_message_renormalizes_order_index(tmp_path):
    convo = storage.create_conversation("Delete msg", data_dir=tmp_path)
    convo = storage.add_message(convo.id, "left", "A", "one", None, data_dir=tmp_path)
    convo = storage.add_message(convo.id, "left", "A", "two", None, data_dir=tmp_path)
    convo = storage.add_message(convo.id, "left", "A", "three", None, data_dir=tmp_path)
    first_id = convo.messages[0].id

    updated = storage.delete_message(convo.id, first_id, data_dir=tmp_path)
    assert [m.body for m in updated.messages] == ["two", "three"]
    assert [m.order_index for m in updated.messages] == [0, 1]


def test_delete_conversation(tmp_path):
    convo = storage.create_conversation("Bye", data_dir=tmp_path)
    assert storage.delete_conversation(convo.id, data_dir=tmp_path) is True
    assert storage.get_conversation(convo.id, data_dir=tmp_path) is None


# --- Alarm presets ---------------------------------------------------------


def test_alarm_preset_crud(tmp_path):
    preset = storage.create_alarm_preset("TECHNICAL ISSUE", data_dir=tmp_path)
    assert preset.label == "TECHNICAL ISSUE"

    reloaded = storage.list_alarm_presets(data_dir=tmp_path)
    assert len(reloaded) == 1
    assert reloaded[0].label == "TECHNICAL ISSUE"

    assert storage.delete_alarm_preset(preset.id, data_dir=tmp_path) is True
    assert storage.list_alarm_presets(data_dir=tmp_path) == []
