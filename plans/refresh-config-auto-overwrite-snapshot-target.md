# Refresh-Config Snapshot Target Apply

## Purpose And Observable Outcome

Make `refresh-config` snapshot and apply its Codex and Git configurations
without interactive ChezMoi overwrite prompts, while preserving normal prompts
for every other managed target.

## Current Context And Scope

- `dot_config/fish/functions/refresh-config.fish` snapshots live
  `~/.codex/config.toml`, captures `~/.gitconfig`, and then invokes a broad
  `chezmoi apply`.
- After that snapshot, ChezMoi prompts because the target differs from its last
  recorded write. The user captured the failure on 2026-08-17.
- Test coverage is `tests/test_refresh_config_function.sh`; public references
  are in `README.md` and `docs/smoke-tests.md`.
- Protected pre-session changes are `README.md`, `docs/smoke-tests.md`,
  `dot_agents/skills/feedback-memory/feedback.log`,
  `dot_codex/AGENTS.md`, `prompts/ignore-codex-model-changes-git-status.md`,
  `tests/test_ai_workflow_contract.py`, `plans/immediate-failure-postmortems.md`,
  and `tests/test_codex_model_skip_worktree.py`.

## Assumptions

- The snapshot helper remains the sole validator and writer for the tracked
  Codex source.
- Targeted forced applies are safe only for the exact Codex and Git targets
  that `refresh-config` intentionally captured in the same invocation.
- The subsequent unforced `chezmoi apply` must preserve interactive protection
  for all other targets.

## Implementation Checklist

- [x] Reproduce and trace the prompt to the broad apply after the snapshot.
- [x] Add a failing shell-test assertion for the targeted forced Codex apply.
- [x] Apply the minimal Fish implementation change.
- [x] Update the README and smoke checklist with the no-prompt guarantee.
- [x] Close the original interactive ChezMoi process and verify the Codex
  target force-applies without a prompt.
- [x] Integrate the requested Git-config snapshot and targeted apply,
  normalize blank helper whitespace, complete live verification, and update the
  postmortem with final evidence.

## Risks, Edge Cases, And Rollback

- Never use broad `chezmoi apply --force`; that could overwrite unrelated
  targets without a prompt.
- If the snapshot fails, no apply, shortcut sync, source, or Fish reload may
  run.
- Rollback removes the targeted forced apply, related test and documentation,
  postmortem update, and this plan.

## Verification Evidence

- RED command: `bash tests/test_refresh_config_function.sh`
  - Expected: fails while either captured target lacks a targeted forced apply
    or blank credential-helper whitespace remains.
  - Observed: first failed with only `chezmoi:apply`; later failed because the
    copied Git config retained whitespace after an empty helper assignment.
  - Exit status: 1.
- GREEN command: `bash tests/test_refresh_config_function.sh`
  - Expected: passes while asserting both targeted applies, normal apply,
    snapshot failure stop, Git-config normalization, shortcut sync, and Fish
    reload behavior.
  - Observed: passed after both targeted applies and blank-helper normalization
    were added; a live run also completed without prompts.
  - Exit status: 0.

- Full-suite verification used `python3 -m pytest -q`: 342 tests and 49 subtests passed, while one unrelated sanitized-vault fixture remains stale for the tracked July 22 note.

## Review Notes

- Both forced applies remain limited to the exact sources captured by this
  workflow; the broad apply remains unforced for all unrelated targets.
- The original interactive ChezMoi process was terminated with user approval,
  and the final live run completed without a prompt or whitespace error.
