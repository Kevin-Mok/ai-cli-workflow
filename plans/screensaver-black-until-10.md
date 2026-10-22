# Screens off until the 10 AM screensaver

Add `sofss` using the existing daily timer installer, then deploy the fish abbreviation. The command pauses idle playback and powers displays off; the daily service wakes displays and resumes idle monitoring at 10 AM local time.

## Scope and decisions

- Extend `scripts/executable_setup-screensaver-timer` with `--black-until-10`; use the existing daily timer, no new scheduler or dependency.
- Add `sofss` beside `sof` in `aliases/key_aliases.tmpl` with the fish-alias helper.
- Update timer tests, screensaver docs, README and the shared smoke checklist.
- Normal input may wake displays, just as with `sof`. No computer wake from suspend or forced blackout through input. On 2026-10-22 the real morning run exposed that browser-unavailable gating dismisses scheduled playback and normal DPMS can blank it afterward. Revise scheduled playback to manual policy while retaining the lock check; inhibit automatic display blanking only while scheduled playback runs.
- After 10 AM the next daily launch is tomorrow. Do not execute the blackout command as verification.

## Checklist

- [x] Capture initial Git status; preserve all pre-existing dirty files (including README, smoke checklist and orientation plan).
- [x] Add tests; observe unsupported-option RED.
- [x] Implement ordered timer setup, idle/daily playback stop, DPMS enable/off; add wake and idle-start steps to the daily service.
- [x] Preview/apply the abbreviation and update docs.
- [x] Run timer regressions and fish syntax checks; refresh configuration and verify deployed abbreviation/help/timer calendar.

## Verification and risks

Automated: `python3 -B -m unittest discover -s tests -p test_screensaver_timer.py -v`. Check success ordering and failure before blackout. Fish syntax via `fish -n` on generated abbreviations. Inspect real CLI help, systemd calendar and deployed unit text without changing display power.

Manual: type `sofss` and press Enter, confirm displays turn off and idle monitor stops; at next local 10 AM confirm displays wake and screensaver starts when browser/lock checks allow. Real overnight waiting, hardware power state and suspend/resume are separate unverified acceptance checks.

Rollback: remove the abbreviation, reinstall the daily timer without blackout, and start `media-screensaver service`. Preserve all unrelated work. No commit requested.

## Progress and review

RED: two new tests rejected unsupported `--black-until-10` (SystemExit 2), four existing tests passed. GREEN: all six timer tests passed, exit 0. Fish-alias helper preview/apply reported one new mapping in power options with zero conflicts. Refresh writes outside the workspace require the approved escalation route. No device power action will be used as a smoke test.

User added a ten-second test-command request. Added mutually exclusive `--test` mode: DPMS off, ten-second wait, guaranteed wake in finally, then immediate manual preview. It does not write or change timer units. RED: unsupported `--test`, six prior tests passed. GREEN: seven tests pass, including interrupted wait wakes without preview, exit 0. Generated fish syntax passes. CLI help lists all modes.

Refresh initially omitted sofss because the live alias source is ignored/unmanaged by chezmoi. Narrow reconciliation added only the new live mapping, then refresh passed and focused fish output verified the expansion. See [incident](../docs/postmortem/2026-10-21-sofss-shortcut-refresh.md). Updated timer setup succeeded; live `list-timers` reports 2026-10-22 10:00 EDT and the loaded service contains display-on and idle-start steps. No blackout or immediate preview executed. No commit/push requested.

## Handoff

Atomic result: timer option, wake/resume steps, sofss mapping, ten-second manual test and matching docs. Documentation updated in README, docs/media-screensaver.md and docs/smoke-tests.md. Automated command and manual acceptance are listed above; actual overnight/hardware behavior remains unchecked.

Cursor prompt: "Review plans/screensaver-black-until-10.md and the timer installer/test diff. Verify sofss resolves correctly, --test wakes after ten seconds without changing the daily timer, and Ctrl+C wakes displays without preview. Preserve all pre-existing dirty files. Do not run blackout without an explicit desktop test request."

Suggested commit: `feat(screensaver): add screens-off shortcut and wake test`.

## Morning blackout correction — 2026-10-22

- [x] Inspect live timer/service/journal/X11 settings: timer and wake succeeded at 10 AM; preview ended at 10:00:02; bridge absent; blanking/DPMS timeout 600 seconds.
- [x] Add failing explicit-schedule and scoped-inhibition regressions.
- [x] Use manual preview policy for scheduled playback, retain locked-session and idle-daemon safety checks, and hold scoped X11 screen blanking/DPMS inhibition until playback cleanup.
- [x] Run focused and broader screensaver regressions, deploy, inspect live bounded playback with unavailable bridge, and update docs/incident/learning (live duration inconclusive due input).

Risk: explicit scheduled playback can cover a browser whose bridge is unavailable, by design; idle automatic behavior remains conservative. Do not change persistent global DPMS values or bypass lockers. Verify inhibition release on exceptions and connection close. Physical sustained overnight observation remains a separate acceptance check.

Morning correction evidence: two defining RED failures (automatic policy and missing inhibitor lifetime); eight timer tests GREEN and 58 broader screensaver tests GREEN under approved isolated Xvfb. Runtime inhibition test holds off one-second blanking for 2.2 seconds, then verifies blanking resumes after exception release and configuration remains unchanged. Refresh succeeded; installed main.py/desktop.py exactly match source. Live scheduled preview with absent bridge reached three rendered items, but physical input dismissed both duration attempts (0.02s and 1.44s); both exited 0 with unchanged xset output. Do not claim full15-second or overnight live acceptance.

Docs: README, media-screensaver guide and smoke checks now describe explicit schedule versus idle gating and scoped display inhibition. Incident: docs/postmortem/2026-10-22-screensaver-morning-blackout.md. Atomic patch: scheduled policy plus scoped inhibition and regression coverage. Cursor prompt: "Review the morning-blackout correction in plans/screensaver-black-until-10.md; preserve prior dirty work, verify scheduled playback without bridge and lock suppression, then perform an uninterrupted live run past the configured display timeout. Check inhibitor cleanup on dismissal and process exit." Suggested commit: `fix(screensaver): keep scheduled playback visible`. No commit/push requested.

Final overnight edge: primary Xss documentation notes suspension does not deactivate an already blanked server screensaver. Strengthened isolated runtime fixture to begin in ScreenSaverOn state; verify scheduled startup clears that state as well as preventing subsequent blanking. Explicit software screensaver reset must not fabricate physical input; the raw-XInput idle clock remains unchanged.

Final edge verified: pre-blanked runtime fixture RED without explicit reset, GREEN after XForceScreenSaver(ScreenSaverReset). Fresh full58 and timer8 suites passed. Postmortem learning registered and targeted check passed. Final deployment refresh and exact source/live comparison are required after this last source update; real overnight acceptance is still pending.

Final deployment verified: refresh-config exited0 with REFRESH COMPLETE; cmp confirmed installed main.py and desktop.py exactly match tested sources; git diff --check passed. Live timer remains armed for 2026-10-23 10:00 EDT. No commit/push performed.

## Commit-session delivery milestone

Subject: `feat(screensaver): add timed blackout and reliable wake`. Completed: sofss, ten-second test command, explicit scheduled-preview policy, scoped display blanking/DPMS inhibition and existing-blank reset, regression coverage, guide/README/smoke updates and incident learning. Verification: 8 timer and 58 screensaver tests passed in the implementation turn, deployment refresh/source equality and targeted ledger checks passed; repeating focused checks for delivery. Remaining: uninterrupted overnight/hardware observation only; no implementation blockers. Next: review the exact scoped candidate, run privacy gate, commit and push origin/main.

Scope uses direct-write fallback for session `01a160dc-46ad-7f42-80d1-0a81ba446b1b`: helper returned unsafe because it detected no writes in the tool-wrapper transcript. Initial pre-write Git status and observed edits are preserved in this conversation. Include only own hunks in baseline-dirty README, smoke checklist, lessons, operational-drift guidance and sources ledger. All unrelated dirty paths/hunks stay out. README recruiter gate returned pass_no_change.

Commit-session fresh verification: timer8 passed, full screensaver58 passed under isolated Xvfb, and generated fish syntax passed. Candidate contains ten whole session-owned files plus five shared files reconstructed from HEAD with only observed session additions; README, UBS, Discord and other-session ledger hunks are excluded. Milestone is ready for privacy check, commit and upstream push; overnight hardware acceptance remains pending.

Commit privacy check initially blocked a machine-specific home alias in newly added ledger records. Public candidate now uses existing placeholder aliases; live local metadata and all unrelated changes remain uncommitted. Added a delivery incident record; repeat gate before commit with hooks intact.

Delivery privacy repair verified: exact staged candidate passed, exit0, without bypassing hooks. Public ledger aliases use established placeholders and machine-specific/unrelated local records remain dirty. Commit milestone now includes 16 scoped files/hunks and the privacy incident record. All implementation checks remain green; next step is the final gate, single commit and push to origin/main.
