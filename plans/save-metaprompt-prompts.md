# Save Metaprompt Prompts

## Purpose And Observable Outcome

Make every metaprompt compilation persist its compiled prompt as a concise
kebab-case Markdown file in the repository-root `prompts/` directory, while
preserving the existing standalone-`go` execution gate. The user receives the
saved path with the normal compile metadata.

## Current Context And Scope

- The implementation is `dot_agents/skills/metaprompt/SKILL.md`.
- The existing focused contract is `tests/test_metaprompt_contract.py`.
- Pre-existing dirty work is protected: `README.md`, `docs/smoke-tests.md`,
  `plans/aerc-multi-account-mail.md`,
  `scripts/executable_setup-aerc-mail.sh`, and
  `tests/scripts/executable_setup-aerc-mail_test.sh`.
- In scope: this plan, the metaprompt skill, its focused contract test, and the
  metaprompt smoke-test entry. Out of scope: creating prompts during this
  change, changing the `go` gate, or touching unrelated dirty work.

## Assumptions And Decisions

- “Repo root” resolves to the active repository’s `prompts/` directory.
- The filename is derived from the prompt subject in concise kebab-case; use a
  non-destructive suffix when that filename already exists.
- The saved file contains the compiled prompt only. Chat retains the existing
  prompt block and gate, augmented with `Saved: prompts/<filename>.md`.
- The save is required before presenting the gate; an unavailable or unwritable
  directory is an actionable error, not permission to skip persistence.

## Ordered Implementation Checklist

- [x] Capture the initial dirty state and review the skill, references, and
  focused contract-test conventions.
- [x] Add a focused failing contract assertion for the required repo-root save,
  kebab-case filename, Markdown extension, collision-safe behavior, and output
  `Saved:` metadata.
- [x] Run `python3 tests/test_metaprompt_contract.py` and confirm the new
  assertion fails because the current skill contains no persistence contract.
- [x] Update `SKILL.md` with the minimal mandatory save instruction and output
  shape, without weakening the fresh standalone-`go` gate.
- [x] Update the metaprompt entry in `docs/smoke-tests.md` with a save-and-gate
  manual check.
- [x] Re-run the focused contract test, the skill validator, and
  `git diff --check`; record fresh results here.
- [x] Review the final diff and protected dirty files; keep this plan current
  and commit its final evidence with the related implementation if asked.

## Risks, Edge Cases, And Rollback

- A generated filename can collide. Require a non-destructive suffix rather
  than overwriting an existing prompt.
- The persisted prompt must not contain `Run`, `Weight`, or `go` metadata; it
  remains a standalone prompt artifact.
- A save failure must surface before the gate so a user never believes the
  artifact exists when it does not.
- Rollback is reverting the isolated skill, test, smoke-test, and plan changes.

## Verification And Review Notes

RED observed: `python3 tests/test_metaprompt_contract.py` exited 1 with seven expected missing-save contract assertions. GREEN observed: the same command ran 12 tests successfully after the skill update (exit 0). `python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/metaprompt` reported `Skill is valid!` (exit 0). `git diff --check` passed with no output (exit 0). Manual usage review: an independent reviewer confirmed the release-notes scenario requires repo-root `prompts/` persistence, a kebab-case `.md` path, collision protection, prompt-only contents, `Saved:` metadata, and a fresh literal `go`. Review also found and prompted the correction from four to five stages. Related baseline limitation: `python3 tests/test_ai_workflow_contract.py` still fails because its delivery-preference test expects the July 13 feedback entry to be the final log line, while the tracked log ends with newer July 28 guidance; this change did not modify that log or test.
