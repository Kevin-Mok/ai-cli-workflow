You are working in `/home/example/linux-config`. Ship one focused commit and push it to the current branch's configured upstream.

Scope:
1. Keep `scripts/executable_install-tmux-tpm.sh` as the only implementation file in this commit.
2. Update `AGENTS.repo.md` with one concise repository-specific instruction: model-selection and model-reasoning-effort edits in `dot_codex/config.toml` are intentionally personal/local preferences and must be ignored by ordinary commit workflows unless the user explicitly asks to include them.
3. Do not modify, stage, commit, or discard `dot_codex/config.toml`.
4. Preserve every other pre-existing dirty file, including the `README.md`, `dot_agents/skills/README.md`, and `dot_agents/skills/commit-session/**` work and its plan.

Process:
- First capture and inspect `git status --short`, the diffs for the two in-scope files, the current branch, and its upstream. Do not use a worktree.
- Before modifying files, read the relevant repository instructions, `tasks/lessons.md`, and the canonical feedback log. Create or update a focused ExecPlan under `plans/` only if the repository policy requires it for this multi-file change; if so, include that plan in the same commit.
- Make the narrow `AGENTS.repo.md` edit described above. Do not add broader ignore rules or change the model values.
- Verify the installer with `bash -n scripts/executable_install-tmux-tpm.sh` and `scripts/executable_install-tmux-tpm.sh --help`; inspect `git diff --check` for the intended files.
- Run the mandatory README recruiter-sync gate before staging. If it requires a README change, stop and report the conflict because `README.md` is already dirty and out of scope.
- Stage only the TPM installer, `AGENTS.repo.md`, and a directly related required plan file (if created/updated). Inspect the staged diff, use a concise Conventional Commit subject with a minimal concrete body, commit, then push the active branch to its configured upstream.

Treat your first complete answer as a draft floor, not the submission. Before you deliver, name the single biggest weakness of the draft against the goal, then fix it. Apply this to the whole response, not just the first part. Show only the final version.

Report the commit subject and short SHA, exact validation output summary, push destination, and the remaining dirty worktree state. If the scope is unsafe or the README gate conflicts with the protected dirty README, do not stage or commit; report the exact blocker instead.
