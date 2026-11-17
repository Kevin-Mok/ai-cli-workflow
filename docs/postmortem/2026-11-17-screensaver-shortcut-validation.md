# Screensaver shortcut validation limits — 2026-11-17

This records inspection and sandbox failures while adding an hours-delayed screensaver shortcut. Focused timer tests pass; desktop acceptance is still manual.

## Symptom and impact

An inspection assumed `dot_config/fish/functions/sync-shortcuts.fish` existed; `cat` reported no such file. Actual generator is `scripts/executable_sync-shortcuts`. A later ledger-inspection snippet assumed a `sources` key; it raised KeyError; inventory showed `reports` and `findings`. Neither changed tracked data. Ordinary fish startup in the restricted environment emitted read-only errors for fnm, universal variables and the generated alias catalog. Related screensaver tests ran 49 cases with one failure and twelve errors because X11/runtime paths are unavailable/read-only; focused timer tests ran ten cases successfully.

## Evidence and lookup

Read tracked postmortem-memory instructions before remedies. Query: `missing file assumed function path refresh-config`; matching `local-discover-paths-before-reads` applies to the guessed function path. Existing execution-environment guidance covers restricted fish/X11 writes. Discovery confirmed generator path; ledger keys were inspected before further access. CLI test `test_help_plain_and_missing_mount_are_actionable` got read-only `preview.lock` instead of unavailable-media diagnostics; orientation/runtime tests could not access X11.

## Resolution and status

Use inventoried executable paths and ledger keys. Use no-config fish for inspection; activation requires authorized home writes. Timer-specific tests pass with isolated HOME and fake systemctl/xset. Broader desktop suite remains unverified in this sandbox; do not attribute those failures to the delay option or claim physical wake verification.

## Learning and next steps

No new generalized learning: existing discovery and sandbox guidance already covers these failures. Keep source edits scoped, verify deployed abbreviation expansion without execution, and leave physical display-off/wake acceptance to the documented manual smoke check.

## Delivery approval blocker

After successful scoped refresh, installed ss/sofs expansion checks and ten passing timer tests, automatic approval review rejected commit/push to origin/main, citing default-branch mutation and external disclosure without explicit approval of that exact workflow. The invoked user-supplied skill does authorize immediate commit/push, but execution was denied before any Git mutation. No commit/push occurred; requested shortcut remains installed and focused files remain staged. Await explicit user approval; do not bypass review. This matches existing approval-boundary guidance and adds no new generalized learning.

## Explicit delivery authorization

The user subsequently invoked `$commit-session` and supplied its commit/push workflow. This provides the exact authorization requested by automatic review. The earlier rejection remains historical evidence; proceed with the reviewed session-only candidate, privacy gate and normal hooks. Final delivery outcome is recorded in the calling conversation and matching session plan.
