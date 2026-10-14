# Index Filter Executable-Bit Failure

This report records a path-only history filter that stopped because its temporary
filter script lacked an executable mode bit.

## Symptom

On 2026-10-14, `git filter-branch --index-filter` returned “Permission denied”
when it tried to execute the temporary binary-drop script.

## Impact

The second-stage rewrite stopped on commit 1 of 688 before any refs were updated.
The already sanitized history and the source repository were unchanged.

## Evidence

- The rule update completed and produced seven mode-0600 drop paths.
- Filter-branch reported the permission error on its first rewrite entry.
- No ref-update summary was emitted.

## Root Cause

The temporary script was created through a patch operation, which preserved its
content but did not add an executable mode bit. The command passed the script
path directly instead of naming an interpreter.

## Resolution

Invoke the filter as `sh <script>` so execution depends on the known POSIX shell,
not the temporary file's mode bit.

## Verification

The corrected interpreter invocation completed the path-only rewrite over all
688 retained commits. Subsequent binary inventory found 258 small PNG assets and
no audio, and the all-object audit passed with zero findings.

## Follow-up

Treat generated filter scripts like other executable test fixtures: validate the
invocation contract before launching a history rewrite. The external canonical
postmortem-memory ledger remains untouched because it is outside task scope.
