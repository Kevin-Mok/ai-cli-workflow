# Post-Commit Check Found Unreachable Staging Blobs

This postmortem records why the first post-commit object-hygiene check found unreachable blobs and how the candidate was pruned before delivery.

## Symptom

After the public-readiness commit, `git fsck --full --unreachable --no-reflogs` listed 13 unreachable blob objects.

## Impact

The candidate did not yet meet the zero-unreachable-object delivery gate. The private-rule all-object audit had already scanned those blobs and reported zero findings, so this was object hygiene rather than a privacy exposure.

## Evidence

- The immediately preceding `--scope all` audit passed across 689 commits and 5,188 blobs with zero findings.
- The unreachable inventory contained blobs only: no commit, tree, or tag object was listed.
- The worktree and index were clean after commit.

## Current status

Resolved in the candidate before transplant.

## Root cause

Repeated `git add` operations wrote intermediate versions of task documentation as loose objects. The final commit references only the last staged versions, leaving earlier public-safe versions unreachable.

## Resolution

Expire candidate reflogs, prune unreachable objects immediately, and repeat the all-object audit plus fsck check before transplant.

## Verification

- After reflog expiration and immediate garbage collection, `git fsck --full --unreachable --no-reflogs` exited successfully with no output.
- The repeated all-object privacy audit passed across 689 commits and 5,175 blobs with zero findings.

## Follow-up

- Expect intermediate staging blobs during a multi-pass documentation commit and run the final unreachable-object gate after committing.
- Continue using the all-object privacy scope so even transient staging objects are scanned before pruning.
