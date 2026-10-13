---
name: commit-session
description: Commit and push only the git changes dirtied during the current Codex session, while leaving pre-existing dirty work from other sessions uncommitted. Use when I say `commit-session`, `commit session`, `ship this session`, `commit only this Codex session`, or explicitly ask to avoid committing pre-existing or other-session dirty changes. Do not use for commit planning only, all-dirty shipping, history rewrites, or work outside Git.
disable-model-invocation: true
---

# Commit Session

Commit and push the work attributable to the current Codex session. Establish
that scope from the initial Git state and observed edits, review and check the
eligible changes, then commit, push, and report what remains.

Use this skill for explicit write requests that should ship only the files dirtied during the current Codex session. Treat the pre-write dirty baseline as the primary safety boundary, with an observed-touch fallback when session metadata or helper evidence is unavailable. Prioritize files touched during the current session and favor including safe related files over omitting them within session scope.

## Required Workflow

1. Confirm the current directory is a git repository and identify the active branch and upstream.
2. Read `CODEX_THREAD_ID` when available. Missing thread metadata does not block directly evidenced current-session changes.
3. Run the scope helper before staging anything:
   - `git rev-parse --show-toplevel`
   - `python3 dot_agents/skills/commit-session/scripts/session_scope.py --repo-root <repo-root>`
4. Inspect the helper output.
   - Use `commitable` as the initial candidate set. If the helper fails, is unavailable, or returns `unsafe` or `empty`, record the reason and build a fallback from successful edits and writes directly observed in the active conversation.
   - Review dirty matching plans, docs, tests, and companion files against the baseline and observed writes; include all with current-session attribution. Do not infer ownership solely from timestamps.
   - Report no eligible changes only after both helper evidence and direct write evidence have been considered.
5. Review diffs for the helper candidates and directly evidenced fallback files.
   - `commitable` can include directly observed edits, including files that were already dirty at the session baseline, and files that became dirty after the session baseline.
   - For mixed files, include separable current-session hunks and leave unrelated hunks untouched. Exclude suspicious content while continuing with other eligible files. Directly touching a baseline-dirty file makes it a priority for review, not blanket authorization for unrelated hunks.
6. Run the smallest relevant automated checks for the scoped change.
   - Record failed focused validation as a warning and continue to staging.
7. Run the `readme-recruiter-sync` skill check against the root `README.md`.
   For a shell-only path, run `./scripts/executable_readme-recruiter-sync`.
   - If the gate passes without README changes, continue.
   - If it fails, repair only truthful, repo-supported README issues before staging.
   - Re-run the scope helper after the repair. If it omits a directly observed repair, include that repair through the direct-write fallback. If unrelated README hunks cannot be separated safely, report the omitted repair and commit the remaining eligible work.
   - Re-run the gate after the repair. Record any remaining failure as a warning and continue to staging.
8. Stage the reviewed eligible paths or hunks from the helper and direct-write fallback. Keep pre-existing staged work outside scope out of the commit without discarding it; inspect the exact staged diff before committing.
9. Write the commit message.
   - Use a concise Conventional Commit subject line.
   - Keep the body minimal, using only as many concrete bullets as needed.
10. Create the commit. If it fails, repair a recoverable staging or command issue and retry the eligible subset. Report persistent failures; preserve uncommitted work and never bypass hooks.
11. Push to the configured upstream.
    - Attempt one upstream push after the local commit or complete commit series and best-effort checks, unless the user explicitly requests another cadence. Report failed checks and push failures accurately.
    - If no upstream exists or the push target is unclear, keep the local commit and report the missing target. Report push failures without undoing safe commits.
    - Do not amend, rebase, squash, or force-push unless the user explicitly asks.
12. Report the result with the validation performed, commit SHA, push target, skipped files, and remaining worktree state.

## Guardrails

- Treat `skipped_preexisting` and `skipped_unknown` as excluded by default; directly observed current-session edits or repairs can establish eligibility for their scoped hunks. Leave every unattributed hunk out.
- Never skip `readme-recruiter-sync` because the scoped diff looks small; repair its truthful findings before committing.
- Never invent README claims, flags, install steps, or recruiter copy that the repo does not support.
- Do not skip a safe scoped commit solely because best-effort validation fails.
- Do not skip a safe scoped commit after all truthful README repairs have been made solely because the rerun gate still reports a non-safety failure.
- Never leave a verified single-commit session workflow unpushed unless the user explicitly requests another cadence.
- If the helper cannot find a pre-write `git status --short` baseline for the session, only directly observed touched files are eligible; leave every other dirty file out of scope instead of reconstructing ownership from timestamps or memory.
- If a file was already dirty at the session baseline and the current session did not directly touch it, leave the file uncommitted unless the user explicitly asks for a manual split.
- Review newly eligible generated or companion files before staging them; baseline-delta scoping is intentionally permissive, not blind.
- Never bundle unrelated dirty changes just because they happen to be present in the same repository.
- Never stage secrets, credentials, caches, build output, or machine-local files unless they clearly belong in version control.

## Scope Helper

Use `scripts/session_scope.py` to compute the session file set from:

- the current session id from `CODEX_THREAD_ID`
- the matching Codex session log under `~/.codex/sessions/`
- successful `apply_patch` edits and known scaffold writes from the current session
- successful in-repo commands from the current session that are not on the helper's read-only allowlist
- the latest successful `git status --short` captured before the first repo write in that session
- the current repository dirty state

The helper returns JSON with:

- `commitable`: files directly touched in the current session or files that were clean at the session baseline and are dirty now, with an `ownership_reason` of `observed_touch` or `newly_dirty_since_baseline`
- `skipped_preexisting`: files that were already dirty before this session started writing and were not directly touched in the current session
- `skipped_unknown`: compatibility bucket for dirty files the helper still cannot classify safely, including unattributed dirties in a missing-baseline session where only observed touches are safe to ship
- `unsafe_reason`: why helper attribution is unavailable; review direct-write evidence before deciding that no eligible scope exists

## Output Contract

After a successful run, report:

- the final commit subject and short SHA
- the session id used for scoping, or the direct-write fallback used
- the validation commands or manual checks that were run
- the branch and push destination
- which files or hunks were committed, with helper `ownership_reason` or direct-write fallback evidence
- which files were left dirty from `skipped_preexisting` and `skipped_unknown`
- whether the worktree is now clean or what still remains dirty
