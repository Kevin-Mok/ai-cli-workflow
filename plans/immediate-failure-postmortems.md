# Immediate Failure Postmortems

## Purpose And Observable Outcome

Require the canonical agent policy to create a living postmortem for every
unexpected task failure as soon as it occurs, then update that same document
when the failure is resolved and verified.

## Current Context And Scope

- Canonical policy: `dot_codex/AGENTS.md`; root `AGENTS.md` remains a routing
  shim and is out of scope.
- Contract coverage: `tests/test_ai_workflow_contract.py`.
- Public workflow documentation: `README.md` and `docs/smoke-tests.md`.
- Protected pre-session work: `prompts/ignore-codex-model-changes-git-status.md`
  is modified and `tests/test_codex_model_skip_worktree.py` is untracked.

## Assumptions

- An unexpected task failure is an unplanned failed command, test, deployment,
  or workflow outcome. Intentional TDD RED tests and deliberately exercised
  failure paths do not create postmortems.
- This policy edit did not itself need a postmortem; the later refresh-config
  incident is captured separately under `docs/postmortem/`.
- The policy belongs in the canonical instruction document and is not duplicated
  in the durable-feedback log.

## Implementation Checklist

- [x] Capture protected pre-session Git state and inspect the canonical policy,
  existing postmortems, contract test, README, and smoke checklist.
- [x] Add a focused contract assertion, run it, and record the expected RED
  failure.
- [x] Add the minimal living-postmortem policy to `dot_codex/AGENTS.md`.
- [x] Align the public README and reusable Repo Instructions smoke check.
- [x] Run the repaired `refresh-config`, complete the final diff review, and
  record the separate refresh incident postmortem.

## Risks, Edge Cases, And Rollback

- Avoid treating planned failure assertions as incidents; the exclusion must be
  explicit.
- `refresh-config` snapshots live Codex configuration into the tracked source.
  Run its dry-run and byte comparison first; stop if they reveal unrelated
  configuration divergence.
- Rollback is limited to reverting the scoped policy, documentation, test, and
  plan changes. Protected pre-session files remain untouched.

## Verification Evidence

- RED command: `python3 tests/test_ai_workflow_contract.py`
  - Expected: the new living-postmortem assertion fails because the policy is
    absent.
  - Observed: the added assertion failed because `unexpected task failure` was absent.
  - Exit status: 1.
- GREEN command: `python3 tests/test_ai_workflow_contract.py`
  - Expected: all contract tests pass.
  - Observed: 12 tests passed.
  - Exit status: 0.
- Documentation and configuration checks: `./scripts/executable_readme-recruiter-sync`,
  `snapshot-codex-config --dry-run`, `cmp -s ~/.codex/config.toml dot_codex/config.toml`,
  and `git diff --check`.
  - Expected: README gate passes, config ownership is safe before refresh, and
    the scoped diff has no whitespace errors.
  - Observed: the README gate returned `pass_no_change`; snapshot dry-run and
    repaired live refresh completed; final `git diff --check` passed.
  - Exit status: README gate 0; snapshot dry-run 0; refresh 0; diff check 0.

- Full-suite verification used `python3 -m pytest -q`: 342 tests and 49 subtests passed, while one unrelated sanitized-vault fixture remains stale for the tracked July 22 note.

## Review Notes

- The final postmortem update for a future failure must share the commit with
  its related fix. This policy-only work will not be committed or pushed unless
  explicitly requested.
- The user approved the live refresh; its documented, targeted capture
  behavior completed and the related postmortem is resolved.
