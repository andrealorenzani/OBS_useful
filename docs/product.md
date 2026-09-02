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
Multiple `screen` clients (e.g. the real OBS Browser Source and a browser tab used for testing)
always reflect identical, synchronized state, since there is a single server-side source of
truth for what's currently showing.

`admin` is split into two kinds of surface:
- **Prep pages** — for building reusable content ahead of time: the speaker roster, WhatsApp
  conversation scripts, and alarm presets. These are visited before or between streams, not
  during one.
- **The live-control page** — a single page containing every action the operator needs while
  actually recording, across all effects. The operator must never need to leave this page or
  hunt across other admin pages mid-stream.

## Status
The first real feature release has shipped: five overlay effects, all wired through the
`screen`/`admin` split described above. A follow-up release simplified the live-control page's
chrome, added the visual style/branding options described per-effect below, and added an
"export/import all presets as one YAML file" backup/transfer tool (reachable from the admin nav):
export bundles the speaker roster, WhatsApp conversation presets, alarm presets, and community
branding into a single downloadable file; import fully replaces those categories from an
uploaded file, after automatically backing up the current data first. Any file reference inside
an exported preset (a speaker's banner image, the community logo) is stored as the full local
filesystem path from the machine it was exported on — importing does not copy the file itself.

### Effects

1. **Speaker presentation** — a lower-third-style banner naming a speaker. The operator
   maintains a reusable speaker roster in a prep page (full name, required; description/title,
   optional), persisted across sessions/restarts. During the stream, the operator selects a
   speaker and a screen side (left or right) from live control. The two sides are independent
   slots — a speaker can be showing on the left and a different one on the right at the same
   time (e.g. for a two-person interview). Selecting a new speaker for a side that's already
   occupied plays that side's out-animation before the new speaker's in-animation, so a side
   never shows two names overlapping; the name materializes as a distinct visual beat after the
   banner slides in from its side. If description is blank, no empty subtitle is shown — the
   name occupies the banner alone. Banner width is dynamic: a lone occupied side gets a
   wide/prominent banner, and when both sides are occupied at once each narrows to share the
   screen, animating smoothly as occupancy changes. Editing the roster only affects future
   selections, not a banner already live; deleting a speaker that's currently live clears that
   side. Each roster entry can also carry a banner style (one of five presets: classic, minimal,
   glass, bold, outline) and an optional banner image, sized to the banner's height and shown on
   whichever side the banner is currently on — both configured once per speaker on the roster
   prep page, not re-picked live.

2. **Community message** — a social-media-styled callout with two authoring paths that converge
   on the same on-screen presentation: importing a message from a connected social account, or
   writing free text and picking which platform's visual style to mimic (at least X, Discord,
   Facebook, WhatsApp). In this release, the free-text-plus-style path is fully functional; the
   import path exists as a provider abstraction with no concrete platform wired up yet (search
   returns no results) so a real provider can be added later without reworking the display.
   Only one community message is shown at a time; showing a new one replaces the previous one
   with the same animate-out-then-in sequencing used by the speaker banner, and the operator can
   dismiss it entirely. It animates in from the left edge, anchors bottom-left, and displays one
   shared community logo alongside an on-brand accent color (both configured once, globally, in a
   small branding section on a prep page) — see Concurrency below for its interaction with the
   speaker banner.

3. **WhatsApp discussion simulator** — pre-authored, named, fake chat scripts (ordered
   messages, each tagged incoming/left-with-sender-name or outgoing/right-with-timestamp-and-
   read-receipts) played back live as a full-screen animated conversation, one message revealed
   at a time. Unlike the other four effects, this one takes over the entire screen while
   playing rather than sharing it — the other effects' state is preserved but visually covered
   underneath, and reappears once the operator stops the conversation. Only one conversation
   plays at a time, and the finished conversation stays fully visible until explicitly
   dismissed.

4. **Timers** — two independent placements (a big centered timer and a corner timer), each
   supporting two modes: countdown from a configured duration to zero, or counting between an
   arbitrary configured start and end value. Both placements can run simultaneously with
   different modes/values. Reaching the end value is visually distinct (a flourish) rather than
   silently continuing or vanishing. Timers are configured ad hoc on the live-control page; no
   timer-preset persistence exists in this release. The central/big timer also offers a choice of
   visual style per start (solid, glass, outline, or a transparent text-only look with no
   background box); this style picker is specific to the central timer — the corner timer keeps
   its single existing look.

5. **Big red alarm** — a bold, high-contrast red banner (top or bottom, centered) for a "pay
   attention" moment, with a pulsing/looping entrance animation and real siren audio played
   through the browser tab (so OBS must be configured to capture that Browser Source's audio
   track for the siren to be heard in the recording/stream). Content can be composed and saved
   as a preset ahead of time in a prep page, or triggered with default content; the operator
   triggers and dismisses it live with a single action each.

### Concurrency
Speaker banner(s), community message, timer(s), and alarm are independent visual layers on
`screen` and can all be visible at the same time, each in its own screen region, without one
effect's animation or state interfering with another's. The WhatsApp simulator is the
deliberate exception: it takes over the full frame while active, covering (but not clearing)
whatever else is showing.

A second, narrower exception: when a community message appears, it anchors bottom-left (the same
corner as the left speaker banner) and any currently-showing speaker banner(s) fade out to make
room for it, then fade back in automatically once the community message is dismissed — the
underlying speaker selection is never cleared, only visually covered, exactly like the WhatsApp
takeover above but scoped to the speaker region instead of the whole screen.

## Open product questions
None outstanding for this release. Future extensions to watch for: wiring a real community-
message import provider (the abstraction is ready but unimplemented), and whether timers or
other effects eventually need persisted presets like the alarm does.
