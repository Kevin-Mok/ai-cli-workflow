# Filter-Branch Environment Shell Mismatch

This incident records why the first history-filter attempt stopped on its first commit. Git sources `--env-filter` through POSIX `sh`, but the helper used Bash-only indirect parameter expansion; the corrected helper assigns author and committer fields explicitly and is verified under `dash` before retry.

## Symptom

`git filter-branch` stopped at commit 1 of 698 with `Bad substitution` while sourcing the environment filter.

## Impact

- No rewritten branch ref was completed or imported into the original repository.
- The temporary clone is treated as disposable and will be recreated from the verified private bundle.
- The source repository remains unchanged.

## Evidence

- The failing expression used Bash indirect expansion (`${!name_variable}`).
- `filter-branch` invoked the env filter through `/bin/sh`, so the helper shebang did not control the sourcing shell.
- Tree and message filter fixture tests had passed; the failure occurred before their first commit result was retained.

## Prior-Knowledge Lookup

- Query: `git filter-branch env-filter bad substitution POSIX sh bash indirect expansion`.
- Matches: cross-shell transport guidance applies; explicitly test the actual shell boundary and avoid unsupported syntax.
- Decision: replace indirection with direct POSIX assignments for author and committer variables, then verify through `dash`.

## Root Cause

The helper was written and tested as an executable Bash script, but `--env-filter` sources its command text inside Git's POSIX shell. Sourcing ignores the helper's shebang and exposes Bash-only syntax to `sh`.

## Current Status

Resolved.

## Resolution And Verification

The direct-assignment environment helper passed its `dash` fixture. The fresh
isolated rewrite processed all 698 original commits, normalized identities, and
completed with 688 retained commits after empty pruning.

## Follow-Up

- Test filter helpers through the exact Git invocation shell, not only their declared interpreter.
- Recreate a clean temporary clone after any interrupted history filter.
- The shared postmortem-memory ledger remains outside the authorized folder and is intentionally untouched.
