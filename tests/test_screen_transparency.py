"""Guard test for the single most important non-negotiable property of
`screen`: it must stay transparent so it composites correctly as an OBS
Browser Source over the rest of the scene."""

from __future__ import annotations

import re
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "obs_director" / "static" / "screen"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_screen_css_sets_html_body_background_transparent():
    css = _read(STATIC_DIR / "screen.css")
    match = re.search(r"html\s*,\s*body\s*\{([^}]*)\}", css)
    assert match, "expected an `html, body { ... }` rule in screen.css"
    rule_body = match.group(1)
    assert "background: transparent" in rule_body or "background:transparent" in rule_body


def test_no_opaque_background_declared_on_html_or_body_anywhere_in_screen_css():
    css = _read(STATIC_DIR / "screen.css")
    # Guard against a future edit accidentally adding a second, opaque
    # background rule for html/body (region/effect-specific backgrounds are
    # fine — those are small chrome elements, not the full-viewport root).
    for selector_match in re.finditer(r"([^{}]+)\{([^}]*)\}", css):
        selector, body = selector_match.groups()
        if re.search(r"\bhtml\b|\bbody\b", selector):
            for decl in re.finditer(r"background(?:-color)?\s*:\s*([^;]+);", body):
                value = decl.group(1).strip().lower()
                assert value in ("transparent", "none", "rgba(0, 0, 0, 0)", "rgba(0,0,0,0)"), (
                    f"non-transparent background found on selector {selector!r}: {value!r}"
                )


def test_timer_text_only_style_has_no_background_box():
    # Code changes §2c: the "text-only" big-timer style is explicitly meant
    # to render with no background/box at all.
    css = _read(STATIC_DIR / "effects" / "timer.css")
    match = re.search(r"\.timer-display--style-text-only\s*\{([^}]*)\}", css)
    assert match, "expected a .timer-display--style-text-only rule in timer.css"
    rule_body = match.group(1)
    for decl in re.finditer(r"background(?:-color)?\s*:\s*([^;]+);", rule_body):
        value = decl.group(1).strip().lower()
        assert value in ("transparent", "none"), f"text-only timer style has a background: {value!r}"


def test_no_effect_css_file_sets_an_opaque_full_viewport_background():
    effects_dir = STATIC_DIR / "effects"
    for css_file in effects_dir.glob("*.css"):
        css = _read(css_file)
        # None of the per-effect region roots (.region--*) should carry an
        # opaque, page-covering background — only their small inner elements
        # (banners/cards/panels) may.
        for selector_match in re.finditer(r"([^{}]+)\{([^}]*)\}", css):
            selector, body = selector_match.groups()
            if re.match(r"^\s*\.region--[\w-]+(\.[\w-]+)?\s*$", selector):
                for decl in re.finditer(r"background(?:-color)?\s*:\s*([^;]+);", body):
                    value = decl.group(1).strip().lower()
                    assert "rgba" in value or value in ("transparent", "none"), (
                        f"{css_file.name}: region selector {selector!r} sets a suspicious "
                        f"opaque background {value!r}"
                    )
