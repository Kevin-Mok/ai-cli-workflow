# Screensaver launch behavior

Reproduce the upper-left black rectangle, correct its source, and start each screensaver launch with a random media item on all three monitors. Test the changes before installing and update the shared usage and smoke checks.

## Context and scope

Relevant implementation: `scripts/media_screensaver/core.py` and `renderer.py`; CLI launch paths share these through `main.preview`. Existing conveyor starts with one left-hand card. Scope includes focused tests, README, usage docs, smoke checks and the incident/learning record. Preserve orientation, cadence, muted looping, browser/lock/input gates and originals. Plan Mode is unavailable in this runtime; this file records the execution plan.

## Assumptions and decisions

- User confirmed the existing photo/video mix should remain. Fill every monitor at launch; preserve adjacent non-repeat selection where possible. The reported box stays over the picture.
- No commit/push requested. Keep the current checkout and unrelated work.
- Initial geometry/order hypothesis was disproved. Direct X11 pixels instead reproduce a GTK3 mixed-photo/video presentation defect. Use the verified video-only buffering workaround; retain exact photographed-mask acceptance as unconfirmed.

## Checklist

- [x] Capture initial Git state; inspect source, prior plan, feedback and relevant lessons.
- [x] Reproduce mixed-card rendering defect and observe failing startup/screen-pixel tests.
- [x] Implement the minimum shared workaround and initial three-card selection.
- [x] Run focused and full screensaver regressions and direct runtime checks.
- [x] Update docs and smoke checks; compare/install live package.
- [x] Update postmortem learning and targeted validation.
- [x] Record final evidence, review and remaining risks.
- [ ] User acceptance: recheck the exact partial upper-left mask on the original content.

## Protected state and rollback

Initial dirty files: two description/redshift handoff postmortems, postmortem-memory API/operational/state references and sources.json, GitHub description and video-orientation plans, and four existing prompt files. Preserve all hunks. Shared learning ledger requires additive edits only. Roll back only this session's implementation; reinstall prior owned package files if necessary. Never change media originals or stop unrelated processes.

## Verification

RED: startup entries cover slots 0/1/2 immediately, random choices avoid adjacent repeats where possible; GTK pixel/geometry reproducer must isolate the box. GREEN and regression: system Python Xvfb `test_media_screensaver*.py` suite, browser CJS and display-layout shell tests. Inspect actual screenshots locally without storing personal pixels in Git. Direct CLI: short preview, 35-second preview with report, and status. No sudo required; X11/home installation may require scoped sandbox escalation.

## Progress and review

Postmortem lookup and current hypothesis recorded in `docs/postmortem/2026-10-20-screensaver-launch-black-box.md`. Startup RED: eight unit tests, two defining failures (only slot0 instead of0/1/2); six prior checks passed, exit1. Added three random initial entries and kept the newest selection adjacent to the leftmost startup card. The single-file case deliberately repeats its only available media. Photo-only native-pixel probe did not reproduce a persistent rectangle; separate video/unequal-geometry diagnosis continues. Installed package matched source before changes, with no newer live edits to merge. Full-resolution native smoothness and physical-input acceptance remain distinct from isolated Xvfb results.

Renderer RED: a red MP4 between green PNG siblings was black on the actual X11 screen while playback advanced; root red channel0 instead of>240. GDK captures can omit native children or change presentation, so synchronize GDK then read separate Xlib root pixels. Native-window forcing alone failed. The minimal one-line video-only `set_double_buffered(False)` workaround passes with red253 and green255, including resize/movement. This uses a deprecated GTK3/X11 API with possible flicker/stacking/performance costs; preserve the pixel regression and reassess during a renderer upgrade. No larger renderer rewrite is justified by this task.

Fresh final automated evidence: `xvfb-run -a /usr/bin/python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py' -v` exited0,57/57passed in26.055s, full log `/tmp/screensaver-final-tests.log` read completely. Focused runtime9/9passed. Browser `node tests/test_media_screensaver_browser.cjs` exited0, and `bash tests/test_desktop_display_layout.sh` exited0 with no output. Expected GTK deprecation and missing Xvfb DRI2 diagnostics; upstream Python Xlib Xauthority ResourceWarning observed. No failures/errors.

Real desktop source check: `/tmp/screensaver-native-check.py` sampled only synthetic green photos/red videos on all three real outputs before and after an accelerated slide. All nine points per phase matched expected media, duration dismissal1.604s, cleanupplayers0, exit0. Installed check: `timeout -k 2s 10s /usr/bin/python3 -B /tmp/screensaver-installed-check.py` exited0; `/tmp/screensaver-installed-check.log` records correct startup/after-slide points, dismissal1.609s and cleanupplayers0. Actual installed launcher plus all12packagefiles match repository bytes. Pre-install comparison confirmed only core/renderer differed and live bytes matched HEAD, so no newer live changes were overwritten. Existing idle daemon loads the new code on each spawned preview; no service restart required.

Installed `~/scripts/media-screensaver status` exited0, listed all three monitors and idle monitor running. Automatic activation remains suppressed because the browser bridge is unavailable; manual `ss` remains available. Required `fish -c refresh-config` exited1 on protected changed-target `scripts/media-screensaver` prompt/EOF (private log `/tmp/refresh-config.972vFun5.log`); its chezmoi source path is this checkout. No forced adoption/overwrite. Explicit installation and byte/runtime checks establish screensaver activation separately.

Review found no production-code blocker. Corrected demo wording to reflect all three initial instances. Final evidence review read both complete logs and independently compared installed bytes: five claims verified (startup, rendering workaround,57-test suite, installed desktop playback/cleanup,12/12packagefiles plus launcher equality), with exact user-photo partial-mask acceptance still unresolved. Postmortem learning finding `local-gtk3-mixed-card-presentation` is registered as `verified_workaround` with runtime scope; report SHA-256 `0c1afa3d2375d7d900ff98510f5c7cd838c65d3689601149506e1cf750c9c294`. Targeted memory check exited0 with no errors, missing sources, changed hashes or unregistered aliases. `git diff --check` exited0. No commit or push performed.

## Atomic handoff

Implemented sequence: startup RED → initial three selections → literal X11 renderer RED → video-only buffering workaround → regression/native checks → install/byte check → docs/learning/review. Rollback only these core/renderer edits and reinstall the prior package, preserving unrelated work and private orientation data.

Cursor prompt: “Review plans/screensaver-launch-black-box.md and the scoped core/renderer/startup/runtime-test diff. Preserve pre-existing dirty work. Use system Python and scoped Xvfb for the documented57-test suite; verify all three outputs populate at launch and mixed photo/video pixels remain visible through movement. Treat GTK3 buffering as a legacy workaround and recheck the user's exact partial mask on original content before claiming that symptom fixed. Do not store personal media/screenshots in Git.”

Documentation updated: README, docs/media-screensaver.md, docs/smoke-tests.md, this plan, living incident, tasks/lessons.md and tracked postmortem knowledge. Suggested Conventional Commit: `fix(screensaver): populate outputs and avoid black video regions`.

## Direct verification

From `/home/example/linux-config`, no sudo. These are expected examples, distinct from the observed checks above. Leave input untouched during previews; physical input dismisses them.

- `~/scripts/media-screensaver preview --seconds 35`: all three outputs show random photos/videos immediately; they slide every ten seconds; no rectangle should mask media. Exact photo-mask acceptance remains pending.
- `~/scripts/media-screensaver demo --seconds 35`: disposable formats probe, corrupt fixture skipped, all outputs populated, item1 travels across outputs and playback is released on exit.
- `~/scripts/media-screensaver status`: all three monitor names, idle monitor running, current browser readiness/suppression reason.

## Session delivery milestone

Authorized single-commit delivery: `fix(screensaver): populate outputs and avoid black video regions`, targeting `main` and its configured `origin/main` upstream in `Kevin-Mok/ai-cli-workflow`. Commit and push status will be reported with the actual hash after execution.

Scope uses direct-write evidence for session `01a15bbc-1aa4-7e83-a6a1-5dfa1da5f7bd`: the helper returned `unsafe` because it detected no successful writes through the current tool-call format. The initial Git status was captured before all edits, and the conversation directly records the twelve scoped files. The eleven full-file candidates were clean initially: README; media usage/smoke docs; new incident; artifact-verification reference; this plan; core/renderer; lessons; startup/runtime tests. The twelfth file, sources.json, was already dirty: stage only our new finding/report on top of HEAD, publishing its neutral alias while preserving the actual local alias and all unrelated changes in the working copy.

Excluded pre-existing files: docs/postmortem/2026-10-20-description-handoff-runtime.md; docs/postmortem/2026-10-20-redshift-handoff-byte-check.md; postmortem-memory references/api-contracts-fixtures.md, references/operational-drift.md and references/state-security.md; all unrelated sources.json changes; plans/github-recruiter-descriptions.md and plans/screensaver-video-orientation.md; prompts/monitor-media-screensaver.md, prompts/recruiter-github-descriptions.md, prompts/redshift-temperature-notification.md and prompts/tmux-drag-scroll-copy.md. No previously staged work was present.

Fresh commit checks: startup8/8 and real Xvfb runtime9/9 passed (exit0); complete logs read at /tmp/screensaver-commit-unit.log and /tmp/screensaver-commit-runtime.log. Prior full57-test/browser/display and installed desktop evidence remains recorded above. README gate: pass_no_change. Exact candidate privacy/whitespace validation is required before committing; preserve hooks. No executable behavior changed during delivery preparation. The current code is installed; only original-content visual acceptance and the protected full-refresh conflict remain open. Rollback is a focused revert of this milestone plus reinstalling the prior package; preserve private orientation data and unrelated edits.

Delivery review: the twelve-file staged candidate contains only observed session work. Its ledger diff adds exactly one finding and one report with a neutral public alias; local aliases and all pre-existing changes remain unstaged. Exact-candidate privacy and staged-whitespace checks passed. Re-run the privacy gate immediately before the normal hooked commit, then perform the single configured-upstream push. Commit milestone: random media on every output at startup plus the verified GTK3 mixed-widget presentation workaround; all implementation, tests, docs and this plan ship together. No delivery blocker remains; the exact original-content mask and full-refresh conflict remain acceptance/operational limitations.
