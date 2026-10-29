# Redshift i3block implementation plan

Add a saved-manual-temperature block to DP-2 by extending the shared controller, testing protocol and layout behavior, then refreshing and checking activation.

## Scope and decisions
Spec: `prompts/redshift-i3block.md`. Reuse controller display scope, flock and atomic state replacement. Status returns a machine-readable integer and never creates files or calls a backend. The block invokes the installed controller; wheel events use adjust, other events status. Errors output a compact warning, never a target. All fixed blocks count in every layout fallback; volume and Redshift outrank song/calendar.
No new scheduler, GUI or dependencies. Default 6500 K; clamp 1000–6500 K; step 250 K; interval 1 second.

## Checklist
- [x] Capture initial dirty state and read prompt/controller/config.
- [x] Add defining controller/block/layout/scheduler tests and observe RED.
- [x] Implement status and block; fix layout width accounting.
- [x] Run focused and broader checks; update README and smoke documentation.
- [x] Inspect newer live targets, run refresh-config, validate live session where available.
- [x] Record review and handoff evidence.

## Protected work and risks
Initial dirty files include README, smoke tests, feedback, postmortem knowledge, canonical instructions, concat scripts/tests, privacy approvals and unrelated untracked reports/plans. Preserve every unrelated hunk; the follow-up commit-session request authorizes only directly evidenced session changes. Backend failure must leave saved state unchanged. Status relies on atomic replacement rather than creating a lock. Live testing may be blocked by display/sandbox access; never claim activation from source checks. Rollback: remove Redshift config stanza/block and revert only session changes.

## Verification
Run `python3 -m unittest discover -s tests -p 'test_redshift*.py' -v`, matching 4K unit/scheduler tests, desktop-layout shell check and existing Redshift key smoke tool. Cover missing/malformed state, no writes/backend calls for status, both wheels and ignored clicks, clamps, concurrent scroll events and presets/reset. Check fitted output width and preservation under pressure. After refresh, inspect installed files and running DP-2 status process, exercise wheel and Windows+2 together if available, restore original target.

## Revised event-delivery decision
Live testing proved i3blocks 1.4 discards rapid events during a running block. Intercept only Redshift wheel events in the existing 4K wrapper before scheduler dispatch, serially invoke the block/controller and retain its output for the next frame (including errors); forward other clicks unchanged. Use a thread-safe result queue and one-second polls, no new daemon. Add scheduler-level regression first.

## Evidence and review
RED: new Redshift suite failed2status assertions plus3missing-block cases. Crowded layout RED exceeded budgets by90px. Rapid-delivery RED observed0of8 in the defining wrapper fixture, and the actual first live run preserved only2of8 wheel events. Minimum fixes implemented before GREEN.

Final automated checks (this turn):
- `python3 -m unittest discover -s tests -p 'test_redshift*.py' -v`:11passed, exit0.
- `python3 -m unittest discover -s tests -p 'test_i3blocks_4k*.py' -v`:13passed, exit0, including strengthened real-scheduler rapid-input/error-overlay fixture.
- `python3 -m unittest discover -s tests -p 'test_i3blocks_now_playing_mpris.py' -v`:39passed, exit0 (handled intentional cache-write diagnostic).
- `bash tests/test_desktop_display_layout.sh`:exit0.
- `python3 scripts/smoke_redshift_keys.py`:PASS; `--live`:PASS against running i3.
- `git diff --check`:exit0. Targeted postmortem-memory checks both exit0.

Activation: all three refresh-config runs completed; final private log `/tmp/refresh-config.jyalEi0O.log`. Four installed block/controller/config/renderer files match source byte-for-byte. i3 validation exit0 with existing deprecated wheel command warnings. One reload plus two targeted DP-2 restarts (initial activation and subsequent rapid-input fix), no full desktop restart. Screenshot `/tmp/redshift-live-up.png` visibly shows2550 K in DP-2 between volume and song. Running process confirmed DP-2 wrapper and its scheduler. Actual X11 Windows+2=2300, wheel-up=2550, down=2300, eight25-ms ups=4300, left/middle/right unchanged4300, Super+grave=6500; all matched. Probe restored original2850, pointer and focus. No human physical-input testing or live crowded workspace changes; isolated layout tests cover crowding without disrupting workspaces.

Review: status intentionally uses atomic state replacement without creating a reader lock. Click events bypass only the busy-scheduler wheel path, still using the same block/controller and display scope. Backend errors retain state and render ERR, with scheduled polling recovering the display. Other clicks/volume stream forwarded unchanged. Source and tests reviewed against prompt; no new dependencies or scheduling policy. README and smoke checklist updated without discarding unrelated hunks. Both inspection and activation reports recorded with reviewed hashes; new scheduler-delivery lesson added to tracked knowledge. Implementation finished before the follow-up commit-session request; delivery state is recorded below. Rollback remains scoped to the new stanza/block, wrapper changes and status action.

Plan Mode is unavailable in the active tool mode; executing the explicit prompt in this session with this saved plan.

## Follow-up handoff
Cursor prompt: Review `plans/redshift-i3block.md` and `prompts/redshift-i3block.md`, run the recorded tests, and finish only explicitly pending live checks without changing unrelated dirty files.
Suggested commit: `feat(i3blocks): add shared Redshift temperature control`.

## Commit-session delivery milestone

Milestone: `feat(i3blocks): add shared Redshift temperature control`.
Completed: controller, DP-2 block, serial wheel routing, width fallbacks, tests, README/smoke documentation and incident learning. Fresh commit-turn verification:11Redshift tests and13layout/scheduler tests, plus desktop-layout shell check, all exit0; README gate `pass_no_change`. Prior-turn live results above remain the activation evidence; desktop interaction was not repeated during commit delivery.

Scoping session: `01a189ad-a614-7230-ac1e-fc6663962a19`. Scope helper returned `unsafe` because it did not recognize successful nested-tool writes or a baseline; direct-write evidence in this conversation and its initial `git status --short` establish ownership. Commit only those observed changes. Split README, smoke-test and ledger files, retaining unrelated hunks. The pre-existing untracked prompt remains outside scope; this plan records all implementation decisions independently.

At the commit boundary: implementation and focused verification complete; no product blocker. Next: run privacy gate on the exact staged candidate, commit and push `main` to configured `origin/main`, reporting actual results in chat. Unrelated work remains dirty. Rollback: revert this focused commit in a separately authorized workflow.

Excluded work: concat scripts/tests and their README/smoke hunks; feedback/canonical policy edits; privacy approvals; unrelated postmortem records/reference edits; `.harness/concat-concert/`, `:memory:.ses`, concat plans, the pre-existing prompt, and concurrent colorful-i3blocks reports/plans. No timestamps were used as ownership evidence.

Concurrent colorful-icon work began changing shared tests during delivery. The staged version was frozen before those edits; a clean `/tmp/redshift-commit-check` export of exact index bytes passed11Redshift and13layout/scheduler tests (exit0). Those concurrent unstaged edits remain outside this commit.

## Follow-up: 150 K wheel steps

The user requested150 K per scroll after the first commit. This supersedes the original250 K wheel specification; keyboard Ctrl+Alt+Up/Down remains250 K and presets/bounds/default stay unchanged.

- [x] Observe RED for4650 K from4500+wheel-up and4200 K after eight ups from3000.
- [x] Change only block wheel mapping to+150/−150; update README/smoke examples.
- [x] Verify focused tests, refresh and live scroll.
- [x] Prepare scoped numeric/doc hunks for commit; commit/push results are reported by milestone subject in the delivery handoff.

First milestone committed as `18c5797`; push deferred to the completed follow-up series. Concurrent colorful-icon edits in the block/tests/docs are protected and will remain outside our staged follow-up.

Follow-up evidence: defining RED2(4750vs4650,5000vs4200), then current-worktree GREEN12Redshift/13layout tests and keyboard smoke exit0 (the extra palette test belongs to concurrent work). Initial refresh completed. Subsequent broad refresh stopped on unrelated calendar-label drift; preserved source/live. The calendar parser error in the user screenshot was reproduced with the installed scheduler, corrected in shared source by concurrent work, and recovered with a DP-2-only restart. Final visible bar and running wrapper/scheduler verified. Pointer-independent live probe exited0:2300→2450→2300, eight rapid ups→3500; original2300 restored, pointer untouched. See `docs/postmortem/2026-10-29-redshift-150-live-probe.md` for failed probes, root cause and verification limits.

Follow-up milestone: `fix(i3blocks): use 150 K scroll steps`. At commit boundary: requested numeric behavior and docs complete; scoped exact-index checks and privacy gate precede commit; push both retained commits together to `origin/main`. Unrelated icon, calendar-label and media edits remain outside scope. Previous milestone `18c5797` remains intact. Physical human-input and full refresh of unrelated drift are not claimed.

Final follow-up exact-index export:11Redshift tests and13layout/scheduler tests passed, exit0. The current shared-source scheduler overflow reproducer also passed after removal of the unsupported calendar property, exit0. README gate passed; targeted incident-memory check passed. The staged follow-up contains only7session-attributed files/hunks, excluding concurrent palette/config work.
