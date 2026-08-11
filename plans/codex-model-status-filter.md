# Codex config model-only status filter

## Purpose and observable outcome
Keep `dot_codex/config.toml` tracked, while only suppressing status visibility for `model`-only diffs.

- `model = ...` local changes should be hidden.
- Any other changed key (for example `model_reasoning_effort`) should remain visible.
- Clean file state should preserve normal status behavior.

## Current context, relevant files, and scope boundaries
- Relevant files:
  - `scripts/executable_codex-model-status` (new)
  - `aliases/key_aliases.tmpl` (status shortcut wiring)
  - `prompts/ignore-codex-model-changes-git-status.md`
  - `tests/test_codex_model_skip_worktree.py`
- Scope is limited to repository status visibility for this tracked file.

## Assumptions and decisions already settled
- The wrapper applies only when invoked (shortcut/manual), not to bare `git status`.
- Model-only detection uses `^[[:space:]]*model[[:space:]]*=` exactly.
- Existing `gs` shortcut is the preferred path in this repo.

## Ordered implementation checklist
- [x] Add model-aware local status wrapper script.
- [x] Wire repo status shortcut to wrapper.
- [x] Update prompt artifact with wrapper usage and regex expectations.
- [x] Replace skip-worktree regression with model-only behavior tests.
- [x] Run focused verification.

## Risks, edge cases, rollback points, and protected dirty state
- Risk: regex-based logic ignores multiline model values unless each changed line matches the same-line regex.
- Edge case: status lines for `dot_codex/config.toml` are filtered by trailing path match.
- Rollback: restore `gs` to `git status -u` and remove wrapper file.
- Protected dirty state (pre-existing before this task): captured by initial status snapshot at task start.

## Exact automated and manual verification
- `python3 -m pytest tests/test_codex_model_skip_worktree.py`
  - expected: all new scenarios pass
  - observed: 3 passed
- `git status --short`
  - expected: only intended task files show changes
  - observed: `M aliases/key_aliases.tmpl`, `M prompts/ignore-codex-model-changes-git-status.md`, `A plans/codex-model-status-filter.md`, `A scripts/executable_codex-model-status`, `A tests/test_codex_model_skip_worktree.py`

## Progress, verification evidence, and review notes
- Status and wrapper are implemented and verified.
- The old skip-worktree approach is fully replaced by model-line-aware filtering.
- No file content or index state is rewritten by the wrapper; it only filters output.
