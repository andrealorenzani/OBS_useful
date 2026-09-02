"""Tests for obs_director/presets_io.py — YAML export/import of "all presets"
(Code changes §4, Deep Dives Q1/Q2/Q7/Q11/Q12/Q13).

Uses `tmp_path` as an explicit `data_dir` throughout (never the real
`data/` directory), and relies on `conftest.py`'s autouse `_reset_live_state`
fixture to give every test a clean in-memory `ScreenState`, since a couple of
these tests exercise the "clear a stale live slot" behavior directly against
`obs_director.state.state` without going through the FastAPI app."""

from __future__ import annotations

from pathlib import Path

import yaml

from obs_director import presets_io, storage
from obs_director import state as state_module
from obs_director.effects.speaker import apply_speaker_select
from obs_director.effects.whatsapp import apply_whatsapp_play
from obs_director.models import Speaker, WhatsAppConversation, WhatsAppMessage


def test_pyyaml_dependency_is_importable():
    import yaml as _yaml  # noqa: F401 — smoke test that the new dependency is installed


def _seed(data_dir):
    storage.create_speaker(
        "Ada Lovelace", "Mathematician", data_dir=data_dir, banner_style="glass", image_path="/home/op/ada.png"
    )
    convo = storage.create_conversation("Interview", data_dir=data_dir)
    storage.add_message(convo.id, "left", "A", "hi", None, data_dir=data_dir)
    storage.create_alarm_preset("TECHNICAL ISSUE", data_dir=data_dir)
    storage.save_community_branding("/home/op/logo.png", "#ff8800", data_dir=data_dir)


# --- Export ------------------------------------------------------------------


def test_export_contains_absolute_path_to_referenced_image(tmp_path):
    _seed(tmp_path)
    yaml_text = presets_io.export_presets(data_dir=tmp_path)
    parsed = yaml.safe_load(yaml_text)

    image_path = parsed["speakers"][0]["image_path"]
    assert Path(image_path).is_absolute()
    logo_path = parsed["community_branding"]["logo_path"]
    assert Path(logo_path).is_absolute()


def test_export_includes_every_entity_family(tmp_path):
    _seed(tmp_path)
    parsed = yaml.safe_load(presets_io.export_presets(data_dir=tmp_path))
    assert len(parsed["speakers"]) == 1
    assert len(parsed["whatsapp_conversations"]) == 1
    assert len(parsed["whatsapp_conversations"][0]["messages"]) == 1
    assert len(parsed["alarm_presets"]) == 1
    assert parsed["community_branding"]["accent_color"] == "#ff8800"


# --- Import: happy path --------------------------------------------------------


def test_import_round_trip_is_equivalent(tmp_path):
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    _seed(source_dir)

    yaml_text = presets_io.export_presets(data_dir=source_dir)
    summary = presets_io.import_presets(yaml_text, data_dir=dest_dir)

    assert summary.speakers == 1
    assert summary.whatsapp_conversations == 1
    assert summary.alarm_presets == 1

    source_speakers = storage.list_speakers(data_dir=source_dir)
    dest_speakers = storage.list_speakers(data_dir=dest_dir)
    assert [s.model_dump() for s in source_speakers] == [s.model_dump() for s in dest_speakers]

    source_branding = storage.get_community_branding(data_dir=source_dir)
    dest_branding = storage.get_community_branding(data_dir=dest_dir)
    assert source_branding == dest_branding


def test_import_creates_a_timestamped_backup_of_the_prior_data(tmp_path):
    _seed(tmp_path)
    original_speakers_json = (tmp_path / storage.SPEAKERS_FILE).read_text(encoding="utf-8")

    # Import a different (empty) bundle over the top.
    empty_bundle_yaml = presets_io.export_presets(data_dir=tmp_path / "empty-source")
    summary = presets_io.import_presets(empty_bundle_yaml, data_dir=tmp_path)

    backup_dir = Path(summary.backup_dir)
    assert backup_dir.is_dir()
    assert (tmp_path / "backups") in backup_dir.parents
    backed_up_speakers_json = (backup_dir / storage.SPEAKERS_FILE).read_text(encoding="utf-8")
    assert backed_up_speakers_json == original_speakers_json


def test_import_with_missing_referenced_image_path_does_not_crash(tmp_path):
    yaml_text = yaml.safe_dump(
        {
            "schema_version": 1,
            "speakers": [
                {
                    "id": "a1",
                    "name": "Ada",
                    "description": None,
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "banner_style": "classic",
                    "image_path": "/this/path/does/not/exist.png",
                }
            ],
            "whatsapp_conversations": [],
            "alarm_presets": [],
            "community_branding": {"logo_path": None, "accent_color": "#5b8def"},
        }
    )
    summary = presets_io.import_presets(yaml_text, data_dir=tmp_path)
    assert summary.speakers == 1
    reloaded = storage.get_speaker("a1", data_dir=tmp_path)
    assert reloaded.image_path == "/this/path/does/not/exist.png"


def test_import_clears_live_slot_referencing_a_removed_speaker(tmp_path):
    speaker = Speaker(id="gone", name="Gone", created_at="now")
    apply_speaker_select(state_module.state, "left", speaker)
    assert state_module.state.speaker_left is not None

    empty_bundle_yaml = presets_io.export_presets(data_dir=tmp_path / "empty-source")
    presets_io.import_presets(empty_bundle_yaml, data_dir=tmp_path)

    assert state_module.state.speaker_left is None


def test_import_clears_live_whatsapp_slot_referencing_a_removed_conversation(tmp_path):
    convo = WhatsAppConversation(
        id="c1", name="Chat", created_at="now", messages=[WhatsAppMessage(id="m1", order_index=0, direction="left", body="hi")]
    )
    apply_whatsapp_play(state_module.state, convo, now_ms=0)
    assert state_module.state.whatsapp is not None

    empty_bundle_yaml = presets_io.export_presets(data_dir=tmp_path / "empty-source")
    presets_io.import_presets(empty_bundle_yaml, data_dir=tmp_path)

    assert state_module.state.whatsapp is None


def test_import_does_not_clear_live_slot_when_id_survives(tmp_path):
    _seed(tmp_path)
    speaker = storage.list_speakers(data_dir=tmp_path)[0]
    apply_speaker_select(state_module.state, "left", speaker)

    yaml_text = presets_io.export_presets(data_dir=tmp_path)
    presets_io.import_presets(yaml_text, data_dir=tmp_path)

    assert state_module.state.speaker_left is not None
    assert state_module.state.speaker_left.speaker_id == speaker.id


# --- Import: malformed input -------------------------------------------------


def test_import_rejects_non_mapping_top_level(tmp_path):
    try:
        presets_io.import_presets(yaml.safe_dump(["not", "a", "mapping"]), data_dir=tmp_path)
        assert False, "expected PresetImportError"
    except presets_io.PresetImportError:
        pass


def test_import_rejects_entity_missing_required_fields(tmp_path):
    yaml_text = yaml.safe_dump(
        {
            "speakers": [{"id": "a1"}],  # missing name/created_at
            "whatsapp_conversations": [],
            "alarm_presets": [],
            "community_branding": {},
        }
    )
    try:
        presets_io.import_presets(yaml_text, data_dir=tmp_path)
        assert False, "expected PresetImportError"
    except presets_io.PresetImportError:
        pass


def test_import_rejects_unknown_top_level_keys(tmp_path):
    yaml_text = yaml.safe_dump(
        {
            "speakers": [],
            "whatsapp_conversations": [],
            "alarm_presets": [],
            "community_branding": {},
            "totally_unexpected_key": 1,
        }
    )
    try:
        presets_io.import_presets(yaml_text, data_dir=tmp_path)
        assert False, "expected PresetImportError"
    except presets_io.PresetImportError:
        pass


def test_failed_import_leaves_data_untouched_and_creates_no_backup(tmp_path):
    _seed(tmp_path)
    original_speakers_json = (tmp_path / storage.SPEAKERS_FILE).read_text(encoding="utf-8")

    try:
        presets_io.import_presets(yaml.safe_dump(["not", "a", "mapping"]), data_dir=tmp_path)
    except presets_io.PresetImportError:
        pass

    assert (tmp_path / storage.SPEAKERS_FILE).read_text(encoding="utf-8") == original_speakers_json
    assert not (tmp_path / "backups").exists()
