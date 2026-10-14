# Preservation Verifier Parent-Count Key Failure

This postmortem records why the first readable preservation comparison reported
two unmatched rewritten commits.

## Symptom

On 2026-10-14, the read-only verifier found unique message/date keys but reported
two rewritten keys absent from the normalized original set.

## Impact

Metadata/topology preservation was not yet proven. The verifier made no
repository changes, and no commit or push occurred.

## Evidence

- Both original and rewritten key sets had zero ambiguity.
- Exactly two rewritten keys were missing.
- The matching key included direct parent count even though empty-commit pruning
  can legitimately change a retained commit's direct parent list.

## Root Cause

Direct parent count was not a stable identity field after empty-commit pruning.
After removing it, one timestamp collision and two messages with overlapping
case-insensitive replacement rules required explicit one-to-one resolution.

## Resolution

The verifier now maps unique author/committer timestamp groups, resolves a
timestamp collision by approved message transformations, checks overlapping
literal rules under every applicable ordering, and verifies parent expansion
separately for topology/order.

## Verification

- 688 retained commits matched original author and committer timestamps.
- 686 messages matched the deterministic rule order directly; two matched an
  approved overlapping-rule ordering; zero messages were unexplained.
- Seven messages had only trailing-newline canonicalization.
- All pruned-parent expansions matched, with zero topology mismatches.
- The count delta is exactly 10 empty commits (698 original to 688 retained).

## Current Status

Resolved.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
