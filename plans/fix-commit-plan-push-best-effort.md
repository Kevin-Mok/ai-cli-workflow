# ExecPlan: Make commit-plan-push best effort

## Purpose and observable outcome

Change the repository-tracked `commit-plan-push` skill so an explicit delivery
request always makes a best-effort pass over the dirty worktree: it classifies
all changes, commits every safe and reviewable group, attempts one upstream
push after the series, and reports any residual files or failed steps instead
of stopping on ordinary ambiguity or validation warnings.

## Current context, relevant files, and scope boundaries

- The target skill is `dot_agents/skills/commit-plan-push/SKILL.md`.
- Its picker metadata is `dot_agents/skills/commit-plan-push/agents/openai.yaml`.
- Contract coverage lives in `tests/test_commit_plan_push_skill.py`.
- Public skill documentation is in `dot_agents/skills/README.md`, `README.md`,
  and `docs/smoke-tests.md`.
- The current worktree also contains an updater implementation, a tooling postmortem, and unrelated
  machine-local Vesktop settings and feedback-log edits; those must be classified independently and never guessed into a
  commit.
- No changes to Git history policy, force-push behavior, secrets handling, or
  the separate planning-only and session-only skills are in scope.

## Assumptions and decisions already settled

- “Always do it” means do not ask for clarification merely because changes are
  mixed, a normal check fails, or the README gate reports a fixable warning.
- Safe, reviewable files are committed in coherent oldest-to-newest groups;
  secrets, credentials, caches, generated output, machine-local files, and
  genuinely unreviewable files remain residuals with a warning.
- A missing upstream or rejected non-fast-forward push does not undo safe
  commits; the workflow reports the push failure and never rewrites history.
- The final status is always inspected. If another safe group remains, the
  workflow makes another best-effort commit attempt before reporting residuals.
- The root README remains subject to the recruiter-sync gate, but a gate
  warning is recorded and does not prevent unrelated safe groups from being
  delivered.

## Ordered implementation checklist

- [x] Capture the initial Git status and identify protected dirty state.
- [x] Write and run the contract test RED for best-effort language.
- [x] Update the skill workflow, guardrails, output contract, and picker text.
- [x] Update the catalog, README, smoke test, and this plan to match behavior.
- [x] Run focused contract tests, updater regression tests, shell syntax checks,
  diff validation, and the README gate.
- [ ] Execute the best-effort commit series, push the configured upstream once,
  and inspect the final residual state.

## Risks, edge cases, rollback points, and protected dirty state

- Risk: broad “clean the worktree” wording could encourage staging secrets or
  personal settings. Mitigation: retain explicit prohibited-file guardrails and
  require residual reporting.
- Risk: a failed commit or push could leave a partial series. Mitigation:
  continue only with independent safe groups, record SHAs, and never amend,
  reset, rebase, or force-push.
- Protected until classified: `dot_agents/skills/feedback-memory/feedback.log`,
  `dot_config/vesktop/settings/quickCss.css`,
  `dot_config/vesktop/settings/settings.json`, and the completed
  `docs/postmortem/2026-09-01-smoke-test-patch-tooling.md`.
- Rollback: revert the focused workflow commit; no destructive cleanup is
  authorized for residual files.

## Exact automated and manual verification

- RED: `python3 -B -m unittest tests.test_commit_plan_push_skill -v` must fail
  because the current skill lacks the best-effort contract.
- GREEN: the same command must pass after the skill and docs updates.
- Regression: `bash tests/test_update_vesktop_script.sh`,
  `bash tests/test_update_chrome_script.sh`, and
  `bash -n scripts/executable_update-vesktop.sh tests/test_update_vesktop_script.sh`.
- Repository checks: `git diff --check` and
  `./scripts/executable_readme-recruiter-sync`.
- Delivery: inspect staged diffs before each commit, push the configured
  upstream after the complete verified series, then run `git status --short`.

## Progress, verification evidence, and review notes

- 2026-09-01: Initial status captured before current-session writes. The
  existing Vesktop updater/test/docs changes are safe candidates; the settings,
  feedback, and incomplete postmortem require separate classification.
- 2026-09-01: Contract test was added and intentionally observed RED because
  `commit-plan-push/SKILL.md` did not contain `best-effort`.
- 2026-09-01: GREEN evidence: `python3 -B -m unittest tests.test_commit_plan_push_skill -v`
  passed all four tests; `bash tests/test_update_vesktop_script.sh`,
  `bash tests/test_update_chrome_script.sh`, and `bash -n scripts/executable_update-vesktop.sh tests/test_update_vesktop_script.sh`
  passed; `git diff --check` and `./scripts/executable_readme-recruiter-sync`
  returned success (`pass_no_change`).
- Review note: this plan intentionally changes the delivery policy from
  clarification-first to best-effort while preserving hard safety and history
  guardrails.
