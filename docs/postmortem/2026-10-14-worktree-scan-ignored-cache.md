# Worktree Scan Included Ignored Bytecode

This postmortem records why a pre-commit worktree scan failed after the focused
tests passed.

## Symptom

On 2026-10-14, the direct filesystem walk reported two sensitive-path findings
under the tests' bytecode cache directory.

## Impact

The generated files are ignored and were never staged, but the worktree scan
could not be used as publication evidence. No history, ref, or remote changed.

## Evidence

- The only findings were compiled Python cache files under an ignored directory.
- The Git-object auditor had no such objects because ignored files are not part
  of any commit.
- The manual scanner walked every filesystem file instead of Git's publishable
  tracked/untracked-nonignored file set.
- The first corrected inventory attempt then failed on an intentionally deleted
  tracked account file because `git ls-files -c` lists index entries even when
  the worktree path is absent.

## Resolution

Remove the generated cache and derive the worktree inventory from
`git ls-files -co --exclude-standard`, while continuing to scan every byte of
each existing publishable text file and every private path rule. Intentionally
deleted index paths must be skipped after an existence check.

## Current Status

Resolved. The corrected inventory checked 1,716 existing publishable files and
reported zero findings. The external postmortem-memory ledger remains outside
the user-authorized folder and is intentionally untouched.
