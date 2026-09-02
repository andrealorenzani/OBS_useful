"""Community message effect tests: platform-style mapping (data-driven per
platform) and the animate-out-then-in replacement semantics (Deep Dive Q7),
tested at the state-model level for the same reason noted in
test_effects_speaker.py (sequencing itself is client JS; what's testable
server-side is that replacement is a same-slot overwrite, matching the
speaker banner's per-side semantics)."""

from __future__ import annotations

import pytest

from obs_director.effects.community_message import (
    PLATFORMS,
    apply_community_message,
    apply_community_message_clear,
)
from obs_director.models import CommunityBranding
from obs_director.state import ScreenState


@pytest.mark.parametrize("platform", PLATFORMS)
def test_each_supported_platform_renders_with_correct_platform_tag(platform):
    state = ScreenState()
    apply_community_message(state, platform, "Hello from " + platform, author="Someone")
    assert state.community_message.platform == platform
    assert state.community_message.text == "Hello from " + platform


def test_unsupported_platform_rejected():
    state = ScreenState()
    with pytest.raises(ValueError):
        apply_community_message(state, "myspace", "hi", author="x")


def test_empty_text_rejected():
    state = ScreenState()
    with pytest.raises(ValueError):
        apply_community_message(state, "x", "   ", author="Someone")


def test_both_authoring_paths_converge_on_same_slot_shape():
    # "search" and "custom" paths both funnel through apply_community_message
    # into the same CommunityMessageSlot type — there is only one rendering
    # pathway regardless of source.
    state = ScreenState()
    apply_community_message(state, "discord", "custom text", author="Operator")
    from_custom = state.community_message

    apply_community_message(
        state, "discord", "imported text", author="Imported Author", avatar_url="http://example/a.png"
    )
    from_search = state.community_message

    assert type(from_custom) is type(from_search)


def test_replacing_shown_message_overwrites_the_single_slot():
    state = ScreenState()
    apply_community_message(state, "x", "first message", author="A")
    apply_community_message(state, "discord", "second message", author="B")
    # Only one message is shown at a time; the new one has fully replaced
    # the old one server-side (the client drives the animate-out-then-in
    # sequencing on top of this replacement, per Deep Dive Q7).
    assert state.community_message.text == "second message"
    assert state.community_message.platform == "discord"


def test_dismiss_clears_slot():
    state = ScreenState()
    apply_community_message(state, "x", "msg", author="A")
    apply_community_message_clear(state)
    assert state.community_message is None


# --- Branding (Code changes §2b) --------------------------------------------


def test_branding_logo_and_accent_propagate_onto_the_slot():
    state = ScreenState()
    branding = CommunityBranding(logo_path="/home/op/logo.png", accent_color="#ff00ff")
    apply_community_message(state, "x", "hello", author="A", branding=branding)
    assert state.community_message.logo_url == "/media?path=%2Fhome%2Fop%2Flogo.png"
    assert state.community_message.accent_color == "#ff00ff"


def test_default_branding_has_no_logo_and_does_not_break_the_slot():
    state = ScreenState()
    branding = CommunityBranding()
    apply_community_message(state, "x", "hello", author="A", branding=branding)
    assert state.community_message.logo_url is None
    assert state.community_message.accent_color == "#5b8def"


def test_branding_defaults_from_storage_when_not_passed_explicitly(tmp_path):
    # No branding file exists yet at this data_dir: falls back to defaults
    # rather than erroring.
    state = ScreenState()
    apply_community_message(state, "x", "hello", author="A", data_dir=tmp_path)
    assert state.community_message.logo_url is None
    assert state.community_message.accent_color == "#5b8def"
