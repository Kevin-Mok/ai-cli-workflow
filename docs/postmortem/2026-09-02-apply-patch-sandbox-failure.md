# Apply-Patch Sandbox Failure

## Symptom

The patch helper failed before applying the installer test and script changes,
reporting `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.

## Impact

No repository file changed in that failed patch attempt; implementation was
temporarily blocked by the sandbox helper.

## Evidence

- 2026-09-02 `apply_patch` returned a sandbox-helper failure with the bwrap
  loopback network-namespace error.

## Current Status And Next Steps

- Resolved with the workspace-provided `apply_patch` executable after the
  integrated helper repeatedly failed while reopening an existing file.

## Root Cause

The integrated patch helper's filesystem sandbox could not configure its
loopback network namespace. Adding a new file happened to work, but updating
an existing file consistently failed before a patch could be applied.

## Resolution And Verification

- Used the workspace-provided patch utility with the same scoped unified diff;
  no ad-hoc file-writing command was used.
- The recovery patches the installer test, README, smoke-test checklist, plan,
  and this postmortem in place.
- Final verification will re-run the focused test, shell syntax check, and
  `git diff --check` before delivery.

## Follow-up

If the integrated patch helper again returns the bwrap loopback error, use the
workspace-provided patch utility for a reviewed, scoped unified diff and retain
the resulting postmortem with the affected change.
