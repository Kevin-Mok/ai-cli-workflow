# Review and deliver dirty worktree

Review all dirty changes, ship safe coherent groups, and push main to origin/main
once after the series. Preserve excluded machine-local artifacts and report
validation limitations.

## Context, scope and decisions

Initial main tracks origin/main; no staged changes. All initial dirty paths are
in scope for review. Exclude :memory:.ses (session marker) and any privacy-gate
findings. No history rewriting, live desktop moves, or i3 reloads. Existing
implementation plans retain historical evidence; this plan records delivery.

## Ordered checklist

- [x] Capture status, branch/upstream, relevant policy and dirty-file inventory.
- [x] Review independent docs/history and Kitty implementation with bounded agents.
- [x] Run README gate (pass_no_change) and focused regression checks.
- [ ] Commit substantive historical postmortem/memory maintenance first; exclude path-only private overlays.
- [ ] Commit Kitty helper, configuration, tests, documentation and matching plans.
- [ ] Reconcile safe residuals, attempt one push, and report exact outcomes.

## Verification and risks

18 focused Python tests and desktop-layout shell check pass. Isolated graphical
smoke failed during Xvfb startup; inspect details before retry. Privacy gate is
mandatory immediately before every commit. Inspect staged diffs and file sizes.
Refresh may retain the documented pre-existing local/source conflicts; never
force overwrite. Kitty internal APIs require version-specific runtime review;
physical font calibration remains manual. Rollback by a new revert, never reset.

## Review and delivery milestones

Pending commits; no push yet. Privacy blocked home-path restorations; use sanitized public index candidates while preserving local overlays. Host isolated smoke passed; host refresh stopped on existing conflicts. README feature entry matches actual helper modes.
Machine-local session marker will remain untracked. Environment incidents are
recorded in docs/postmortem/2026-10-22-commit-push-environment.md with reviewed
memory registration.

### Milestone 1: reviewed memory maintenance

Prepared `docs(memory): reconcile reviewed incident evidence` with Discord
residual-report evidence, exact verification timestamp, four reviewed external
no-new-learning sources, delivery environment report and this plan. Public
contract validation passes; full memory suite25/26 due unavailable sanitized
default roots. Focused Kitty18 tests and shell check pass, host isolated smoke
passes, README gate passes. Explicit privacy gate required after final staging.
Concurrent memory edits after the initial inventory remain protected residuals.
Next: Kitty commit with its implementation, docs, plans and reviewed learning.
