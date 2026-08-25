# Package Sudo-Required Commands Prompt

## Purpose And Observable Outcome

Provide a reusable prompt that requires a narrow privileged script, an
elevation summary, and an exact user-run `sudo` invocation.

## Current Context, Relevant Files, And Scope Boundaries

- `prompts/package-sudo-required-commands.md` is the reusable template.
- The canonical feedback log preserves the durable workflow preference.
- The August 25 sandbox incident records the failed tooling path and recovery.

## Assumptions And Decisions

- The user reviews and runs privileged scripts; the prompt never runs `sudo`.
- The script contains only privileged commands and names rollback and checks.

## Implementation Checklist

- [x] Add the reusable prompt and durable feedback entry.
- [x] Maintain the related sandbox-failure postmortem.
- [x] Recheck prompt requirements, whitespace, and the README gate.

## Risks, Verification Evidence, And Review Notes

- No credential, command execution, or system-state change is introduced here.
- Automated: `git diff --check` and `./scripts/executable_readme-recruiter-sync`.
- Manual: review placeholder handling and the exact example `sudo` invocation.
- Progress: final evidence is recorded before the documentation commit.
- Evidence: placeholders and no-direct-sudo requirement are present; `git diff
  --check` exited 0 and the README gate returned `pass_no_change` on 2026-08-25.
