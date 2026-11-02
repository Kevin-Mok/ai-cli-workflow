# Workspace block spacing

Set every i3 workspace button to 15px left, 10px number/icon gap and 30px right on the current desktop. Preserve existing font changes and bindings.

## Context and decisions
- Native i3bar adds 6px per side at the current Xft.dpi=135. Use Pango spacers of 9px left and 24px right, plus a 10px internal spacer. These are physical pixels at the current DPI.
- Numeric prefixes plus strip_workspace_numbers keep workspace ordering and shortcuts. Remove minimum widths to avoid extra centering.
- Update status-width measurement and existing smoke checks; preserve every unrelated dirty file (including README, smoke tests, i3 font and memory ledger).

## Checklist
- [x] Capture initial status, inspect source/live config and existing feedback.
- [x] Observe defining RED checks for padded labels and status measurement.
- [x] Update labels, bar settings, status measurement and smoke documentation.
- [x] Run checks, refresh-config, validate deployed config, reload and verify live identities. Two reloads were needed because unchanged status commands retained old code. No move/focus commands were issued.

## Verification and risks
Run python3 scripts/smoke_workspace_icons.py, python3 -m unittest discover -s tests -p test_i3blocks_4k_status.py, i3 -C -c ~/.config/i3/config, and the live smoke checker. Pango measurements verify spacer advances. A future DPI change requires recalibrating outer spacers. Rollback: restore only this task’s label/bar and measurement edits, refresh and rename by workspace number.

## Progress and review
Implementation complete and verified. Commit-session requested after verification; prepare one focused commit and push origin/main. Live IPC needs approved host access; sandbox cannot connect to the desktop socket. See the task postmortem.

RED: label checker rejected all 15 old compact labels; new measurement test rejected missing strip_numbers argument. GREEN: all 18 status tests and label checker passed. Pango measured 9/10/24px added spacing across all three font sizes (native side inset is 6px). Live screenshot /tmp/workspace-spacing-after.png confirmed appearance. Status processes survived initial reload, so exec prefix on status commands triggers an orderly restart to load updated measurement. One order-sensitive focus comparison failed after rename; it did not establish focus change (workspace 6 remains focused).

Cursor prompt: Review the workspace spacing diff against this plan; preserve unrelated dirty edits and confirm all three bars use 15/10/30px at 135 DPI.
Suggested commit: fix(i3): set explicit workspace button spacing.

Final evidence: fresh 18/18 status tests, source and live smoke checks pass. refresh-config exited 0. i3 -C exited 0 with pre-existing wheel command deprecations. All three IPC bar configs return workspace_min_width=0 and strip_workspace_numbers=true; status processes restarted at 18:55:51. git diff --check reports a pre-existing EOF blank line in api-contracts-fixtures.md:726; left unrelated work intact. Source and live scoped changes persist, though chezmoi intentionally ignores i3 targets; future deployment must preserve that migration boundary. Final manual check: visually inspect existing single/double-digit buttons without switching workspaces. Commit/push pending for the milestone below.

## Delivery milestone: fix(i3): set explicit workspace button spacing
- Completed: labels, bar settings, adaptive status measurement, tests, README and smoke instructions; postmortem evidence and reviewed hash included.
- Verified: 18 focused tests, source/live smoke checks, all three bar IPC settings, Pango measurements, deployed i3 validation and refresh-config. README gate pass_no_change.
- Scope: session 01a189db-9604-7411-9fa8-6bdaeabb634b. Helper returned unsafe because it detected no writes; use directly observed writes from this conversation. Mixed README, smoke and ledger candidates contain only this session’s changes.
- Remaining: commit the reviewed candidate and push configured origin/main. No implementation blockers; unrelated dirty work remains excluded. Existing wheel deprecations and a pre-existing whitespace warning remain outside scope.
