# Status Comparison Collapsed Untracked Directories

This postmortem records why a read-only source-versus-candidate status comparison tried to read an untracked directory as a file and the corrected inventory mode.

## Symptom

The comparison script raised `IsADirectoryError` on an untracked task directory returned by porcelain status.

## Impact

The command did not finish classifying the source checkout. It was read-only and changed no worktree, ref, remote, or object.

## Evidence

- Porcelain status returned the directory name as one untracked record.
- The script assumed every record represented a concrete file and called `read_bytes`.

## Current status

Resolved before transplant.

## Root cause

The status command used its default directory-collapsing behavior instead of the file-complete form required by a byte comparison.

## Resolution

Request every untracked file explicitly and reject any non-file record before comparing source bytes to the candidate tip.

## Verification

The corrected comparison classified all 35 records: four protected media paths and 31 task-owned files. Every task-owned path existed in the candidate; 11 matched exactly, 20 had newer candidate content, and none were missing or non-files. The transplant separately backed up all 35 source paths before replacing the checkout.

## Follow-up

- Use file-complete porcelain status whenever downstream logic reads paths as files.
