# Task completion verification commands

Extend the existing commit handoff rule to every completed task. Update the
canonical instructions, public explanation, and smoke checks, then apply the
managed configuration and verify the installed policy.

## Purpose and observable outcome

Every final completion handoff includes 5–10 direct verification commands with
working directory, sudo requirement, and labeled expected output after each,
including tasks completed without commits or pushes.

## Context and scope

Update `dot_codex/AGENTS.md`, `README.md`, `docs/commit-status-overviews.md`,
`docs/smoke-tests.md`, and the append-only canonical feedback log. Record the
unexpected runner failure and its reviewed ledger entry. The subsequent explicit
`commit-session` request authorizes a session-only commit and upstream push.

## Assumptions and decisions

- Extend the trigger to all completed tasks, including docs, configuration,
  analysis and planning; preserve the existing command quality and output rules.
- Commands must inspect or exercise the delivered outcome and remain useful
  for tasks without new executable behavior. Do not pad with unrelated checks.
- Plan Mode cannot be entered with the tools in this session; keep this small,
  decision-complete document in the current mode.

## Implementation checklist

- [x] Read current guidance and capture the initial dirty state.
- [x] Record the new preference and sandbox workaround incident.
- [x] Broaden the completion trigger and synchronize public docs and smoke checks.
- [x] Run `fish -ic 'refresh-config'` and verify installed instructions.
- [x] Review session diffs and record verification and handoff evidence.

## Risks, protected work, and rollback

Initial dirty tracked files: README, commit-status-overviews, smoke-tests,
feedback log, postmortem ledger, canonical AGENTS, notification script and its
tests. Existing untracked incident reports, session-insights, voice plan and
voice tests are protected. Preserve all baseline edits; snapshots of touched
existing files are under `/tmp/task-completion-policy-before/`. Rollback means
reverting only this session's changes and refreshing configuration again.
No history rewrite is in scope. Stage only attributable session changes;
preserve all pre-existing and concurrently added work.

## Verification

This is a policy/documentation edit; no implementation-mirroring tests are added.
Review the delta against the captured baseline, run `git diff --check`, run
`python3 dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check
--postmortem /home/example/linux-config/docs/postmortem/2026-10-09-task-completion-policy-sandbox-startup.md`,
run `fish -ic 'refresh-config'`, and compare source and installed AGENTS bytes.
Manual smoke: fresh Codex sessions completing docs, configuration explanation,
analysis and planning without Git writes must include the same command handoff.
These agent compliance checks remain manual; activation verifies file delivery,
not guaranteed future model compliance.

## Progress and evidence

Initial default commands failed before execution; approved instruction/status
reads exited 0. Existing sandbox workaround applies; host repair is outside scope.

- `git diff --check`: exit 0, no whitespace errors.
- Targeted postmortem-memory check: exit 0; errors, changed sources, new sources,
  missing sources and unregistered aliases all empty.
- `fish -ic 'refresh-config'`: exit 0, `REFRESH COMPLETE`; log
  `/tmp/refresh-config-20261009-115647-594473.log` records its stages.
- Python byte comparison of `dot_codex/AGENTS.md` and `~/.codex/AGENTS.md`:
  passed, installed policy matches source byte-for-byte.
- Reviewed policy/docs deltas against `/tmp/task-completion-policy-before/`:
  extension is limited to completion scope and related docs; pre-existing work
  retained. No commit or push created.
- Final handoff includes five optional fresh-session CLI probes for policy
  explanation, docs summary, configuration explanation, analysis, and planning.
  Fresh-model compliance remains an operator smoke check, not an observed result.

## Review notes

Keep this plan with its related edits in any later authorized commit.
Suggested subject: `docs: require verification commands at every task completion`.

## Commit milestone — docs: require commands at every task completion

- Completed: all-task completion rule, public docs, durable feedback, incident
  record and reviewed ledger entry. Managed instructions were refreshed.
- Verified: README gate returned `pass_no_change`; whitespace check and targeted
  incident-memory check passed. Installed canonical instructions match source.
- Scope: helper returned `unsafe` because tool-orchestrated writes were not
  detected. Direct-write fallback uses the captured initial status and saved
  pre-edit snapshots. Stage only this session's policy/docs changes, its appended
  feedback entry, its incident ledger entry, and its new incident and plan.
- Mixed-file boundary: retain the earlier post-commit command-format edits and
  voice-audition changes in the working tree. The committed canonical opening
  extends completion scope while preserving HEAD's existing formatting suffix;
  this session's explicit formatting preference and completion guide apply.
- Remaining: commit and push to `origin/main`; no implementation blockers.
  Fresh-session agent compliance checks remain manual.
- Next: report the resulting commit hash and upstream push outcome in Codex.
