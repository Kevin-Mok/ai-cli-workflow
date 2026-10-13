---
name: commit-dirty
description: Use when I explicitly want the current intended dirty git worktree committed and pushed now, including requests like `commit dirty`, `commit all dirty`, `commit and push this`, or `ship these changes`, after verifying scope and running the minimum relevant checks. Do not use for commit planning only, history rewrites, force-pushes, or work outside Git.
disable-model-invocation: true
---

# Commit Dirty

Commit and push the authorized dirty work in a repository. Review the scope
and diffs, run relevant checks and the README gate, then commit eligible
changes, attempt the push, and report any remaining work.

Use this skill for explicit write requests to create a real git commit and push it from the current repository, including the "commit dirty" and "commit all dirty" cases where the intended scope is the current dirty worktree. Make a best-effort commit of every eligible change within the requested scope. Prioritize files touched during the current session and favor including safe related files over omitting them.

## Required Workflow

1. Confirm the current directory is a git repository and identify the active branch and upstream.
2. Inspect `git status`, changed files, and relevant diffs before staging anything.
3. Decide whether the worktree is safe to ship as requested.
   - If the changes are coherent, continue.
   - Classify mixed changes and exclude unsafe or out-of-scope paths or hunks; continue with the eligible subset. An explicit all-dirty request includes every safe, reviewable dirty change.
   - Include matching plans, documentation, tests, and companion files. Prioritize session-touched files when scope must be narrowed.
4. Verify the change.
   - Run the smallest relevant automated checks.
   - Add or run a failing reproducer first for bug fixes when practical.
   - Record failed or unavailable checks as warnings and continue with eligible files; never claim they passed.
5. Run the `readme-recruiter-sync` skill check against the root `README.md`.
   For a shell-only path, run `./scripts/executable_readme-recruiter-sync`.
   - Treat the gate as mandatory before staging or committing.
   - If the README is stale or missing required install or bootstrap, usage, core command flag, repo-based tech stack rationale, or recruiter-facing coverage, update it in the same change before continuing.
   - If a repair cannot be safely separated, leave that repair as a reported residual and commit the remaining eligible work. Non-safety README findings do not block delivery.
6. Stage only the intended files or hunks, including `README.md` when the gate required it.
7. Write the commit message.
   - Use a concise Conventional Commit subject line.
   - Keep the body minimal, using only as many concrete bullets as needed.
8. Create the commit. If it fails, repair a recoverable staging or command issue and retry the eligible subset. Report persistent failures; preserve uncommitted work and never bypass hooks.
9. Push the branch.
   - Attempt one upstream push after the local commit or complete commit series and best-effort checks, unless the user explicitly requests another cadence. Report failed checks and push failures accurately.
   - Push to the configured upstream by default.
   - If no upstream exists or the target remote is unclear, keep the local commit and report that pushing needs a known target. A push failure does not undo a commit.
   - Do not amend, rebase, squash, or force-push unless the user explicitly asks.
10. Report the result with the validation performed, commit SHA, push target, and remaining worktree state.

## Guardrails

- Treat `commit all dirty` as authorization to include every safe, reviewable dirty change. For narrower requests, exclude unrelated work.
- Do not use this skill when the task is only to plan commits or group dirty changes without writing. Use `commit-plan` for that case.
- Do not use this skill when the user explicitly wants to ship only the current Codex session's changes. Use `commit-session` for that case.
- Never bypass `readme-recruiter-sync` because the code diff looks small.
- Never invent README claims, flags, install steps, or recruiter copy that the repo does not support.
- Never leave a verified single-commit workflow unpushed unless the user explicitly requests another cadence.
- Keep all eligible changes in the requested single commit; do not widen a narrower request to unrelated work.
- Never stage secrets, credentials, caches, build output, or machine-local files unless they clearly belong in version control.
- Respect pre-existing user changes. Do not revert or discard work you did not make.
- Before creating a commit, isolate its index contents from pre-existing staged work outside scope without discarding that work; inspect the exact staged diff.
- Attempt a commit whenever an eligible subset exists. Report empty scope, excluded paths, commit failures, and push failures accurately; never bypass hooks or rewrite history to force success.

## Output Contract

After a successful run, report:

- the final commit subject and short SHA
- the validation commands or manual checks that were run
- the branch and push destination
- whether the worktree is now clean or what still remains dirty
