# OBS_director — Architecture

## Summary
A Python backend (FastAPI, served via Uvicorn) serves two web pages:

- `screen` — transparent overlay page, added as an OBS Browser Source. Renders one fixed-
  position CSS region per effect family, each driven by a small client-side JS module.
- `admin` — control panel, split into prep pages (per-entity content authoring) and a single
  live-control page (every mid-stream action for every effect).

Both pages are server-rendered with Jinja2 templates; there is no frontend build step — client
behavior is vanilla JS/CSS. State is pushed from server to `screen` over a WebSocket.

## Framework and rendering
- **FastAPI + Uvicorn**, chosen for native async WebSocket support, Pydantic request/response
  models, and OpenAPI docs on the admin API "for free."
- **Jinja2** server-rendered templates for both `admin` and `screen`; **vanilla JS + CSS** (no
  bundler/build step) for client behavior. Each effect's animation is CSS keyframes/transitions
  driven by a small per-effect JS module on the `screen` page (`static/screen/effects/*.js`).

## Real-time channel
**WebSocket broadcast of a single authoritative state object**, resolving the previously open
"websockets vs. SSE vs. polling" question in favor of websockets:

- Admin actions are plain HTTP `POST`/`PUT`/`DELETE` calls to explicit REST endpoints — there is
  no generic dynamic dispatcher. Each request is parsed into the relevant effect module's
  Pydantic model and handled by that module's `apply_*` function.
- Each mutation updates one field/slot of an in-memory `ScreenState` object held by the server,
  then the server broadcasts the **entire** updated state as a JSON snapshot to every connected
  `/ws/screen` client via `ConnectionManager`.
- New WebSocket connections receive the current state immediately on connect, so a `screen`
  page reloading (e.g. OBS Browser Source refresh) or a second browser tab used for testing
  always resyncs to the same state as every other connected client — there is one server-side
  source of truth.

## Concurrency / layer model
`ScreenState` is flat, with one independent field/slot per effect family:

```
ScreenState:
  speaker_left:  SpeakerSlot | None      # independent per-side slots
  speaker_right: SpeakerSlot | None
  community_message: CommunityMessageSlot | None
  whatsapp: WhatsAppSlot | None
  timer_big:    TimerSlot | None
  timer_corner: TimerSlot | None
  alarm: AlarmSlot | None
```

`screen.html` has one fixed-position CSS region per family (left/right speaker banner strip —
width dynamic depending on which sides are occupied, community-message region, a full-viewport
WhatsApp panel, big-centered/corner timer slots, top/bottom alarm strip), with a documented
static z-index stack: alarm topmost, then the WhatsApp full-screen takeover, then community
message, then speaker banners, then timers lowest. Each region's JS module subscribes only to
its slice of state and independently drives its own enter/exit animation sequencing — that
sequencing lives entirely in client JS; the server only holds and broadcasts state (there is no
server-side animation sequencer).

At minimum, speaker banner(s), community message, timer(s), and alarm can all be visible at
once in their own regions without interference. WhatsApp is the deliberate exception: while
playing, it takes over the full frame; other slots' state is preserved underneath (not cleared)
and reappears once WhatsApp is stopped.

A second, narrower exception was added for the community-message visual overhaul: while a
community message is showing, the speaker banner region(s) fade out (opacity only) and fade
back in automatically once the message is dismissed — the same "preserve state underneath,
don't clear it" pattern WhatsApp already uses, just scoped to the speaker region instead of the
whole screen. This is implemented entirely client-side, in `static/screen/effects/speaker.js`'s
own `update(state)` (which already receives the full state snapshot): it additionally reads
`state.community_message` — not just its own `speaker_left`/`speaker_right` slice — purely to
toggle a `.hidden-by-community` CSS class. No server-side state changes: `speaker_left`/
`speaker_right` are never touched by a community message appearing or being dismissed, so
existing state-independence guarantees (and their tests) hold unchanged. The community-message
region is deliberately positioned in the same bottom-left corner as `speaker-left-region` — this
overlap is intentional and relied upon by the fade, not an oversight.

## Effect module structure
Each effect gets a module under `obs_director/effects/` (`speaker.py`, `community_message.py`,
`whatsapp.py`, `timer.py`, `alarm.py`) exposing Pydantic action-payload model(s) plus pure
`apply_*(state, payload) -> state` functions and any effect-specific pure logic (e.g.
`timer.py::value_at`, `whatsapp.py::reveal_count`, `speaker.py::banner_width`/
`default_description`). Routing is an explicit set of REST endpoints under
`obs_director/routers/`, one route per live action; each route parses its request into the
corresponding effect module's model, calls that module's `apply_*` function, and broadcasts the
resulting state. Adding a future effect means: add its module, add its route(s), add its
screen-side JS/CSS module and template region.

## Persistence
Per-entity JSON files under `data/` (`data/speakers.json`, `data/conversations.json`,
`data/alarm_presets.json`, `data/community_branding.json`), loaded/rewritten via
`obs_director/storage.py`, each repository function taking an optional data-directory override
for test isolation. This is a single local operator tool with no concurrent-writer contention, so
a file-backed store avoids standing up SQLite/migrations while still being durable and
human-inspectable/editable. Live/ephemeral effect state (`ScreenState` itself, including timers
and the current community message) is in-memory only and is not persisted — it resets on server
restart, while the reusable libraries (speakers, WhatsApp conversations, alarm presets, community
branding) survive restarts.

`obs_director/presets_io.py` adds a cross-cutting YAML export/import on top of these same JSON
files (`obs_director/routers/presets_api.py`, `GET`/`POST /api/presets/export|import`): export
bundles every entity family into one YAML document; import is a full replace of each category,
always preceded by an automatic timestamped backup of the whole `data/` directory under
`data/backups/<timestamp>/`. This is the one new third-party dependency in this release
(`pyyaml`) — nothing else in the stack needed YAML before. No new generic "Preset" entity was
introduced; existing entities are simply bundled together for transfer, and any file reference
inside a bundled entity (a speaker's `image_path`, the branding `logo_path`) round-trips as the
same absolute filesystem path it was exported with — this module never copies or relocates the
referenced file.

## Security / trust model
This app is built for one specific trust model: **a single local operator's own machine**, per
its own stated design ("a single local operator tool" — see Persistence, above). Two decisions
in this codebase are deliberate, user-accepted consequences of that model, not oversights:

- **Full filesystem paths, no portability guarantees.** A speaker's banner image and the
  community-message logo (`Speaker.image_path`, `CommunityBranding.logo_path`) are stored as the
  full, absolute local filesystem path, not copied into an app-managed directory. Exporting and
  re-importing presets on a different machine round-trips the same path string; if that path
  doesn't exist on the importing machine, the preset still imports successfully and the image is
  simply absent/broken (a 404 from `/media`) until the path is corrected. This is accepted, not a
  bug to fix.
- **`GET /media?path=<abs path>` is LAN-reachable and unrestricted.** This app's default bind is
  `0.0.0.0` (see `config.py`), so `/media` is reachable from any device on the operator's local
  network, not just `localhost`. It will read and stream back *any* file on disk that exists, is
  a regular file, and has an allow-listed image extension — there is no additional access
  restriction (no localhost-only check, no directory allow-list). In principle, another device on
  the same LAN could read arbitrary image-extension files off the operator's machine by
  knowing/guessing paths, or probe path existence via 200 vs 404 responses. This is a deliberate,
  explicitly user-accepted tradeoff (matching the same spirit as the filesystem-path decision
  above), not something to "fix" later without a new product decision — do not add localhost-only
  restrictions or a directory allow-list to `/media` without re-confirming that decision.

## Project layout
```
obs_director/
  app.py                  # FastAPI app factory: mounts static files, includes every router
  config.py                # env-driven settings (data dir, host, port)
  templating.py            # shared Jinja2 environment/helpers
  state.py                 # ScreenState model + ConnectionManager (WS broadcast)
  storage.py                # JSON-file repositories: speakers, conversations, alarm presets,
                              #   community branding
  models.py                 # Pydantic models for persisted entities + live-slot payloads
  media.py                   # media_url(): local fs path -> `/media?path=` URL translation
  presets_io.py               # YAML export/import of all presets (PresetBundle, backups)
  effects/
    speaker.py  community_message.py  whatsapp.py  timer.py  alarm.py
  providers/
    base.py                # MessageProvider ABC
    manual.py               # NoOpProvider (always returns [])
  routers/
    pages.py                # admin/screen page routes
    speakers_api.py  whatsapp_api.py  alarm_presets_api.py   # prep-entity CRUD
    community_api.py        # search endpoint (always empty in this release) + branding CRUD
    live_api.py              # every live-control action, across all five effects
    media_api.py              # GET /media?path= — serves an arbitrary local image path
    presets_api.py             # GET/POST /api/presets/export|import
    screen_ws.py              # WS /ws/screen endpoint
  templates/
    base.html
    admin/  (live.html, speakers.html, whatsapp.html, alarms.html, _icons.html)
    screen/screen.html
  static/
    admin/ (admin.css, live.js, speakers.js, whatsapp.js, alarms.js, presets.js)
    screen/ (screen.css, screen.js, ws-client.js, effects/*.{js,css})
data/
  speakers.json  conversations.json  alarm_presets.json  community_branding.json
  backups/<timestamp>/   # created automatically before each preset import
tests/
main.py                     # entry point: `python main.py` runs uvicorn against obs_director.app:app
```

The router split is one module per resource area (rather than a single `admin.py`/`live.py`),
kept flat and explicit per the "no generic dispatcher" principle above — every live action and
every CRUD operation is its own named route.

The admin UX constraint — many prep pages, but exactly one live-control page for everything the
operator touches mid-stream — is implemented directly in this layout: `routers/live_api.py` and
`templates/admin/live.html` are the only page/router exposing select/dismiss/trigger controls
for all five effects; the prep routers/templates (`speakers_api.py`/`speakers.html`,
`whatsapp_api.py`/`whatsapp.html`, `alarm_presets_api.py`/`alarms.html`) are purely for building
the reusable libraries ahead of time.

## Diagram
```mermaid
flowchart LR
    Operator((Operator)) --> AdminPrep[admin: prep pages]
    Operator --> AdminLive[admin: live-control page]
    AdminPrep -- CRUD via REST --> Server[FastAPI app]
    AdminLive -- POST/PUT/DELETE live action --> Server
    Server -- read/write --> Data[(data/*.json)]
    Server -- mutate ScreenState,\nbroadcast full snapshot --> WS{{ConnectionManager}}
    WS -- WS /ws/screen --> Screen1[screen page: OBS Browser Source]
    WS -- WS /ws/screen --> Screen2[screen page: browser tab, testing]
    Screen1 -- rendered via Browser Source --> OBS[OBS Studio scene]
```

## Open architecture questions
None outstanding for this release. Future work to revisit if scope grows: whether a sixth
concurrent effect changes the flat single-`ScreenState`-object model, and whether a real
community-message provider needs its own auth/rate-limit handling layer beyond
`providers/base.py`.
