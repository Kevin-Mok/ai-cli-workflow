# Redshift arrow shortcuts

Add free Ctrl+Alt+Up/Down bindings for cooler/warmer 250 K steps and apply them to the desktop.

## Scope and decisions
Use one Python standard-library helper for set, adjust and reset, storing the last successful temperature under XDG_STATE_HOME. Existing number presets and fish redshift-set delegate to it. Default is neutral 6500 K; clamp adjustments to 1000–6500 K. Login setters and the rx alias also delegate to the helper; raw external Redshift commands are outside this state model. No dependencies or automatic schedule.

## Checklist
- [x] Capture initial git status and inspect bindings/helper/docs.
- [x] Observe defining RED, implement shared helper and bindings, observe GREEN.
- [x] Update README, smoke checklist and existing binding checker.
- [x] Attempt refresh-config; apply task-only live changes, validate installed syntax, reload and verify live bindings.

## Risks and rollback
Preserve initial dirty postmortem reference/ledger files and untracked prompts. State writes happen only after Redshift succeeds; lock serializes key repeat. Reset records 6500 K. Rollback task-owned changes and refresh/reload. External setters and a running automatic Redshift daemon can override manual settings.

## Verification
Automated: python3 -B tests/test_redshift_control.py; python3 scripts/smoke_redshift_keys.py; installed and --live variants; i3 -C -c ~/.config/i3/config. Manual: press Ctrl+Alt+Down then Up; select a numbered preset then repeat; exercise lower/upper limits.

## Progress and review
Initial Ctrl+Alt arrow bindings absent. Existing presets reset then set absolute temperatures. Desktop IPC requires approved host route; see docs/postmortem/2026-10-20-redshift-shortcut-inspection.md.

Cursor prompt: Verify plans/i3-redshift-arrows.md against the shared helper and installed i3 bindings; preserve unrelated changes.
Commit suggestion: feat(i3): add 250 K Redshift arrow shortcuts

Evidence: RED assertion missing helper (1 failure); GREEN helper test and binding checker pass. Full refresh stopped on unrelated MIME drift; exact i3 apply then refused because migrationPreservedTargets protects live i3 config. Updated only the live Redshift block and installed helper, preserving the rest. i3 -C exited 0 with existing wheel-command deprecations; reload success:true; --live checker passed. Real helper set/adjust/adjust printed 3000, 3250, 3000 K (exit 0). No automatic daemon was running. Full refresh remains blocked by unrelated MIME drift.

Final review: focused controller, binding, Ubuntu startup and fish syntax checks passed; simulated actual i3 Ctrl+Alt+Up/Down verified 3250/3000 K. git diff --check passed. Subjective screen warmth and fresh-login behavior not visually checked. Scope includes updated Ubuntu startup assertion.

## Delivery milestone

Subject: feat(i3): add 250 K Redshift arrow shortcuts. Completed: bindings, shared controller, preset/reset/login integration, tests, README/smoke docs and incident record. Fresh focused checks all exited 0; README gate pass_no_change. Runtime shortcut round trip verified. Scope helper returned unsafe (no detected repo-writing actions) for session 01a15b40-faf9-7ba0-ab19-cab7196eba74; use observed-write fallback. Stage only task files and this report’s isolated ledger entry; retain all other dirty work. Remaining task work: privacy gate, commit and one push to origin/main. No task blocker; broad refresh remains outside this task due unrelated MIME drift.

Commit preparation: privacy gate rejected one live-home ledger alias; public candidate uses a neutral alias while local lookup retains the real path. Concurrent unrelated staging requires an isolated index. Fresh README gate and focused checks pass. Candidate commit contains all task files plus only its own ledger record; unrelated source hunks remain uncommitted.

### Concurrent commit recovery

Created e4c6ca1, but main advanced to e1cdb24 during hooks; the resulting commit reversed unrelated parent changes. Do not push this intermediate state. Corrective milestone: fix(git): preserve concurrent session changes. Restore only those parent bytes and ledger records, preserve Redshift behavior, retain active hooks/privacy gate, and use explicit-parent commit publication with an old-HEAD guard. The series will be pushed once after combined-tree verification. See docs/postmortem/2026-10-20-redshift-commit-head-race.md.

Recovery verification: disposable stale-parent update-ref returned 128 and preserved the newer branch. The corrective commit runs active hooks, checks its immutable tree with privacy-gate --tree, explicitly records its parent and publishes by compare-and-swap. Verify six restored blobs and the final net session scope before pushing.
