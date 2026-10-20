# Correct screensaver video orientation

Honor video orientation tags and let the user review an additional rotation in a separate GTK window. Reproduce with asymmetric pixel fixtures, add automatic and manual filters, persist private corrections, then install and verify without changing originals.

## Context and scope

The supplied plan is the specification. Scope: `scripts/media_screensaver/{renderer,main,orientation,review}.py`, screensaver tests, README, usage docs and smoke checks. Installation already copies all package files. Keep muted looping playback, persistent movement and black letterboxing. No orientation guesses or changes to originals. No commit/push was requested during implementation; the later commit-plan-push authorizes delivery (see dirty-worktree-delivery.md). Suggested subject: `fix(screensaver): honor and remember video orientation`.

Initial dirty state: README, media-screensaver docs, smoke tests, three postmortem references and sources.json (partly staged), i3 template; untracked postmortems, shortcut/GitHub plans and prompts. Preserve all of these; add only scoped documentation to their existing content. Working in existing checkout; no worktree requested. Plan mode is not available in this runtime, so this file records execution decisions.

## Decisions and interfaces

Automatic `videoflip video-direction=auto` precedes a second flip for additional clockwise degrees 0/90/180/270. Shared Card owns both; review uses the same Card and never subscribes to screensaver dismissal. Read corrections per Card creation. Save keyed by absolute path plus size and nanosecond mtime; stale records ignored. Validate the entire JSON before mutation; invalid data warns and blocks save. Private atomic replacement under XDG_CONFIG_HOME, preserving other records and serializing saves.

Postmortem lookup: `screensaver orientation gstreamer rotation` returned stream-copy compatibility guidance (artifact-verification); it concerns concat/remux, not this renderer. No applicable orientation fix. The defining reproducer will determine this change's scope. Exploratory help/file probes encountered invalid lookup subcommand and nonexistent guessed test filename; no runtime or tracked data affected; use catalog-supported commands and mapped files going forward.

## Checklist

- [x] Capture initial Git state and inspect renderer, CLI, docs and relevant feedback.
- [x] Observe RED for actual rotation pixels and correction persistence/review behavior.
- [x] Add filters, validated private store and independent review/chooser command.
- [x] Cover all rotations, absent metadata, portrait/landscape, correction/reset/cancel, malformed/stale data, spaces, loop/move/cleanup.
- [x] Update README, usage and grouped smoke checks.
- [x] Run Xvfb Python suite, browser/display regressions and fresh review.
- [x] Install, compare installed bytes, inspect local clip and unchanged hashes if identifiable.

## Verification

Use `xvfb-run -a /usr/bin/python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py' -v`; browser: `node tests/test_media_screensaver_browser.cjs`; display: `bash tests/test_desktop_display_layout.sh`. Synthetic FFmpeg fixtures encode asymmetric colored quadrants and remux rotation metadata; compare GTK output pixels with literal expected arrangements, not dimensions. Store tests use temporary XDG config and real files. Review tests click real GTK controls and reopen files.

Manual/direct checks (no sudo, repo cwd): installed `orient`, `orient --file '/absolute/path/problem.mov'`, and `preview --media '/absolute/path/containing-directory' --seconds 35`. Need an identified known troublesome clip before claiming its particular cause resolved. Hash originals before/after; personal paths and pixels stay outside tracked artifacts.

## Risks, rollback and evidence

Rotation convention must be proved with pixels. GTK/GStreamer requires X11 and system Python GI. Metadata may itself be wrong: review correction is explicit. Renames need review again. Rollback: reinstall previous renderer/package; private corrections can remain inert. Installation writes home and needs workspace escalation. Refresh tracked configuration only if configuration changes; this task changes script/package and docs.

## Progress and verification evidence

- RED: initial fixture lacked GTK initialization and the default sandbox blocked X11. The legacy FFmpeg rotate option also silently omitted display matrices. These were test-infrastructure defects, recorded in `docs/postmortem/2026-10-20-orientation-test-gtk-init.md`; no production inference was accepted from those runs.
- True RED: ffprobe-verified matrices using input `-noautorotate -display_rotation`; dynamically loaded HEAD renderer in a temporary module failed six 90/180/270 pixel subtests for both shapes. Identity/no-metadata cases remained upright.
- GREEN: automatic filter consumes GStreamer orientation tags, manual filter applies additional clockwise rotation afterward. Focused suite passed; full Xvfb Python suite initially passed 48 tests in 23.912s, browser CJS and display shell checks both exited 0. Full log inspected. Final expanded checks recorded below.
- Store tests: all rotations, reset preserving neighbors, permissions, stale size/mtime, malformed data preservation, symlink rejection; additional exceptional replacement and competing-writer checks included in final suite.
- Review: actual GTK buttons and rendered pixels establish right/left/reset/save/reopen/cancel, input persistence and NULL-state cleanup. Additional real CLI main-loop, decoder-failure and ASCII progress/save checks included in final suite.
- Independent evidence review: eight claims verified; found Unicode degree/bullet characters leaking into new plain CLI messages, plus stale plan status. Added defining ASCII test, observed RED, changed CLI messages to ASCII degree text and separators. GTK labels retain degree glyphs. Lifecycle/exceptional-write coverage gaps addressed with focused real-path checks. No architecture change.
- Installation: source-vs-installed comparison found only intended main/renderer source-newer differences; no newer installed work to merge. Existing installer exited0 and installed all12 deployable package files with byte equality. Final reinstall after the plain-output fix exited0 and retained byte equality for all12files.
- Personal-library evidence: sampled two local files, encoded 3840×2160 and1920×1440, each with FFprobe rotation -90. Captured identical timestamp frames with baseline and installed renderer, inspected both pairs locally: sideways before, upright after with black bars. Paths/pixels stay in private temporary artifacts, outside tracked docs. Both original SHA-256 hashes remained unchanged.
- Installed renderer ran the first personal sample for35seconds under Xvfb with three simulated320×240 outputs. Item1 settled in slots0/1/2 and exited; no decode errors; final cleanup players0; both original hashes rechecked unchanged. This establishes installed orientation/movement/cleanup, not native three-monitor smoothness.
- README gate: `update_in_same_change`; existing recruiter hook, stack rationale and navigation retained. Added truthful orient/--file documentation using actual --help. Existing unrelated README/doc/i3 edits retained.

## Final handoff and rollback

Atomic sequence: reproduce pixels → shared filters/private store → separate chooser/review → docs → regression/review → install/compare/runtime. Roll back by reinstalling the previous package; saved corrections remain private and inert with the previous renderer. No original-media rewrite and no guessed orientation. No runtime configuration file was changed by this task; the explicit installer deploys scripts (refresh excludes scripts). At implementation handoff no commit or push had been requested/performed; later commit-plan-push delivery is recorded in dirty-worktree-delivery.md.

Cursor prompt: “Review the screensaver orientation change against plans/screensaver-video-orientation.md. Preserve unrelated dirty work and originals, run the documented Xvfb/browser/display checks, and verify orient chooser/save/reset/cancel plus upright playback across slots. Use scoped X11 execution here. Do not claim native desktop smoothness from Xvfb.”

Suggested Conventional Commit: `fix(screensaver): honor and remember video orientation`.

Remaining acceptance: native desktop full-resolution multi-video smoothness and review of any other incorrectly tagged or untagged personal clips. The two sampled clips are verified fixed by honoring their metadata. Final evidence: full Python screensaver suite54/54passed in24.565s (exit0, complete log inspected); latest black-letterbox pixel matrix passed separately (exit0) after landing during that run. Browser CJS passed and display shell regression exited0 silently. New CLI ASCII test observed RED then GREEN. Atomic replacement-failure, competing8writers, mtime-only staleness, CLI loop/chooser cancellation, decoder-error disabled Save and cleanup all passed. Scoped Xvfb emits missing DRI2 diagnostic; no test failed. An initial focused rerun omitted PYTHONPATH and failed import; corrected invocation passed, captured in the fixture incident.

Final installer exited0; all12deployed package files match source bytes. Installed `orient` selected a real library file through its chooser, saved90degrees in a temporary private config, reopened with90, reset through Use metadata and saved0; every playback pipeline reached NULL. Personal source hashes rechecked unchanged after those checks. No personal corrections were added to the user's live orientation store. Git diff --check exited0. Postmortem learning report/hash updated in tracked memory and targeted check passed with no errors. No unrelated staged or dirty work was discarded or staged by this session. The implementation and verification are complete; native full-resolution smoothness remains manual acceptance.

## Direct verification commands

Working directory `/home/example/linux-config`, no sudo. Replace the example file path. These are expected UI observations; observed automated/installed evidence is recorded above.

`~/scripts/media-screensaver orient`: chooser opens in the library; selected video loops with rotation, Save and Cancel controls.

`~/scripts/media-screensaver orient --file '/absolute/path/problem.mov'`: save a correction, reopen to retain it; Use metadata followed by Save removes it.

`~/scripts/media-screensaver preview --media '/mnt/linux-files-3/hevin' --seconds 35`: corrected video remains upright across slots, aspect ratio preserved, movement continues; physical input dismisses. Random selection may require a small directory for an identified clip.
