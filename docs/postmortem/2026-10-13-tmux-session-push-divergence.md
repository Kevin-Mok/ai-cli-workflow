# tmux session push divergence

Preserve the successful session commits, inspect the newer remote history, and integrate it without rewriting history or losing unrelated local edits before retrying delivery.

## Symptom and impact

The first origin/main push returned exit 1 with `main -> main (fetch first)` because remote main advanced. Local commits 8d2d0da and d499d64 remain intact. Cached origin/main was 5d5cd02; ls-remote reported 182713c66b3358154df5f9469de4020e5a29d53d. No automatic approval rejection occurred. A follow-up ancestry probe used that unfetched object and returned128 with `Not a valid commit name`; its false result is invalid, not proof of divergence.

## Lookup and applicability

Reviewed the tracked postmortem-memory skill and searched push/fetch/concurrent merge terms, then non-fast-forward. The applicable safety finding is local-ignored-merge-collision-preflight: protect dirty, untracked and ignored paths before merging. Its worktree-specific implementation is not needed or authorized here. The observed remote rejection requires fetching the object before valid ancestry/diff checks. No verified general remedy for this particular shared-index delivery flow was found.

## Status and next steps

Remote history inspected and normal merge prepared successfully, with protected local overlays verified. Configuration refresh and fourteen focused tmux tests passed; next steps are the reviewed merge commit, normal push retry and remote reachability check. Keep matching reviewed evidence in that commit. Never force-push, reset, rebase, amend or discard other-session work.

## Root cause, resolution and verification

Confirmed a concurrent remote update, not a tmux or credential defect. Fetch returned0 and installed the advertised remote object. The valid graph is two local session commits against two remote harness commits; merge-base checks for8d2d0da/d499d64 against fetched182713c each return1 without object errors. Treat128 as a failed prerequisite, never a negative ancestry answer.

Inspected all four remote paths. git merge-tree returned0 with clean tree cea0a806f5fabd492c447f8924103b4467cdf9eb. The two remote new paths were absent and not ignored. Prepared three-way overlays of the two dirty instruction files, then verified an inverse merge reconstructs their exact original bytes. Captured37 dirty-file hashes and backed up the original two files and real index under /tmp/tmux-remote-integration-syav0n78. Cleaned only the backed-up instruction bases, ran normal git merge --no-ff --no-commit --no-overwrite-ignore origin/main, then immediately restored verified combined overlays. Merge returned0; staged write-tree equals the reviewed tree; MERGE_HEAD equals182713c; all other dirty files retain exact hashes. No unrelated hunk is staged, no worktree created and no history rewritten.

Integration is prepared and ready for the scoped merge commit plus matching report/plan/learning, configuration refresh and normal push retry. Final commit and remote verification results are reported in the task handoff. Recovery learning is limited to fetching before ancestry probes and preserving reviewed local overlays during disjoint remote integration. The report does not claim the retry succeeded before it runs.
