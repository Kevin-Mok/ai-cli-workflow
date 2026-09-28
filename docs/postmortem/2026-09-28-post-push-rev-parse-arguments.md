# Post-push SHA check used invalid rev-parse arguments

## Symptom and impact

After the three planned commits were pushed on 2026-09-28, an extra read-only SHA comparison exited 128 with `fatal: Needed a single revision`. The push itself succeeded, and `git status --short --branch` showed clean `main...origin/main`.

## Evidence and root cause

The failed command was `git rev-parse --short HEAD @{upstream}`. `--short` expects one revision in this invocation; passing both names made the verification command invalid. No repository or remote content was changed by that read-only command.

## Resolution, verification, and follow-up

Run `git rev-parse --short HEAD` and `git rev-parse --short '@{upstream}'` separately, then compare their outputs. Keep the command syntax separate in future post-push checks. This record is a documentation follow-up to the delivery workflow.
