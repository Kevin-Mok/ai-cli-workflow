You are a Linux configuration maintainer. I need local changes to `dot_codex/config.toml` (especially Codex `model` updates) to stop showing up in `git status`, while still keeping the file tracked for normal updates.

Give me precise shell commands to do this locally and how to safely revert later.

Run, from repo root:

1) Confirm the path is tracked: `git ls-files --error-unmatch dot_codex/config.toml`.
2) Mark it as skip-worktree so local diffs are ignored in status/diff: `git update-index --skip-worktree dot_codex/config.toml`.
3) Verify: change model field, then `git status --short dot_codex/config.toml` should remain clean.
4) Add a quick rollback command: `git update-index --no-skip-worktree dot_codex/config.toml`.

If `skip-worktree` is too blunt, provide fallback commands for `--assume-unchanged` and a short tradeoff for both.
