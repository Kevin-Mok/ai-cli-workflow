# Delivery

Read this procedure when its mandatory canonical AGENTS trigger applies. Follow
the preserved rules below before acting; active user/developer instructions govern.

- When asked to create a new GitHub repository, also configure it as the current
  working repository's `origin` unless another remote is specified, and verify
  its fetch/push URLs. Keep the current checkout; explain any filesystem
  restriction before substituting a separate checkout.

- Authorized commit workflows make best-effort commits of every eligible change.
  Prioritize session-touched files and favor including safe related files over
  omitting them within the requested scope. Ordinary validation, README, or
  scope-helper problems are warnings: use direct-write evidence when needed,
  exclude only unsafe or unattributed hunks, and continue with eligible work.
  Missing upstream or push failure leaves local commits intact. Planning-only
  requests remain read-only; secrets and unrelated-work exclusions still apply.
- For commit delivery, follow [Handoff Format](#handoff-format). Include the
  verified commit hash and actual push status (remote and branch) in **Verified**.
  Include `Full commit message:` with the recorded Conventional Commit subject
  and any body in **Implemented**. State failed or unperformed pushes accurately.
- After each commit, promptly report the result in Codex output with a high-level
  overview of where the task stands: completed work, verified results, remaining
  work, blockers (or none), and the next step. Maintain the same overview in the
  active plan, or `docs/task-status.md` when no plan exists, retaining prior commit
  milestones. Update the document before committing and include it with the
  related work; identify the milestone by subject or sequence, then report the
  resulting commit hash in Codex output. Link the status document in the response.
- Use [Handoff Format](#handoff-format) for each commit overview and push result:
  commentary for intermediate milestones and the final response for delivery.
  Preserve the configured push cadence.
- Single-commit workflows push after the commit passes verification; multi-commit workflows push once after the complete verified series, unless the user explicitly requests another cadence.
- After pushing a web-app commit, attempt a Vercel deployment when the project
  is configured for Vercel, then provide the deployed URL. If deployment cannot
  complete, report the failure and its cause clearly.
- If an explicitly requested worktree is merged, push `main` after the merge
  succeeds.

### Handoff Format

For every task-completion handoff, with or without a commit or push, use this
visible order. Keep the commands together in execution order and outside
`<details>` or other collapsed sections.

1. **Three direct verification commands:** start with exactly 3 concrete,
   copy-pasteable commands. State the working directory and whether sudo is
   needed before them. Immediately after each command, give its own labeled
   **Expected:** output block; include relevant manual actions before the
   command that needs them.
2. **Verified:** report observed checks and results, link evidence or the plan,
   and state unverified behavior, skipped checks and material risks. Distinguish
   previous-run results from checks run in this turn.
3. **Use:** give the user's usage or restore instructions and relevant
   persistence behavior.
4. **Implemented:** summarize what changed. State commit/push status when
   relevant. Keep this summary last.

Commands must exercise the completed behavior through the actual CLI, app, API
or delivered artifact, including relevant edge cases. For non-executable work,
use relevant artifact or workflow commands. Automated tests, linters, type
checks, builds, Git hygiene checks and source-text searches do not count; run
required checks before completion and summarize their results in **Verified**.
Use task-relevant commands rather than invented behavior or unrelated padding.
Follow the runnable-command presentation rules: raw one-line fish commands at
column zero; expected output uses separate language-tagged fenced blocks.
For silent success, write "No output; exit status 0." Mark variable values as
placeholders and label examples as expected rather than observed. Prefer
existing reusable scripts and documented commands that directly exercise the
result. Do not wait for the user to ask for the three commands.
- For coding-task handoff, include the atomic plan, a paste-ready Cursor prompt,
  exact automated and manual test plan, docs updates, a Conventional Commit
  suggestion, and any additional validation notes.
