# Canonical Codex Instructions

This is the canonical Codex instruction document for
`/home/example/linux-config`. Root-level AGENTS files are routing shims; they
must not duplicate or weaken this policy. Historical merge provenance lives in
`docs/ai-workflow-optimization.md`.

## Authority And Required Context

Apply guidance in this order:

1. Active user and developer instructions.
2. This file.
3. Nested `AGENTS.md` files that add stricter local constraints.
4. Untracked `AGENTS.override.local.md` strict additions.

Lower layers may specialize but never relax higher-layer safety or quality.
Before changing files, read the relevant source, active plan, roadmap or docs,
the canonical `feedback.log` when durable preferences may apply, and relevant
`tasks/lessons.md` entries. Follow existing patterns rather than assumptions.

### System Design Routing

For ExampleProject-style product, platform, UI, AI-workflow, source-lineage, or
education work:

- Read `~/.agents/system-design/architecture.md` for platform architecture,
  hosting, tenancy, data flow, AI validation, sources, assignments, analytics,
  security, observability, or CI/CD.
- Read `~/.agents/system-design/coding-standards.md` before implementing
  apps, APIs, databases, frontends, AI workflows, tests, security, reviews, or
  documentation.
- Read `~/.agents/system-design/ui-design.md` before all UI work.
- When the topic applies, read `~/.agents/system-design/knowledge-base.md`,
  `~/.agents/system-design/student-practice-packages.md`,
  `~/.agents/system-design/trusted-sources.md`, or
  `~/.agents/system-design/business-strategy.md`.

## Scope, Safety, And Clarity

- Do not break production behavior unless explicitly asked. Prefer small, safe, reversible changes and minimal diffs.
- Preserve pre-existing user work. Before the first modifying command in a Git
  repo, capture `git status --short`. Never discard, overwrite, stage, or
  bundle unrelated changes.
- Touch only what the task needs. Do not remove comments, files, or apparently
  dead code without understanding ownership and external callers; ask before
  deleting ambiguous leftovers.
- Never stage secrets, credentials, caches, generated output, or machine-local
  files unless they clearly belong in version control.
- Surface assumptions before implementation. If conflicting evidence or a
  missing choice could materially change the result, stop, name the conflict,
  and ask. Push back directly on unsafe or unsound approaches and propose a
  concrete alternative.
- Do not suggest, create, or use a Git worktree unless the user explicitly asks for one. When requested, create it under the repository's `.worktrees/`
  directory and switch into its branch before continuing.

## Planning And Coordination

- Use Plan Mode for non-trivial work: three or more steps, multiple files, or an
  architecture decision. Create and maintain `plans/<task-slug>.md` according
  to `.agent/PLANS.md`.
- Make plans decision-complete: record scope, assumptions, checkboxes, risks,
  verification evidence, and review notes. Keep progress current while working.
  Commit matching plan updates in the same change as the work they describe.
- A small task may use a short inline plan. If evidence invalidates any plan,
  stop and revise it before continuing.
- Use focused subagents when two or more independent tasks can proceed in
  parallel or a non-trivial bug benefits from separate root-cause analysis.
  Give each agent one bounded task and independently verify its report.

## Bugs, Tests, And Implementation

- Start every bug fix with a failing test or executable reproducer. Confirm it
  fails for the expected reason before implementing. If automation is
  impractical, explain why and create the closest reliable reproducer.
- For non-trivial bugs, use subagents for independent investigation or candidate
  fixes when useful. A bug is fixed only when the reproducer passes and relevant
  regression checks remain green.
- For features, fixes, and behavior changes, write the defining test first,
  observe RED, implement the minimum GREEN change, then refactor without losing
  coverage. Tests are the specification; do not weaken them to fit an
  implementation.
- Prefer the simplest correct implementation. Optimize only after correctness is
  demonstrated. Match surrounding conventions, favor readable explicit code,
  and avoid hypothetical abstractions.
- In typed code, define public types in the established location, avoid
  unbounded `any`, and run the type checker. Validate persisted data on load,
  handle schema drift, and fail with actionable errors and logs.
- Keep modules cohesive. Split files that cross multiple concerns or grow beyond
  roughly 1,000 lines; avoid adding features to an already oversized file
  without organizing it.
- When a user must run commands manually, create a reusable script instead of a
  chat-only command list. State when it requires `sudo` and provide the exact
  invocation.

## Documentation And Repo Surfaces

- Start every how-to or procedural document with a short, plain-language
  overview directly below the title. Explain what the document helps the
  reader accomplish and summarize the main steps before detailed instructions
  or commands. Keep it direct and easy to understand.
- Documentation is part of the implementation. Update behavior, setup, usage,
  test instructions, known risks, and relevant plans in the same change.
- Treat root `README.md` as the public operating surface. When instructions,
  config, skills, plans, onboarding, or documented commands change, keep it
  accurate. Preserve its technical-deep order: recruiter hook, hero, stack
  rationale, navigation, AI proof, then setup and broader dotfiles detail.
- Before staging or finalizing any commit or push workflow, run the
  `readme-recruiter-sync` skill (or
  `./scripts/executable_readme-recruiter-sync`). The gate requires truthful
  install/bootstrap, day-to-day use, documented command options, repo-grounded
  tech-stack rationale, and recruiter value. Include safely separable README
  repairs; report remaining findings without blocking eligible commits.
- When a reusable manual check appears or changes, update
  `docs/smoke-tests.md` in the same change. Use grouped `Action` and
  `Expected` entries; update stale checks rather than duplicating them.
- When a user asks for clarification because a smoke test or documented
  procedure is unclear, update `docs/smoke-tests.md` or the relevant
  document in the same change; do not leave the clarification only in chat.
- For every unexpected task failure—an unplanned unsuccessful command, test, deployment, or workflow outcome—immediately create a dated, descriptive postmortem under `docs/postmortem/`. Record the symptom, impact, evidence, current status, and next steps; keep that same document current throughout investigation. When the issue is fixed, update it with root cause, resolution, verification, and follow-up, and keep the completed postmortem in the same commit as the related fix. Deliberately failing TDD RED tests and intentionally exercised failure paths do not trigger a postmortem.
- When asked to create a prompt, write it to a concise kebab-case Markdown file
  under `prompts/`, not only in chat.
- After every tracked configuration change, run `refresh-config` before completion
  unless explicitly told not to; this applies to every change, not only environment
  behavior changes. The helper
  snapshots live `~/.codex/config.toml` into tracked
  `dot_codex/config.toml`, applies chezmoi, regenerates shortcuts, and reloads
  fish; do not describe it as repo-to-home-only sync.

## Feedback And Lessons

- Use `dot_agents/skills/feedback-memory/feedback.log` as the canonical
  append-only log for durable cross-task user preferences. Never rewrite,
  reorder, deduplicate, or reconcile old entries.
- Personal-context conversations and their life-derived learnings belong only
  in the external private store described below, including communication or
  workflow preferences learned there; do not mirror them into tracked feedback.
- Record a repo-specific failure pattern or correction in
  `tasks/lessons.md`; create it if missing. Do not copy the same note into both
  files: durable user preference belongs in `feedback.log`, while a local
  engineering lesson belongs in `tasks/lessons.md`.
- Apply the newest applicable durable preference when an older historical entry
  conflicts with it.

### Conditional Session Memory

- Use `personal-context` only when explicitly invoked for a discussion that
  learns about example-user to improve development and design choices. Its private
  source and structured memory stay in `/home/example/coding/personal-context`.
  Ordinary coding requests do not activate it, including through other skills.
  Keep its conversations and learnings out of repository artifacts, Second Brain,
  Graphiti, and other services; do not start session capture from this invocation.
- Use the `second-brain-session` skill for established project/session
  context, explicit session capture, a ExampleProject daily outcome, or natural-end
  closeout. Keep its detailed procedure in the skill instead of loading the
  entire vault into standing instructions. A personal-context discussion alone
  does not activate its capture, focus, reminders, or closeout workflows.

## Git And Delivery

- Authorized commit workflows make best-effort commits of every eligible change.
  Prioritize session-touched files and favor including safe related files over
  omitting them within the requested scope. Ordinary validation, README, or
  scope-helper problems are warnings: use direct-write evidence when needed,
  exclude only unsafe or unattributed hunks, and continue with eligible work.
  Missing upstream or push failure leaves local commits intact. Planning-only
  requests remain read-only; secrets and unrelated-work exclusions still apply.

- Keep commits focused and chronologically ordered from oldest prerequisite to
  newest follow-up. Use concise Conventional Commit subjects and minimal bodies
  with only concrete bullets.
- Keep relevant documentation and ExecPlan updates in the same commit as their
  implementation. Stage only intended files or hunks and inspect the staged diff
  before committing.
- Single-commit workflows push after the commit passes verification; multi-commit workflows push once after the complete verified series, unless the user explicitly requests another cadence.
- Push the configured upstream only when the target is clear. Do not amend,
  rebase, squash, reset, force-push, or rewrite history unless explicitly asked.
- After pushing a web-app commit, attempt a Vercel deployment when the project
  is configured for Vercel, then provide the deployed URL. If deployment cannot
  complete, report the failure and its cause clearly.
- If an explicitly requested worktree is merged, push `main` after the merge
  succeeds.

## Verification And Completion

- Evidence precedes every completion claim. Identify the command or observable
  result that proves each requirement, run it fresh, read the complete output
  and exit status, and report the actual result.
- Run the focused regression test plus relevant broader tests, type checks,
  builds, linters, logs, diffs, and manual/runtime checks in proportion to risk.
  A passing partial check does not prove an untested surface.
- Compare behavior before and after when relevant. Confirm documentation and
  plans match the final implementation, and record exact verification evidence
  and unresolved risks.
- Before committing, check that another engineer can reproduce the result,
  review the rollback path, and ask whether the solution remains the simplest
  robust option.
- For coding-task handoff, include the atomic plan, a paste-ready Cursor prompt,
  exact automated and manual test plan, docs updates, a Conventional Commit
  suggestion, and any additional validation notes.
