# Pre-push history privacy gate

Add a local pre-push gate that audits exactly the commits Git proposes to push,
blocks findings without exposing values, and installs with the existing gate.

## Scope and decisions

- Start from origin/main (502ac1f), in `.worktrees/pre-push-history`, branch
  `feat/pre-push-history`. Initial root and worktree status were clean.
- Extend `scripts/privacy_gate.py` and `scripts/executable_audit-public-history`;
  use the existing launcher, snapshot bundle and private identity policy.
- Existing refs scan remote-OID..local-OID; new refs scan all history reachable
  from local-OID; deleted refs require no scan. Multiple updates are all checked.
- Preserve both existing hooks, including pre-push argv/stdin, exit codes and
  permissions. Upgrade an existing pre-commit-only installation idempotently.
- Never print raw auditor errors, policy categories, refs, filenames or values.
- No chezmoi/refresh, secret edits, Codex model/effort changes, history rewrites,
  main push, or force push. No dependencies.

## Implementation checklist

- [x] Inspect gate, scanner, fixtures, identity policy, docs and protected state.
- [x] Write RED fixtures for findings, clean ranges, new/deleted refs, identity
  approvals, hook preservation, installer upgrades and failure safety.
- [x] Add revision selection and shared identity rules to the auditor; add stdin
  pre-push command and reversible two-hook installation.
- [x] Update README and grouped smoke checks; run focused and existing gate tests.
- [ ] Review diff, verify disposable actual pushes and installation, and commit
  code/docs/this plan together as `feat(privacy): audit history before pushes`.
- [ ] Push only the feature branch and open a PR targeting main.

## Risks and rollback

New-branch scans can expose legacy findings and take time; retain ten-second
progress and fail closed on incomplete history or invalid input. Approved
identities exempt only exact metadata pairs, never messages, blobs or explicit
private prohibitions. Binary/LFS coverage retains the auditor's documented
limits. Uninstall restores prior hooks. Existing hooks retain their own output.
Roll back by uninstalling the gate; no history or user content is rewritten.

## Verification and review evidence

- Automated: `python3 -m unittest discover -s tests -p test_pre_push_privacy_gate.py`
  and existing `test_pre_commit_privacy_gate.py`, `test_audit_public_history.py`,
  `test_checkpoint_privacy_gate.py` suites.
- Manual/runtime: disposable bare remote: blocked fake historical finding, clean
  push and deletion; install twice and status; audit an explicit empty range.
- Setup: sandbox fetch failed because Git metadata is read-only; approved fetch
  and worktree creation succeeded. See dated setup postmortem.
- RED: initial focused suite exited 1 with eight expected failures (11 cases);
  baseline pre-commit suite passed 45/45. Review regressions then observed two
  expected failures in 17 cases before installer fixes.
- GREEN: focused pre-push 17/17, pre-commit 45/45, auditor 14/14, checkpoint 1/1;
  all commands above exited 0. Python compilation and `git diff --check` passed.
  README recruiter gate via Bash returned `pass_no_change`.
- Independent review found hook publication could leave the prior hook inactive
  after an error, and reinstall did not restore executable mode. Both were fixed
  with RED/GREEN tests: prepare replacements, copy originals with permissions,
  atomic replacement, and restore execute mode for owned hooks. Exact preserved
  exit status, shallow repositories, missing remote objects, supplied tips and
  scoped path rules are covered. No deferred review findings.
- Baseline diagnostic at origin/main: new-branch full ancestry blocks 692
  pre-existing findings (677 unapproved commit emails, 11 credential blobs,
  4 provider-token blobs). The exact configured identity approval is reused;
  legacy identities and blobs are not silently approved. Local hook activation
  remains a separate install step; disposable fixtures verify both hooks.
- Postmortem ledger records an explicit no-new-learning decision. Targeted check
  exited 0 against a byte-identical public-safe temporary copy, avoiding real
  machine paths in the public ledger.
- Delivery milestone: `feat(privacy): audit history before pushes` includes source,
  tests, README, smoke checks, this plan and required incident bookkeeping.
  Verified implementation complete; feature-branch publication/PR pending.

## Cursor handoff

Review the pre-push implementation against this plan and the documented smoke
checks. Preserve existing hooks and private policy; reproduce all negative cases
only in disposable repositories. Do not apply chezmoi or rewrite Git history.
