# Fish session delivery shared-index race

Concurrent sessions staged and committed into the same Git index. Inspect the resulting commit, preserve history and finish only the remaining directly evidenced session changes.

## Symptom and impact

At delivery entry the index was empty. A partial cached patch failed at docs/smoke-tests.md:925 after another session staged ctp smoke text. Inspection immediately afterward found commit 5451db5 (feat(aliases): add Codex time projects shortcut), including this session's already staged README, tcs, helper/skill, tests, plan and initial incident. No history was rewritten. Intended atomic separation could no longer be achieved without rewriting another session's commit.

## Lookup and evidence

Query: concurrent shared git index staging. Reviewed paths-ownership local-skip-worktree-and-scoped-state: status alone is insufficient, direct evidence and exact staged content control scope. Applicable to inspection and scoped remaining changes; it does not prevent concurrent index writers. git show --stat confirms 12 files in the concurrent commit. Remaining work is tcs smoke documentation and fish-home-path incident ledger coverage.

## Resolution and limitations

Preserve 5451db5. Commit remaining session documentation, ledger coverage and this incident with the updated active plan. Review exact staged contents before committing; exclude any new unrelated staged changes. Push the complete existing branch once after verified follow-up. Underlying shared-index concurrency remains a workflow limitation; no rollback or force-push authorized.
