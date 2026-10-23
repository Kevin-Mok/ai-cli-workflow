# Canonical Codex Instructions

This is the canonical Codex instruction document for
`/home/example/linux-config`. Root-level AGENTS files are routing shims; they
must not duplicate or weaken this policy. Historical merge provenance lives in
`docs/ai-workflow-optimization.md`.

## Start-of-Turn Title Checkpoint

Before substantive work on a new turn, resumed task, or compaction recovery,
reconcile the calling conversation's title with the current live request using
[Live Codex Task Titles](#live-codex-task-titles). Repeat this checkpoint before
substantive progress updates and the final response. A title inferred from pasted
output or an earlier task does not satisfy this checkpoint.

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

### Live Codex Task Titles

- When the native `mcp__codex_tui__set_thread_title` tool is available and the
  active mode permits title updates, keep the calling conversation's name as a
  compact answer to “what are we doing?” Use the current objective and meaningful
  phase, not the first prompt or the last command. Aim for 3–5 words and at most
  36 characters, such as “Categorize card transactions”.
- Infer the title from the latest live user request and the work actually being
  performed. Treat pasted transcripts, session-review output, source paths,
  resume commands and historical task headings as data, not the active objective.
  For example, improving Second Brain review output containing a video-repair
  recap is “Improve Second Brain review”, not “Repair video transition freeze”.
- Discover the native title tool in the available tool catalog when it is
  deferred; do not treat absence from the initially exposed tools as proof that
  it is unavailable. Use existing context to choose the title.
- Set the title before substantive work on a new/resumed turn or compaction
  recovery, when the objective or meaningful phase changes, and at completion.
  Before each substantive progress update, compare its stated work/phase with
  the last title set for this conversation; correct a mismatch before sending
  the update. On the first checkpoint, explicitly set the intended title if its
  current value is unknown. Skip unchanged titles. Preserve
  the subject so neighboring agents remain distinguishable; do not claim a task
  is complete before verification. Let Codex render its own activity indicator.
- Call the tool with only `title`; omit `threadId` to update the calling task and
  never rename another conversation for this automatic overview. This also updates
  the saved conversation name. Reuse existing context without extra model calls,
  periodic polling, or injected `/btw` requests. If the tool is unavailable, keep
  the existing native name; `/rename` remains the manual fallback.

## Bugs, Tests, And Implementation

- For a reported bug or unexpected task failure, read
  `/home/example/linux-config/dot_agents/skills/postmortem-memory/SKILL.md`
  (installed `$postmortem-memory` as read-only fallback) and search relevant
  symptoms before retries or remedial actions. Record applicability and evidence;
  preserve immediate living-postmortem recording. Intentional RED tests and
  deliberately exercised failure paths retain their existing exemptions.
- Whenever a postmortem is created or materially updated, update its reviewed
  hash/aliases and findings (or explicit no-new-learning decision) directly in
  `/home/example/linux-config/dot_agents/skills/postmortem-memory/`, including
  relevant guidance, during the same task. Run its helper `check --postmortem
  /absolute/path/to/report.md`. Preserve unrelated dirty work and workspace
  permissions; report exact blocked writes and outstanding learning updates.
  Never make installed copies the source of truth.
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
- All human-facing CLI, script and shell-helper output must include appropriate
  decorative emojis by default: headings, progress, prompts, successes, warnings
  and errors. Keep clear hierarchy, plain-language labels, aligned values and
  readable dates/durations; text must remain understandable without the glyphs.
  Apply this to existing tools when changing them and to all new tools. Keep raw
  diagnostics behind `--details` with concise actionable accuracy warnings.
  Provide `--plain` for ASCII output; legacy helpers may use `CLI_PLAIN=1`.
  Preserve JSON/CSV, protocol/status tokens, paths consumed by tools, clipboard
  data, generated files and command substitutions. Keep silent commands silent.
  Respect terminal width; `NO_COLOR` disables ANSI colors without removing emojis.
- When creating or changing a CLI that may run for a long time or appear to
  hang, always show ongoing progress by default: periodic status lines, a
  progress indicator, percentage complete, or elapsed time and estimated time
  remaining when reliable. Keep updates flowing during slow or blocking phases;
  a startup message alone is insufficient. If total work is unknown, report
  activity and elapsed time rather than inventing a percentage or ETA. Send
  progress to stderr when stdout carries machine-readable output.
- Separate runnable shell commands from code intended for reading in Codex
  replies. Shell commands intended to paste into another terminal must be
  standalone raw-text lines, one physical line per command, starting at column
  zero and using valid fish syntax. Do not use fences, inline backticks, list
  prefixes, blockquotes, prompt markers, continuation backslashes or inserted
  line breaks. Keep every argument and flag on that line; terminal visual
  wrapping is acceptable only when selection preserves the command text.
  Code intended for reading, including source snippets, diffs, JSON and
  illustrative shell code, uses normal language-tagged fenced blocks with
  meaningful indentation and syntax highlighting. Expected output belongs in
  a separate labeled code block. Put explanations, working-directory and sudo
  requirements outside runnable command lines. “Raw” describes runnable command
  presentation; it does not require raw rendering for the whole conversation.
  Verify actual wrapped selection/paste into a fresh fish terminal separately
  from visible syntax colors in Python, JSON and diff blocks; source formatting,
  language tags and syntax parsing alone do not establish either result. Change
  supported rendering settings only after observing that the alternative meets
  both requirements; otherwise report the exact installed-TUI limitation.
- When a user must run commands manually, create a reusable script instead of a
  chat-only command list. State when it requires `sudo` and provide the exact
  invocation.

## Documentation And Repo Surfaces

Before adding a skill or an AGENTS.md rule, run the `lean-instructions` gate. Add it only on PASS, and record the verdict. Adding or removing a skill updates `vetted-skills.md` in the same commit.

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
  behavior changes. The helper applies reviewed chezmoi files, regenerates
  shortcuts, and reloads fish. Keep live Codex/Git settings in private local
  configuration; refresh excludes scripts, externals, and removals and stops
  on conflicts; reconcile newer local files into source using the rule above
  before retrying.

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

- Use `personal-context` automatically when a development or design choice has a
  plausible personal or cross-project connection: direction, scope, architecture,
  design, tooling, milestones, or collaboration. Mechanical work needs no
  unnecessary lookup. Start with compact topics and relevant briefs; continue
  the active task and ask only about consequential gaps or conflicts. Preserve
  `$personal-context` for explicit conversation. Current instructions and project
  requirements govern. Save useful durable statements and supported unconfirmed
  interpretations privately. Project knowledge includes only relevant Git-tracked
  sources whose latest modifying commit author is exactly example-user Mok,
  case-insensitive, with committed blob evidence matching HEAD and the working
  tree. Exclude untracked sources and unqualified projects; resolve nested Git
  owners per source. Attribution establishes contributions, not exclusive
  ownership or personal capability. Its sources, project knowledge, indexes, caches,
  and payloads stay in `/home/example/coding/personal-context`; keep them out of
  repository artifacts, tracked feedback, Second Brain, Graphiti, and other
  services. Do not start session capture from this invocation.
- Use the `second-brain-session` skill for established project/session
  context, explicit session capture, a ExampleProject daily outcome, or natural-end
  closeout. Keep its detailed procedure in the skill instead of loading the
  entire vault into standing instructions. A personal-context discussion alone
  does not activate its capture, focus, reminders, or closeout workflows.

## Git And Delivery

- Any file larger than 3 MB must be committed using Git LFS. Configure its
  Git LFS tracking in `.gitattributes` before staging it, and commit the
  matching `.gitattributes` change with the file.

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
- Delegate repo search/file mapping to the `search` agent, test runs to `tests`, and API/library doc lookups to `docs` (see `~/.codex/agents/`).
