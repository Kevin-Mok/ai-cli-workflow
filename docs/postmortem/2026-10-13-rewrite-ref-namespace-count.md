# Rewrite Ref Namespace Count Failure

This report records a failed post-rewrite measurement command and the corrected
way to count commits reachable from a Git ref namespace.

## Symptom

On 2026-10-13, a verification command passed `refs/heads/archive` directly to
`git rev-list`. Git rejected it because the name is a namespace containing
multiple refs, not a concrete ref.

## Impact

The read-only commit-count measurement stopped before printing the remaining
metrics. The completed history rewrite and all rewritten refs were unchanged.

## Evidence

- `git rev-list refs/heads/main refs/heads/archive --count` exited 128.
- Git reported that `refs/heads/archive` was an ambiguous argument.
- The failed command performed no writes.

## Root Cause

The verification command treated a ref prefix as a revision. Git revision
arguments must name concrete refs or receive the enumerated refs separately.

## Resolution

Enumerate concrete refs below `refs/heads/archive/` with `git for-each-ref`, then
pass those refs to `git rev-list` together with `refs/heads/main`.

## Verification

Enumerating concrete heads reports 18 public-safe local heads reaching 688
unique retained historical commits. No namespace name is passed to `rev-list`
as though it were a concrete revision.

## Follow-up

Record the namespace-enumeration pattern in the local task lessons. The
canonical postmortem-memory ledger is outside the user-authorized folder and
must not be changed during this task.
