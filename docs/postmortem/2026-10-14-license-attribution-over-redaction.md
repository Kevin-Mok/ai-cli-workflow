# License Attribution Over-Redaction

This postmortem records why the sanitized repository's MIT license checksum did
not match the original even though retaining its public attribution was an
explicit plan decision.

## Symptom

On 2026-10-14, the original LICENSE checksum differed from both the rewritten
historical tip and working tree. The rewritten and worktree checksums matched
each other.

## Impact

The file remained an MIT license, but the rewrite unnecessarily normalized its
copyright attribution. The public-readiness commit was not yet staged or made,
and nothing was pushed.

## Evidence

- The plan explicitly treats the primary author display name and MIT copyright
  holder as intentionally public.
- A late calendar account rule overlapped with that public attribution and was
  applied case-insensitively to blob content.
- Calendar configuration is independently removed from the public tip and
  replaced with a chezmoi template.

## Root Cause

A case-insensitive calendar account rule overlapped with the intentionally
public author name in the MIT copyright line. Applying that rule globally to
blob content changed the sole historical LICENSE blob.

## Resolution

The original LICENSE blob was restored in every retained tree that contains the
file. The overlapping account rule was removed from final verification because
the account configuration is independently sanitized and templated, while the
same name is intentionally retained as public author attribution.

## Verification

- The original license had no generic or remaining private-rule findings.
- The rewritten historical LICENSE checksum now matches the original.
- The rewrite still contains 688 commits on 18 heads with zero unreachable
  objects.
- After the later LFS image removal, the all-object audit passed across 688
  commits and 5,128 unique blobs with
  zero findings after the correction.

## Current Status

Resolved before the public-readiness commit.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
