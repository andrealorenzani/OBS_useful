"""Cross-cutting: every live action for all five features is reachable from
exactly the one /admin/live page (no navigation required mid-stream), and
prep-only actions (speaker CRUD, whatsapp authoring, alarm presets) are
absent from that page — while conversely the live actions are absent from
the prep pages."""

from __future__ import annotations

LIVE_ACTION_MARKERS = [
    'data-action="speaker-show"',
    'data-action="speaker-clear"',
    'id="community-custom-form"',
    'id="community-search-form"',
    'data-action="community-clear"',
    'data-action="whatsapp-play"',
    'data-action="whatsapp-stop"',
    'data-action="timer-start"',
    'data-action="timer-pause"',
    'data-action="timer-reset"',
    'data-action="timer-clear"',
    'data-action="alarm-trigger"',
    'data-action="alarm-dismiss"',
]


def test_live_page_contains_every_live_action(client):
    html = client.get("/admin/live").text
    missing = [marker for marker in LIVE_ACTION_MARKERS if marker not in html]
    assert not missing, f"live-control page is missing action(s): {missing}"


def test_live_page_offers_both_speaker_sides_independently(client):
    html = client.get("/admin/live").text
    assert 'data-side="left"' in html
    assert 'data-side="right"' in html


def test_live_page_offers_both_timer_instances_independently(client):
    html = client.get("/admin/live").text
    assert 'data-timer="big"' in html
    assert 'data-timer="corner"' in html


def test_prep_pages_do_not_contain_live_action_controls(client):
    for path in ("/admin/speakers", "/admin/whatsapp", "/admin/alarms"):
        html = client.get(path).text
        for marker in LIVE_ACTION_MARKERS:
            assert marker not in html, f"{path} unexpectedly contains live action {marker!r}"


def test_speaker_prep_page_has_crud_not_present_on_live_page(client):
    prep_html = client.get("/admin/speakers").text
    live_html = client.get("/admin/live").text
    assert 'id="speaker-form"' in prep_html
    assert 'id="speaker-form"' not in live_html
