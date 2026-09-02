# OBS_director

A director's toolkit for live-streaming/recording with OBS Studio. A single Python (FastAPI)
app serves two web surfaces:

- **`screen`** — a transparent overlay page, added as a Browser Source in OBS. Renders five live
  effects: speaker banners, community message, WhatsApp discussion simulator, timers, and a big
  red alarm.
- **`admin`** — the operator's control panel: prep pages (speaker roster, WhatsApp conversation
  authoring, alarm presets) plus one single "Live control" page with every action needed
  mid-stream.

See `docs/product.md` and `docs/architecture.md` for the full product/architecture rationale.

## Requirements

- Python 3.10+

## Setup

```bash
cd /home/andrea/workspace/OBS_useful
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt   # app deps + pytest/httpx for testing
# or, to run the app only (no test deps):
# pip install -r requirements.txt
```

## Running the app

```bash
source .venv/bin/activate
python main.py
```

This starts the server on `http://0.0.0.0:8000` by default:

- Admin (live control): http://localhost:8000/admin/live
- Admin (prep pages, linked from the nav bar): `/admin/speakers`, `/admin/whatsapp`, `/admin/alarms`
- Screen (add this as an OBS Browser Source): http://localhost:8000/screen

### Configuration (optional environment variables)

| Variable                 | Default          | Purpose                                  |
|---------------------------|------------------|-------------------------------------------|
| `OBS_DIRECTOR_HOST`       | `0.0.0.0`        | Bind address                              |
| `OBS_DIRECTOR_PORT`       | `8000`           | Bind port                                 |
| `OBS_DIRECTOR_DATA_DIR`   | `./data`         | Where speakers/conversations/alarm presets are persisted as JSON |

Example:

```bash
OBS_DIRECTOR_PORT=8080 OBS_DIRECTOR_DATA_DIR=/path/to/data python main.py
```

Alternatively, run directly with uvicorn (useful for `--reload` during development):

```bash
uvicorn obs_director.app:app --reload --host 0.0.0.0 --port 8000
```

## Stopping the app

- If running in the foreground: press `Ctrl+C` in that terminal.
- If running in the background: `pkill -f "python main.py"` (or `pkill -f "uvicorn obs_director"`
  if you started it that way).

## Running the tests

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt   # if not already installed
pytest
```

The suite is fully automated and isolates every test's data behind a temporary directory, so it
never touches your real `data/` folder. Run with `-v` for per-test names, or target a single file,
e.g. `pytest tests/test_effects_timer.py -v`.

### What's automated vs. manual

Persistence/CRUD, all pure calculation logic (timer math, WhatsApp message-reveal pacing,
platform-style mapping), server-side state transitions (including the dynamic speaker-banner
width logic and multi-effect concurrency), and the WebSocket push channel (state broadcast,
resync-on-connect, multi-client consistency) are covered by `pytest`.

The following can only be verified by hand, in a browser and/or real OBS:

- Animation choreography (slide directions, animate-out-before-in timing, the WhatsApp
  message-arrival stagger, alarm pulsing).
- `screen`'s transparency and compositing when added as a real OBS Browser Source.
- The alarm's siren audio being captured into OBS's audio mix (in OBS, make sure the Browser
  Source's audio is enabled/captured, e.g. via "Control audio via OBS").
- Long-running/soak behavior of looping alarm animation and audio.

**Manual smoke test**: add `http://localhost:8000/screen` as an OBS Browser Source, confirm there
is no background matte (true transparency), confirm the alarm's siren is audible in your OBS audio
mix, and run through all five effects live from `/admin/live` to confirm everything composites and
animates as expected.

## Project layout

```
obs_director/
  app.py            # FastAPI app factory
  config.py         # settings (data dir, host, port)
  models.py         # pydantic models (persisted entities + live state slots)
  state.py          # ScreenState + WebSocket ConnectionManager
  storage.py        # JSON-file persistence (data/*.json)
  effects/          # one module per effect: payload models + apply_* functions
  providers/        # community-message import provider abstraction (no-op in v1)
  routers/          # explicit REST/page/WebSocket routes
  templates/        # Jinja2 templates (admin pages + screen)
  static/           # CSS/JS for admin and screen (per-effect modules under static/screen/effects/)
data/                # JSON persistence (speakers/conversations/alarm presets; gitignored)
tests/               # pytest suite
main.py              # entry point (python main.py)
```
