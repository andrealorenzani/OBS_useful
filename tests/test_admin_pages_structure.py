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


def test_live_page_no_longer_offers_the_dead_import_search_ui(client):
    # The community-message "Import (search)" path is dead UI (v1 ships no
    # concrete provider) and was intentionally removed from Live Control —
    # this reverses what was previously asserted as present.
    html = client.get("/admin/live").text
    assert 'id="community-search-form"' not in html
    assert 'id="community-search-results"' not in html


def test_live_page_is_simplified(client):
    html = client.get("/admin/live").text
    assert "<h1>Live control</h1>" not in html
    assert "Everything the operator needs mid-stream lives on this one page." not in html
    # Left/Right speaker sub-blocks collapse to one row each: no more
    # dedicated <h3>Left</h3>/<h3>Right</h3> subheadings.
    assert "<h3>Left</h3>" not in html
    assert "<h3>Right</h3>" not in html
    # The "show"/"clear" icon buttons are the same two components reused for
    # both sides, not four distinct *visible-text* labeled buttons (an
    # accessible `title`/`aria-label` tooltip is fine and expected — it's the
    # old plain-text button *content* that must be gone).
    assert ">Show on left<" not in html
    assert ">Clear left<" not in html
    assert ">Show on right<" not in html
    assert ">Clear right<" not in html
    # Community message: heading removed, but the section container remains.
    assert "<h2>Community message</h2>" not in html
    assert 'id="community-message-section"' in html
    assert ">Show on screen<" not in html
    assert ">Dismiss community message<" not in html
    # Big timer gets a style picker; the corner timer does not.
    big_block = html.split('data-timer="big"')[1].split('data-timer="corner"')[0]
    corner_block = html.split('data-timer="corner"')[1]
    assert 'data-role="timer-style"' in big_block
    assert 'data-role="timer-style"' not in corner_block


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
