# Alpha Intro Push Transport

Record the SSH disconnect encountered while the new-branch privacy hook scans
history, preserve all enabled gates, and verify the final remote branch before
claiming delivery.

## Symptom, impact, and current status

The initial feature-branch push ran the installed pre-push privacy gate, which
scans all reachable history for a new remote branch. At roughly six minutes,
the command printed `Connection to github.com closed by remote host.` while
the local gate continued reporting progress. The local commit remains intact;
the initial remote publication was unconfirmed. No hook was disabled or bypassed.

## Lookup and diagnosis

The postmortem-memory query `SSH keepalive pre-push` returned public-metadata
gate guidance and unrelated SSH transport findings. None established a remedy
for this symptom. Source inspection showed the installed gate checks all
765 reachable commits for a new branch, deduplicating trees but not blobs
across different trees. For an existing remote branch it instead checks
`git rev-list <local-oid> ^<remote-oid>`, including new trees and commit metadata.

The expensive full-history path is confirmed. The precise reason GitHub
closed the idle connection is not established; no SSH timeout fix is claimed.

## Recovery and verification

After the SSH disconnect, stopped only the task-owned push process group;
the interrupted invocation exited 143. Read-only `git ls-remote` confirmed
that remote main was `4366ee0cdc2317bd56b9b9fbd66afe434f26b5f6` and the
requested feature ref did not yet exist.

Initialized only `refs/heads/feat/alpha-digest-intro` at that already-public
base using GitHub's create-ref API through the GitHub CLI wrapper. Then ran
`git push --set-upstream origin feat/alpha-digest-intro` normally. The enabled
hook checked every new feature commit and printed
`Privacy gate PASS: pushed history checked locally.` The push exited 0 and
advanced only the feature branch from `4366ee0` to `16c01c1`.

PR [#4](https://github.com/Kevin-Mok/ai-cli-workflow/pull/4) was created with
base `main` and head `feat/alpha-digest-intro`. The first commit's exact-index
and commit privacy checks also passed with no findings. Main was never pushed.

## Status, learning, and limits

Verified delivery workaround: reusing a verified public base ref bounds the
ordinary hook to new feature commits. Preserve hooks and their complete
outgoing-delta checks; this is not permission to ignore gate findings or to
initialize a branch at unpublished content. No gate implementation or SSH
configuration changed. A more efficient all-history scanner is outside scope.

Register this reviewed report and its workaround in tracked postmortem memory,
record the repo-specific lesson, and include these delivery records with the
matching plan update. Final remote receipts belong in the PR and handoff.

An optional reviewer query through `gh pr view` could not reach the API from
its restricted sandbox, exit 1. The primary agent's authorized GitHub CLI
wrapper query succeeded, exit 0, confirming the open PR and its full body.
This review-environment limitation did not indicate a remote delivery failure.
