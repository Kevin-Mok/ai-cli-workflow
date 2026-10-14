# Filter Map Save Failure

This report records a failed attempt to retain the rewrite hash map before
removing temporary filter-branch refs.

## Symptom

On 2026-10-13, the cleanup script invoked `git show --output=<file>` for the
`filter.map` blob. Git printed the blob to standard output and created an empty
file. The script then removed the temporary state ref and pruned unreachable
objects as intended.

## Impact

The temporary old-to-new commit hash map was not retained. The mapping contained
only object IDs, not repository content or secret values. Previously recorded
counts still establish 698 input mappings and 688 unique rewritten commits, but
later preservation checks must compare the verified original bundle and the
rewritten graph without relying on the map.

## Evidence

- Before cleanup, the state blob contained 698 lines.
- Before cleanup, rewritten refs reached 688 unique commits.
- After cleanup, the intended map file had zero lines.
- The 17 historical branch tips were renamed, all 18 original backup refs were
  removed, the state ref was removed, reflogs expired, and garbage collection
  completed.

## Root Cause

`git show --output=<file>` was assumed to redirect blob output. That option does
not provide reliable blob redirection for this invocation.

## Resolution

Use independent graph, metadata, and content comparisons against the verified
original bundle. Future scripts must capture blob output through a tested file
descriptor or `tee`, verify the destination is non-empty, and only then remove
the source ref.

## Verification

The independent comparator mapped all 688 retained commits to original
author/committer dates and approved message transformations, explained the
10-commit empty-prune delta, and found zero topology mismatches. The all-object
audit passed with zero findings and `git fsck` found no unreachable objects.

## Follow-up

Add the verified capture-before-delete pattern to `tasks/lessons.md`. The
canonical postmortem-memory ledger is outside the user-authorized folder and
must not be changed during this task.
