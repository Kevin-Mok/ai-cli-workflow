# Repository shell sandbox startup failure

## Symptom and impact

The first repository inspection commands failed before starting the shell with
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. This delayed
inspection but did not alter repository files.

## Evidence and root cause

Three default-sandbox shell starts failed with the same network-namespace setup
error. Read-only inspection succeeded after approved elevated command execution,
confirming the failure was sandbox startup rather than a repository command.

## Resolution and verification

Repository inspection continued using read-only commands through the approved
execution path. The initial `git status --short` was empty; subsequent inspection
and work proceeded without overwriting pre-existing changes.

## Follow-up

No repository-level change is indicated. Retry through the approved execution
path if the default sandbox reports the same namespace setup error again.
