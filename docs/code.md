# OBS_director — Code

## Status
The first real feature release shipped a FastAPI application implementing all five overlay
effects (speaker banners, community message, WhatsApp simulator, timers, alarm) described in
`docs/product.md`, using the architecture described in `docs/architecture.md`. A follow-up
release simplified the Live Control page's chrome, added banner/timer style presets and a
speaker-banner image attachment, gave community messages a logo/accent-color/bottom-left
placement (with a client-side speaker-fade cross-effect), and added a YAML export/import of all
presets (`obs_director/presets_io.py`, `routers/presets_api.py`, `routers/media_api.py`).

## Layout
```
main.py                     # entry point: `python main.py` runs uvicorn against obs_director.app:app
requirements.txt            # fastapi, uvicorn[standard], jinja2, pydantic, python-multipart, pyyaml
requirements-dev.txt        # + pytest, httpx (for FastAPI's TestClient)
pyproject.toml              # pytest config (testpaths = ["tests"])

obs_director/
  app.py                    # create_app(): FastAPI app factory; mounts /static; includes every router
  config.py                 # env-driven settings (data dir, host, port)
  templating.py             # shared Jinja2 environment/helpers used by routers/pages.py
  state.py                  # ScreenState (Pydantic BaseModel) + ConnectionManager (WS broadcast)
  media.py                   # media_url(): local fs path -> `/media?path=` URL translation
  presets_io.py               # YAML export/import of all presets (PresetBundle, auto-backups)
  storage.py                 # JSON-file repositories: speakers, conversations, alarm presets,
                              #   community branding (CRUD functions, each takes an optional
                              #   data_dir override)
  models.py                  # persisted entities (Speaker, WhatsAppConversation/-Message,
                              #   AlarmPreset, CommunityBranding) + live-slot payloads (SpeakerSlot,
                              #   CommunityMessageSlot, WhatsAppSlot, TimerSlot, AlarmSlot)
  effects/
    speaker.py                # apply_* + banner_width(), default_description()
    community_message.py      # apply_* for both free-text and (future) imported paths
    whatsapp.py                # apply_* + reveal_count() (elapsed-time message reveal math)
    timer.py                   # apply_* + value_at() (single range-timer formula, both modes)
    alarm.py                    # apply_* for trigger/dismiss
  providers/
    base.py                    # MessageProvider ABC (search interface for community-message import)
    manual.py                   # NoOpProvider — always returns [] (no concrete provider shipped)
  routers/
    pages.py                    # GET /admin/speakers, /admin/whatsapp, /admin/alarms, /admin/live, /screen
    speakers_api.py             # GET/POST/PUT/DELETE /api/speakers[/{id}]
    whatsapp_api.py              # GET/POST/PUT/DELETE /api/whatsapp/conversations[/{id}],
                                  #   nested message routes /api/whatsapp/conversations/{cid}/messages/{mid}
    alarm_presets_api.py          # GET/POST/DELETE /api/alarm-presets[/{id}]
    community_api.py              # GET /api/community/search?platform=&q= (always [] in this release);
                                    #   GET/PUT /api/community/branding
    live_api.py                    # every live-control action:
                                    #   POST/DELETE /api/live/speaker/{side}
                                    #   POST/DELETE /api/live/community-message
                                    #   POST /api/live/whatsapp/play, /api/live/whatsapp/stop
                                    #   POST /api/live/timer/{slot}/start|pause|reset,
                                    #     DELETE /api/live/timer/{slot}
                                    #   POST /api/live/alarm/trigger, /api/live/alarm/dismiss
    media_api.py                    # GET /media?path= — serves an arbitrary local image path
                                     #   (LAN-reachable, unrestricted: accepted tradeoff)
    presets_api.py                   # GET /api/presets/export, POST /api/presets/import
    screen_ws.py                    # WS /ws/screen
  templates/
    base.html                     # nav incl. Export/Import presets links
    admin/live.html               # the single live-control page: every action, all five effects
    admin/_icons.html              # shared inline-SVG icon macros for the simplified live page
    admin/speakers.html            # prep: manage speaker roster + community branding form
    admin/whatsapp.html             # prep: author named conversations
    admin/alarms.html                # prep: manage alarm presets
    screen/screen.html                # one fixed-position region per effect family + z-index stack
  static/
    admin/admin.css, live.js, speakers.js, whatsapp.js, alarms.js, presets.js
    screen/screen.css, screen.js, ws-client.js
    screen/effects/{speaker,community_message,whatsapp,timer,alarm}.{js,css}

data/
  speakers.json  conversations.json  alarm_presets.json  community_branding.json
                              # created/rewritten by storage.py
  backups/<timestamp>/        # created automatically before each preset import

tests/
  conftest.py                     # isolated tmp_path data dir + global live-state reset per test
  test_storage.py                  # CRUD + persistence-across-restart + data-dir isolation +
                                    #   community branding round-trip
  test_effects_timer.py            # range-timer math, both directions, clamping at end value,
                                    #   style defaulting
  test_effects_whatsapp.py         # reveal-count-from-elapsed-time math
  test_effects_speaker.py          # per-side sequencing, dynamic-width logic, default description,
                                    #   banner style enum, image-path -> media-url derivation
  test_effects_community_message.py # data-driven per-platform styling + branding propagation
  test_effects_alarm.py
  test_state_concurrency.py         # all 5 effect families live at once in independent slots;
                                     #   WhatsApp preserves-but-covers other slots while active;
                                     #   community-message fade is client-side only (untested here)
  test_screen_transparency.py       # guard test: screen never gets an opaque background
                                     #   (incl. the timer's text-only style)
  test_api_entities.py
  test_api_live.py                  # includes delete/edit-while-live speaker behavior
  test_api_presets.py                # export/import HTTP-level behavior
  test_media_api.py                  # GET /media?path= happy/error paths
  test_presets_io.py                  # YAML export/import: round-trip, backups, malformed input,
                                       #   live-slot clearing on removed-id import
  test_ws_broadcast.py               # full-state resync on connect + multi-client consistency
  test_admin_pages_structure.py      # single live page contains every live action; prep pages don't;
                                      #   Live Control simplification (no h1/hint, no dead import UI)
  test_providers.py                   # no-op provider always returns []
```

## Key implementation notes
- `ScreenState` is a Pydantic `BaseModel` (not a plain dataclass), giving `.model_dump_json()`
  for `ConnectionManager.broadcast()` for free.
- There is no generic action dispatcher: routing is the explicit, enumerated set of REST routes
  in `routers/live_api.py` (and the CRUD routers), each calling directly into its effect
  module's `apply_*` function.
- Router files are split one-per-resource (`pages.py`, `speakers_api.py`, `whatsapp_api.py`,
  `alarm_presets_api.py`, `community_api.py`, `live_api.py`, `media_api.py`, `presets_api.py`,
  `screen_ws.py`) for clarity.
- `media.py::media_url()` is the one place a raw local filesystem path is turned into the
  `/media?path=` URL the browser is allowed to load — used by both `effects/speaker.py` (banner
  image) and `effects/community_message.py` (branding logo) so the translation rule only exists
  once. `routers/media_api.py` is the other half: it validates and streams the file back,
  deliberately with no localhost-only restriction (see `docs/architecture.md`'s security/
  trust-model section).
- The community-message-fades-the-speaker-banner interaction (Code changes §2b) is implemented
  entirely in `static/screen/effects/speaker.js`'s `update(state)`, which reads
  `state.community_message` in addition to its own slice — a small, deliberate, documented
  exception to "each screen module only touches its own slice of state" (see `screen.js`'s header
  comment and `docs/architecture.md`'s concurrency section). No server-side state changes.
- `presets_io.py`'s `PresetBundle` is a plain aggregation of existing entity models (no new
  generic "Preset" entity) with `model_config = ConfigDict(extra="forbid")` so an unknown
  top-level key in an imported YAML file fails validation clearly rather than being silently
  ignored. Import always writes a timestamped backup of `data/` *before* overwriting, and only
  after the uploaded YAML has already passed full Pydantic validation — a malformed import never
  touches disk at all.
- WhatsApp message-level routes are nested under their conversation
  (`/api/whatsapp/conversations/{conversation_id}/messages/{message_id}`) since messages are
  stored inside their conversation's JSON record with no separate global index.
- Timer logic is a single generalized "range timer" (`effects/timer.py::value_at`) covering
  both countdown-to-zero and count-from-A-to-B with one formula/model, mirrored in
  `static/screen/effects/timer.js` for smooth client-side ticking between server pushes.
- WhatsApp reveal pacing is server-computed from a fixed `message_interval_ms=1500` set at
  launch time (`started_at_epoch_ms`); the client computes revealed-message count from elapsed
  time, so a reconnecting client resumes correctly mid-conversation.
- The alarm's siren is synthesized client-side via a Web Audio oscillator (no bundled audio
  asset), started/stopped off the state-change event rather than page load, to work with
  browser autoplay policy; alarm top/bottom positioning is applied via a JS-set CSS region
  class (`region--alarm-top`/`-bottom`) rather than CSS `:has()`, to avoid depending on a newer
  CSS feature inside OBS's embedded Chromium.
- Animation enter/exit/materialize sequencing lives entirely in client JS per effect region;
  there is no server-side sequencer to test — server-side tests instead cover per-side slot
  independence/replacement and the pure width/reveal/timer math that the client sequencing
  depends on.

## Testing
- **Runner**: pytest (`pyproject.toml` sets `testpaths = ["tests"]`). Dev dependencies
  (`requirements-dev.txt`) add `pytest` and `httpx` (used by FastAPI's `TestClient`).
- **Run the suite**: `pytest -q` from the repo root (or `.venv/bin/pytest -q`).
- **Isolation**: `tests/conftest.py` gives every test an isolated `tmp_path` data directory
  (overriding `storage.py`'s data-dir default) and resets the global in-memory `ScreenState`
  between tests, so tests never share persisted files or live state.
- **Current status**: 139 tests, all passing. Coverage spans JSON-repository CRUD/persistence
  (including the new banner-style/image-path speaker fields and the community-branding
  singleton), each effect's pure logic (timer math + style defaulting, WhatsApp reveal math,
  speaker width/default-description/banner-style/image-url derivation, per-platform
  community-message styling + branding propagation), cross-effect concurrency (all five families
  live at once, WhatsApp preserve-but-cover behavior, and the new fields' safe defaults), the
  screen-transparency guard (including the timer's text-only style), REST CRUD + live-action
  endpoints (including edit/delete-while-live), `/media?path=` happy/error paths, YAML preset
  export/import (round-trip equivalence, automatic timestamped backups, malformed-input
  rejection, live-slot clearing when an import removes a currently-shown id), WebSocket
  resync-on-connect and multi-client consistency, and admin-page structure (the live page exposes
  every action and is measurably simplified — no `<h1>`/hint, no dead Import-search UI, prep
  pages don't expose live actions).
- **Manual-only (not automated, and not yet performed against real OBS)**: adding `/screen` as
  a real OBS Browser Source to confirm transparency compositing and that the alarm's siren audio
  is capturable into OBS's audio mix; all animation choreography by eye (slide directions,
  animate-out-before-in timing, the name "materialize" beat, WhatsApp arrival stagger feel,
  alarm pulsing/siren pacing); browser autoplay-policy behavior for the siren on first load in a
  real browser/OBS; long-running soak testing of the looping alarm animation/audio.
