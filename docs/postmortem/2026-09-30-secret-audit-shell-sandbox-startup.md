# Secret audit shell sandbox startup failure

Date: 2026-09-30

## Symptom and impact

Initial read-only repository inspection commands exited before running with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. The Git history audit was delayed; those commands changed no repository files.

## Evidence and status

The `cat`, `git status --short`, and `rg` commands all returned exit 1 with the same sandbox startup error. An approved elevated `git status --short` returned exit 0 with a clean working tree, and subsequent read-only commands succeeded.

## Root cause and resolution

The shell sandbox could not configure its loopback interface. The commands and repository data were not the cause. Continue this audit through approved elevated command access.

## Verification and follow-up

The elevated repository status and instruction reads completed successfully. The sandbox configuration remains outside this repository's scope.
