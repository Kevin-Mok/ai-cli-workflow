# Canonical Codex Instructions

This is the canonical Codex instruction document for
`/home/example/linux-config`. Root-level AGENTS files are routing shims; they
must not duplicate or weaken this policy. Historical merge provenance lives in
`docs/ai-workflow-optimization.md`.

## Mandatory Conditional Procedures

Reconcile the live task title before substantive work, updates and final responses. For title-tool discovery or changes, MUST read [task titles](references/task-titles.md).
Before product, platform, UI, AI-workflow, lineage or education work, MUST read [system-design routing](references/system-design.md).
On a bug or unexpected task failure, before retrying or changing a postmortem, MUST read [failure learning](references/postmortems.md) and record the living incident immediately.
Runnable commands remain standalone raw fish lines. Before CLI/script output, manual commands or shell-helper changes, MUST read [CLI and shell rules](references/cli-and-shell.md), including wrapped-copy verification.
For personal-context, project/session context, capture/resume/closeout, or development/design choices with personal or cross-project relevance, MUST read [conditional memory](references/session-memory.md); keep private context external.
Before docs, README, manual checks, configuration, commits or pushes, MUST read [documentation and configuration](references/documentation-and-config.md).
Before any repo creation, commit, push, merge or task handoff, MUST read [delivery and handoff](references/delivery.md); authorization and cadence govern.

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
- When a local managed file is newer than its repository source, always copy
  its changes into this repo before applying configuration. Compare modification
  times and review the diff; preserve templates and unrelated repo edits when
  merging. Keep secrets and machine-local data outside tracked source.
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
- For work spanning sessions, use the `context-handoff` skill (brief,
  `/goal`, `evidence-reviewer` pass, `progress.md` handoff).
  Commit matching plan updates in the same change as the work they describe.
- Before browser automation or Playwright commands, use the `playwright` skill.
- Use `grok-cli-handoff` for remote-assistant delegation to local CLI; verify authorization, checkout evidence and STOP.
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

## Documentation And Repo Surfaces

Before adding a skill or an AGENTS.md rule, run the `lean-instructions` gate. Add it only on PASS, and record the verdict. Adding or removing a skill updates `vetted-skills.md` in the same commit.
- Documentation is part of the implementation. Update behavior, setup, usage,
  test instructions, known risks, and relevant plans in the same change.
- When asked to create a prompt, write it to a concise kebab-case Markdown file
  under `prompts/`, not only in chat.

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

## Git And Delivery

- Any file larger than 3 MB must be committed using Git LFS. Configure its
  Git LFS tracking in `.gitattributes` before staging it, and commit the
  matching `.gitattributes` change with the file.
- Keep commits focused and chronologically ordered from oldest prerequisite to
  newest follow-up. Use concise Conventional Commit subjects and minimal bodies
  with only concrete bullets.
- Keep relevant documentation and ExecPlan updates in the same commit as their
  implementation. Stage only intended files or hunks and inspect the staged diff
  before committing.
- Push the configured upstream only when the target is clear. Do not amend,
  rebase, squash, reset, force-push, or rewrite history unless explicitly asked.

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
- Delegate repo search/file mapping to the `search` agent, test runs to `tests`, and API/library doc lookups to `docs` (see `~/.codex/agents/`).
