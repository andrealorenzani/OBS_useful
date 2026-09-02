"""Speaker banner effect tests: per-side independence (Deep Dive Q1), the
dynamic-width rule, and the no-fabricated-filler-text default (Deep Dive Q5).

Note on scope: per the architecture, enter/exit animation *sequencing*
lives entirely in client JS (static/screen/effects/speaker.js) — "the server
just holds/broadcasts state" — so there is no server-side sequencer to unit
test. What's tested here is everything that *is* server-side: independent
per-side slot replacement (which is what the client's change-detection relies
on) and the width-computation pure function. Animation timing/ordering itself
is manual-only, per the plan's own instruction to flag animation choreography
for manual verification.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from obs_director.effects.speaker import (
    apply_speaker_clear,
    apply_speaker_select,
    banner_width,
    default_description,
)
from obs_director.models import Speaker, SpeakerSlot
from obs_director.state import ScreenState


def _speaker(name="Ada", description=None, banner_style="classic", image_path=None):
    return Speaker(
        id=name.lower(),
        name=name,
        description=description,
        created_at="now",
        banner_style=banner_style,
        image_path=image_path,
    )


def test_default_description_is_none_not_fabricated():
    assert default_description("Ada Lovelace") is None


def test_select_speaker_on_left_only_affects_left_slot():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    assert state.speaker_left is not None
    assert state.speaker_left.name == "Ada"
    assert state.speaker_left.side == "left"
    assert state.speaker_right is None


def test_both_sides_can_hold_different_speakers_simultaneously():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    apply_speaker_select(state, "right", _speaker("Alan"))
    assert state.speaker_left.name == "Ada"
    assert state.speaker_right.name == "Alan"


def test_selecting_new_speaker_on_a_side_replaces_only_that_side():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    apply_speaker_select(state, "right", _speaker("Alan"))
    apply_speaker_select(state, "left", _speaker("Grace"))
    assert state.speaker_left.name == "Grace"
    assert state.speaker_right.name == "Alan"  # untouched


def test_clear_one_side_leaves_other_untouched():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    apply_speaker_select(state, "right", _speaker("Alan"))
    apply_speaker_clear(state, "left")
    assert state.speaker_left is None
    assert state.speaker_right.name == "Alan"


def test_banner_with_no_description_renders_with_no_second_line_data():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada", description=None))
    assert state.speaker_left.description is None


# --- Dynamic width (Deep Dive Q1) ------------------------------------------


def test_width_none_when_no_speakers_active():
    state = ScreenState()
    assert banner_width(state) == {"left": None, "right": None}


def test_width_wide_when_only_one_side_occupied():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    assert banner_width(state) == {"left": "wide", "right": None}

    apply_speaker_clear(state, "left")
    apply_speaker_select(state, "right", _speaker("Alan"))
    assert banner_width(state) == {"left": None, "right": "wide"}


def test_width_narrow_on_both_sides_when_both_occupied():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    apply_speaker_select(state, "right", _speaker("Alan"))
    assert banner_width(state) == {"left": "narrow", "right": "narrow"}


def test_width_widens_again_after_clearing_one_side():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    apply_speaker_select(state, "right", _speaker("Alan"))
    assert banner_width(state)["left"] == "narrow"

    apply_speaker_clear(state, "right")
    assert banner_width(state) == {"left": "wide", "right": None}


# --- Banner style presets (Code changes §2a) --------------------------------


@pytest.mark.parametrize("style", ["classic", "minimal", "glass", "bold", "outline"])
def test_speaker_and_speaker_slot_accept_every_supported_banner_style(style):
    speaker = _speaker("Ada", banner_style=style)
    assert speaker.banner_style == style
    slot = SpeakerSlot(speaker_id="a", name="Ada", side="left", banner_style=style)
    assert slot.banner_style == style


def test_unknown_banner_style_is_rejected():
    with pytest.raises(ValidationError):
        Speaker(id="a", name="Ada", created_at="now", banner_style="neon")
    with pytest.raises(ValidationError):
        SpeakerSlot(speaker_id="a", name="Ada", side="left", banner_style="neon")


def test_apply_speaker_select_copies_banner_style_onto_the_slot():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada", banner_style="bold"))
    assert state.speaker_left.banner_style == "bold"


# --- Image attachment (Code changes §3) -------------------------------------


def test_apply_speaker_select_derives_media_url_from_image_path():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada", image_path="/home/op/ada.png"))
    assert state.speaker_left.image_url == "/media?path=%2Fhome%2Fop%2Fada.png"


def test_apply_speaker_select_leaves_image_url_none_when_no_image_path():
    state = ScreenState()
    apply_speaker_select(state, "left", _speaker("Ada"))
    assert state.speaker_left.image_url is None
