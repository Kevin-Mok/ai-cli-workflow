# Git LFS Status Sandbox Failure

This incident records why the initial repository status check failed and how the audit continued without risking pre-existing work. Git LFS attempted to write its temporary clean-filter state inside the sandboxed `.git` directory; the workaround disables LFS filters for read-only status and reserves approved `.git` access for the authorized history rewrite.

## Symptom

The first `git status --short` invocation failed while Git LFS tried to create a temporary file under `.git/lfs/tmp`. Git reported a read-only-filesystem error, a failed LFS filter process, and a failed clean filter for a tracked LFS image.

## Impact

- The ordinary initial status command did not produce a baseline.
- No tracked file, ref, index entry, remote, or external system changed.
- Three read-only audit agents independently encountered the same baseline condition before switching to object-only inspection.

## Evidence

- The repository's `.git` directory is read-only in the default workspace sandbox.
- The affected image and three audio files are covered by `filter=lfs` attributes.
- Running status with the LFS process, clean, and smudge filters disabled succeeded and showed exactly those four LFS worktree paths as modified.
- Exact sizes and SHA-256 digests were recorded privately, and byte-for-byte copies were saved under `/tmp/ai-cli-dotfiles-public-protected-20261013/` before any history mutation.
- On 2026-10-14, the same failure recurred when a compound artifact-copy
  command ended with an ordinary `git status --short`. The preceding copies and
  executable-mode update completed; only the trailing status probe failed.

## Prior-Knowledge Lookup

- Query: `Git LFS clean filter read-only .git lfs tmp git status`.
- Closest matches: the reviewed sandbox approved-route workaround and protected-local-state guidance.
- Applicability: partial. The evidence supports using a narrowly approved route for required `.git` writes and preserving local bytes, but it does not identify an LFS defect or prove the history-rewrite procedure.
- Decision: use disabled LFS filters for read-only state checks, verify protected bytes independently, and use approved Git mutation only for the explicitly authorized rewrite.

## Current Status

Mitigated for inspection. The LFS-disabled status command succeeded, protected
files were backed up, and object-level audits can proceed without invoking
worktree filters. The recurrence is contained by keeping every source-repository
status probe explicit about disabled LFS filters. History mutation and final
restoration checks remain pending.

## Root Cause

The command runner permits repository working-tree writes but not default-sandbox writes inside `.git`. `git status` invoked the configured LFS clean filter, which attempted to create temporary state under the read-only Git directory.

## Resolution And Verification

Pending completion of the rewrite. Final evidence must show that approved Git mutation succeeded, protected file hashes remained unchanged, normal repository inspection has an explicit LFS-safe path, and no private objects remain.

## Follow-Up

- Keep history audit/rewrite commands independent of LFS worktree filters where possible.
- Record a repository lesson after final verification.
- The canonical postmortem-memory ledger lives in another repository and is intentionally not edited because the user explicitly prohibited touching any other folder. That learning update remains outstanding outside this task's authorized scope.
