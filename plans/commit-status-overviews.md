# Commit status overviews

Keep example-user informed after every commit with a short status overview in both a maintained document and Codex output, alongside the existing smoke-test commands. Save the preference, update delivery guidance and public docs, then verify and refresh the managed configuration.

## Purpose and observable outcome

Every authorized commit workflow reports where the task stands after each commit. The maintained document and Codex response cover completed work, verified results, remaining work, blockers and the next step, with a link to the document.

## Context and scope

Change only the relevant policy paragraph in `dot_codex/AGENTS.md`, append to canonical feedback, add a public delivery guide, link it in README, and add a smoke check. Maintain the task incident and its reviewed ledger entry. Preserve all extensive pre-existing dirty work; the initial `git status --short` was captured before writes and edited-file byte snapshots are in `/tmp/commit-status-overviews-baseline`.

## Assumptions and decisions

- This request changes standing reporting guidance; it does not authorize a commit or push now.
- Use the active plan for status when available; otherwise use `docs/task-status.md` in the working repository. Retain prior commit milestones.
- Prepare status before each commit and include it with related changes. Identify that milestone by subject or sequence in the document; report the resulting hash in Codex output to avoid a self-referential commit hash.
- For a multi-commit series report each milestone promptly in Codex output, preserving the configured push cadence.

## Ordered checklist

- [x] Capture baseline and read required guidance.
- [x] Save durable preference and record the shell-startup incident with a no-new-learning ledger review.
- [x] Update canonical policy, public guide, README and smoke verification.
- [x] Review focused diffs and run targeted incident coverage check.
- [x] Run refresh-config and confirm managed policy matches, or record exact blockage.
- [x] Reconcile progress and provide a concise handoff with the status-document link.

## Risks, edge cases and rollback

Policy, README, feedback, smoke docs and ledger already contain unrelated changes. Preserve their baseline content and append or replace only scoped text. Do not stage or commit. Status distinguishes checked behavior from deployment/live activation. Rollback removes only this session's additions; do not restore whole dirty files. Refresh snapshots live Codex/Git configuration and applies all managed targets; inspect its output and record failures.

## Verification

Review the new policy, guide and smoke expectation against the requested fields and per-commit cadence. Run `git diff --check` on scoped tracked files and `python3 dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/example/linux-config/docs/postmortem/2026-10-08-commit-overview-shell-startup.md`. Run `fish -ic 'refresh-config'`, then compare the installed policy with `dot_codex/AGENTS.md`. Documentation-only change: no application behavior test is needed. The smoke check is a future fresh-agent reporting review, not a claim of agent compliance already tested.

## Progress and evidence

- Saved the durable preference and updated the canonical per-commit reporting rule, public guide, README link and smoke expectation.
- Focused baseline-to-working-tree review confirmed scoped edits; feedback remains append-only and pre-existing ledger records are unchanged. `git diff --check` on the scoped tracked files exited 0.
- Targeted incident ledger check exited 0 with no errors, missing sources or unregistered aliases.
- `fish -ic 'refresh-config'` exited 0 and printed `REFRESH COMPLETE`; log: `/tmp/refresh-config-20261008-141706-1987053.log`. Its normal conflict recovery adopted the existing live Second Brain `cli.py` and `session_review.py` targets; those incidental refresh effects are excluded from this task's proposed commit scope.
- `cmp dot_codex/AGENTS.md /home/example/.codex/AGENTS.md` exited 0: the managed policy is applied.

### Current overview

Completed: the standing commit-reporting rule is saved and applied, with matching public guidance and a manual smoke expectation. Verified: focused diff checks, incident coverage and configuration refresh passed. Remaining: no work remains in the requested documentation scope; future agent adherence has a documented manual check. Blockers: none for this task; default sandbox startup remains an unrelated host issue. Next: use this reporting format during the next authorized commit workflow. No commit or push was requested or performed.

## Review notes

Keep this plan with related documentation in any later authorized commit. Suggested subject: `docs: require commit status overviews`. No commit or push requested in this task.
