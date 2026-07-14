# Shell Interpolation Caused An Early Push

## Symptom

A read-only plan search unexpectedly ran `git push` while Task 3 was still
uncommitted.

## Impact

The already-reviewed Task 1 and Task 2 commits, `bd3d835` and `dec36e0`, reached
`origin/feat/ai-workflow-optimization` earlier than the approved single-push
checkpoint. No Task 3 file, uncommitted change, or protected
`dot_codex/config.toml` content was included. Published history was not
rewritten.

## Evidence

The command output reported the upstream movement from `dbc311d` to `dec36e0`.
The repository still showed all Task 3 work as uncommitted and the protected
config checksum remained
`3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`.

## Root Cause

The search expression contained Markdown backticks inside a double-quoted
shell argument. The shell treated the enclosed text as command substitution and
executed it before `rg` received the pattern.

## Resolution

The accidental push was disclosed immediately. The published prerequisite
commits remain intact; Task 3 will be verified, committed, and pushed as a
separate follow-up. Subsequent shell search patterns use single-quoted or
fixed-string arguments with no executable interpolation.

## Verification

The upstream ref resolved to `dec36e0` after the incident, while Task 3 remained
only in the local worktree. Final local/upstream equality is tracked in the
[Second Brain ExecPlan](../../plans/integrate-second-brain.md).

## Follow-Up

- Treat shell command strings as executable input even for read-only tools.
- Keep the reusable command-substitution warning in `tasks/lessons.md`.
- Preserve published history and finish the remaining verified commit normally.
