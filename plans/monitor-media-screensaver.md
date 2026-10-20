# Media conveyor screensaver implementation plan

Build the requested X11/i3 screensaver, verify its timing and browser playback gate, install the launcher and idle integration, and record desktop evidence. This plan and the usage guide record the implementation scope. The original prompt was pre-existing local work and is excluded from the session commit.

## Purpose and observable outcome

Random photos/videos travel left → middle 4K → right → exit at fixed 10-second intervals with 750ms slides. Video playback survives moves. Idle activation after 300 seconds is suppressed by qualifying Chrome video or an unavailable bridge; manual preview remains usable. Activity or qualifying playback dismisses it.

## Context and boundaries

Preserve `scripts/executable_dual-monitor-slideshow` and never invoke its display switching. Read `scripts/executable_apply-desktop-display-layout` only. Live geometry is DVI-D-0 2048x1152+0+504, DP-2 3840x2160+2048+0, HDMI-0 1920x1080+5888+540 (approved xrandr inspection, exit 0). Media root /mnt/linux-files-3/hevin is mounted. Installed: Python GI/GTK3/GStreamer, mpv, ffmpeg, ImageMagick HEIC reader, Python Xlib, Xvfb. No PyQt/PySide.

Protected initial dirty state: postmortem-memory references/api-contracts-fixtures.md, references/state-security.md, sources.json; untracked prompts/monitor-media-screensaver.md and prompts/tmux-drag-scroll-copy.md. Preserve all pre-existing edits. No commit/push requested.

## Decisions and assumptions

- Implement inline with focused read-only search/docs/testing/review agents; user specification authorizes implementation. Active harness is Default mode; Plan Mode is unavailable, so use this living ExecPlan.
- Choose the smallest installed renderer after a synthetic runtime probe; persistent Gtk widgets and GStreamer or embedded mpv can move without restarting video. No new dependency unless required by evidence.
- Never change xrandr outputs, lock settings, suspend timers or originals. Read live geometry at launch; require three horizontally ordered outputs and a middle 4K display for automatic activation.
- Native messaging carries only playback state and geometry/IDs; no URLs, titles or browsing content. Missing/stale/malformed state fails closed for auto mode.
- Browser extension enablement may require the user’s Chrome developer-mode action. Prepare a concrete installable package and document any activation still outstanding.

## Ordered implementation checklist

- [x] Capture initial state; read spec and desktop scripts; inspect dependencies and live geometry.
- [x] Map install/idle/lock/test conventions and relevant feedback/lessons.
- [x] Write and observe failing tests for cadence, selection, geometry/gating, stale state and cleanup.
- [x] Implement core and renderer, synthetic media fixtures/probe, then verify persistent playback and error handling.
- [x] Implement MV3 extension/native host and strict bridge protocol; exercise multiple windows, active tabs, fullscreen/iframes and failure.
- [x] Add installed launcher and idle startup while preserving lock/suspend; update README, usage and grouped smoke checks.
- [x] Attempt refresh-config (blocked on unrelated mimeapps conflict); verify scoped installation, automated checks and real desktop acceptance.
- [x] Obtain independent review; resolve material findings; reconcile docs and report exact remaining limitations.

## Tests and verification

Defining tests must run RED before implementation, then GREEN. Use synthetic images/video and temporary homes only; never commit personal media. Test fixed cadence without drift, identity through three slots, no immediate duplicates, corrupt/missing mount, browser gate intersection/active/minimized/audio/paused/stale/multiple clients, protocol bounds, child cleanup and signal handling. Use Xvfb for offline renderer checks and approved real desktop access for observed movement/timestamps/input dismissal and unchanged geometry. Browser enablement must distinguish synthetic protocol tests from real Chrome evidence.

## Risks, rollback and review focus

Rendering at 7808x2160 can be expensive; verify frame movement on actual hardware. Browser content restrictions, zoom, nested/cross-origin frames, minimized/fullscreen windows, state freshness and disconnected profiles require explicit handling. Missing codecs must produce actionable status and skip individual bad files. Avoid restarting existing lock services. Roll back by stopping only the new daemon and removing its i3 startup line/installed files; old slideshow and lock/suspend remain untouched.

## Progress and evidence

Initial xrandr in sandbox failed; living report `docs/postmortem/2026-10-20-screensaver-x11-sandbox.md` records lookup and approved workaround. Actual geometry queried with require_escalated, exit 0; no mutation. Search and browser API documentation agents are running.

## Review notes

Independent source/evidence review completed. Monitor projection, full native-window matching, audio-only video detection, deeply nested JSON and iframe WindowProxy initialization findings were fixed with executable regression evidence. No outstanding known implementation finding; live five-minute idle and suspend/resume remain unobserved.

Core 7/7, real escalated Xvfb renderer 2/2, CLI install/usage 2/2, bridge bounds/native framing 14/14 pass after observed missing-feature RED. Browser geometry passes; closed-shadow traversal is undergoing RED/GREEN. Renderer startup was corrected to start only after widget parenting and prefer CPU-compatible libav decoders. No live movement claim yet.

Implementation and independent review milestone: full installed launcher, native host/extension, calibrated UI scale, raw XI2 inactivity, complete browser-window reconciliation, scoped live i3 registration, documentation and smoke checks are present. Automated suite31/31 plus Node geometry, existing desktop layout shell check and compilation passed. Full refresh was attempted and blocked by unrelated live mimeapps conflict; scoped installer preserves it. Real installed status: idle monitor running; automatic activation suppressed for uncovered Chrome profiles. Browser end-to-end matrix and full quiet-window visuals remain pending.

## Atomic handoff and Cursor prompt

Keep the launcher, package/extension, tests, i3 startup, README/usage/smoke changes, local lesson, living postmortem/ledger update and this plan in one related implementation change. Preserve initial dirty references/ledger hunks and untracked unrelated prompts; no commit or push was requested. Suggested subject: `feat(desktop): add media conveyor screensaver`.

Cursor prompt: Read this plan and `docs/media-screensaver.md`. Verify the installed screensaver and remaining live acceptance cases without rewriting working modules. Use synthetic media, preserve original media/display layout/lock behavior and unrelated dirty state, run the focused Python/Xvfb and Node suites, and update this plan with exact observed evidence. Do not claim missing browser/profile enablement or visual/lock acceptance is complete from unit tests alone.

Fresh full suite32/32 passes after requiring XI2.1: an executable regression observed XI2.0 missing raw keys while another client owned a keyboard grab; XI2.1 keeps the idle clock accurate through existing lock grabs. Browser matrix has nine observed passing cases (middle/side/move/pause/fullscreen/audio/ended), with cross-origin iframe investigation ongoing. A final40-second quiet-window run was explicitly coordinated with the user and browser worker.

## Observed real desktop acceptance

The final coordinated 35-second synthetic preview exited0. Item#1 visibly occupied left, middle and right in separately captured/screenshotted GTK frames. Advances were at elapsed10.017,20.017,30.018seconds; settlements10.766/20.751seconds, about750ms after the deadlines. Item#1 playback progressed9.870→10.620→19.871→20.604→29.872→30.620seconds across transitions; it was released at30.766seconds, with no restart. Duration dismissal at35.016s, cleanup at35.032s, pipelines0. xrandr --listmonitors bytes were identical before/after (exit0). Earlier previews demonstrated physical-input dismissal and cleanup. Temporary synthetic screenshots/report remain under /tmp, not tracked.

Final acceptance additions: real Xvfb short-video looping and portrait black-letterbox pixels passed (suite34/34). Explicit manual-preview bridge-runtime failure was then reproduced (RuntimeError before renderer launch); manual mode now supplies an unavailable gate and continues, while automatic mode remains suppressed. Fresh35-test verification follows. Actual full desktop screenshot/timing evidence above supersedes earlier interrupted attempts; input detection deliberately retains all real/synthetic keyboard/mouse events rather than filtering accessibility or imwheel sources.

## Final deliverables and verification

- `scripts/media_screensaver/core.py`: discovery, random selection, fixed deadlines and interpolated live geometry. `renderer.py`: persistent GTK/GStreamer cards, HEIC temporary conversion, XI2.1 input and complete cleanup. `main.py` plus installed launcher: preview/probe/demo/status/install, 300-second idle supervision and safe per-user i3 registration.
- `bridge.py` and `browser/`: strict private native messaging, active-tab/frame/shadow-root playback geometry, calibrated browser scale and fail-closed state; `desktop.py` reconciles all native Chrome windows and excludes unmapped playback. `fixtures.py` generates disposable synthetic media. Matching Python/Node tests, README, usage, smoke checklist, lessons and this living plan travel with the implementation.
- Final automated evidence: `xvfb-run -a python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py' -v` exited0,37/37. This includes exact299.9→300s activation boundary with a real owned child that is reaped, actual GStreamer continuity/loops, portrait pixels, bridge failure fallback and video-start dismissal. `node tests/test_media_screensaver_browser.cjs` exited0 after the final iframe/scale/audio changes. Existing `bash tests/test_desktop_display_layout.sh` and syntax compilation passed. Xvfb only emitted its expected missing DRI2 warning.
- Real mounted library samples decoded: MKV/H264, MOV/H264, MP4/HEVC; original sizes/mtimes unchanged. HEIC conversion succeeded and original SHA-256 stayed identical. Synthetic JPG/JPEG/PNG/WebP and containers decoded; corrupt MP4 skipped without abort. Missing mount case passes actionable CLI regression.
- Real sandboxed Chrome146 isolated profile:20 passing cases cover middle/left/right/moving/pause/ended/fullscreen, audio element and audio-only source inside video, cross-origin iframe, closed shadow root, two windows, hidden i3 scratchpad, active versus background tab and native disconnect/reconnect. Native files contained no test URLs, media paths or page content. Raw bridge checks and native-filtered owned-window checks are distinguished from the global gate: ordinary user profiles remain unchanged and uncovered, so the global automatic gate correctly suppresses activation. Temporary evidence `/tmp/media-screensaver-browser-matrix-m0gHOE/results.json` and summary were independently read.
- i3 ignored conventional minimize: Chrome stayed normal and X11 viewable, so continuing to block was correct. Actual non-viewable scratchpad playback was excluded successfully; minimized protocol behavior is also unit-tested. Browser package permissions omit unnecessary tabs access.
- Final install byte comparison:9 deployable package files matched source. Installed daemon restarted with final code; old owned daemon stopped, new i3 launch succeeded. No commits, push or changes to the legacy slideshow.

Remaining acceptance limits: ordinary profiles still require documented unpacked extension enablement; no real uninterrupted300-second idle wait or suspend/resume was performed. Full refresh remains blocked on protected local mimeapps differences, with scoped screensaver installation complete. Mixed/unreconciled scaling, uncertain transforms/PiP/restricted tabs fail closed; non-HTML-video canvas players are unsupported. The default media mount remains `/mnt/linux-files-3/hevin`.

Final delivery checks: browser cleanup receipt confirms no owned browser/window/server/native state left. Final normal refresh was attempted after the manifest change and still stopped on the preserved mimeapps conflict; the clean-shell invocation correction is recorded in the living report. Scoped install remains verified and daemon status is running/suppressed pending normal-profile enablement. All pre-existing dirty sources and unrelated prompts remain unstaged; no commit/push. Final postmortem hash/alias check exited0 with no errors or missing sources (SHA-256 c3bcad1e220d659d0e1dbc0898b91b1c1bdf22abddb4c12c97dfef1d90a3cf53); source/install identity and git diff --check also passed immediately before handoff.

## Delivery milestone: feat(desktop): add media conveyor screensaver

Session-scoped commit requested after implementation. Scope helper returned unsafe because it did not detect writes made through this tool transport; use direct observed-write attribution and the captured initial Git status. Include the launcher/package, six test files, README/usage/smoke docs, i3 startup, local lessons, this plan and the screensaver postmortem. Stage only the screensaver report addition from the baseline-dirty memory ledger. Exclude all unrelated ledger edits, the two baseline-dirty reference files and both untouched pre-existing prompts.

Fresh pre-commit verification:37/37 Xvfb Python tests, Node browser tests, existing desktop layout check and README gate (`pass_no_change`) passed. The earlier real35-second desktop and20-case isolated-browser evidence remains applicable; implementation is unchanged. Installed launcher and package were verified identical to source. No known implementation blocker; normal-profile enablement, actual300-second/suspend observations and the unrelated MIME refresh conflict remain as documented. Next step: privacy-check the exact staged candidate, commit this milestone, and push main to origin/main. Preserve unrelated dirty work.

Commit packaging: privacy lookup matched existing public-alias guidance. The staged ledger publishes a neutral example-home alias; the working ledger retains the machine-specific alias with unrelated local edits. Removed one trailing blank line. Postmortem reviewed hash updated; exact candidate checks follow. No executable behavior changed.
