# Public-Tip Patch Stale Gitattributes Context

This report records an atomically rejected public-tip patch whose expected
`.gitattributes` context no longer matched after a later history rewrite.

## Symptom

On 2026-10-14, `apply_patch` could not find the expected LFS lines while applying
a combined public-readiness patch to the isolated rewritten clone.

## Impact

The combined patch was rejected before applying any of its requested changes.
The sanitized history, source repository, and rewritten working tree remained
unchanged.

## Evidence

- The patch tool reported a context mismatch in `.gitattributes`.
- A case-insensitive text rewrite had completed after the earlier file read.
- The patch tool provides atomic failure for this change set; a status check will
  confirm no partial edits.

## Root Cause

The patch bundled several files while relying on `.gitattributes` content read
before the case-fold rewrite. That rewrite updated private-name text in the same
file, invalidating the expected hunk.

## Resolution

Reread each small target, verify the clean working-tree baseline, and apply
focused patches with current context.

## Verification

The rejected patch left the worktree unchanged. Focused patches applied against
fresh context. A later visual review rejected the final JPEG payload because it
contained contact information, so that path was removed from all history and
the now-empty `.gitattributes` file was removed from the public tip.

## Follow-up

After any history-wide content rewrite, refresh file context before constructing
tip-level patches. The external canonical postmortem-memory ledger remains out of
scope and untouched.
