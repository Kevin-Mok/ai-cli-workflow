---
name: commit-plan-push
description: Use when planning dirty Git commits (`commit-plan`) or explicitly asked to plan, commit, and push or split and ship changes. Planning-only stays read-only.
disable-model-invocation: true
---

# Commit Plan Push

Plan the current dirty worktree into coherent oldest-to-newest commits.
Choose the mode from the user's request. Planning-only stays read-only;
execution requires an explicit request to create commits and push. A skill name
or proposed command alone never expands that authorization.

Prioritize files touched during the current session and favor including safe related files over omitting them. Cover the full requested worktree, including reviewable companion files; touched-file priority must not invert prerequisite chronology.

## Planning-only mode

Use for `commit-plan`, `commit plan`, `plan to commit all dirty`, grouping dirty
changes into commits, or a safe plan without execution. This mode performs
**no Git writes**. Do not stage, commit, push, restore, reset, stash, clean, or
change files, index state or history. An explicit execution request selects the
delivery workflow below instead; uncertainty stays read-only.

Inspect the repository, branch, status, all staged/unstaged/untracked diffs,
history and related files. Plan every safe, reviewable group oldest-to-newest;
preserve prerequisite chronology and explain ambiguity. Identify secrets,
credentials, caches, generated files, risky binaries and ownership questions as
exclusions. Review README impact without applying repairs. Keep companion
plans, docs, tests and postmortems with the matching implementation. Treat
ordinary validation and README findings as warnings for later execution.

Then return: working-tree summary; numbered commit groups with purpose, files,
rationale, README impact and concise Conventional Commit subjects/minimal
concrete bodies; risks and exclusions; optional manual commands in chronology;
and a final subject-only message summary. Recommend the smallest checks for
later execution and **return before the delivery workflow**.

Single-commit workflows push after the commit passes verification; multi-commit workflows push once after the complete verified series, unless the user explicitly requests another cadence.

## Required Workflow

1. Confirm the directory is a Git repository; identify the branch, upstream,
   and current `git status --short` before any write.
2. Inspect every staged, unstaged, deleted, renamed, and untracked change with
   the relevant diffs, file history, plans, and related documentation.
3. Infer the smallest coherent commit series in chronological order. Keep each
   matching implementation, plan, smoke-test, postmortem, and README update in
   the commit it describes. Cover every safe, reviewable change, even when the
   worktree contains multiple unrelated groups.
4. Classify each change. Do not stop for ordinary mixed or ambiguous changes:
   isolate them into separate commits when the file-level boundary is clear,
   and leave only genuinely unsafe or unreviewable items as reported residuals.
   Never stage secrets, credentials, caches, generated output, machine-local
   files, or content whose ownership and intent cannot be safely established.
5. Identify and run the smallest relevant checks before staging. For a bug
   fix, require a failing reproducer or test first when practical. If a check
   fails, record it as a warning, continue with independent safe groups, and
   continue attempting the affected reviewable group as well when the failure is non-safety; never claim that failed validation passed.
6. Run the `readme-recruiter-sync` skill check against the root `README.md`.
   For a shell-only path, run `./scripts/executable_readme-recruiter-sync`.
   Update the README in its matching commit when required. If the gate reports
   a warning or a README change cannot be safely separated from unrelated
   edits, record the issue and continue delivering independent safe groups.
7. For each planned commit, in oldest-to-newest order:
   - stage only its intended files or hunks, keeping pre-existing staged work outside that group out of the commit without discarding it;
   - inspect the staged diff and confirm no secrets, credentials, caches,
     generated output, or machine-local files were included;
   - create a concise Conventional Commit-style subject with a minimal body of
     concrete bullets; and
   - record its short SHA and run any commit-specific validation that the
     change requires. If one commit fails, record the failure and continue with
     independent safe groups whenever possible.
8. Always make a best-effort delivery attempt. After the planned groups, rerun
   status and make another safe commit attempt for any remaining reviewable
   change. Do not claim a clean worktree if prohibited or unresolved residuals
   remain.
9. Attempt one push to the configured upstream after the complete best-effort
   series, not after intermediate commits. If the upstream is absent, unclear,
   rejected, or non-fast-forward, report the condition without rewriting
   history; safe local commits still stand.
10. Report the final commit subjects and short SHAs, validation evidence and
    warnings, branch and push destination, and every residual path with its
    reason.

## Guardrails

- In execution mode, treat this as permission to execute a safe inferred commit plan across the
  whole dirty worktree, not as permission to bundle unrelated work into one
  commit for speed.
- Respect pre-existing user changes. Never discard, overwrite, stage, or bundle
  work outside the requested and verified scope. Best effort means shipping
  safe, reviewable groups—not guessing about ownership or intent.
- For planning only, use the read-only mode above and stop before delivery.
- Do not use it when the user explicitly wants one current dirty-worktree
  commit; use `commit-dirty` instead.
- Do not use it for current-session-only work; use `commit-session` instead.
- Never bypass the README gate because a diff looks small. A gate warning is a
  reported delivery risk, not a reason to abandon unrelated safe commits.
- Never invent README claims, commands, install steps, or recruiter copy.
- Do not amend, rebase, squash, reset, force-push, or rewrite history unless
  the user explicitly asks.
- Never leave a completed best-effort series unpushed unless the user explicitly
  requests another cadence; if push fails, report the exact failure.

## Output Contract

After a successful run, report:

- the final commit subjects and short SHAs in execution order;
- the validation commands or manual checks that ran, including warnings and
  failures that did not block independent delivery;
- the branch and push destination; and
- the remaining worktree state, including every residual path and why it was
  not shipped.

## Public privacy gate

Immediately before every commit attempt, run
`python3 scripts/executable_privacy-gate check` from the repository root,
using the same `GIT_INDEX_FILE` when committing an isolated candidate. Treat
findings and scanner errors as blocking safety failures; repair and restage the
candidate before retrying. Preserve the active Git hooks. Plumbing commits must
pass the exact immutable tree OID with `--tree OID` to the same shared gate.
See the root README privacy-gate section for activation, private rules and limits.
