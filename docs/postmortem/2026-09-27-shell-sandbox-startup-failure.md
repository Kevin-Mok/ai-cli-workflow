# Shell sandbox startup failure during HDD wizard work

## Symptom and impact

The initial read-only repository command and a simpler retry both exited 1
before the shell ran, printing `bwrap: loopback: Failed RTM_NEWADDR: Operation
not permitted`. They could not capture Git status or read instructions. No
repository file or machine state changed in those attempts.

## Evidence and root cause

Both failures came from the command sandbox's loopback setup, before command
execution. The same read-only Git and instruction command completed with exit
0 under reviewed elevated execution; its initial `git status --short` was
empty. This isolates the failure to sandbox setup, not the repository command.

## Resolution and verification

Use reviewed elevated shell execution for this task's repository inspection
and verification. The first elevated command read the active instructions and
returned exit 0; later elevated read-only inspections and `bash -n` also
returned exit 0. File edits stayed within the authorized repository.

## Follow-up and rollback

No runtime repair is needed. If restricted shell startup still fails in later
work, report its exact error and use an approved execution route. This record
documents the tooling failure; deleting it is the only repository rollback.
