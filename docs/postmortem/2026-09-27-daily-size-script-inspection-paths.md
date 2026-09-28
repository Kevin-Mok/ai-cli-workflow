# Inspection path errors during daily size script work

## Symptom and impact

Read-only inspection commands exited nonzero after looking for a `.sh` suffix on `scripts/executable_rsync-media-date` and for a test guide at an incorrect skill path. An `rg` search with no matches also returned 1. No repository content changed in those commands.

## Evidence and root cause

`sed` reported that the guessed script path did not exist. `cat` reported that the guessed guide path did not exist. A later `rg --files scripts` located the actual extensionless command, and reading it succeeded. The root cause was guessing path names instead of discovering them first. The test guide path was unneeded for implementation.

## Resolution, verification, and follow-up

The actual extensionless command was inspected successfully. The new command's focused tests passed all four cases, its `--help` invocation exited 0, and `git diff --check` exited 0. Future inspections should use discovered paths rather than inferred suffixes. No repository rollback is needed for the read-only failures.
