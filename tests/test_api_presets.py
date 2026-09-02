"""HTTP-level tests for GET/POST /api/presets/export|import."""

from __future__ import annotations

import io

import yaml


def test_export_returns_yaml_with_correct_headers_and_content(client):
    client.post("/api/speakers", json={"name": "Ada", "description": "Mathematician"})
    client.post("/api/alarm-presets", json={"label": "TECHNICAL ISSUE"})

    res = client.get("/api/presets/export")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/yaml")
    assert "attachment" in res.headers["content-disposition"]
    assert "obs_director_presets.yaml" in res.headers["content-disposition"]

    parsed = yaml.safe_load(res.text)
    assert any(s["name"] == "Ada" for s in parsed["speakers"])
    assert any(p["label"] == "TECHNICAL ISSUE" for p in parsed["alarm_presets"])


def test_import_valid_file_fully_replaces_data_and_returns_summary(client):
    client.post("/api/speakers", json={"name": "Old Speaker"})

    new_bundle = {
        "schema_version": 1,
        "speakers": [
            {
                "id": "new-1",
                "name": "New Speaker",
                "description": None,
                "created_at": "2026-01-01T00:00:00+00:00",
                "banner_style": "classic",
                "image_path": None,
            }
        ],
        "whatsapp_conversations": [],
        "alarm_presets": [],
        "community_branding": {"logo_path": None, "accent_color": "#5b8def"},
    }
    yaml_bytes = yaml.safe_dump(new_bundle).encode("utf-8")

    res = client.post(
        "/api/presets/import",
        files={"file": ("presets.yaml", io.BytesIO(yaml_bytes), "text/yaml")},
    )
    assert res.status_code == 200
    summary = res.json()
    assert summary["speakers"] == 1

    listing = client.get("/api/speakers").json()
    assert len(listing) == 1
    assert listing[0]["name"] == "New Speaker"
    assert not any(s["name"] == "Old Speaker" for s in listing)


def test_import_invalid_file_returns_400_and_leaves_data_untouched(client):
    client.post("/api/speakers", json={"name": "Keep Me"})

    res = client.post(
        "/api/presets/import",
        files={"file": ("bad.yaml", io.BytesIO(b"- just\n- a\n- list\n"), "text/yaml")},
    )
    assert res.status_code == 400

    listing = client.get("/api/speakers").json()
    assert len(listing) == 1
    assert listing[0]["name"] == "Keep Me"
