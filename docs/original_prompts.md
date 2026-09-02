# OBS_director — Original Prompts

Append-only log of the user's original prompts, verbatim, most recent last. Appended by the
`documenter` agent after each change is implemented.

## 2026-09-02 — Set up the coordinator agent workflow

> I want to create a director tool for OBS. This is mainly divided into 2 parts:
> * one called `screen` that is a transparent screen that I can add to an OBS scene so that I
>   can make visual effect appear while I am recording (OBS lets a browser window being
>   overlapped on the screen to create the scene)
> * one called `admin` in which there are a lot of tools to create visual effects to appear on
>   the `screen`
> This is a python application that is generating a web page that I can access through a
> browser or with OBS.
>
> To setup this new project, I need the following Claude agents:
> * a coordinator - this is what I call every time I need to implement something new
>     * a product owner - this uses the document `./docs/product.md` and analyse the new
>       changes and produce a Product briefing with all the product details and how the new
>       changes would impact the product in detail. It also generates acceptance criteria and
>       questions
>     * an architect - this uses the document `./docs/architecture.md` and analyse the new
>       changes and produce an Architecture briefing with all the architecture details and how
>       the new changes would impact the architecture of the code in detail. It also produces
>       mermeid diagrams and questions
>     * a developer - this uses the document `./docs/code.md` and analyse the new changes and
>       produce a code change briefing with all the code changes details and how the new
>       changes would impact the previous code in detail. It also generates questions
>     * a tester - this uses the document `./docs/code.md` and analyse the new changes and
>       produce a test plan. It also generates questions
> * after getting an input from every other agent, the coordinator generates a plan with the
>   details of the change in the form of
> ```
> # <TITLE OF THE CHANGE> - <DATETIME>
> ## Context of the changes
> <product owner input>
> ## Architectural Impact
> <architect input>
> ## Code changes
> <developer input>
> ## Testing information
> <tester input>
>
> # Deep Dives
> <Most important questions>
> ```
> * the coordinator estimates if there is any need of asking questions to the user. It uses
>   only questions from the other agents. If possible, it answer itself questions using the
>   input of the other agents
> * the coordinator asks an advisor to estimate if the plan makes sense, if there are other
>   questions to ask to the user, and if that is the case, it asks these questions
> * then the coordinator start the following two agent, in this order
>     * the implementer: this takes the plan and implements it, silently
>     * the documenter: takes the plan and updates all the documents: 1. `./docs/product.md`,
>       2. `./docs/architecture.md`, 3. `./docs/code.md`, 4. `./docs/plans.md` (by appending the
>       last plan to the file), 5. `./docs/original_prompts.md` with all the user prompts (this
>       included)
>
> This is the first task for you. Feel free to ask my any question to clarify, but don't do
> that if it is not strictly needed for solving ambiguities

## 2026-09-02 — First release: five live overlay effects

### Original request (start of task)

> This is the first real feature set for OBS_director (currently greenfield: only docs/ seed files exist, no code, no framework chosen yet — see docs/product.md and docs/architecture.md for the current "undecided" state). Drive this from idea to implemented-and-documented code, per your normal process (product-owner, architect, developer, tester agents → composed plan → advisor sanity check → resolve open questions, asking the user only when truly necessary → implementer → documenter).
>
> The user wants FIVE features built together as one coherent first release, all controllable from the `admin` page and rendered on the `screen` page (transparent OBS Browser Source overlay). Exact user request, verbatim:
>
> 1. **Speaker presentation**: Admin can set up a list of speakers (persisted, reusable across sessions). Each speaker has a full name (large, majority of the banner) and a smaller description/title ("who he is"); if description is missing, default it sensibly from the name. From the admin, operator selects a speaker AND a screen side (left or right). On selection, a fancy bar animates in from that side, then the name materializes on it (entrance direction must match the selected side). The banner stays until: the speaker is deselected in admin, OR a different speaker is selected — in which case the current one animates out before the new one animates in (never both on screen at once on that side).
>
> 2. **Community message**: Two input paths feeding the same on-screen animated display: (a) read/import messages from a free-to-access social account (X, Discord, Facebook, WhatsApp, etc.) and let the operator search/pick one from what could be a huge list; (b) a free-text field to paste/write a custom message plus a selector for which social platform's visual style to simulate. Either path results in the message being shown on screen with a nice entrance animation, styled to look like the chosen/source social platform.
>
> 3. **WhatsApp discussion simulator**: Admin lets the operator author one or more named conversations ahead of time. Each conversation is a named list of messages; each message is tagged as arriving from the left (incoming, shows a sender name) or right (outgoing/"me", shows timestamp + blue double-check marks). Selecting a saved conversation in admin makes it take over the full screen and animates the messages in one by one as if arriving live.
>
> 4. **Timers**: Be creative. Support at least: a big centered timer and a corner (bottom-right or top-right) timer. Support simple countdown-to-zero, and also count from a set start point to a set end point (i.e., configurable start/end, not just count-up-from-zero or countdown-from-N). Operator controls placement/mode/values from admin.
>
> 5. **Big red alarm**: A bold, attention-grabbing red alarm banner/effect, centered at bottom or top of the screen, in the spirit of a loud "whining" alert — operator triggers/dismisses it from admin.
>
> Admin UX constraint (explicit from the user): it's fine to have multiple admin pages/sections for *preparing* content ahead of time (setting up the speaker list, writing whatsapp conversations, configuring timers, composing alarms). But everything the operator actually *does live during a stream* — selecting/deselecting a prepared speaker+side, pasting or picking a community message and its style, launching a prepared whatsapp conversation, starting/stopping/configuring a timer, triggering/dismissing the alarm — must be reachable from one single, minimal, clear "live control" admin page. Don't make the operator hunt across pages mid-stream.
>
> Since the web framework, real-time push channel (websockets/SSE/polling), and project layout are all still open architecture questions per docs/architecture.md, have the architect agent make and justify concrete choices as part of this change — don't leave them open. Multiple concurrent effects (speaker banner + community message + timer + alarm all live at once, on independent layers) should be supported since these are visually distinct screen regions that could reasonably be shown together.
>
> Use AskUserQuestion sparingly and only for genuine product decisions you can't reasonably default (e.g., if there's a real fork in direction for the social-message import mechanism given "any free to access social media" is vague, or persistence choice, etc.) — otherwise make sensible calls and proceed, consistent with how you normally operate.

### Clarifying answers given by the user during plan resolution

> User answers to all three open questions — proceed to finalize the plan and implement:
>
> 1. Speaker banner model: Two independent per-side slots (Option B), CONFIRMED — but with one added requirement: if the opposite side's slot is empty, the occupied side's banner should take up most of the screen width (i.e. banner width is dynamic — a lone speaker gets a wide/prominent banner, but if both sides are occupied simultaneously, each banner narrows to share the screen with the other side). Both slots' animations (enter/exit, materialize) still work exactly as previously designed per-side.
>
> 2. Community message import: Option C — skip real import for v1. Build the provider interface/abstraction so a real platform can be plugged in later, but ship with no concrete provider wired up (search returns no results for now). The free-text-plus-platform-style path must be fully functional.
>
> 3. Big red alarm: Option B — include real siren audio via Web Audio, played through the browser tab. Handle browser autoplay restrictions sensibly (e.g. trigger only on an explicit admin action, which counts as a user-gesture-adjacent trigger from the operator's perspective — document that OBS needs to be configured to capture that Browser Source's audio track for the siren to be heard in the stream/recording).

## 2026-09-02 — Live Control simplification, screen visual overhaul, preset YAML export/import

### Original request (start of task)

> The user wants a substantial UI/UX overhaul of OBS_director's admin ("Live Control") panel and the OBS "screen" display page, plus new preset import/export capability. Full requirements from the user, verbatim intent preserved:
>
> 1. Simplify the admin panel (currently called "Live Control") — it's too big with too many elements:
>    a. Remove the top "Live Control" heading and the descriptive text below it.
>    b. "Speaker banners" section: keep the title, but collapse each subgroup ("Left" and "Right") to one line each. Put an icon representing Left/Right to the left of the selection box. Replace the "Show on left"/"Clear left" (and right equivalents) buttons with standardized icon buttons: one "show" icon and one "clear" icon (reused for both left and right, i.e. just two icon meanings total, applied per row).
>    c. "Community message" section: remove the "Import" tab/feature for now — only keep "Compose". Remove the section title. Keep: icons for selecting which social platform, two text fields (one short for name/handle, one longer for the message), and replace "Show"/"Dismiss" text buttons with icon buttons.
>    d. Overall goal: simplify visually using icons, and lay elements out inline/horizontally and aligned wherever possible to save vertical space.
>
> 2. Improve the "screen" (OBS browser source output) page's visuals:
>    a. Speaker banner should look more like a modern, elegant news-broadcast lower-third/banner. Add the ability in the admin page to choose between banner styles — design ~4-5 distinct style presets that make sense for this use case (e.g. classic lower-third, minimal, glassmorphism, bold color-block, outline/ghost style — use your judgment on what's tasteful).
>    b. The community message banner should animate in from the left, positioned at the bottom, and should fade out any currently-showing speaker banner when it appears. The community message banner should include the community's logo on its left side. Colors should be visually appealing/on-brand.
>    c. The central countdown timer is good as-is functionally, but needs a few visual style options too — including one style with no background (transparent/text-only).
>
> 3. Be creative with presets: add the ability to attach an image to a banner/preset and have it sized to the same height as the banner, positioned on the left or right side depending on which side the controller is showing it on (i.e. ties into the existing Left/Right speaker banner concept).
>
> 4. Add the ability to export and import all presets as a YAML file. For any custom file reference within a preset (e.g. custom images), store/use the full machine filesystem path.
>
> Please gather input from your usual sub-agents (product-owner, architect, developer, tester), compose one coherent change plan, get it sanity-checked by the advisor, resolve any open questions yourself where reasonable (ask the user only if something is truly ambiguous or high-stakes, e.g. destructive/breaking changes to existing presets/config format), then run the implementer and documenter in sequence. This is a real implementation task — please write the actual code changes, not just a plan.

### Clarifying answers given by the user during plan resolution

> Export/import scope: (A) Everything — full backup. Bundle includes speaker roster (with new per-speaker banner style + image path), WhatsApp conversation presets, alarm presets, and the new community branding config (logo path + accent color).
>
> Import behavior: (A) Full replace + auto-backup. Importing overwrites current data for each included category with the YAML contents, but first auto-saves a timestamped backup of the current data/ directory so the prior state is always recoverable.

> Decision: (B) Leave /media LAN-reachable, no additional restriction — matches the app's existing "single local operator tool" trust model, same spirit as the already-accepted full-filesystem-path tradeoff. Please document this as an explicit accepted tradeoff (in docs/architecture.md's security/trust section) and proceed with finalizing the plan and running the implementer and documenter.
