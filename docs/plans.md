# OBS_director — Plans

Append-only log of implemented change plans, most recent last. Each entry is produced by the
`coordinator` agent and appended here by the `documenter` agent once a change has been
implemented.

---

# OBS_director First Release: Five Live Overlay Effects (Speaker Banners, Community Message, WhatsApp Simulator, Timers, Alarm) - 2026-09-02 19:13 BST

## Context of the changes

`docs/product.md` currently describes OBS_director only at the vision level: two pages (`screen`, an OBS Browser Source overlay, and `admin`, the operator's control panel), no features built yet, and one open question — "what should the first effect be." This change answers that question decisively and supersedes it: instead of a single validating effect, the first real release ships **five effects at once**, all wired through the same `screen`/`admin` split, because the user wants a coherent first release rather than an incremental single-feature slice. `docs/architecture.md` is fully undecided (framework, real-time channel, layout, effect-registration model) — this change explicitly asks the architect to resolve those as part of this plan rather than leave them open, since five concurrent, independently-controlled effects is exactly the kind of scope that makes "websockets vs. polling," "server-rendered vs. JS frontend," and "how effects register" load-bearing decisions.

The five effects, from a product point of view:

1. **Speaker presentation** — a lower-third-style banner naming a speaker. It's a "prep ahead, trigger live" workflow: the operator builds a reusable speaker roster in admin (name + optional description, persisted across sessions/restarts), then during the stream picks a speaker and a screen side (left/right) to display them. The side selection is per-instance, not global — nothing in the request says only one speaker can be shown at a time; the "never two banners on the same side" rule is explicitly scoped per side, which implies two speakers (one left, one right) can be on screen simultaneously, e.g. for a two-person interview. Swapping the speaker on a given side plays an out-animation for the old one before the in-animation for the new one, so a side never shows two names overlapping. **[Finalized: confirmed as two independent per-side slots — see Deep Dive Q1 for the added dynamic-width requirement.]**

2. **Community message** — a social-media-styled callout, fed by two authoring paths that converge on the same on-screen presentation: importing a real message from a connected social account, or hand-writing free text and picking which platform's visual style to mimic. This is the one feature with a genuine external-integration fork (see Deep Dive Q2 for the finalized v1 scope).

3. **WhatsApp discussion simulator** — pre-authored, named, fake chat scripts (ordered messages, each tagged incoming/left-with-sender-name or outgoing/right-with-timestamp-and-read-receipts), played back live as a full-screen animated conversation. Notably, the user's own concurrency example ("speaker banner + community message + timer + alarm all live at once") pointedly omits the WhatsApp simulator — consistent with it being described as "takes over the full screen," i.e. the one effect that is not meant to layer alongside the others but to dominate the frame while active.

4. **Timers** — at least two placements (big centered, and a corner badge) and at least two modes (countdown-to-zero from a set duration, and count between an arbitrary configured start and end value, not just count-up-from-zero). Both placements are independent layers, so a centered timer and a corner timer can run at once with different modes/values.

5. **Big red alarm** — a bold, high-contrast red banner (top or bottom, centered) for a "something's wrong / pay attention" moment, in the spirit of a loud alert, with content that can be composed/prepared in admin ahead of time and triggered/dismissed live with a single action. **[Finalized: includes real siren audio — see Deep Dive Q3.]**

Cross-cutting product requirement: admin is split into **prep surfaces** (manage the speaker roster, author WhatsApp conversations, save alarm presets, and whatever setup timers need) and exactly **one live-control surface** that has to contain every action the operator needs mid-stream: select/deselect speaker+side (independently per side), pick or compose the community message and its style, launch/stop a saved WhatsApp conversation, configure/start/stop each timer instance, and trigger/dismiss the alarm. This is a deliberate, explicit constraint from the user, not a suggestion — the operator must never need to leave that one page while recording.

Concurrency is also explicit: speaker banner(s), community message, timer(s), and alarm are independent visual layers on `screen` and must be able to be live simultaneously, since they occupy visually distinct regions (banners at the sides/bottom, timers centered/corner, alarm top-or-bottom-center, community message presumably a corner/side toast-like region). The WhatsApp simulator is the deliberate exception that takes over the whole frame.

### Acceptance criteria

**Cross-cutting / admin structure**
- Admin has a single "Live control" page/section reachable without navigation during a stream, containing every live action for all five features: speaker select+side (per side), community message pick/compose+style, WhatsApp conversation launch/stop, timer configure/start/stop (both placements independently), alarm trigger/dismiss.
- Admin has separate prep page(s)/section(s) for: managing the speaker roster (add/edit/remove speaker name+description), authoring/editing named WhatsApp conversations and their messages, and composing/saving alarm presets (at least a default alarm text/style, with the option to customize before triggering).
- Speaker roster and WhatsApp conversations persist across app restarts (not just in-memory for the current process).
- Multiple `screen` clients (e.g. the real OBS Browser Source plus a browser tab used for testing) reflect identical, synchronized state — there is one server-side source of truth for what's currently showing.
- At minimum, speaker banner(s), community message, timer(s), and alarm can all be visible on `screen` at the same time, in their own screen regions, without one effect's animation or state interfering with another's.

**1. Speaker presentation**
- Operator can create/edit/delete speakers in the prep page: full name (required) and description/title (optional).
- If description is left blank, `screen` shows the banner without a redundant/empty subtitle rather than fabricating filler text (name occupies the banner; no second line is rendered).
- From live control, operator selects a speaker and a side (left/right) independently for each side; selecting for a side that already has a speaker showing plays that speaker's out-animation (matching its side) before the new speaker's in-animation plays (matching the newly selected side).
- Deselecting a speaker (per side) plays the out-animation and clears that side; nothing else is affected.
- Name renders large/dominant on the banner; description renders smaller, both introduced via a directional entrance animation matching the selected side, followed by the name "materializing" (a distinct visual beat, not just a plain fade).
- **[Finalized addition, see Deep Dive Q1]:** banner width is dynamic — if the opposite side's slot is empty, the occupied side's banner takes up most of the screen width (wide/prominent); if both sides are occupied simultaneously, each banner narrows to share the screen (e.g. roughly half-width each). Enter/exit/materialize animations still work exactly as designed per side; the width transition should itself animate smoothly rather than jump-cut when the opposite side's occupancy changes.

**2. Community message**
- Operator can compose a free-text message and pick a platform visual style (at minimum the platforms named: X, Discord, Facebook, WhatsApp) from live control; on submit, it appears on `screen` with an entrance animation and is visually styled to resemble that platform. This free-text+style path must be fully functional in v1 (see Deep Dive Q2).
- Operator can browse/search a list of importable messages via a provider abstraction; **for v1, no concrete provider is wired up (search returns no results)** — see Deep Dive Q2. The abstraction must be built so a real platform provider can be added later without reworking the rendering path.
- Both paths converge on the same on-screen rendering/animation pathway.
- Only one community message is shown at a time; showing a new one replaces the previous one using the same animate-out-then-in sequencing as the speaker banner (see Deep Dive Q7), and the operator can dismiss it entirely from live control.

**3. WhatsApp discussion simulator**
- Operator can create/edit/delete named conversations in the prep page; each conversation is an ordered list of messages, each tagged left/incoming (renders with sender name) or right/outgoing (renders with timestamp + blue double-check marks), matching real WhatsApp visual conventions.
- From live control, operator can launch a saved conversation by name; it takes over the full `screen` frame and plays messages in one at a time with a "live arrival" animation/pacing (fixed interval, see Deep Dive Q11), in authored order.
- After the last message, the full conversation remains visible (doesn't auto-clear) until the operator stops/dismisses it from live control, at which point `screen` returns to showing whatever other effects (speaker/timer/alarm/community message) are still active in their normal regions (their state is preserved underneath throughout — see Deep Dive Q8).
- Only one conversation plays at a time.

**4. Timers**
- Operator can configure and independently start/stop two timer instances: one big/centered, one corner (top-right or bottom-right, operator's choice).
- Each instance supports two modes, selectable and configurable from live control: countdown from a configured duration to zero, and count between a configured start value and a configured end value.
- Timers are visually legible against a transparent background at both placements/sizes.
- Reaching the configured end value is visually distinct (e.g. a flourish/flash) rather than silently continuing past it or abruptly vanishing.
- Timers are configured ad hoc directly on the live control page; no separate timer-preset persistence is required for v1 (see Deep Dive Q9).

**5. Big red alarm**
- Operator can trigger the alarm from live control with one action, using either a saved preset (composed ahead of time in the prep area) or the default alarm content if no preset is chosen.
- Alarm renders as a bold, high-contrast red banner/effect, centered at the top or bottom of the frame, with an attention-grabbing entrance/looping animation ("whining"/pulsing in spirit) **and real siren audio** (see Deep Dive Q3), played through the browser tab so it is present on the Browser Source's audio track.
- Operator can dismiss the alarm from live control with one action at any time; it does not auto-dismiss on a timer unless that's explicitly part of a preset's configuration.

## Architectural Impact

This is the first real feature set for OBS_director, landing on greenfield docs (`docs/architecture.md` lists framework, real-time channel, layout, and effect-registration as all open, and `docs/code.md`/`docs/plans.md` are empty stubs). These open questions are resolved concretely as part of this change.

**Framework: FastAPI + Uvicorn, server-rendered Jinja2 templates, vanilla JS on the client.** FastAPI gives native async WebSocket support, Pydantic models for the five effects' payloads, and OpenAPI docs "for free" on the admin action endpoints. No frontend build step — `admin` and `screen` stay simple HTML/CSS/JS. Each effect's animation is CSS keyframes/transitions driven by small per-effect JS modules on the `screen` page.

**Real-time channel: WebSocket broadcast of a single authoritative state object.** Admin actions are plain HTTP `POST` calls to explicit REST endpoints (see Code changes — there is no generic dynamic dispatcher, see Deep Dive Q10). Each POST mutates one field of an in-memory state object held by the server, then the server broadcasts the *entire* updated state to every connected client. New WS connections get the current state immediately on connect, so OBS reloading the Browser Source recovers state correctly. This resolves the doc's open "websockets vs SSE vs polling" question in favor of websockets.

**Concurrency / layer model.** The state object is flat, with one independent sub-object per effect family (the authoritative field-by-field shape is the `ScreenState` model in Code changes — see Deep Dive Q12):

```
state = {
  speaker:  { left: SpeakerSlot|null, right: SpeakerSlot|null },   # two independent per-side slots — Deep Dive Q1
  community_message: { active: null | {text, style, source} },
  whatsapp: { active: null | {conversation_id, messages: [...]} },
  timers:   { big: TimerState|null, corner: TimerState|null },
  alarm:    { active: bool, position: "top"|"bottom" }
}
```

`screen.html` has one fixed-position CSS region per family (left/right speaker banner strip — width dynamic per Deep Dive Q1, community-message region, a full-viewport whatsapp panel, big-centered/corner timer slots, top/bottom alarm strip) with a documented static z-index stack (alarm topmost, then whatsapp full-screen takeover, then community message, then speaker banner, then timers lowest). Each region's JS module subscribes to only its slice of state and independently drives its own enter/exit animation sequencing — this sequencing lives entirely in client JS, the server just holds/broadcasts state.

**Effect module structure (reconciled per advisor review — see Deep Dive Q10)**: each effect gets a module under `obs_director/effects/` (`speaker.py`, `community_message.py`, `whatsapp.py`, `timer.py`, `alarm.py`) exposing Pydantic action-payload model(s) plus `apply_*(state, payload) -> state` function(s). Routing is the explicit set of REST endpoints in `obs_director/routers/` (see Code changes), one route per live action, each route parsing its request into the corresponding effect module's model and calling that module's `apply_*` function, then broadcasting the resulting state. Adding a sixth effect later means: add its module, add its route(s), add its screen-side JS/CSS module and template partial.

**Persistence: per-entity JSON files under `data/`** (`data/speakers.json`, `data/conversations.json`, `data/alarm_presets.json`), loaded/rewritten via `obs_director/storage.py`. This is a single local operator tool with no concurrent-writer contention, so a file-backed store avoids standing up SQLite/migrations for v1 while still being durable and human-inspectable/editable. **This is the authoritative persistence decision** — see Deep Dive Q4.

**Project layout** (authoritative package name is `obs_director/`, see Deep Dive Q4 — actual implemented layout, see the Deviations note under Code changes for the router-file split actually used):
```
obs_director/
  app.py / main.py       # FastAPI app factory, mounts routers/static/templates, WS endpoint
  state.py               # ScreenState model + ConnectionManager (WS broadcast)
  storage.py             # JSON-file repositories: speakers, conversations, alarm presets
  models.py              # Pydantic models for all entities + ScreenState
  effects/
    speaker.py  community_message.py  whatsapp.py  timer.py  alarm.py
  providers/
    base.py  manual.py (no-op provider)
  routers/
    (explicit route modules — see Deviations for actual file split)
  templates/  (admin/live.html, admin/speakers.html, admin/whatsapp.html, admin/alarms.html, screen/screen.html, base.html)
  static/  (admin/*.css,*.js ; screen/screen.css, screen.js, ws-client.js, effects/*.{js,css})
data/
  speakers.json  conversations.json  alarm_presets.json
tests/
```

The user's explicit admin UX constraint — many prep pages, but **one** live-control page for everything the operator touches mid-stream — is implemented directly: the live-control page/router is the only page rendering select/dismiss/trigger controls for all five effects; the prep routers/templates are purely for building the reusable libraries ahead of time and are never needed once recording starts.

## Code changes

**Stack** (Python): **FastAPI** + **uvicorn[standard]**; **Jinja2** server-rendered `admin`/`screen` HTML shells; **vanilla JS + CSS** (no build step) for animations and the WebSocket client; **WebSocket** (`/ws/screen`) as the push channel; **JSON-file repositories** (`obs_director/storage.py`) for speakers, WhatsApp conversations, alarm presets. Timers and community messages are live/ephemeral — not persisted.

### Persistence / data model (JSON files)
- `speakers.json`: list of `{id, name, description: str|null, created_at}`
- `conversations.json`: list of `{id, name, created_at, messages: [{id, order_index, direction: "left"|"right", sender_name: str|null, body, timestamp_label: str|null}]}`
- `alarm_presets.json`: list of `{id, label, created_at}`

### Live screen state (`state.py`, in-memory, not persisted — authoritative shape, see Deep Dive Q12)
```python
class ScreenState:
    speaker_left: SpeakerSlot | None = None
    speaker_right: SpeakerSlot | None = None   # two independent per-side slots — Deep Dive Q1
    community_message: CommunityMessageSlot | None = None
    whatsapp: WhatsAppSlot | None = None
    timer_big: TimerSlot | None = None
    timer_corner: TimerSlot | None = None
    alarm: AlarmSlot | None = None
```
(Implemented as a Pydantic `BaseModel`, not a plain dataclass, for free JSON serialization — see Deviations.)

Every mutation (`effects/*.apply_*`) updates one slot and calls `ConnectionManager.broadcast(state)`, which sends the **full state snapshot** as JSON to every connected `/ws/screen` socket, including immediately on connect (so a reconnecting Browser Source resyncs correctly).

Slot payload shapes:
- `SpeakerSlot{speaker_id, name, description, side}` — `side` drives entrance/exit direction client-side. The client computes banner width from whether the *other* side's slot is occupied (Deep Dive Q1): both slots present -> narrow/shared width each; only one present -> wide/prominent width, animated smoothly on change.
- `CommunityMessageSlot{platform, author, avatar_url|None, text, timestamp_label|None}` — same shape whether from search-import or custom-text; both paths funnel through `effects/community_message.py::apply_community_message()`.
- `WhatsAppSlot{conversation_id, messages: [...], started_at_epoch_ms, message_interval_ms}` — server says "play this conversation starting at time T"; screen JS computes revealed-message count from elapsed time since `started_at_epoch_ms`, so a reconnect resumes correctly. **Message reveal pacing (Deep Dive Q11):** fixed `message_interval_ms=1500` (1.5s) between reveals, set server-side at launch, not proportional to length, not operator-configurable in v1.
- `TimerSlot{start_seconds, end_seconds, anchor_epoch_ms, paused_offset_seconds, running, position}` — a single generalized "range timer": `displayed(now) = start_seconds + direction*(elapsed)`, clamped at `end_seconds`, covering both countdown-to-zero and count-from-A-to-B with one model. Pure function `effects/timer.py::value_at(now, slot)`, mirrored client-side in `screen/effects/timer.js` for smooth ticking (server only pushes on Start/Pause/Reset).
- `AlarmSlot{label|None, position: "top"|"bottom"}` — presence/absence = active/dismissed. **Audio (Deep Dive Q3):** when active, `screen/effects/alarm.js` plays a looping siren (synthesized via Web Audio oscillator, no bundled audio asset) for as long as the slot is present, stopping on dismiss, triggered off the state-change event (not page load) to help with autoplay policy. OBS must be configured to capture that Browser Source's audio track for the siren to be heard in the stream/recording — documented in code comments and this doc.

### Routes (explicit, no generic dispatcher — Deep Dive Q10)
- Prep pages: `GET /admin/speakers`, `GET /admin/whatsapp`, `GET /admin/alarms`
- Live control: `GET /admin/live` — the single page with every live action for all five effects
- `GET /screen`, `WS /ws/screen`
- REST, prefixed `/api`: `GET/POST/PUT/DELETE /api/speakers[/{id}]`; `GET/POST/PUT/DELETE /api/whatsapp/conversations[/{id}]`, message sub-routes nested under their conversation (see Deviations); `GET/POST/DELETE /api/alarm-presets[/{id}]`; `GET /api/community/search?platform=&q=` (always `[]` in v1, Deep Dive Q2); live actions: `POST/DELETE /api/live/speaker/{side}`, `POST/DELETE /api/live/community-message`, `POST /api/live/whatsapp/play`, `POST /api/live/whatsapp/stop`, `POST /api/live/timer/{slot}/start`, `.../pause`, `.../reset`, `DELETE /api/live/timer/{slot}`, `POST /api/live/alarm/trigger`, `POST /api/live/alarm/dismiss`.

### Per-feature implementation notes
1. **Speaker** — `effects/speaker.py::default_description(name)` returns nothing (no fabricated filler text, Deep Dive Q5). Per-side client state machine plays exit-then-enter animations correctly; width recomputed on either slot's occupancy change (Deep Dive Q1). Editing a live speaker's roster entry does not retroactively update the banner (Deep Dive Q6); deleting one clears that side.
2. **Community message** — `providers/base.py::MessageProvider` ABC, no concrete provider in v1 (Deep Dive Q2), free-text+style path fully functional. Both paths render via one `screen/effects/community_message.js` path with a `platform` CSS modifier class. Replacement uses the same animate-out-then-in sequencing as speaker (Deep Dive Q7).
3. **WhatsApp simulator** — prep page authors ordered, directional messages; `POST /api/live/whatsapp/play` snapshots the conversation into `WhatsAppSlot` with `started_at_epoch_ms=now`, `message_interval_ms=1500`. Full-viewport overlay reveals messages via elapsed-time math (Deep Dive Q11); other slots are preserved but visually covered while active (Deep Dive Q8), reappearing on stop.
4. **Timers** — one `TimerSlot` model for both `timer_big` and `timer_corner`; pure `value_at()` function unit-tested; ad hoc configuration only, no presets in v1 (Deep Dive Q9).
5. **Alarm** — `AlarmSlot` presence toggles a pulsing red banner plus looping synthesized siren; optional label from a saved preset or typed ad hoc (Deep Dive Q3).

### Deviations from the original plan (as implemented)
- `ScreenState` is a Pydantic `BaseModel`, not a `dataclasses.dataclass` — same fields/semantics, gives `.model_dump_json()` for the broadcaster for free.
- Router files are split more granularly, one module per resource (`pages.py`, `speakers_api.py`, `whatsapp_api.py`, `alarm_presets_api.py`, `community_api.py`, `live_api.py`, `screen_ws.py`) rather than the plan's `live.py`/`speakers_prep.py`/... sketch — same explicit-route philosophy (Deep Dive Q10), organized differently for clarity.
- WhatsApp message-level routes are nested under their conversation (`/api/whatsapp/conversations/{conversation_id}/messages/{message_id}`) rather than a flatter `/api/whatsapp/messages/{id}`, since messages are stored inside their conversation's JSON record with no separate global index.
- There is no server-side animation-ordering "sequencer" — per the Architectural Impact section's own statement that sequencing lives entirely in client JS. What's tested server-side is per-side slot independence/replacement and the width-computation pure function; animation timing/ordering itself is manual-only (as the plan itself designates for animation choreography).
- Alarm position styling uses a JS-set region class (`region--alarm-top`/`-bottom`) instead of CSS `:has()`, to avoid relying on a newer CSS feature inside OBS's embedded Chromium.

## Testing information

pytest is the test runner, set up fresh in this change (`tests/`, `pyproject.toml` pytest config). Every test uses an isolated `tmp_path` data directory and resets global live state (`tests/conftest.py`).

**Implemented and passing (95 tests, all green):** `test_storage.py` (CRUD + persistence-across-restart + data-dir isolation for speakers/conversations/alarm presets), `test_effects_timer.py` (range-timer math, both directions, clamping at end value), `test_effects_whatsapp.py` (reveal-count-from-elapsed-time math), `test_effects_speaker.py` (per-side sequencing + Deep Dive Q1 width logic + Deep Dive Q5 default description), `test_effects_community_message.py` (data-driven per platform style), `test_effects_alarm.py`, `test_state_concurrency.py` (all 5 effect families live at once in independent slots; WhatsApp preserves-but-covers per Deep Dive Q8), `test_screen_transparency.py` (guard test that `screen` never gets an opaque background), `test_api_entities.py`, `test_api_live.py` (including Deep Dive Q6 delete/edit-while-live behavior), `test_ws_broadcast.py` (full-state resync on connect + multi-client consistency), `test_admin_pages_structure.py` (single live page contains every live action; prep pages don't), `test_providers.py` (no-op provider always returns `[]`).

A live end-to-end smoke test was also run outside pytest: started the real app, hit `/admin/live`, `/screen`, and static assets over HTTP, created a speaker via REST, connected a real websocket client to `/ws/screen`, and confirmed a live action was pushed to the open socket immediately.

**Manual-only, explicitly not automatable and still pending (flag to the user):**
- The mandatory OBS smoke test: add `/screen` as a real OBS Browser Source, confirm true transparency compositing, confirm the alarm's siren audio is capturable into OBS's audio mix (needs "Control audio via OBS" considered), and run through all five effects live end-to-end.
- All animation choreography by eye: speaker/community-message slide directions and animate-out-before-in timing, the name "materialize" beat, WhatsApp message-arrival stagger feel, alarm pulsing + siren perceived loudness/pacing.
- Browser autoplay-policy behavior for the alarm's Web Audio siren on first `screen` load in a real browser/OBS.
- Long-running soak testing (memory/frame-rate/audio-glitch behavior of looping alarm animation+audio over time).

# Deep Dives

**Q1. Speaker banner model — one active speaker, or two independent sides?**
The spec's exclusivity rule ("never both on screen at once on that side") is scoped per side, which the product-owner read as implying two independent slots, while the architect and developer both defaulted to a single global active-speaker slot. **User decision: two independent per-side slots (Option B), confirmed**, with an added requirement: banner width is dynamic — lone occupied side gets a wide/prominent banner; both sides occupied narrows each to share the screen, animated smoothly on change.

**Q2. Community message live-import — which real platform, if any, for v1?**
Three briefings proposed three different defaults (Discord, Mastodon/Bluesky, or no real provider). **User decision: Option C — skip real import for v1.** Provider interface/abstraction built for future extension; ships with no concrete provider (search returns no results). Free-text-plus-platform-style path is fully functional and is the primary v1 path.

**Q3. Big red alarm — visual only, or does v1 need actual sound?**
**User decision: Option B — include real siren audio**, via Web Audio, played through the browser tab for as long as the alarm is active, triggered by the explicit admin trigger action. OBS needs to be configured to capture that Browser Source's audio track for the siren to be heard in the stream/recording — documented in code and this doc.

**Q4. Persistence mechanism and project layout — architect (JSON files, `obs_director/`) vs. developer (SQLite, `app/`) disagreed.**
The architect's decisions are authoritative since the user explicitly tasked the architect with resolving these open questions: JSON-file persistence via `obs_director/storage.py`, package name `obs_director/`.

**Q5. Speaker description default when missing.**
Resolved from the product-owner's acceptance criteria: no second line/subtitle is rendered when description is blank — the name occupies the banner alone, no fabricated filler text.

**Q6. Editing/deleting a speaker currently live.**
Resolved as a sensible default: editing the roster only affects future selections, not what's already showing live; deleting a speaker that's currently live clears that side.

**Q7. Does replacing a community message use the same animate-out-then-in sequencing as the speaker banner?**
Resolved from the product-owner's acceptance criteria describing it as "consistent with the banner-replacement pattern elsewhere" — yes.

**Q8. When WhatsApp "takes over full screen," what happens to other active effects?**
Resolved: other effects' state is preserved but visually covered while a conversation plays; dismissing reveals whatever else is still active underneath, rather than clearing/resetting it.

**Q9. Do timers and alarms need persisted presets, or is ad hoc live configuration sufficient?**
Resolved: alarm gets persisted, named presets (label only); timers are configured ad hoc directly on the live control page, no timer-preset persistence in v1.

**Q10. Advisor-flagged contradiction: generic dynamic dispatcher vs. explicit per-feature routes.**
Resolved by the coordinator: there is no generic dynamic dispatcher. Routing is the explicit set of REST endpoints. Each effect module owns its Pydantic payload model(s) and `apply_*` business logic, imported directly by the specific route(s) that need them.

**Q11. Advisor-flagged gap: WhatsApp message-reveal pacing was undefined.**
Resolved by the coordinator: fixed interval of 1.5 seconds (`message_interval_ms=1500`) between message reveals, set server-side at launch, not proportional to length, not operator-configurable in v1.

**Q12. Naming reconciliation: illustrative `state` sketch vs. the concrete `ScreenState` model.**
The `ScreenState` model in Code changes (fields `speaker_left`, `speaker_right`, `community_message`, `whatsapp`, `timer_big`, `timer_corner`, `alarm`) is the authoritative, literal shape implemented.
