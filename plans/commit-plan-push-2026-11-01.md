# Deliver reviewed dirty worktree

Review existing changes, commit coherent groups with their documentation, and push the complete verified series once to origin/main.

## Scope and decisions

Initial state: main tracks origin/main; no staged files. All initial dirty paths are authorized for review, preserving unsafe or machine-local content. No product implementation is added by this delivery task. Shared README and smoke-test hunks are assigned to their related groups. Existing plan evidence describes earlier runs, not checks performed here.

## Ordered checklist

- [x] Capture initial status, branch, upstream and diffs.
- [x] Run backup, startup, skill contract, admission and README checks.
- [ ] Review privacy and exact candidates; commit backup, skill routing, review policy, startup, desktop configuration and learning updates separately.
- [ ] Run refresh-config for tracked configuration and record actual result.
- [ ] Push once and inspect final worktree and upstream state.

## Verification and risks

This turn: backup49 tests, commit-skill5 tests, admission7 tests and startup shell check passed. README gate: pass_no_change. Privacy check is required immediately before each commit. No actual backup/restore, desktop restart or disposable-repo agent evaluation is claimed. Existing changes can be reverted by a future ordinary revert; history is never rewritten. Machine-local fields and private source material must stay unshipped.

## Milestones and review

Commit subjects and verification will be recorded here before each related commit. Push remains pending.

Milestone 1 prepared: `fix(backup): exclude disposable Snap caches`. Backup source, both policies, regression, README/smoke docs and historical incident/plan travel together. Fresh49 backup tests passed; direct excludes preview passed. refresh-config completed successfully this turn. Other groups and one final push remain pending.
