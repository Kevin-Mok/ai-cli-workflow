# Commit inspection sandbox failure — 2026-09-22

## Symptom and impact
The first read-only repository inspection could not start because bubblewrap
reported `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1).
No repository command ran and no files changed in that attempt.

## Cause and resolution
The sandbox could not configure its loopback network namespace in this runtime.
The same inspection succeeded with approved execution outside that sandbox
(exit 0), including capture of the initial Git status before any writes.

## Verification and follow-up
Resolved for this delivery through approved execution. Continue repository
validation through that execution path; no repository configuration workaround
or sandbox policy change is needed.
