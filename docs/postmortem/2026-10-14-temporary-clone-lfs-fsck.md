# Temporary Rewrite Clone LFS Fsck Failure

This postmortem records why an LFS integrity check failed in the isolated
history-rewrite clone.

## Symptom

On 2026-10-14, `git lfs fsck` reported that the one provisionally retained JPEG
object was absent from the temporary clone's local LFS object store. It exited
nonzero and attempted its normal corrupt-object quarantine path.

## Impact

The Git pointer and rewritten history were unchanged, but the temporary clone
cannot prove LFS payload availability. No remote access or push occurred.

## Evidence

- `git lfs ls-files` reports exactly one retained pointer path.
- The rewrite clone was created from Git objects/bundle data; LFS payload bytes
  are stored separately and were never copied into this temporary `.git/lfs`.
- The original repository still contained the protected JPEG payload, previously
  verified byte-for-byte against its safety copy but not yet visually cleared.

## Resolution

The evidence reviewer found embedded contact information in the resolved image.
The path was therefore removed from every retained commit rather than restored.
The candidate's original refs and reflogs were deleted, Git objects were pruned,
and `git lfs prune --force` removed the sole local candidate payload.

## Current Status

Resolved in the candidate: `git lfs ls-files` is empty, the removed path is
absent from the all-ref object inventory, the LFS store retains no payload, and
the all-object privacy audit passes. Final source-repository pruning is still a
delivery gate. The external postmortem-memory ledger remains outside the
user-authorized folder and is intentionally untouched.
