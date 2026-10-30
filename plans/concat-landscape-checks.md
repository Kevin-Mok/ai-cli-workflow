# Landscape concat and start-frame checks

Extend the existing concat CLI so one command joins mixed camera clips into a landscape video, checks the result, and saves one start-frame preview per joined clip for visual orientation review.

## Purpose, scope and decisions

- Spec: the live request is a reusable script to concat, then check only the start of each clip. Output is always landscape; portrait footage gets side bars.
- Modify `scripts/executable_concat-timestamped-videos`, its existing unittest file, README and grouped smoke checks. Preserve existing stream-copy and selected-pair reencode behavior.
- Add `--landscape`: sequentially normalize clips to a common 16:9 H.264/AAC SDR format, join, verify landscape geometry and generate `<output-stem>.review/index.html` with one frame from each segment start in the actual joined output. Temporary normalized clips live beside the destination and are cleaned automatically.
- Add `--sort mtime` (oldest first, filename tie-break), retaining capture order by default. Include uppercase MOV/MP4 via existing case-insensitive matching.
- Add repeatable `--rotate NAME=90|180|270` with `--landscape` for manual correction after embedded rotation is applied. No semantic/AI upright claim: the review page explicitly requires human visual checking, and cannot detect a rotation later in a clip.
- Choose 16:9 dimensions from the first clip's longest side (even dimensions), preserving 3840x2160 for the actual source folder. Normalize frame rate and audio consistently; keep existing HLG-to-SDR handling and reject unsupported transfer functions.
- Never overwrite the output or an existing review directory. Keep sources untouched, use no new dependencies, support `--plain`, show elapsed activity throughout expensive work, and keep raw FFmpeg errors behind `--details`.

## Protected initial state

Initial `git status --short`: dirty feedback.log, postmortem references/browser-integrations.md, execution-environments.md, state-security.md, sources.json, and dot_codex/AGENTS.md; untracked `:memory:.ses` and two October 23 postmortems. Preserve all. Only append this task's reviewed lookup report record to the dirty sources.json. No commit or push requested.

## Ordered implementation and verification

- [x] Inspect implementation, callers/tests, README, smoke checks, lessons and feedback; sample first frames of all 30 real clips without modifying originals.
- [ ] Add real-FFmpeg tests before implementation: three mixed-shape clips, rotation metadata plus 180-degree manual correction, mtime ordering, output non-overwrite, start previews reflecting joined content and portrait side bars.
- [ ] Delegate tests to the tests agent; observe expected RED for missing flags.
- [ ] Implement the smallest compatible landscape-and-review path in the existing CLI.
- [ ] Run focused tests GREEN, inspect actual report/previews, decode a short real-source sample, and obtain independent review.
- [ ] Update README and smoke checks; run relevant regression checks and refresh-config with protected local changes preserved.
- [ ] Record exact evidence, limitations, rollback and final review here.

## Risks, rollback and manual checks

Reencoding is slow, lossy, converts HLG to SDR, and requires disk space for temporary normalized files plus final output. Sampling just the first frame misses later orientation changes and may show black/blurred footage. Manual corrections are explicit; no automatic upright detector is implied. Partial output/report may remain on error; sources are never removed. Rollback is reverting only this task's hunks and deleting only newly generated outputs when no longer needed.

Automated command: `python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py -v`. Check rotation fixtures with ffprobe before pixel assertions. Manual workflow: run `--landscape --sort mtime` on a short fixture, inspect ffprobe geometry and all report images in a browser. Run short samples of the real originals under `/tmp`; do not render the entire concert during development.

## Progress and review notes

- Real folder inventory: 30 HEVC 3840x2160 clips, no rotation side data; 8 uppercase MOV and 22 lowercase mp4. `/tmp/olivia-orientation-58ivf00x/contact-sheet.jpg` contains their first frames. Visible scenes look upright; two initial frames are blurred/obscured, so semantic orientation is inconclusive there.
- Minor read-only skill-path lookup error is resolved and registered in `docs/postmortem/2026-10-28-concat-skill-reference-path.md`; targeted memory check exited 0.
- Execution choice: implement inline in the existing checkout as requested, with tests delegated and one independent final review. No commit or push.

## Resumable full-concert scope (latest user steering)

The user now explicitly requests eliminating mixed HDR/SDR/time-base concat warnings, preserving **capture order** and originals, verifying short transitions in both camera directions before starting the full 30-clip render, and resumability with ongoing progress. This supersedes using modification-time order for the actual render. Keep `--sort mtime` as an available reusable option.

- [x] Initial landscape mode: 14 focused tests pass, including distinct-color 60fps preview timing and non-square SAR regressions. Short real MOV+MP4 sample encodes/decodes and first-frame images are upright.
- [x] Add explicit `--resume` with validated per-clip completion and manifest-bound source identities/settings; retained work, exclusive lock and mismatch refusal pass defining checks. Publication interruption ordering fixes remain under review below.
- [x] Implement common SDR H.264 High/yuv420p,3840x2160,60fps,1/90000 time base and AAC LC48kstereo for these sources; final continuous audio encode and warning-level DTS rejection. All17 focused tests pass before final recovery-window fix.
- [x] Both real one-second direction samples passed: matching normalized video/audio signatures, no DTS warnings, full decode, video duration2.083333s equal normalized sum, audio2.026s within0.1s; before/after cut images and nonzero PCM checked. Evidence `/tmp/olivia-transition-checks-g6lzwh78/verification.json` and `.harness/concat-concert/checks.md`.
- [x] Final scoped refresh succeeded; installed bytes match source. Both transition jobs resumed successfully. Started user service `olivia-rodrigo-concat-20261028212506.service` only after both real directions and all19 focused tests passed; manifest contains30capture-ordered inputs. Persistent progress/handoff records live paths. Fullrender remains in progress.
- [ ] Verify final 30-clip output geometry, duration/audio and start previews; record independent evidence review and remaining visual limitations.

### Latest verification and protected work

Full repo unittest discovery ran 1,382 tests in 267.504s and exited 1: 52 failures, 105 errors, 1 skipped. No focused concat tests failed. Missing private fixtures, sanitized `/home/example` paths, unavailable tmux/display/runtime dependencies affect broad suites; do not claim the whole repo is green. Full log: `/tmp/concat-full-tests.log`; the living broader-regression report records details.

The isolated scoped `refresh-config` succeeded after explicitly sourcing `cli-message`; only the concat helper was a chezmoi apply target. The scope avoids unrelated `.config/mimeapps.list` conflicts and pre-existing dirty Codex/postmortem files. Shell lookup/activation-wrapper failures are preserved in living reports. A native title update transport failed when the objective changed; retain the current title under the unavailable-tool fallback and do not repeatedly retry it.

## Reproducible handoff

Atomic delivery: script + defining/regression tests + README + grouped smoke checks + this plan and task evidence belong together if a commit is later requested. Suggested subject: `feat(media): add resumable landscape concat checks`. No commit/push is currently requested.

Automated plan: focused unittest discovery for `test_concat_timestamped_videos.py`; targeted memory checks for this task's incident reports; `git diff --check`; actual short transition signatures, complete short decodes, before/after image/PCM checks and duration assertions as recorded in `.harness/concat-concert/checks.md`. Full repository discovery was performed once and failed in unrelated environment/fixture suites; do not hide that result or repeat it without a reason.

Manual plan: inspect both short direction cuts, then the final output's generated first-frame review page. Confirm upright scenes, landscape canvas and portrait side bars where applicable. A blurred/black first frame is inconclusive; do not claim later frames or a full listening pass were checked.

Paste-ready Cursor prompt:

```text
Continue the resumable concert concat task from .harness/concat-concert/progress.md and plans/concat-landscape-checks.md. Preserve unrelated dirty files and all originals. Inspect the recorded service/process and cache before starting anything; do not launch a second render. Follow the saved next action, keep capture order, verify every required acceptance criterion with current evidence, update checks.md/progress.md, and do not claim completion while the full render or its start-frame review remains pending. No commit/push is authorized.
```

## Full render in progress

The final source has19passing focused tests, including both exact recovery publication windows. The narrow independent review found no remaining launch blocker. Source/installed bytes match. Both direction samples have compatible streams, noDTSwarnings, complete decodes and inspected upright frames/audio at the cuts. A user systemd service is now normalizing all30clips to a new output outside the input directory; it survives closing this terminal. Unit, mainPID, log, cache and resume command are recorded in `.harness/concat-concert/progress.md`. Do not claim final output acceptance until the job exits and its duration/audio/geometry/first-frame review checks are complete. No commit/push.

## Delivery review, 2026-10-30

Explicit commit-plan-push supersedes prior no-commit notes. Fresh focused tests: 19 passed. README gate passed and refresh-config exited 0. Full render remains stopped at user request; earlier running-state observations are historical. Final output acceptance remains incomplete; do not restart. Harness evidence is excluded after automatic approval review rejected publication of local service/media metadata.
