# Public-Tip Restore Needed Parent Directories

This postmortem records a failed restore step after the final narrow history rewrite and the safe correction used to complete the public-tip recovery.

## Symptom

Restoring six backed-up untracked files failed because their parent directories did not exist after the candidate worktree was cleaned for the history rewrite.

## Impact

The affected files were temporarily absent from the candidate worktree. The versioned backup remained intact, and the tracked patch plus all other untracked files restored successfully.

## Evidence

- Copy errors named only missing destination parent directories.
- The backup manifest and source files remained present under the task-specific temporary backup directory.
- The failed paths were limited to the harness, three replacement templates, and one placeholder directory.

## Current status

Resolved. No history or source backup was lost.

## Root cause

The restore loop copied files without first recreating directory structure. The earlier backup used `cp --parents`, but the restore side did not mirror that behavior.

## Resolution

The restore loop now creates each destination parent directory before copying. It then recopied every path from the same immutable backup manifest.

## Verification

Every path in the 38-file untracked backup manifest exists after restoration; the missing-file count is zero.

## Follow-up

- Make future untracked-file restore loops create each destination parent directory before copying.
- Compare the restored untracked path set with the backup manifest before resuming edits.
