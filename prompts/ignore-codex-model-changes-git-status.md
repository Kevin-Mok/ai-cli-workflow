You are a Linux configuration maintainer. I need local changes to `dot_codex/config.toml` (especially `model` updates) to stop showing up in status output while keeping the file tracked.

Use repo-local model-only status filtering, not skip-worktree.

1) Keep `dot_codex/config.toml` tracked and unchanged in index.
2) Confirm it is tracked before any filtering:
   `git ls-files --error-unmatch dot_codex/config.toml`
3) Use the wrapper for status checks:
   `~/linux-config/scripts/executable_codex-model-status --short -u`
4) Verify model-only behavior:
   - Modify only `model = ...` in `dot_codex/config.toml`.
   - Run the wrapper status.
   - Expect no status line for `dot_codex/config.toml`.
5) Verify non-model keys are not suppressed:
   - Modify `model_reasoning_effort` (or `developer_instructions`, `personality`, etc.).
   - Run the wrapper status.
   - Expect `dot_codex/config.toml` to be reported.
6) Verify clean files remain unchanged:
   - Commit `dot_codex/config.toml` and make no edits.
   - Wrapper status should match plain `git status` behavior for this path.
7) Manual fallback checks if the wrapper is unavailable:
   - `git ls-files --error-unmatch dot_codex/config.toml`
   - `git diff -- dot_codex/config.toml`

Model-only detection in the wrapper uses:
`^[[:space:]]*model[[:space:]]*=`
Only changed added/removed lines matching this regex are treated as ignorable.

If the wrapper path is unavailable, use plain `git status` behavior (no model-only suppression) and re-enable the wrapper in the repo workflow.
