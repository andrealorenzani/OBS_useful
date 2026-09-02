"""Speaker banner effect.

Two independent per-side slots (Deep Dive Q1) — a side's selection never
touches the other side's slot. Enter/exit sequencing and the dynamic
wide/narrow width behaviour live entirely in client JS
(``static/screen/effects/speaker.js``); the server here only ever holds and
replaces the *current* slot value per side.
"""

from __future__ import annotations

from pydantic import BaseModel

from ..models import Side, Speaker, SpeakerSlot
from ..state import ScreenState


class SpeakerSelectPayload(BaseModel):
    speaker_id: str


def default_description(name: str) -> str | None:
    """Deep Dive Q5: no fabricated filler text.

    If a speaker has no description, ``screen`` should render the banner with
    no second line at all — not a made-up subtitle derived from the name.
    """

    return None


def apply_speaker_select(state: ScreenState, side: Side, speaker: Speaker) -> ScreenState:
    slot = SpeakerSlot(
        speaker_id=speaker.id,
        name=speaker.name,
        description=speaker.description,
        side=side,
    )
    if side == "left":
        state.speaker_left = slot
    else:
        state.speaker_right = slot
    return state


def apply_speaker_clear(state: ScreenState, side: Side) -> ScreenState:
    if side == "left":
        state.speaker_left = None
    else:
        state.speaker_right = None
    return state


def banner_width(state: ScreenState) -> dict[str, str | None]:
    """Deep Dive Q1's dynamic-width rule, as a pure/testable function.

    Mirrored client-side in ``static/screen/effects/speaker.js`` (which needs
    the same "is the *other* side occupied" visibility). Returns, per side,
    ``None`` (nothing showing), ``"wide"`` (lone occupied side), or
    ``"narrow"`` (both sides occupied, sharing the width).
    """

    left_active = state.speaker_left is not None
    right_active = state.speaker_right is not None
    both_active = left_active and right_active

    def _width(active: bool) -> str | None:
        if not active:
            return None
        return "narrow" if both_active else "wide"

    return {"left": _width(left_active), "right": _width(right_active)}
