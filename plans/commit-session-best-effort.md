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

## 2026-11-05 follow-up: always attempt safe delivery

This follow-up supersedes the older unsafe/empty-scope hard-stop decisions above. Retain prior milestones as historical evidence.

# Make commit-session always attempt safe delivery

Update the canonical skill so ordinary invocation completes the safe commit/push path without another scope-confirmation round. Preserve unrelated work, privacy gates, hooks and truthful reporting. This plan follows `.agent/PLANS.md`.

## Context and scope

The existing skill already says best effort, but requires `force` for an empty/local-only fallback and excludes pre-existing prerequisites without a manual split. That let an agent stop a resume-default shipping request when the catalog existed only in the dirty tree. Change only the skill, its admission cost record, durable feedback, an engineering lesson, relevant README/smoke guidance and this plan. Preserve all initial dirty work, especially shared postmortem knowledge, fish functions and machine configuration. No helper or runtime code change is needed.

## Decisions

- Include the minimum reviewed prerequisites automatically, recording dependency evidence. Unrelated pre-existing changes remain excluded.
- If a coherent implementation cannot ship safely, commit independent safe work or a useful factual handoff; never fabricate implementation completion.
- Attempt the clear upstream push, including verified earlier session commits when there is no new commit. Mandatory privacy, hooks and permission failures remain blockers.
- User correction explicitly authorizes this permanent workflow change. No new skill or trigger is introduced.

## Progress

- [x] Capture linux-config dirty baseline; read canonical source, feedback and instruction-edit guidance.
- [x] RED evidence: the preceding actual commit-session invocation stopped for scope confirmation instead of shipping the eligible subset.
- [x] Update skill and durable correction; refresh admission costs.
- [x] Four pressure scenarios pass; 9 session tests, vetted sync (241 entries), trigger routing (46/51) and README gate pass. Admission rerun passes all 7 tests after removing the redundant added paragraph that exceeded 20,000B.
- [x] `fish -c refresh-config` exited 0 with REFRESH COMPLETE; installed parity checked below.
- [ ] Review exact candidate, privacy-check, commit and push focused linux-config work.

## Verification and review

Use read-only agent pressure scenarios for a mixed dirty prerequisite, empty/helper-unsafe fallback, and a privacy-blocked subset. The agent must select coherent reviewed prerequisites or independent deliverables and attempt the clear upstream push without asking routine scope questions. Run existing session-scope and skill-admission tests, vetted-skill sync, trigger routing, README gate, and trim benchmark. Refresh uses the existing managed configuration path; preserve local drift and other sessions' work.

## Risks and recovery

Required prerequisites must have concrete dependency evidence; this is not all-dirty shipping. No privacy or hook bypass is allowed. Restore only this task's edits if rollback is needed; do not reset the worktree. Existing session-scope code retains its conservative classification; the skill supplies the reviewed dependency fallback.

## Outcomes

Pending fresh verification and activation. Atomic plan: clarify delivery scope, verify agent decisions, activate and ship. Cursor prompt: Review this plan and the canonical commit-session SKILL.md, retain unrelated dirty files, verify prerequisite and privacy handling, then check installed parity. Suggested commit: `fix(commit-session): always attempt safe commit and push`.

### Follow-up evidence and delivery status

Four read-only agent pressure scenarios returned the expected safe-subset commit/push decisions without routine scope questions. This verifies instruction decisions, not a live end-to-end repository workflow. No helper/runtime logic changed. Existing scope/contract suite: 9 tests pass. Vetted catalog: 241 entries, zero missing/stale. Trigger gate: 46/51, unchanged. README gate: pass_no_change. Targeted postmortem registration: zero errors. Initial admission-size failure was this task's redundant added prose; removed it while keeping the refreshed existing PASS costs. Fresh reruns: 7 admission tests, 9 session tests and targeted postmortem registration all pass. Trim gate fails inherited canonical-instruction and total-loaded budgets; skill description and loaded delta remain zero, and no budget was relaxed. Refresh completed successfully; shared managed files retain its normal local-drift reconciliation. Prior unrelated fish, machine settings and postmortem edits stay excluded from this commit.

Verified focused milestone prepared for commit: `fix(commit-session): always attempt safe commit and push`; stage only this task's reviewed paths/hunks, run exact-candidate privacy gate, commit, then push origin/main. Preserve every unrelated index/worktree change. Public skill catalog and root README now describe minimum reviewed prerequisites and independent safe delivery.

Scope helper returned unsafe because nested tool writes were not recognized; direct-write evidence in this conversation establishes the reviewed skill/docs/feedback/plan changes. Mixed smoke and learning-ledger files contribute only this task's block/report. No raw session identifier is published.
