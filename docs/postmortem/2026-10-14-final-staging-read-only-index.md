# Final Staging Hit The Read-Only Git Index

This postmortem records why the first attempt to stage the verification-only commit failed and the narrow approved route used afterward.

## Symptom

`git add -A` could not create `.git/index.lock` because the source repository's Git metadata is read-only in the default workspace sandbox.

## Impact

No path was staged or modified. The verification worktree remained intact, but the final commit workflow could not continue through the default command route.

## Evidence

- Git reported a read-only filesystem error for the exact index lock path.
- The status printed immediately afterward still showed the same six modified evidence files and four new postmortems, plus this subsequently recorded incident.

## Current status

Resolved for staging. Commit creation uses the same narrow Git-metadata route.

## Root cause

The final staging command was issued through the default sandbox despite earlier evidence that `.git` writes require the approved route in this workspace.

## Resolution

Run only the scoped `git add` and commit operations with approved Git-metadata access, preserving the exact verified worktree.

## Verification

- The elevated `git add -A` completed successfully.
- The staged whitespace check exited successfully with no output.
- Eleven focused tests pass, the README gate reports `pass_no_change`, the 1,726-file worktree scan has zero findings, and the private-rule all-object scan of committed plus staged objects has zero findings.

## Follow-up

- Reuse the known Git-metadata execution route for every source-repository mutation in the same task.
