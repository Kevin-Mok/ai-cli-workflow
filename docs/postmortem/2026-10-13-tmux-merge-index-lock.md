# tmux merge commit index-lock check

Keep the prepared merge and all local edits intact, then validate a saved index copy before committing under the owned real-index guard.

## Symptom, impact and evidence

The scoped merge-commit helper acquired .git/index.lock, then invoked git write-tree against the real index. Git tried to acquire the same lock and returned128 File exists. The helper exited before commit creation and removed only its owned lock in finally. HEAD remains d499d64; the reviewed normal merge remains staged with MERGE_HEAD182713c. No working files or history changed in this failed attempt.

## Status and next steps

Record lookup, then validate the copied original index through GIT_INDEX_FILE rather than invoking a real-index lock-taking operation while holding its guard. Preserve merge parents, hooks and all local overlays. Rebuild the scoped incident/plan/knowledge candidate and verify the corrected helper before retrying the commit.

## Lookup, cause and verified correction

Search index.lock write-tree matched local-git-index-same-filesystem-publish and local-shared-index-commit-race. Their index guarding and scope preservation apply, but neither documented write-tree taking its own lock. Root cause confirmed: the helper invoked a lock-taking operation on an index whose guard it already owned.

Copied the original index to a separate GIT_INDEX_FILE while retaining the real-index guard; write-tree then returned0 and the expected merge tree cea0a806f5fabd492c447f8924103b4467cdf9eb. Verified the real index remained byte-identical and released only the owned lock. Corrected the commit helper to validate this copied index under the guard, keeping the reviewed private commit index and same-filesystem publication. HEAD/merge state remains intact; no history rewrite or bypassed hook. The executable probe verifies this lock correction; merge commit and push remain the next delivery actions.
