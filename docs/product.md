# OBS_director — Product

## Vision
OBS_director is a director's toolkit for live-streaming/recording with OBS Studio. It is a
Python application that serves web pages, split into two surfaces:

- **screen** — a transparent page meant to be added as a Browser Source in an OBS scene. It
  renders visual effects (overlays, animations, lower-thirds, etc.) so they appear directly in
  the recording/stream, layered on top of whatever else is in the scene.
- **admin** — a control page with the tools needed to trigger, configure and sequence the
  effects that appear on `screen`. This is what the operator (the "director") uses while
  recording.

Both pages are served by the same Python app. `admin` is used from a regular browser; `screen`
is added to OBS as a Browser Source (and can also be opened in a regular browser for testing).

## Status
No features have been built yet. This file is the seed document the product-owner agent reads
before analysing new changes; it is expanded after every implemented change (see
`docs/plans.md` for the full change history).

## Open product questions
- What is the first effect/tool that should be built end-to-end to validate the screen/admin
  split (e.g. a single image/text overlay that admin can show and hide on screen)?
