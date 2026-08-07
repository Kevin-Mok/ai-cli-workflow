# ExecPlan: Sync Clarifications Back to Documentation

## Purpose and observable outcome

Require Codex to correct the applicable smoke-test or procedure document when
the user asks for clarification because those instructions are unclear, so the
same ambiguity does not remain for the next reader.

## Current context, scope, and decisions

- `dot_codex/AGENTS.md` is the canonical instruction body; root `AGENTS.md`
  routes to it and does not duplicate its policy.
- The new rule belongs in **Documentation And Repo Surfaces**, immediately
  after the existing `docs/smoke-tests.md` maintenance rule.
- `dot_agents/skills/feedback-memory/feedback.log` is the append-only,
  repo-tracked durable-preference log.
- Scope is limited to instruction and preference documentation. Runtime
  configuration, smoke-test content, README copy, and the pre-existing edits
  in `aliases/key_dirs.tmpl` and
  `docs/superpowers/specs/2026-08-04-commit-plan-push-design.md` are protected
  and out of scope.

## Assumptions

- “Following docs” means an existing documented procedure whose ambiguity
  prompted the user’s clarification request.
- “Updates the doc as well” means the relevant document is updated in the
  same change, rather than leaving the answer only in chat.

## Implementation checklist

- [x] Capture the initial dirty state and read the canonical instructions,
  plan contract, durable-feedback log, and engineering lessons.
- [x] Add a canonical instruction requiring documentation updates for unclear
  smoke-test and documented-procedure clarification requests.
- [x] Append the durable user preference to the canonical feedback log.
- [x] Confirm the README’s existing documentation-sync description remains
  accurate, so no unrelated README rewrite is needed.
- [x] Verify the exact policy text, final diff, and protected dirty state.

## Risks, edge cases, and rollback

- The rule must not require an update when the clarification is unrelated to
  a smoke test or documented procedure.
- `docs/smoke-tests.md` is used for smoke-test clarifications; other
  procedures update their own relevant document.
- Rollback is a single-line removal from the canonical instruction file plus
  removal of this plan and the appended durable-preference line if the policy
  is rejected.

## Verification and review notes

- `rg` found the new canonical rule and the appended durable-preference entry (exit 0).
- `git diff --check` completed without output (exit 0).
- `git status --short` kept the protected pre-existing edits separate from this change.
- No executable behavior changed, so targeted text inspection and diff review are proportionate checks.
