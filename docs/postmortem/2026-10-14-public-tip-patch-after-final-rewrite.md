# Public Tip Patch Failed After Final Rewrite

This postmortem records why the backed-up public-facing worktree changes did not
apply cleanly after the last historical rewrite and how they were recovered.

## Symptom

On 2026-10-14, `git apply` rejected the backed-up patch at `README.md` and the
historical calendar configuration.

## Impact

The public README and template changes were not yet restored. The backup patch
and copies of every untracked file remained intact outside the rewrite clone, so
no user work or sanitized history was lost. Nothing was pushed.

## Evidence

- The patch file was 16,810 bytes and had been validated before the rewrite.
- The final rewrite intentionally changed private host/account literals in the
  checked-out tip, so the patch's original context no longer matched.
- The failed `git apply` reported both rejected paths and exited nonzero.

## Root Cause

The final history rewrite changed an account identifier in both the checked-out
README and the calendar configuration. Those changes made two patch contexts
stale even though the desired public-tip edits themselves remained valid.

## Resolution

The unaffected tracked hunks were applied selectively. The one rejected README
section was restored with its intended public-vault wording against the new
sanitized context, the legacy calendar file was deleted explicitly, and every
untracked template/placeholder was copied from the verified backup.

## Verification

The restored `git status --short` output exactly matched the manifest captured
before the rewrite. The backup remains available until the final repository is
committed and rescanned.

## Current Status

Resolved with no lost public-tip changes.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
