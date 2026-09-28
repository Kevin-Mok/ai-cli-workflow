# Command sandbox loopback startup failure

Date: 2026-09-28

## Symptom and impact

The first parallel repository inspection commands exited before running with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. This delayed the media-script audit; no repository files were changed by those commands.

## Evidence and status

`git status --short`, `cat`, and `rg` each returned exit 1 with the same sandbox startup error. Repeating `git status --short` with approved elevated command access exited 0 and exposed the pre-existing dirty files. Repository inspection now works through that path.

## Root cause and resolution

The command sandbox could not configure its loopback interface in this environment. The command itself and repository data were not the cause. Use approved elevated command access for this session's shell commands.

## Verification and follow-up

The elevated `git status --short` completed with exit 0. The sandbox configuration remains outside this repository's scope; future sessions should retry ordinary access first.
