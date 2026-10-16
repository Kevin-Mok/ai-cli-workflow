# Completed migration: read-only verification

The migration is complete. Verify the active public checkout and report any
remaining differences without another cutover. Inspect origin/upstream and the
private completed migration journal locally; keep settings and recovery data
private. Do not run apply/rollback, replace the checkout, import old Git objects,
or restore accepted files merely because their old hashes changed during later
work. Read the completed-state sections of both migration plans first.

The original request below is retained as historical context, not current
execution authorization. A future cutover requires a new explicit request.

## Historical completed request

# Continue sanitized repository migration

Continue from the isolated worktree `~/linux-config/.worktrees/migrate-sanitized-repo` on `feat/migrate-sanitized-repo`. Finish the already implemented migration after confirming other sessions have stopped writing to the original active checkout. Read `plans/migrate-sanitized-repo.md` and `plans/migrate-sanitized-repo-progress.md`, inspect current dirty state, and preserve all unrelated work. Review newly arrived edits, rebuild the private hash-bound transfer manifest, run focused synthetic checks, preview, then run the authorized cutover using `scripts/executable_migrate-ai-cli-workflow --apply --review` with the private manifest. Keep the active checkout at `~/linux-config`. Preserve the old repository and linked worktrees privately; never import its Git history. Verify in the replacement working directory, including fresh fish refresh and separate pending/history audits. Do not commit, push, delete recovery material, rewrite history, or rotate credentials. Stop if concurrent writers remain or expected state changes.
