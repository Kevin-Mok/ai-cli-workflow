# ExecPlan: Best-effort Git commit skills

## Purpose and observable outcome

Authorized delivery skills attempt every eligible change rather than abandoning
commits for ordinary validation, README, scope-helper, or push problems. Favor
including reviewable in-scope companion files and prioritize session-touched files.

## Context and scope

Update commit-dirty, commit-session, commit-plan-push, the planning-only
commit-plan, README checking guidance, picker prompts, canonical policy, and
public documentation. Preserve secret exclusions and history restrictions.
The session helper remains unchanged; explicit observed writes supply a fallback.

## Assumptions and decisions

Planning-only requests still perform no Git writes. This request updates skill
policy, without asking to ship the repository's existing dirty work. Missing
upstream affects pushing only. Non-safety check failures are reported warnings.
Session touch attribution permits review of a baseline-dirty file, while unrelated
hunks remain excluded. Never remove another session's staged work.

## Checklist

- [x] Capture initial status and read relevant policy, feedback, skills, and docs.
- [x] Identify blocking rules and define scope-preserving fallbacks.
- [x] Update delivery skills, planning guidance, metadata, and README checking.
- [x] Update matching docs, durable preference, and canonical policy.
- [x] Run focused contract checks, diff review, README check, and refresh-config.
- [x] Record final evidence and limitations.

## Risks, protected state, and rollback

Existing README, skills catalog, smoke tests, metaprompt sources, lessons, and
VPS repair files were dirty before this task, including staged files. Preserve
their contents and index state. Apply focused edits only. All other baseline
files are outside this task. Roll back only this task's hunks and new documents.
Best effort never authorizes secrets, unrelated session work, hook bypasses,
force pushes, or pretending unsuccessful checks passed.

## Verification

Run existing commit-plan-push and commit-session contract/helper suites, inspect
changed policy for contradictory stop rules, run scoped `git diff --check` and
`./scripts/executable_readme-recruiter-sync`. Run `refresh-config` after checking
snapshot scope. Record actual outputs; these documentation checks do not prove
future agent behavior in every repository.

## Progress and review notes

Initial sandbox commands failed before execution; escalated reads succeeded.
Known baseline blockers: commit-dirty rejects failed validation and mixed diffs;
commit-session stops on missing thread/helper evidence or README inclusion;
README guidance hard-blocks other safe commits. Existing commit-plan-push already
supports partial delivery but needs explicit touched-file priority.

Independent read-only review confirmed the missing-session, mixed-file, failed-check,
README-conflict, missing-upstream, and staged-index scenarios. Fallback remains
limited to attributable work; the helper implementation and planning-only mode
remain unchanged.

## Final verification evidence

- `python3 -B -m unittest discover -s dot_agents/skills/commit-session/tests -p 'test_*.py' -v`: 9 passed, exit 0.
- `python3 -B -m unittest tests.test_commit_plan_push_skill -v`: 4 passed, exit 0.
- `./scripts/executable_readme-recruiter-sync`: `pass_no_change`, exit 0.
- `./scripts/executable_snapshot-codex-config --dry-run`: passed, exit 0.
- Scoped `git diff --check`: exit 0.
- `fish -c refresh-config`: `REFRESH COMPLETE`, exit 0; log
  `/tmp/refresh-config-20261003-163920-2615020.log`. No config/gitconfig source drift.
- Final scope review: no whole-workflow ordinary stop rules remain in delivery
  skills. README `blocked` describes only a repair residual. Empty eligible scope,
  denied execution, persistent hook failure, and unsafe files can still prevent
  an actual commit and must be reported truthfully.
- These are instruction changes with existing contract/helper regression coverage
  and independent scenario review, not an end-to-end proof of future agents.
- Delivery authorized by `$commit-session`. Scope helper returned `unsafe` with
  no detected writes for session `01a1037a-33aa-7e12-aac5-58ab76c91ba6`; use
  directly observed edits from the conversation. Commit full clean-baseline skill
  files plus only this task's README/catalog/smoke hunks, feedback append, plan,
  and postmortem. Leave metaprompt, SSH, and other-session work uncommitted.
  Target: `main` -> `origin/main`.

Suggested commit: `fix(skills): make Git delivery best effort`.
Review/continuation prompt: Read this plan and the affected commit skills; review
missing-thread, mixed-hunk, failed-check, README-conflict, staged-index, and
missing-upstream scenarios. Preserve unrelated work and include this plan with
any commit of the related policy/docs changes.
