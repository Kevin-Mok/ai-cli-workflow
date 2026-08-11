# ExecPlan: Make `commit-session` Best-Effort After Safe Scoping

## Purpose and observable outcome

Once `commit-session` has a safe, non-empty session-scoped file set, it must
attempt relevant validation and the README recruiter gate, repair any truthful
README issue the gate reports, then stage and create the scoped commit even if
non-safety validation remains unsuccessful. It must continue to stop before
staging when session ownership cannot be established or the scoped set is
empty.

## Context, scope, and decisions

- `dot_agents/skills/commit-session/SKILL.md` defines the workflow to change.
- `dot_agents/skills/commit-session/tests/` currently validates the Python
  scope helper; this change adds a small documentation-contract regression
  test rather than changing scope-helper behavior.
- `README.md` and `dot_agents/skills/README.md` describe the public skill
  inventory and must accurately state the new best-effort behavior.
- `docs/smoke-tests.md` and a linked postmortem record the changed reusable
  workflow verification and incident repair in the same commit.
- The initial protected worktree state includes unrelated edits to
  `docs/smoke-tests.md`, `dot_codex/config.toml`,
  `dot_config/fish/functions/fn-progress.fish`, `tests/test_fn_progress.sh`,
  `docs/postmortem/2026-08-11-fn-progress-days-and-rounding.md`,
  `plans/fn-progress-days-and-rounding.md`, and
  `scripts/executable_install-tmux-tpm.sh`; do not stage or alter them.
- A safe non-empty `commitable` set remains mandatory. Missing thread ID,
  unsafe/empty scope, mixed/suspicious scoped diffs, unstageable README repair,
  and unclear upstream remain hard stops.
- If `readme-recruiter-sync` fails, repair only truthful, repo-supported
  README issues and include the repair in the scoped commit; do not invent
  claims. If the repair cannot safely enter the scoped set, stop.
- Focused and broader validation failures after their results are recorded are
  warnings, not reasons to skip a safe commit.

## Checklist

- [x] Capture current status and inspect existing workflow, tests, plans, and
  durable feedback.
- [x] Confirm the policy boundary with the user: fix README-gate failures,
  then commit; preserve scope and other safety stops.
- [x] Add a failing documentation-contract test for best-effort validation and
  README repair before commit.
- [x] Update `commit-session` workflow and guardrails to distinguish hard
  safety stops from best-effort checks.
- [x] Update public skill catalog descriptions to describe the outcome.
- [x] Add the required smoke check and postmortem for the workflow repair.
- [x] Run the targeted contract and scope-helper regressions, plus a Markdown
  diff check.
- [x] Review the exact diff and worktree state, then record final evidence and
  rollback guidance.

## Risks, rollback, and verification

- Risk: softening checks could accidentally permit unowned files. Mitigation:
  retain all pre-staging scope and suspicious-diff stops verbatim.
- Risk: a README repair may be outside session scope. Mitigation: retain the
  hard stop when it cannot safely be included.
- Rollback: restore the prior hard-stop wording in the skill and remove the
  contract assertions; no runtime implementation state is changed.
- RED: run the new contract test before editing the skill; it must fail because
  current wording declares validation and README gate mandatory.
- GREEN: rerun that test after the edit; it must pass. Also run
  `python3 -m unittest discover -s dot_agents/skills/commit-session/tests -p
  'test_*.py'` and `git diff --check` limited to this plan and changed skill
  documents/tests.

## Progress, verification evidence, and review notes

- Initial inspection found that the workflow currently requires the smallest
  relevant checks and treats the README gate as mandatory before staging.
- RED evidence: the focused contract test exited 1 because the prior skill
  lacked the best-effort contract.
- GREEN evidence: the focused contract test passed, then the full commit-session
  suite passed all 9 tests. The scoped diff check exited 0. Fresh pre-commit
  verification again ran `python3 -m unittest discover -s
  dot_agents/skills/commit-session/tests -p 'test_*.py'` (9 tests, exit 0),
  `git diff --check` (exit 0), and the README gate (`pass_no_change`).
- Review: the final diff affects only commit-session workflow documentation,
  its public catalog entries, its picker prompt, its contract test, smoke and
  incident records, and this plan. Reverting this single commit restores
  hard-stop validation behavior.
- Deployment note: full refresh-config was deferred because it is unavailable in
  this non-interactive shell and its live-to-repo snapshot would overwrite the
  protected pre-existing dot_codex config edit. No live configuration was changed.
