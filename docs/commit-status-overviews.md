# Commit status overviews

After each commit, give a short overview of where the task stands in both a maintained document and Codex output. Prepare the document with the related work, report the commit result with a link to it, and include the smoke-test commands so example-user can immediately check the result. Every task completion also includes these commands, even when no commit or push occurs.

## Document and reporting cadence

Use the active plan under `plans/` when one exists; otherwise maintain `docs/task-status.md` in the working repository. Retain previous commit milestones so the series remains understandable. Update the status before committing and include it in the same commit as the work it describes.

Identify the document milestone by commit subject or sequence. After the commit succeeds, report its actual hash in Codex output; a document inside the commit cannot contain its own final commit hash. Report each intermediate commit in commentary, and include the current overview again in the final response. Keep the established push cadence.

## What each overview covers

- Completed: the outcome of this commit and the current phase of the overall task.
- Verified: checks that ran and their actual results; distinguish live activation from local checks.
- Remaining: unfinished work and blockers, explicitly stating when there are none.
- Next: the next concrete step, or that the requested scope is complete.

Keep the overview high-level and specific to the task. Link the maintained document from the Codex response and include 5–10 copy-pasteable smoke-test commands with the working directory, expected results and whether sudo is required. Prefer an existing reusable smoke script. Push reports also include the smoke-test commands.

## Task completion without a commit

Include 5–10 copy-pasteable direct verification commands in every final completion
handoff, including documentation, configuration, analysis, planning and feature
tasks. The trigger is task completion; a commit or push is not required. Use the
same working-directory, sudo and per-command expected-output format described
above. For tasks without new executable behavior, verify the delivered artifact
or exercise the relevant workflow. Keep each command useful and specific to the
completed result; do not invent behavior or pad the list with unrelated checks.
Complete required automated checks before the handoff and report them separately.

## Example milestone

> Commit 2 — fix: show progress during scans
>
> Completed: long scans now show elapsed time while they run. The scan feature is implemented.
> Verified: focused regression checks passed; live installation remains pending.
> Remaining: install and exercise the CLI on the intended machine. No blockers.
> Next: refresh the managed configuration and run the documented live smoke check.

The accompanying Codex response reports the actual commit hash, links this milestone document and gives the task's smoke-test commands.

See the [canonical delivery policy](../dot_codex/AGENTS.md#git-and-delivery) and [repository smoke checks](smoke-tests.md#repo-instructions).
