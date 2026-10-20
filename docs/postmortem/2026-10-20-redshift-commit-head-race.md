# Concurrent HEAD changed during Redshift commit

Preserve both sessions by restoring the concurrent commit in a follow-up; publish only an exact reviewed tree with an explicit parent and an atomic old-HEAD check.

## Symptom and impact

Redshift candidate was built from cc5f2e3 in a private index. While ordinary commit hooks ran, another session created e1cdb24 on main. Git commit e4c6ca1 used that newer parent with the older candidate tree, reversing six unrelated files and two ledger entries. No push was performed by this session. The working copies remain intact.

## Lookup and root cause

Query `concurrent HEAD isolated index commit` matched local-shared-index-commit-race in references/paths-ownership.md. It applies: a private index guards candidate bytes but does not pin the parent read by ordinary git commit after hooks. Before/after HEAD and git show --stat establish the race.

## Resolution and verification

Restore the six unrelated paths exactly from e1cdb24 and merge both parent ledger records alongside the Redshift record. Use commit-tree with an explicit parent and immutable tree privacy check, run active hooks, then update-ref with the reviewed old HEAD; refusal on an intervening HEAD change must preserve the branch. Never bypass hooks or rewrite history.

Verification: disposable Git fixture confirmed stale update-ref refusal (exit 128) and preserved the newer ref. Corrective tree must retain all six e1cdb24 file object IDs and both report records; inspect the combined diff before one upstream push. Status: resolved through follow-up commit 26d6452; original history preserved.

Learning: no new independent finding; existing shared-index race guidance applies. This recurrence limits the isolated-index remedy: it must also pin the parent and guard ref publication.

## Final delivery evidence

Corrective commit 26d6452 restored all six blobs exactly and retained both prior ledger records. Active pre-commit hook and exact immutable-tree privacy gate passed. Atomic guarded update published the correction; push to origin/main succeeded for e1cdb24..26d6452, and the pre-push history gate passed. Combined diff against e1cdb24 contains only Redshift work and its incident documentation.

A subsequent shared-index cleanup attempt failed because update-index --cacheinfo omitted --add for the new report. It changed no index entry; use target-scoped git restore --staged for the already-committed task paths. This cleanup does not affect the committed or pushed tree. Existing scoped-index guidance applies; no new reusable finding.
