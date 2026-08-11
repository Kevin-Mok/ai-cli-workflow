---
name: commit-plan-push
description: Use when I explicitly want the current dirty Git worktree planned into coherent commits, committed, and pushed now, including requests like `commit-plan-push`, “plan, commit, and push all dirty work,” or “split and ship these changes.” Do not use for planning only, a single forced dirty commit, history rewrites, or ambiguous mixed diffs.
---

# Commit Plan Push

Use this skill for an explicit request to plan the current intended dirty
worktree, create the safe commit series immediately, and push it. Treat the
inferred commit plan as a delivery contract: execute it oldest-to-newest unless
new evidence makes the series unsafe.

## Required Workflow

1. Confirm the directory is a Git repository; identify the branch, upstream,
   and current `git status --short` before any write.
2. Inspect every staged, unstaged, deleted, renamed, and untracked change with
   the relevant diffs, file history, plans, and related documentation.
3. Infer the smallest coherent commit series in chronological order. Keep each
   matching implementation, plan, smoke-test, postmortem, and README update in
   the commit it describes.
4. Decide whether the worktree is safe to ship. If the changes are unrelated, suspicious, or cannot be split safely, stop and ask one short clarification instead of guessing.
5. Identify and run the smallest relevant checks before staging. For a bug
   fix, require a failing reproducer or test first when practical; do not ship
   failing or unverified work.
6. Run the `readme-recruiter-sync` skill check against the root `README.md`.
   For a shell-only path, run `./scripts/executable_readme-recruiter-sync`.
   Update the README in its matching commit when required. If doing so would
   mix unrelated dirty README work, stop and ask.
7. For each planned commit, in oldest-to-newest order:
   - stage only its intended files or hunks;
   - inspect the staged diff and confirm no secrets, credentials, caches,
     generated output, or machine-local files were included;
   - create a concise Conventional Commit-style subject with a minimal body of
     concrete bullets; and
   - record its short SHA and run any commit-specific validation that the
     change requires.
8. Confirm the whole series is verified and the upstream target is clear.
   Push the configured upstream once after the full verified series succeeds;
   do not push intermediate commits unless the user explicitly requested that
   cadence. If the upstream is absent, unclear, rejected, or non-fast-forward,
   stop and report the condition without rewriting history.
9. Report the final commit subjects and short SHAs, validation evidence, branch
   and push destination, plus whether the worktree is clean or what remains.

## Guardrails

- Treat this as permission to execute a safe inferred commit plan, not as
  permission to bundle unrelated work for speed.
- Respect pre-existing user changes. Never discard, overwrite, stage, or bundle
  work outside the requested and verified scope.
- Do not use this skill for planning only; use `commit-plan` instead.
- Do not use it when the user explicitly wants one current dirty-worktree
  commit; use `commit-dirty` instead.
- Do not use it for current-session-only work; use `commit-session` instead.
- Never bypass the README gate because a diff looks small.
- Never invent README claims, commands, install steps, or recruiter copy.
- Do not amend, rebase, squash, reset, force-push, or rewrite history unless
  the user explicitly asks.
- Never leave a completed verified series unpushed unless the user explicitly
  requests another cadence.

## Output Contract

After a successful run, report:

- the final commit subjects and short SHAs in execution order;
- the validation commands or manual checks that ran;
- the branch and push destination; and
- the remaining worktree state.
