# KM's Four-Codex Operating Environment

A reproducible Linux workspace for AI-assisted engineering. This repo keeps
desktop settings, Codex instructions and defaults, reusable skills, public-safe
workflow code, and work plans under version control. Review the workflow, install the
prerequisites, preview and apply the configuration with `chezmoi`, then use
the daily commands and checks to keep the environment consistent.

For recruiters and AI-native engineers, the point is concrete: this
repo is a public artifact of how I structure leverage. It shows
planning before edits, small reversible diffs, reproducible setup,
durable context across sessions, and verification before claiming work
is done. Personal values and knowledge-vault contents are intentionally excluded.

## Tech Stack And Why Chosen

| Layer | Repo evidence | Why chosen |
| --- | --- | --- |
| `chezmoi` | [`dot_config/chezmoi/chezmoi-template.toml.tmpl`](dot_config/chezmoi/chezmoi-template.toml.tmpl) | Keeps the environment reproducible across machines instead of trapping setup inside one laptop. |
| Codex CLI and tracked config | [`dot_codex/config.toml`](dot_codex/config.toml) | Versions model, reasoning, trust, MCP, and session defaults so new Codex panes start from repo policy instead of memory. |
| AGENTS instruction chain | [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md), with compact [`AGENTS.md`](AGENTS.md) and [`AGENTS.repo.md`](AGENTS.repo.md) routing layers | Keeps one inspectable policy body for planning, verification, commit hygiene, and docs sync instead of loading duplicated instructions. |
| Claude Code global config | [`dot_claude/CLAUDE.md`](dot_claude/CLAUDE.md.tmpl) and [`dot_claude/settings.json`](dot_claude/settings.json) | Wires `dot_codex/AGENTS.md` into Claude Code globally via `@path` import so both Codex and Claude share the same behavioral baseline without a separate copy. |
| Local skills | [`dot_agents/skills/`](dot_agents/skills/) and [`dot_agents/skills/README.md`](dot_agents/skills/README.md) | Packages recurring jobs into reusable local capabilities shared across Codex (`~/.agents/skills/`) and Claude Code (`~/.claude/skills/<name>/` directory symlinks) via a post-apply chezmoi script. |
| Ponytail Codex plugin | [`run_onchange_after_install-codex-ponytail-plugin.sh.tmpl`](run_onchange_after_install-codex-ponytail-plugin.sh.tmpl) and [`dot_codex/config.toml`](dot_codex/config.toml) | Installs [Ponytail](https://github.com/DietrichGebert/ponytail) (pinned to `v5.2.0`) so Codex prefers the smallest correct change and gets `ponytail-review`/`ponytail-audit` skills; trust its hooks once via `/hooks`. |
| Graphiti MCP with Neo4j | [`dot_codex/config.toml`](dot_codex/config.toml), [`scripts/executable_codex`](scripts/executable_codex), and [`docs/graphiti-mcp-codex.md`](docs/graphiti-mcp-codex.md) | Adds a retrievable memory layer for multi-session work where provenance and evolving context matter. |
| Shell and terminal tooling | [`dot_config/fish/config.fish.tmpl`](dot_config/fish/config.fish.tmpl), [`dot_tmux.conf`](dot_tmux.conf), [`dot_config/st/config.def.h.tmpl`](dot_config/st/config.def.h.tmpl), [`dot_config/kitty/kitty.conf`](dot_config/kitty/kitty.conf), and [`dot_config/i3/config.tmpl`](dot_config/i3/config.tmpl) | Optimizes for terminal-first execution and multiple parallel panes, with `kitty` as the default terminal, `st` kept ready as the low-friction alternate, and tmux handling the heavier session workflow. |
| Python and Bash automation | [`scripts/`](scripts/) and [`dot_config/fish/functions/refresh-config.fish`](dot_config/fish/functions/refresh-config.fish) | Keeps repeatable operations small, inspectable, and version-controlled instead of burying them in chat or muscle memory. |
| Private-context workflow | [the vault placeholder](second-brain/README.md), [the session skill](dot_agents/skills/second-brain-session/SKILL.md), and [the command package](scripts/second_brain/) | Publishes the privacy-aware workflow and validation code without publishing the operator's notes, captures, attachments, or account data. |

## Table Of Contents

- [Operating Model At A Glance](#operating-model-at-a-glance)
- [AI Layer Highlights](#ai-layer-highlights)
- [Core Components](#core-components)
- [Second Brain Context Layer](#second-brain-context-layer)
- [Graphiti Memory Layer](#graphiti-memory-layer)
- [Public-Safe Personal Values](#public-safe-personal-values)
- [Install And Bootstrap](#install-and-bootstrap)
- [Day-to-Day Use](#day-to-day-use)
- [Core Command Reference](#core-command-reference)
- [Reproducibility Through Chezmoi](#reproducibility-through-chezmoi)
- [Rest Of Repo](#rest-of-repo)
- [License](#license)

## Operating Model At A Glance

The most distinctive part of this repo is its tracked operating surface:

```text
AGENTS.md
AGENTS.repo.md
dot_codex/
dot_agents/
plans/
second-brain/README.md
```

Those paths define how the AI layer behaves:

- [`AGENTS.md`](AGENTS.md) and [`AGENTS.repo.md`](AGENTS.repo.md) are
  compact compatibility layers that route assistants to one policy body.
- [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md) is the canonical merged
  instruction document that pushes Codex toward plan-first,
  verification-heavy engineering behavior.
  Procedural guides begin with a plain-language overview of their purpose
  and main steps before commands.
- [`dot_codex/config.toml`](dot_codex/config.toml) tracks model,
  reasoning, trust boundaries, MCP servers, and repo-specific developer
  instructions.
- [`dot_agents/skills/`](dot_agents/skills/) packages recurring work
  into reusable local capabilities.
- [`plans/`](plans/) is where non-trivial work becomes explicit,
  checklisted, and reviewable under the
  [ExecPlan contract](.agent/PLANS.md).
- [`second-brain/README.md`](second-brain/README.md) documents the boundary for
  an optional private vault. The vault itself, raw events, attachments, and
  migration ledgers do not enter this public repository.

## AI Layer Highlights

The interesting changes in this repo are often workflow upgrades, not
just dotfile tweaks. The current operating surface has a few
high-leverage properties:

- Instruction-chain upgrades can tighten planning, bug-fix discipline,
  documentation rules, and verification requirements across every new
  Codex session.
- Tracked runtime defaults in [`dot_codex/config.toml`](dot_codex/config.toml)
  change how new sessions start without requiring re-prompting.
- Skill growth in [`dot_agents/skills/`](dot_agents/skills/) turns
  repeated prompting into reusable local tools for shipping, research,
  browser automation, design work, docs lookup, and media tasks.
- [`commit-plan`](dot_agents/skills/commit-plan/SKILL.md) makes commit
  hygiene inspectable: before anything is staged, it can review a dirty
  worktree the way a senior SWE would review a PR draft, separating
  concerns, flagging risky mixed changes, and turning messy local work
  into a coherent commit sequence.
- The Graphiti MCP layer gives Codex a local temporal memory surface
  for longer-running, multi-session work.
- [`dot_agents/system-design/`](dot_agents/system-design/) keeps a
  chezmoi-managed `~/.agents/system-design/` reference pack for
  ExampleProject-style architecture, coding, UI, source-lineage, Knowledge
  Base, and education-platform decisions.
- The README gate itself is versioned: the repo includes a
  recruiter-first sync skill that forces the public docs to keep pace
  with setup, usage, command flags, and repo positioning.
- Non-trivial work is expected to move through tracked plans instead of
  disappearing into chat scrollback.
- The Second Brain package turns explicit focus, deterministic session capture,
  reviewed closeout, and copy-first migration into a tested workflow while its
  operator data remains private.

## Core Components

### 1. Instruction Chain

[`dot_codex/AGENTS.md`](dot_codex/AGENTS.md) is the behavioral backbone
shared across Codex and Claude Code. Root [`AGENTS.md`](AGENTS.md),
[`AGENTS.repo.md`](AGENTS.repo.md), and the deprecated
[`AGENTS-BASE.md`](AGENTS-BASE.md) are deliberately small routing layers,
so the same policy is not loaded and maintained twice.

- [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md) is the only canonical
  working instruction document for this codebase.
- [`dot_claude/CLAUDE.md`](dot_claude/CLAUDE.md.tmpl) wires that same
  canonical document into Claude Code globally via an `@path` import.
  No separate Claude-specific copy is maintained.

That canonical document is not generic philosophy. It encodes concrete
engineering behavior:

- Plan mode for non-trivial work so larger tasks move through explicit
  steps, assumptions, risks, and verification.
- Decorative emojis throughout human-facing CLI/script/helper output, including
  headings, progress, prompts, successes, warnings and errors. Text stays readable;
  `--plain` (or `CLI_PLAIN=1` for legacy helpers) removes decoration. JSON/CSV,
  clipboard data and protocol output remain clean; `NO_COLOR` controls ANSI color.
  See the [output guide](docs/cli-output.md) for safe examples and scope.
- Failing reproducers before bug fixes so changes are grounded in
  observed behavior instead of guesswork.
- Living postmortems for unexpected task failures so the observed evidence,
  investigation, resolution, and verification remain reviewable in one record.
  Shared [postmortem memory](dot_agents/skills/postmortem-memory/SKILL.md)
  retrieves prior remedies before retries and keeps reviewed learning aligned
  with new or changed reports.
- Explicit verification before done so completion is demonstrated with
  tests, diffs, logs, or clear manual checks.
- Docs updates with behavior changes so README, plans, setup steps, and
  workflows stay truthful.
- Small reversible diffs so changes remain reviewable and easy to back
  out.
- Conventional Commit discipline so commit history communicates intent
  clearly.
- A concrete definition of done so another engineer can verify the
  result without reverse-engineering the whole session.

This is where agent behavior stops being prompt folklore and becomes
versioned repo policy.

### 2. Tracked Codex Defaults

[`dot_codex/config.toml`](dot_codex/config.toml) makes each Codex
session start strong instead of neutral.

It tracks:

- the default model and reasoning effort
- trusted local project paths
- MCP servers
- notification, status-line, TUI keymap, and default Vim-mode preferences
- repo-specific developer instructions for plan and commit hygiene

That matters because a new Codex pane inherits the same defaults
immediately. No re-briefing. No guesswork.

One concrete example is the repo-local Graphiti MCP entry: Codex can
launch the local Graphiti checkout over `stdio`, while the detailed
setup and validation workflow lives in
[`docs/graphiti-mcp-codex.md`](docs/graphiti-mcp-codex.md).

### 3. Reusable Local Skills

[`dot_agents/skills/`](dot_agents/skills/) turns repeated prompting into
reusable capabilities shared across Codex and Claude Code. Each skill is
installed to `~/.agents/skills/<name>/SKILL.md` for Codex and symlinked
as a complete directory at `~/.claude/skills/<name>/` for Claude Code via a
post-apply chezmoi script. Directory links preserve optional references,
scripts, assets, and metadata beside `SKILL.md`; Claude Code documents
directory symlinks for this personal-skill layout. The full inventory lives in
[`dot_agents/skills/README.md`](dot_agents/skills/README.md), but the
main categories are more interesting than a flat list.

#### Git Workflow

Representative highlights:

Delivery workflows favor complete coverage within the requested scope, prioritize
session-touched files and safe companions, and report ordinary check failures
without abandoning eligible commits. Planning-only requests remain read-only.
After each commit, Codex reports a [high-level status overview](docs/commit-status-overviews.md)
in both the active plan (or `docs/task-status.md`) and its response, alongside
direct verification commands that exercise the implemented behavior, with example
expected output immediately after each command, verified results, remaining work,
blockers and the next step. Every task completion also includes exactly 3 direct
verification commands with working directory, sudo requirements and labeled
expected output after each command, even when no commit or push occurs. This
applies to documentation, configuration, analysis and planning as well as features.
In Codex replies, runnable shell commands are standalone raw-text lines at
column zero, one physical line per command, using valid fish syntax. Omit fences,
inline backticks, list prefixes, blockquotes, prompt markers and continuation
backslashes; keep all arguments and flags on that line. Code for reading,
including source snippets, JSON, diffs and illustrative shell code, keeps normal
language-tagged fences and meaningful indentation. Expected output has a separate
labeled code block; explanations, working-directory and sudo requirements stay
outside command lines. “Raw” describes command presentation, not a requirement
to render the whole conversation raw. The existing raw scrollback startup setting
is a supported copying option, toggled with `/raw` or Alt+R; it does not establish
selective rendering. See the [Codex configuration reference](https://developers.openai.com/codex/config-reference/)
and the [formatting verification plan](plans/single-line-codex-commands.md#follow-up-separate-runnable-commands-from-displayed-code).
Verify actual selection and paste of a visibly wrapped command into a fresh fish
terminal separately from visible Python, JSON and diff colors. Change supported
rendering settings only when observed evidence satisfies both requirements;
report exact installed-TUI limitations otherwise. Automated checks run before
completion and any commit, and are reported separately.

- [`commit-plan-push`](dot_agents/skills/commit-plan-push/SKILL.md) makes a
  best-effort pass over the entire dirty worktree, separates safe changes into
  chronological commits, pushes once after the series, and reports residuals
  when a file cannot be safely shipped.
- [`commit-plan`](dot_agents/skills/commit-plan/SKILL.md) turns a dirty
  worktree into something closer to a senior engineer's pre-PR pass. It
  inspects staged, unstaged, and untracked changes, groups them into
  the smallest coherent commits, calls out risky mixes like README
  drift or suspicious artifacts, and gives execution-ready commands
  without staging, committing, or rewriting history.
- [`commit-session`](dot_agents/skills/commit-session/SKILL.md) ships
  only the files owned by the current Codex session, with fallback logic
  when a session missed its pre-write baseline; after safe scoping, it
  records validation warnings and repairs truthful README-gate findings
  before committing. Missing session metadata falls back to directly observed
  writes; mixed files contribute their safely separable session hunks.
- [`open-pr`](dot_agents/skills/open-pr/SKILL.md) turns branch-vs-base
  evidence into reviewer-ready PR titles and bodies, including
  `docs/pr/` sync and ExampleProject DD/Reviewer A handoff context when those
  workflows apply.
- [`gh-fix-ci`](dot_agents/skills/gh-fix-ci/SKILL.md) investigates
  failing GitHub Actions checks and plans the fix before touching code.

This category matters because the repo stores reusable guardrails for
commit hygiene, session scoping, CI repair, and shipping discipline,
not just aliases or workflow notes.

#### Design And Frontend

Representative highlights:

- [`design-taste-frontend`](dot_agents/skills/design-taste-frontend/SKILL.md)
  generates React and Next.js interfaces with stronger art direction and
  motion than default LLM UI output.
- [`high-end-visual-design`](dot_agents/skills/high-end-visual-design/SKILL.md)
  pushes interfaces toward agency-grade typography, spacing, card
  treatment, and animation quality.
- [`redesign-existing-projects`](dot_agents/skills/redesign-existing-projects/SKILL.md)
  upgrades existing sites or apps in place without throwing away the
  current framework or functionality.

This category matters because it turns design direction into a
repeatable local capability instead of a one-off prompting exercise.

The managed public design stack adds Impeccable, 21st, Review Animations,
Scroll World, and Higgsfield through chezmoi externals.
[UI/UX Pro Max](dot_agents/skills/ui-ux-pro-max/SKILL.md) is a pinned,
MIT-licensed offline Python/CSV design search skill shared by Codex CLI
(`$ui-ux-pro-max`) and Claude Code (`/ui-ux-pro-max`), explicit-invoke only.
The stack's daily refresh, bootstrap behavior, upstream links, and explicit authentication
boundaries are documented in
[the design-skill guide](docs/design-skills.md).

#### Coding Practice And Scaffolding

Representative highlights:

- [`leetcode-init`](dot_agents/skills/leetcode-init/SKILL.md) turns a
  copied LeetCode `.txt` prompt dump and matching `.py` stub into a
  local runner and inline `unittest` scaffold without filling in the
  actual solution.

This category matters because it preserves the repo's preference for
practice scaffolding and verification without turning every LeetCode
request into solution leakage.

#### Research And Output Control

Representative highlights:

- [`postmortem-memory`](dot_agents/skills/postmortem-memory/SKILL.md) searches
  reviewed incident solutions before remediation and updates shared knowledge as
  postmortems change. Its [read-only helper contract](dot_agents/skills/postmortem-memory/references/workflow.md)
  documents `scan` with repeatable `--root`, `search QUERY`, and full or targeted
  `check --postmortem PATH`, plus fixture `--knowledge` overrides. Exact copied
  content retains source aliases; verified fixes, workarounds, unresolved causes
  and changes awaiting live activation stay distinguishable.
- [`ai-workflow-doctor`](dot_agents/skills/ai-workflow-doctor/SKILL.md)
  turns instruction size, duplicate policy, local references, skill-catalog
  drift, and source provenance into deterministic text or JSON evidence. Its
  `--check` mode blocks objective errors while leaving semantic candidates for
  human review.
- [`metaprompt`](dot_agents/skills/metaprompt/SKILL.md) creates and sharpens
  prompts using Sentry's pinned `prompt-optimizer` workflow, with an eight-section
  report and a separately saved optimized prompt. The original compiler remains available
  as [`metaprompt-alxve`](dot_agents/skills/metaprompt-alxve/SKILL.md), including
  its strict per-pass `go` gate. Both save prompt artifacts; the
  [skill guide](docs/metaprompt-skills.md) records the upstream comparison,
  usage, reviewed updates, and rollback. The
  [benchmark report](docs/metaprompt-benchmark.md) separates maintenance evidence
  from downstream trials and links the pinned fixtures and quota-limited replay
  harness. `python3 scripts/metaprompt-benchmark.py dry-run` previews its schedule
  without using model quota; `verify` checks source and fixture integrity.
  The [maintained-repository selection](docs/metaprompt-selection.md) compares
  three native skills from repositories with at least 1,000 stars, with linked
  skill-level maintenance diffs and equal create/sharpen/template/coding cases.
  Its completed benchmark recommends Sentry's `prompt-optimizer`: 14/16 versus
  Wshobson's 13/16 and Senior's 11/16. Raw and minimal instructions both reached
  15/16 at lower cost; the report includes adapter defects and a sensitivity
  check for an ambiguous template. All 100 attempts used 754 inference requests.
  `python3 scripts/metaprompt-selection.py dry-run` previews the new capped
  schedule without inference; `verify` checks its pinned sources and fixtures.
  Replay phases and `--jobs`/`--development-round` options are documented in the
  report. The benchmark itself installed nothing; the later authorized
  [replacement](plans/replace-metaprompt-with-sentry.md) puts Sentry behind
  the existing `$metaprompt` invocation.
- [`Metaprompt & Run`](dot_agents/skills/metaprompt-run/SKILL.md)
  (`$metaprompt-run`) uses that current compiler to improve and save the
  original request, then immediately starts a new Codex conversation with fresh
  context to execute the saved prompt. No extra `go` is needed. It keeps the
  task's constraints and normal permissions; missing inputs leave execution
  pending, and runtimes without the new-task tool report the limitation.
  `$metaprompt` remains available for prompt review alone.
- [`feedback-memory`](dot_agents/skills/feedback-memory/SKILL.md)
  carries forward durable user corrections through a repo-tracked
  `feedback.log`.
- [`personal-context`](dot_agents/skills/personal-context/SKILL.md) automatically
  informs relevant direction, scope, architecture, design, tooling, milestones,
  and collaboration choices through compact private briefs. Mechanical work
  needs no lookup. `$personal-context` still starts a thoughtful conversation;
  try `$personal-context Let's discuss what makes a project worth pursuing for
  me.` Useful durable statements and unconfirmed interpretations stay private.
  The [storage helper](dot_agents/skills/personal-context/references/store-format.md)
  offers `topics`, `projects --query`, `brief`, and explicit `detail` retrieval;
  normal catalogs and briefs default to eight records and 6,000 characters.
  Read-only project inspection indexes relevant tracked files whose latest
  modifying commit author is exactly example-user Mok, case-insensitive. Committed blob
  evidence must match HEAD and the working tree; untracked and modified source
  bytes are excluded. Summaries describe supported contributions and retain their
  authorship qualification. The source-backed technical summaries stay under
  `/home/example/coding/personal-context/ai-context/project-knowledge.json`, beside
  the personal `context.json` and rebuildable `cache/topic-briefs.json`. All real
  records and payloads stay in that external directory, outside tracked feedback,
  Second Brain, and Graphiti. Normal chezmoi apply installs the skill and implicit
  metadata; missing private storage supports empty reads and conversation.
- [`readme-recruiter-sync`](dot_agents/skills/readme-recruiter-sync/SKILL.md)
  checks install, usage, command flags, stack rationale, and recruiter-facing
  value; safe repairs ship with the change and remaining findings are reported
  without blocking eligible commits.
- [`openai-docs`](dot_agents/skills/openai-docs/SKILL.md) answers
  OpenAI product and API questions from current official docs first.

This category matters because it makes repository knowledge,
documentation quality, and output discipline persistent instead of
fragile session state.

#### Browser And Desktop Automation

Representative highlights:

- [`playwright`](dot_agents/skills/playwright/SKILL.md) drives a real
  browser from the terminal for navigation, screenshots, extraction, and
  UI debugging.
- [`playwright-interactive`](dot_agents/skills/playwright-interactive/SKILL.md)
  keeps a Playwright browser session alive for faster repeated inspection
  and debugging passes.
- [`screenshot`](dot_agents/skills/screenshot/SKILL.md) handles
  desktop-level capture when a normal browser tool cannot grab the right
  evidence.

This category matters because terminal-first agent work still needs
direct access to browser state and desktop evidence when text-only
inspection is not enough.

#### Documents And Media

Representative highlights:

- [`imagegen`](dot_agents/skills/imagegen/SKILL.md) runs image
  generation and editing workflows through the OpenAI Image API.
- [`pdf`](dot_agents/skills/pdf/SKILL.md) handles PDF reading,
  generation, and review workflows where rendered layout matters as much
  as extracted text.
- [`transcribe`](dot_agents/skills/transcribe/SKILL.md) converts speech
  from audio or video into text with optional diarization and
  known-speaker hints.

This category matters because the repo packages higher-friction media
workflows as inspectable local tools instead of leaving them as ad hoc
prompts.

The managed research and discovery skills include
[`last30days`](dot_agents/skills/last30days/SKILL.md), which researches recent
community discussion and provides a source health check, and
[`find-skills`](dot_agents/skills/find-skills/SKILL.md), which finds and installs
skills through the Skills CLI. Both are installed under `~/.agents/skills/`
by the normal chezmoi refresh; provenance is recorded beside each package.

Several skills also include `SOURCE.md`, helper scripts, reference
material, or agent metadata. That makes them closer to local tools than
to copied prompt snippets.

### 4. ExecPlans

[`.agent/PLANS.md`](.agent/PLANS.md) defines the decision-complete plan
contract, and [`plans/`](plans/) is where non-trivial work stays explicit.
The contract requires assumptions, checkboxes, verification evidence, review
notes, and matching plan updates in the same commits as the work they describe.

A representative plan such as
[`plans/commit-all-dirty.md`](plans/commit-all-dirty.md) does not just
say "commit the changes." It inventories the dirty worktree, groups
changes into coherent commit boundaries, notes partial-staging concerns,
defines verification after each step, and calls out concrete risks.

That is execution discipline you can inspect.

The point of keeping plans in the repo is simple: larger tasks should
not live only in chat scrollback or memory.

### 5. Four Codex Workflow

The operating model is four Codex sessions in parallel, each with a
distinct job:

1. Exploration: read the codebase, trace behavior, inspect docs, and
   surface constraints before editing.
2. Implementation: make focused code changes once the path is clear.
3. Review and refinement: look for regressions, weak assumptions, and
   cleaner solutions.
4. Verification and docs: run tests, validate behavior, and keep
   documentation or plans aligned with the work.

This split only works because every pane inherits the same instruction
chain, config defaults, trust rules, and reusable skills. The result is
parallelism with less chaos.

## Second Brain Context Layer

The public repository contains the
[second-brain-session skill](dot_agents/skills/second-brain-session/SKILL.md),
the deterministic [command package](scripts/second_brain/), and the full
[operator guide](docs/second-brain.md). It does not contain a personal vault.
The placeholder at [`second-brain/README.md`](second-brain/README.md) explains
that boundary, and `.gitignore` prevents accidental note or attachment commits.

Operators provide their own private vault path and XDG state. Raw captures,
recaps, reminders, migrations, and personal/project briefs remain outside this
repository; only deliberately authored public examples should be committed.
The included doctor, schema checks, approval gates, and copy-first migration
workflow are the reusable product surface.

## Graphiti Memory Layer

Graphiti is the memory and retrieval layer that sits beside the repo's
instruction chain, local skills, and ExecPlans. In this setup it is not
just a theoretical fit. It is a local MCP service that helps Codex keep
longer-running work coherent across sessions.

The practical use case is straightforward:

- preserve evolving facts about tasks, services, files, branches, and
  verification state instead of leaving them buried in chat scrollback
- keep provenance back to the source episodes that produced those facts
- support multi-session Codex work where exploration, implementation,
  review, and docs all need the same durable context

The local setup is intentionally repo-specific. Instead of relying on
Graphiti's default HTTP transport, the working config launches Graphiti
over `stdio` from `/home/example/coding/graphiti/mcp_server`, keeps
runtime settings in that checkout's `.env`, and expects Neo4j on
`localhost:7687`. That keeps the Codex-side config small and avoids the
host-port `8000` collision that already exists on this machine.

The repo-level `codex` wrapper also starts the same Graphiti command in
the background before handing off to the real Codex CLI. That sidecar
is useful for making sure the command is already alive when you launch
Codex, but it does not replace the actual stdio MCP child that Codex
spawns for tool communication.

For the plain dotfiles bootstrap path, Graphiti is not required. For
the repo's tracked `codex` launcher, it is part of the documented AI
operating path.

The detailed setup, validation steps, and troubleshooting notes live in
[`docs/graphiti-mcp-codex.md`](docs/graphiti-mcp-codex.md). The short
version is:

1. Keep Neo4j running on `localhost:7687`.
2. Let Codex launch Graphiti through the `graphiti` MCP entry in
   [`dot_codex/config.toml`](dot_codex/config.toml).
3. Use Graphiti as the temporal memory layer that complements AGENTS
   files, skills, and ExecPlans instead of replacing them.

## Public-Safe Personal Values

This repository contains templates and neutral examples, not live account
values. Keep machine and identity data in the untracked chezmoi configuration at
`~/.config/chezmoi/chezmoi.toml`, and keep passwords, tokens, SSH material,
browser state, and private notes in their dedicated local stores.

Raw benchmark output under `benchmarks/metaprompt/runs/` and
`benchmarks/metaprompt-selection/runs/` stays private and ignored. Do not publish
request/response traces, installation/session/turn identifiers, cache keys or
raw ledgers. The benchmark guides retain reviewed aggregate findings. The
history auditor reports keyed runtime UUIDs as `runtime_identifier`; inspect
pending files separately because a history scan does not inspect uncommitted bytes.

The mail and calendar templates expect these non-secret chezmoi data keys:

```toml
[data]
mailHost = "smtp.example.invalid"
mailPort = 587
mailTlsStarttls = "on"
mailAddress = "user@example.invalid"
mailRealName = "Example User"
calendarHost = "calendar.example.invalid"
calendarPath = "/calendars/example"
calendarUsername = "example-user"
```

The msmtp template reads its password at runtime from `pass show mail/smtp`;
never add that password to TOML or Git. The optional private knowledge vault is
also external: [`second-brain/README.md`](second-brain/README.md) documents the
boundary. Before publishing changes, run the repository's history auditor:

```bash
./scripts/executable_audit-public-history --scope all
```

The auditor defaults to reachable objects. Use `--scope all` to include
unreachable local objects, `--format text|json` for human or machine output,
`--plain` for ASCII status text, and `--rules PATH` for a mode-`0600` private
literal/path rule file that is never committed.

### Local pre-commit privacy gate

Activate the local gate after cloning with
`python3 scripts/executable_privacy-gate install`. Check installation with
`python3 scripts/executable_privacy-gate status`; repeat `install` after changing
the scanner. Installation snapshots the scanner into the effective Git hooks
directory, preserves and chains an existing pre-commit hook, and leaves
`core.hooksPath` unchanged. Linked worktrees share that directory. A configured
shared hooks directory also shares this gate; choose the hook scope deliberately.
The snapshot continues working if unstaged edits change the source scanner.

Before daily commits, `python3 scripts/executable_privacy-gate check` scans the
entire exact index candidate, including unchanged files and names, rather than
the worktree or added patch lines. Git commits invoke the installed gate
automatically. It checks again after a preserved hook modifies the index.
A refusal leaves the gate's HEAD/index inputs unchanged; repair the private data
locally, stage the safe replacement or removal, and retry. Existing hooks retain
their own side effects and output. The three commit skills require the same check;
Second Brain checks its immutable tree before its hook-bypassing plumbing commit.
Private vault paths are refused in this public checkout, including checkpoint
candidates; keep the actual vault external.

Use `--plain` for ASCII output and `--details` for hashed location references.
No matched values, source lines or filenames appear in gate diagnostics. Resolve
references locally by hashing the exact path bytes with SHA-256 and comparing
the first 12 hex characters. Findings exit 1; incomplete inspection exits 2.
Nothing is uploaded, and no provider/model call runs. Large scans print elapsed
progress every ten seconds. Unresolved index conflicts, unsupported submodules,
missing objects, unavailable rules, and scanner failures refuse inspection.

Shared detection covers recognizable OpenAI/Anthropic, GitHub, AWS access-ID,
Google API and Slack token shapes; credential assignments (including JSON keys),
PEM/base64 private-key headers and SSH key material; email/home/IP identifiers;
and known keyed runtime UUIDs, including nested serialized JSON. Nil runtime UUIDs,
example domains, documentation networks and exact placeholder values remain safe.
There are no blanket fixture-directory exemptions. Candidate path rules block raw
benchmark runs, private credentials, private vault data, and recovery locations
even when force-added. Review false positives locally; use a neutral example
rather than exempting a directory.

Reviewed legacy source expressions, synthetic redaction fixtures and public
recovery runbooks are listed in `scripts/privacy_gate_approvals.json` using only
path references, full content SHA-256 hashes, specific categories and public review
reasons. Each approval applies to those exact bytes at that exact path; any edit
requires a fresh review. All other categories still run, and explicit private forbidden literals/path globs
always override public approvals. There is no test-directory
or general recovery-document exemption. The installer snapshots this manifest;
missing or malformed policy blocks inspection. After a scanner/policy update,
repeat `install` before relying on the installed hook.

If the gate reports an email category only for `identity-author` or
`identity-committer`, decide whether that Git identity is public. Keep it unchanged
only after explicitly approving its exact name/email pair in the private rules
file described below; otherwise configure an appropriate public identity locally.
Do not add an email-domain exemption or copy real identity rules into this repo.

Optional private policy uses `--rules PATH` or local Git config `privacyGate.rules`.
Keep that mode-`0600` JSON file outside the repository. It accepts the history
auditor's `forbidden_literals` and `forbidden_path_globs`; the gate deliberately
ignores `allowed_paths` so private policy cannot weaken built-in restrictions.
An optional `approved_public_identities` array holds exact `{ "name": "Example
Maintainer", "email": "maintainer@example.invalid" }` pairs. This approval only
permits that identity's Git metadata; the same address in file bytes is still
checked. It does not alter Git identity settings or approve arbitrary addresses.
Keep real approvals and private literals out of tracked documentation.

Every candidate blob, including binary raw bytes, is checked. LFS pointers require
a readable local payload with matching size and SHA-256; nothing is fetched.
Missing payloads refuse the commit. Compressed, encrypted, visual, or otherwise
encoded payloads are not semantically inspected. These heuristic patterns cannot
detect every possible secret; review all public content. History auditing remains
a separate operation and does not establish candidate safety.

This is local enforcement. `--no-verify`, another `core.hooksPath`, removing the
hook, alternate scanners, and direct plumbing commits can bypass it. Commit
messages and arbitrary custom identity headers are outside pre-commit coverage;
review them and audit history separately. No CI or server gate is installed.
Concurrent external index mutations outside Git's commit locking remain outside
the local scanner's control.

Rollback with `python3 scripts/executable_privacy-gate uninstall`: it restores the
preserved hook and removes only the gate bundle. If the hook has changed, removal
refuses to overwrite it; review locally. If the bundle was damaged, reinstall
from reviewed source before removing it. See [the implementation record](plans/pre-commit-privacy-gate.md)
and [the smoke checklist](docs/smoke-tests.md#local-pre-commit-privacy-gate).

## Install And Bootstrap

The minimum bootstrap path is `git` plus `chezmoi`.

If you want to use the repo's local AI operating layer, install OpenAI's
Codex CLI separately first and make sure the real `codex` binary is on
`PATH`. The official starting point is the OpenAI Codex docs:
<https://platform.openai.com/docs/codex>.

If you want the repo's AI operating layer as documented here, add Codex
CLI plus the Graphiti-backed prerequisites that the tracked `codex`
launcher expects: a local Graphiti checkout and Neo4j reachable on
`localhost:7687`.

```bash
git clone https://github.com/example-user/dotfiles.git
cd ai-cli-dotfiles

# Preview what this repo would write into $HOME
chezmoi -S "$PWD" diff

# Apply the tracked source state from this clone
chezmoi -S "$PWD" apply
```

That apply path also follows the native-discovery install flow for
[`obra/superpowers`](https://github.com/obra/superpowers): `chezmoi`
installs the latest release archive into `~/.codex/superpowers` and
writes `~/.agents/skills/superpowers` as a symlink to its `skills/`
directory.

The same apply installs the Second Brain command, shared session skill, and
user-level checkpoint units, but it does not enable the timer. The tracked
source command remains available as
`scripts/executable_second-brain`, and the installed `second-brain` command
works from unrelated directories without sudo.

After the verified implementation is pushed, opt into the daily checkpoint
with `setup-second-brain-timer --enable`. The setup command reapplies and
validates only the installed launcher, exact runtime-package modules, and two
user units before enabling the timer; it never invokes sudo. Chezmoi ignores
generated Python bytecode, and setup rejects unexpected runtime-package root
entries that could shadow the reviewed modules. On a clean first install,
setup transactionally creates only the missing launcher, runtime-package, and
unit parent directories; it preserves existing modes and rejects symlinks
before the exact-file apply.

To use the AI layer after the dotfiles are in place, run the
repo-managed wrapper directly, or make sure it is the `codex` command
that wins on your `PATH`:

```bash
"$HOME/scripts/codex"
```

The tracked wrapper is installed from
[`scripts/executable_codex`](scripts/executable_codex). It ensures the
Graphiti startup command
`uv run main.py --transport stdio --database-provider neo4j --model qwen3:14b`
is already running in the background before it hands off to the real
Codex CLI.

## Day-to-Day Use

On the i3 desktop, `ubs` (`ubuntu-start`) needs the wallpaper disk mounted at
`/mnt/linux-files-3`. Use `python3 scripts/enable-ubs-boot-mount.py --check`
to preview the UUID-based boot mount, then run
`sudo python3 scripts/enable-ubs-boot-mount.py --apply` once from the repo root.
The installer backs up `/etc/fstab`, refuses conflicting entries, and enables
an on-demand boot mount without changing sudo permissions or formatting data.
An unavailable disk does not block boot; wallpaper still requires it to be connected.

Treat this repository as the source of truth for most of the environment
layer. Keep machine and identity values private. `refresh-config` applies reviewed sources without importing live settings.

1. Edit the tracked source files in this repo when the repo-managed copy
   is meant to stay authoritative.
2. Preview the resulting home-directory diff with
   `chezmoi -S "$PWD" diff`.
3. Run `refresh-config` to apply reviewed chezmoi files and regenerate shortcuts. Live Codex/Git settings stay private; refresh excludes scripts, externals, and removals and never adopts conflicts.
   Here, `scripts` means chezmoi run hooks; ordinary managed files under
   `~/scripts/` still apply. A permission-only difference can stop refresh just
   like a content edit. Inspect the private log and the exact target diff before
   reconciling a conflict; keep the broad apply unforced.
4. Apply changes with `chezmoi -S "$PWD" apply` when you want the direct
   chezmoi path instead of the higher-level refresh helper.
5. Preview the protected daily Git operation with
   `second-brain checkpoint --dry-run`; use `--no-push` only when you
   intentionally want the resulting checkpoint commit to remain local.
6. Use `setup-second-brain-timer --check` to validate an installed setup,
   `--enable` to opt into the persistent 16:20 user timer, and `--disable` to
   stop it.
7. Run `sync-superpowers-release` when you want chezmoi to refresh the
   external `obra/superpowers` bundle from the latest GitHub release.
8. Use `setup-superpowers-release-timer --check` to validate the optional
   user-scoped daily timer; `--enable` schedules it for 05:00 local time
   with `Persistent=true`, and `--disable` stops it. No sudo is required.
   Timer setup is intentionally bound to the standard `$HOME/linux-config`
   checkout; `sync-superpowers-release` itself still supports an alternate
   `LINUX_CONFIG_SOURCE` for manual refreshes.
   Refreshed skills are picked up by newly started Codex sessions; already-
   running sessions remain unchanged until restarted.
9. Run the repo-managed `codex` wrapper from the repo root when you want
   the tracked AGENTS chain, Codex config, local skills, and plans to
   shape the session.
10. Keep the root `README.md` aligned whenever the repo's public workflow
    changes, especially for install steps, usage, command flags, the
    repo-based tech stack section, and recruiter-facing positioning.

For a context-aware work session, start with
`second-brain status --format json`, confirm exactly one measurable ExampleProject
outcome, and let the shared skill use `focus` and `closeout` only after
confirmation. Use `doctor --format json --check` before trusting structural
changes. Migration and protected upgrades always start with their read-only
inventory, plan, or dry-run steps; see the
[operator guide](docs/second-brain.md) before applying either.

Search saved conversations across projects with `codex-search "cache.*refresh"`
or `csg -iF "exact phrase"` in fish. Use `codex-search --pick "pattern"`
to select a match in fzf and resume in its recorded directory; Esc cancels.
Use `codex-search --recent` for the newest 20 sessions without a pattern, or
`crg` (`codex-search --recent --pick`) for sessions ranked by AI priority:
urgent, actionable, unknown, waiting, then complete, with activity breaking ties.
The preview explains each priority and labels stale or missing evidence. Use
`--sort recent` for newest-first picking, or `--recent --sort priority` to list
cached priorities without calling a model.
Picker rows use compact Toronto timestamps (`Oct 8 12:24`), with full timestamps
in the preview. Abbreviated paths and tight spacing keep titles visible; Ctrl-/
toggles the responsive preview. Guardian review and untitled rows use AI recap headlines,
updating in the list as recaps arrive. Waiting rows show queue position and elapsed
time; generating rows show a ticking timer. Guardian/session changes refresh
titles, activity, dialogue and discovery in the background, then update recaps
and ordering. The query and selected UUID remain stable while still matching.
`--no-summaries` keeps cached recaps and local previews without model calls;
Ctrl-G requests a recap for the highlighted session when generation is enabled.
Use `codex-search --help` for options and examples, and the grouped
[smoke checks](docs/smoke-tests.md#codex-session-search) to verify the workflow.
The recent picker opens available local metadata before full archive indexing
finishes, including when another refresh holds the index lock. Cold caches begin
with bounded native metadata; remaining native titles catch up in the background.
Pending dialogue ranks as unknown or keeps visibly stale cached evidence.
Indexing continues with concise progress and no per-file
warning flood; Ctrl-G waits for pending dialogue. `--details` adds bounded
background diagnostics to the preview. Python 3.11+ and ripgrep are
required for pattern search; fzf is optional for selection. See the [session search guide](docs/codex-session-search.md)
for tool-output searches, cache controls, and verification.
Terminal searches show the newest 20 matches with a short highlighted excerpt;
use `--details` for full blocks and `--limit 0` for all results. Piped output
includes every full block without color; recent listing defaults to 20 even in
pipes. Pattern picking sees all matches; recent picking adds usable sessions as
background indexing progresses.

## Core Command Reference

These are the core entrypoints the README depends on. The flags and
options listed below are verified against local CLI help or script
source in this repo.

| Command | When to use it | Flags and options that matter |
| --- | --- | --- |
| `chezmoi -S "$PWD" diff` | Preview what the checked-out source tree would change in `$HOME`. | `-S` / `--source` points chezmoi at this clone instead of the default source directory. `--reverse` flips the diff direction when you need the comparison the other way around. |
| `chezmoi -S "$PWD" apply -n -v` | Dry-run an apply with extra detail before touching files in `$HOME`. | `-S` / `--source` uses this repo as the source state. `-n` / `--dry-run` previews changes without writing them. `-v` / `--verbose` prints more detail. |
| `chezmoi -S "$PWD" apply` | Apply the tracked source state from this clone into `$HOME`. | `-S` / `--source` uses this repo as the source state. `-P` / `--parent-dirs` is useful when you apply a nested target and also want its parent directories handled. |
| [`codex-search`](docs/codex-session-search.md) | Search decoded local Codex conversations across directories, print snippets and resume commands, or select a session to resume. Installed from `scripts/executable_codex-search`; fish abbreviations `csg` (search) and `crg` (recent picker). | `--recent` lists newest 20 sessions without a pattern or model calls; `--recent --pick` opens available metadata before full archive indexing, then adds usable sessions in the background and ranks them by AI priority. Pending dialogue stays unknown/stale and defers recap generation; Ctrl-G remembers a request until ready. Malformed archive records do not flood the picker; `--details` exposes diagnostics. Guardian/session changes refresh automatically. `--sort priority\|recent` selects the order; picking defaults to priority, listing to recent. Priority is urgent/actionable/unknown/waiting/complete with activity ties; the preview explains its reason and freshness. `--summary-count N` sets the automatic newest-session window (default 20, 0 disables it); Ctrl-G requests a selected recap. `--summary-model MODEL` overrides the configured model; `--no-summaries` prohibits all generation. `-i` ignores case; `-F` uses literal text; `--all-text` adds tool calls/output; `--pick` uses optional fzf and browses all matches. Terminal output defaults to 20 compact results; `--details` shows full blocks; `--limit N` caps printing (0 means all). Pipes default to all full blocks without ANSI; `NO_COLOR` disables terminal color; `--plain` also uses ASCII printed decoration and ASCII borders in the recent picker. `--rebuild-index` reparses sources; `--clear-cache` deletes this Codex home's private index. `CODEX_HOME` selects sessions, `XDG_CACHE_HOME` selects cache storage; `--help`, `-h` or no arguments show usage and examples. Requires Python 3.11+ and rg for pattern search, fzf (tested 0.44.1) for recent picking, and compatible Codex with login for recaps; no sudo to run. |
| `refresh-config` | Apply reviewed chezmoi files and reload shortcuts. | No flags; `CLI_PLAIN=1` provides ASCII decoration. Excludes scripts, externals, and removals; reports elapsed progress, stops on conflicts, and never imports live settings. Diagnostics remain in a private temporary log. |
| [`./scripts/executable_fix-vps-codex.sh`](docs/fix-vps-codex.md) | Run locally to repair Codex npm permissions on a VPS using SSH keys, without sudo. Reuses compatible Node/npm and verifies a normal update through a second SSH session. | Defaults to `example-user@192.0.2.10`; `--host`, `--port`, and `--identity` override the connection. `--dry-run` reads diagnostics without repair writes or npm execution; `--help` shows prerequisites. Requires remote Linux, Python 3.8+, bash or fish, and an already trusted host key. |
| `sync-superpowers-release` | Refresh the externally managed `obra/superpowers` skill bundle from the latest GitHub release archive through chezmoi. | `--dry-run` previews the release refresh without writing files. `LINUX_CONFIG_SOURCE` points the helper at this repo when it is not checked out at `$HOME/linux-config`. |
| `sync-design-skills` | Refresh the managed public design skill externals; preserve vendored UI/UX Pro Max. | `--dry-run` previews the external refresh. `--bootstrap` is a compatibility no-op; normal shared-skill deployment supplies pinned UI/UX Pro Max. It never authenticates accounts, generates media, spends credits, or upgrades the Higgsfield CLI. |
| `setup-design-skills-timer` | Validate, enable, or disable the daily 05:00 design-skill refresh timer. | Exactly one of `--check`, `--enable`, or `--disable` is required. `--enable` validates and activates the `Persistent=true` user timer without sudo. |
| `setup-superpowers-release-timer` | Validate, enable, or disable the optional user-scoped release-sync timer. It runs daily at 05:00 local time and catches up missed runs with `Persistent=true`; no sudo is required. Refreshed skills are picked up by newly started Codex sessions; already-running sessions remain unchanged until restarted. | Timer setup requires the standard `$HOME/linux-config` checkout. Exactly one of `--check`, `--enable`, or `--disable` is required. `--check` validates the managed sources and installed units without changing state; `--enable` applies and activates the timer; recovery-oriented `--disable` stops it without needing chezmoi or a source checkout. |
| `./scripts/executable_ai-workflow-doctor` | Audit the repo's AI instruction and skill surface, or capture a stable before/after measurement for workflow optimization. | `--repo PATH` selects the repository. `--format text\|json` selects human or machine output. `--snapshot PATH` writes a deterministic JSON baseline; `--compare PATH` compares the current report with one. `--verify-sources` resolves declared local source archives when available. `--check` exits nonzero for objective errors while review findings remain non-blocking warnings. |
| `./scripts/executable_apply-pywal-theme <wallpaper>` | Regenerate the active `pywal` theme through the repo-owned wrapper so wallpaper changes also refresh kitty and the i3 color resources this repo depends on. | Pass an image path directly, or pass raw `wal` flags when you need that lower-level control. The wrapper runs `wal --saturate 0.8 -e`, reloads Xresources, refreshes running kitty windows when the socket is available, and regenerates the derived i3 palette file. |
| `./scripts/executable_install-chatgpt-linux` | Download and install the official ChatGPT desktop app package for a supported Linux desktop. | No flags. Supports Ubuntu 24.04/26.04, Debian 13, and Fedora 43/44 on x64 or ARM64. It prints the selected official package URL, then prompts for sudo only to run `apt install` or `dnf install`. |
| `./scripts/executable_install-tmux-tpm.sh` | Install or fast-forward the TPM plugin manager, correct the tracked tmux bootstrap path when needed, and reload an active tmux server. | `--help` prints usage. With no flags, it clones or fast-forwards TPM under `~/.tmux/plugins/tpm`; restart tmux if no server is active, then press `prefix + I` to install plugins. |
| `./scripts/executable_directory-sizes [--depth N] [DIRECTORY]` | Show allocated usage in a nested directory report with provisional Dust indexing feedback. | Defaults to current directory and display depth 1; depth does not limit scanning. `--threads N`, `--json`, `--apparent-size` (logical, with different hardlink/directory semantics), and `--backend PATH` are supported. Install pinned Dust with `./scripts/executable_setup-directory-sizes --prefix /tmp/directory-sizes-tools`; use `--backend /tmp/directory-sizes-tools/bin/dust`. No sudo or source writes; reported errors/interruption withhold totals. See [setup, accounting and measured limits](docs/directory-sizes.md). |
| `./scripts/executable_largest-day-file-size DIRECTORY` | Show the three local modification dates whose regular files have the largest combined sizes. | Scans recursively, skips symlinks, and prints up to three lines such as `2026-08-21 30.5 GiB`, largest first. Sizes use binary units; equal totals choose the earlier date. Requires Python 3, needs no sudo, and exits with an error for an empty or invalid directory. |
| [`./scripts/executable_backup-pc backup`](docs/backup-pc-recovery.md) | Create a standalone full-system recovery backup of Ubuntu 24.04 amd64 UEFI, offline by default. | Requires sudo and, by default, read-only ext4 root/home plus FAT EFI mounts beneath `--source-root /mnt/source`; `--destination /mnt/backup/system-backups` selects backup storage. `--dry-run` previews coverage and exclusions without writing. Uses xz `-9e` for `system.tar.xz`; `--resource-percent 75` (default, integer 1–100) selects that share of available CPU threads and a compressor-memory ceiling based on currently available RAM. This is a budget, not an exact utilization target; home rsync is unchanged. New bundle directories use local `MM-DD-YY` dates (same-day extras get `-02`, etc.) and retain `.incomplete` until publication. Home stays browsable in normal `home/` files with metadata and integrity verification. Use an ext4 backup filesystem; FAT/exFAT/NTFS are rejected. Includes installed state and personal data; omits runtime contents, known caches, its destination and unrelated mounts. `--live --source-root /` permits the mounted running system and marks the bundle `live-nonatomic`; services keep running. `excludes` prints the embedded policy. Generated artifacts belong to the invoking sudo user; copied home ownership stays intact. `access --bundle PATH --user example-user` repairs access to older bundles (requires sudo). Legacy `PROFILE tar-root` and `PROFILE home` remain partial backups. |
| [`sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup`](docs/backup-pc-recovery.md#back-up-the-running-machine) | Back up this running machine to the mounted backup HDD. | Add `--dry-run` to preview without writing. Requires the same supported root/home/EFI layout and Linux backup filesystem. Root, home and service data are copied at different times; this is not a snapshot or an application-consistency guarantee. Terminal output shows root/home progress bars, elapsed time, estimated remaining time and the current file; root/EFI progress is an estimate and copying is followed by integrity verification. Timestamped phases, filenames and warnings/errors are written to the bundle’s private `backup.log`, readable by the user invoking sudo; use `tail -f /path/to/BACKUP.incomplete/backup.log` while it runs. Changed/vanished tar-file warnings are checksummed in `warnings.json`; vanished home files are skipped after one best-effort rsync pass and recorded in the warnings, while read/permission/I/O errors fail visibly incomplete. `sync-home --bundle PATH --source-root / --live` reruns only home copying into an incomplete bundle, preserving the root tar and log; it keeps the bundle incomplete. Restore the complete bundle from a live USB. |
| [`backup-pc restore`](docs/backup-pc-recovery.md#restore-onto-a-replacement-hdd) | Run the script included in a completed backup from a live USB to restore onto an unmounted replacement whole disk. | Requires sudo, `--archive /mnt/backup/BACKUP/system.tar.xz` and `--target-disk /dev/disk/by-id/TARGET-HDD`. `--dry-run` verifies and previews without destructive operations; `--root-size 80` or `80GiB` overrides root size. Requires the complete bundle including intact `home/` and its index; verifies both components, protects source/backup/running disks, requires exact `ERASE <resolved-device-path>` confirmation, then replaces every partition with EFI/root/swap/home. See the guide for supported layouts, dependencies and the disposable-VM boot check; Secure Boot has not been boot-tested. |
| `bash scripts/hdd-init-wizard.sh` | Diagnose a USB SATA dock and explicitly initialize one selected disk as GPT/ext4, then mount it by UUID. Run as your normal user; the wizard calls `sudo` for privileged steps. | `--help` shows usage; `--dry-run` shows read-only diagnostics and a plan without writes. The interactive path blocks system and mounted disks, requires exact device and erase phrases, backs up `/etc/fstab`, and checks `mount -a`. Requires `parted`, `smartmontools` only for optional SMART data, and standard Ubuntu disk utilities. |
| `./scripts/executable_concat-timestamped-videos DIRECTORY OUTPUT` | Join top-level camera clips in capture-time order. | `--list-only` writes `OUTPUT_STEM.ffconcat.txt` beside the output for review. `--clips FIRST SECOND` selects exactly two filenames in the directory, excluding other clips and prior outputs. Pixel `PXL_` timestamps come from filenames; iPhone `IMG_` timestamps come from MOV metadata and require `ffprobe`. The default join uses FFmpeg stream copy for compatible streams. Use `--reencode` with `--clips` for mixed SDR/HDR sources: it tone-maps HLG to SDR and writes H.264/AAC, so the output loses HDR/Dolby Vision metadata and takes longer to create. Supports `.mp4`, `.mov`, and `.m4v`; excludes nested folders and symlinks, never overwrites an existing output, and needs no sudo. Example: `./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic /mnt/usb-8tb/concerts/logic/logic-pair.mp4 --clips PXL_20260928_011900910.mp4 IMG_1377.MOV --reencode`. |
| `./scripts/executable_screenshot-all-monitors` | Save one combined `scrot` capture of the full X virtual desktop, covering every active monitor in one image. | No flags. Saves to `/home/example/Pictures/screenshots/desktop/unsorted/screenshot-YYYY-MM-DD_HH:MM:SS.png`. `SCREENSHOT_ALL_MONITORS_DIR`, `SCREENSHOT_ALL_MONITORS_SCROT`, and `SCREENSHOT_ALL_MONITORS_DATE` override the destination, capture binary, and timestamp binary for tests or alternate hosts. |
| `./scripts/executable_setup-st.sh` | Render the tracked `st` config, sync it into your `st` source checkout, and install the compiled terminal you actually want to use. | `--source-dir` points the script at a non-default `st` checkout path. `--skip-install` only refreshes `~/.config/st/config.def.h` plus the source-tree `config.def.h` and prints the exact `sudo make -C ... install` command instead of running it. `--clone-if-missing` clones the official upstream source from `https://git.suckless.org/st` into the target checkout path before syncing and building. |
| [`~/scripts/codex-notification-activate`](docs/codex-notification-sound.md#installation-and-activation) | Activate the optional notification hook after applying sources. | Restarts only your current session's Dunst bus owner, clearing its history/queue; `--open-kitty` also opens a fresh Kitty process while preserving existing terminals. Requires deployed notification files, Dunst and dbus-send; no sudo. Does not enable sound. |
| [`~/scripts/codex-notification-sound`](docs/codex-notification-sound.md) | Play a local MP3, optionally followed by the exact Codex conversation title or one sentence about a queued question using Voice Contributor high at the celebrate audition pace (0.95), generated locally while the clip plays. Popup audio and speech are separately disabled until configured. | `set PATH`, `preview [--title TEXT] [--speech-only]`, `disable`, `status`, `speech enable|disable`, and `smoke tagged|kitty`; `--plain` uses ASCII, `--details` shows paths/diagnostics. Speech requires the installed voice and restarted/resumed Codex sessions; covers focused/background user-facing answers with nonblank final text and accepted queued questions. Question speech requires enabling/trusting the two exact entries in `/hooks`; it reads the prompt, omits choices and combines up to three prompts and any remaining count into one bounded sentence. `python3 -B scripts/smoke_codex_question_events.py --installed --case all --plain` verifies question delivery with a silent isolated player. Helper-agent completions, empty answers, unknown origins, invalid/secret questions, permission requests and automatic reviews stay silent while Dunst audio is suppressed. `python3 -B scripts/smoke_codex_notification_events.py --installed --case all --plain` verifies event eligibility with a silent isolated player. Disabling speech restores MP3-on-popup behavior. Python 3/mpv, no sudo; settings stay machine-local. Select an existing local MP3 outside the checkout; a missing selected file blocks both clip and speech. |
| [`~/scripts/setup-codex-notification-speech`](docs/codex-notification-sound.md#optional-offline-title-speech) | Install and verify the optional English title voice. | `--install` downloads pinned Piper 1.8.0 and `en_US-Voice Contributor-high` into an isolated XDG data environment; `--check` verifies offline WAV synthesis; `--plain` uses ASCII and `--details` shows download logs/paths. Python venv/pip required, no sudo; installation needs internet, playback does not. Does not enable speech. |
| [`~/scripts/codex-voice-auditions`](docs/codex-notification-sound.md#audition-ten-local-voices) | Compare ten numbered local voices with upbeat lines and the question clip before each sample; includes a committed [Voice Contributor celebrate MP3](scripts/Voice Contributor-celebrate.mp3) reference. | Default plays all ten; `--list`, `--samples`, `--voice NUMBER [NUMBER ...]` (names/IDs also accepted), `--sample all|short|celebrate|technical`, `--text TEXT`, `--length-scale 0.95`, `--offline`, `--render-only`, `--output-dir PATH`, `--clip PATH`, `--dry-run`, `--plain`, `--details`. Requires installed Piper 1.8.0 and mpv for playback; first model downloads need internet. Saves WAVs/manifest under XDG data, reports remaining clip-to-speech gap, changes no notification settings, no sudo. |
| `rintro` → [`~/scripts/Voice Contributor-intro`](docs/codex-notification-sound.md#short-Voice Contributor-introduction) | Play example-user's saved Voice Contributor introduction without the question clip. | No arguments plays [Voice Contributor-intro.mp3](scripts/Voice Contributor-intro.mp3) immediately; `--text "WORDS"` synthesizes custom Voice Contributor high speech only, pace 0.95; `--help` prints usage. Autoloadable fish command, available in existing shells after deployment; mpv required, custom speech also needs installed Piper. Local-only, no sudo. |
| `~/scripts/kitty-scrollback-smoke` | Open a separate Kitty window to check dragging, paging, selection, wrapping, and streaming history without sudo or model requests. | `--lines` defaults to 10000; `--stream-lines` to 300; `--interval` to 0.1 seconds. `--emit` prints in the current terminal instead. Press Enter to start streaming and again after it finishes to close the test. See the [scrolling smoke checks](docs/smoke-tests.md#kitty-and-codex-scrolling). |
| [`~/scripts/tmux-scrollback-smoke`](docs/smoke-tests.md#tmux-pane-history-scrolling) | Open an isolated Kitty/tmux fixture for held-edge multi-screen selection and drag/release/Ctrl+Shift+C copying. | `--lines` defaults to 3000, with long logical lines for wrapping checks; `--app-mouse` checks application mouse ownership; `--plain` gives ASCII output. Escape returns to live input; Ctrl+D at empty input closes only the fixture. No sudo. |
| `./scripts/executable_setup-aerc-mail.sh` | Install aerc mail prerequisites or add one Gmail/Outlook.com account at a time without storing addresses, app passwords, client IDs, or OAuth tokens in Git. | `--install` may prompt for sudo to install shared packages. `--init-pass GPG_KEY_ID` initializes an empty password store. `--add-gmail` prompts for a Gmail app password; `--add-outlook` prompts for a Microsoft app client ID and launches device-code OAuth; `--status` checks configured accounts without printing credentials; `--dry-run` previews write actions without changing files or starting OAuth. |
| `sudo ./scripts/executable_setup-neovim-python-completion.sh` | Upgrade Neovim from Ubuntu's older package, install the repo's `vim-plug` Neovim stack including `nvim-lspconfig`, and install the Python language server used for strong completion and signature help. | `--neovim-version` pins a different official release. `--skip-plugins` skips `vim-plug` bootstrap and `PlugInstall`. `--skip-lsp` skips `uv tool install --upgrade basedpyright`. |
| `sudo ./scripts/executable_update-chrome.sh` | Refresh APT metadata and upgrade Google Chrome when a newer candidate is available. | `--check` prints installed and cached candidate versions without modifying the system. Normal runs refresh metadata before deciding whether to upgrade, then re-read the candidate after installation. Installed versions equal to or newer than the candidate succeed using Debian version ordering. Prints initial activity and actionable query errors. Relaunch Chrome afterward to use the updated binary. |
| `"$HOME/scripts/codex"` or `codex` when that wrapper wins on `PATH` | Start Codex in the repo so the tracked instruction chain and config take effect. The repo wrapper also ensures the Graphiti sidecar command is running first. | `-C` / `--cd` sets the repo root when you launch from another directory. `--search` enables live web search for tasks that need current external information. `CODEX_WRAPPER_GRAPHITI_CWD` and `CODEX_WRAPPER_STATE_DIR` override the wrapper's Graphiti checkout path and state directory. |
| `codex mcp list --json` | Verify which MCP servers Codex is loading from the tracked config. | `--json` emits machine-readable output that is easier to inspect or diff. |
| `second-brain status` plus `capture`, `focus`, and `closeout` | Retrieve targeted context, keep raw session text private, and persist only explicitly confirmed public-safe focus or closeout records. | `status --format text\|json`; `capture --kind raw-session\|personal-decision --payload PATH_OR_DASH`; `focus --payload PATH_OR_DASH`; `closeout --payload PATH_OR_DASH`. Payload shapes live in the [routing reference](dot_agents/skills/second-brain-session/references/routing.md). |
| `second-brain sessions` | Refresh the private cross-project Codex digest or review it on request; preserve unresolved checks and explicit dispositions outside Git. | `review` defaults to five recent directories with three sessions each; `--limit 1..20` changes the directory count, `--refresh-limit 0..20` caps recap generation (default three per directory, capped at 20), full recaps, evidence, check history, session metadata and coverage are shown by default (`--details` is compatible); interactive text opens in `bat`/less with emoji cues (`r` refreshes discovery/recaps; `q` quits) and ongoing elapsed progress on stderr; `--no-pager` prints directly, `--plain` provides ASCII text, and `--all` selects eligible history (cannot combine with `--limit`; default refresh budget 20). `refresh --limit 1..20` remains a background queue budget (default 20). Both accept `--format text\|json`; `resolve --payload -` accepts confirmed checked/dismissed JSON on stdin. Review requires no ExampleProject outcome; see [the digest guide](docs/second-brain.md#private-daily-codex-work-digest). |
| `setup-second-brain-sessions-timer` | Independently manage the persistent 16:00 America/Toronto private digest refresh with no notifications. | Exactly one of `--check`, `--enable`, or `--disable`; no sudo. Does not activate checkpoint or deferred timers. Disable retains private state. |
| `second-brain doctor` | Audit the tracked vault for structure, privacy, ownership, import-frontmatter, hard-link, and Git LFS errors without mutating it. | `--format text\|json` selects output. `--check` exits 1 when objective errors exist. |
| `second-brain migrate` | Inventory and plan selected external text, copy one explicitly approved batch into the archive, or verify its private resume ledger. | Subcommands are `inventory --source PATH` with repeatable absolute roots, `plan --inventory PATH`, `apply --plan PATH --approve SHA256`, and `verify --ledger PATH`. Follow [the copy-first procedure](docs/second-brain.md#copy-first-text-migration); no initial migration is automatic. |
| `second-brain upgrade` | Preview append-only protected-vault changes and exact-byte dated backups. | `--dry-run` prints the current batch and approval SHA. `--apply --approve SHA256` accepts only that unchanged batch; the current schema-v1 preview has zero pending operations. |
| `snapshot-codex-config` | Validate live Codex configuration without copying it to public source. | `--dry-run` retains the same read-only behavior. Validates ownership, size, TOML, likely secrets, exact mapping, and filesystem boundaries; checkpoint also binds the expected repository. |
| `second-brain checkpoint` | Validate and ship one allowlisted daily Second Brain/Codex-config checkpoint on the current branch. | `--dry-run` performs candidate preflight without staging, committing, or pushing; it does not prove the later immutable-tree or shipping gates. `--no-push` commits after all gates but leaves the commit local. With no flags, the command explicitly uploads reachable LFS objects and pushes only the exact configured-upstream ref without local hooks, tags, or force. |
| `setup-second-brain-timer` | Validate, enable, or disable the persistent 16:20 systemd user checkpoint timer without sudo. | Exactly one of `--check`, `--enable`, or `--disable` is required. `--enable` applies the launcher, exact runtime-package modules, and two unit targets before daemon reload and activation; unexpected package-root files, directories, or symlinks fail closed, while an owned real `__pycache__` directory is allowed. Recovery-oriented `--disable` does not require chezmoi or a source checkout. |

To inspect short real joins across every adjacent pair in a directory, run
`python3 tests/check_concat_boundary.py --directory /mnt/usb-8tb/concerts/logic`.
It uses the directory's FFmpeg concat list when one exists, or scans top-level
video files otherwise. `--concat-list PATH` selects a specific list and
`--seconds N` changes the sampled duration (default: 4 seconds per source).
It retains joined samples and boundary contact sheets under `/tmp` for visual
review and reports FFmpeg timestamp warnings. No sudo is needed.

For a full stream-copy join, inspect both output stream durations and decode
frames across the join. FFmpeg can exit successfully while incompatible video
time bases collapse later video frames into a fraction of a second; see the
[Logic and iPhone join incident](docs/postmortem/2026-09-28-logic-1377-stream-copy-freeze.md).

## Reproducibility Through Chezmoi

The productivity gain is not trapped inside one laptop.

This repo is `chezmoi`-managed, which means the environment itself is
tracked as source state and can be applied back into `$HOME` through the
standard `chezmoi` workflow. The same files that shape the Codex
workflow, including AGENTS documents, Codex config, skills, aliases,
templates, and supporting dotfiles, are part of a reproducible setup
rather than fragile local state.

That means the workflow is portable when the setup changes, and the
leverage is inspectable because you can see exactly which instructions,
defaults, packaged skills, and plans are doing the work.

Typical commands are still the usual ones:

```bash
chezmoi -S "$PWD" diff
chezmoi -S "$PWD" apply
```

The difference is what is being reproduced. It is not only shell
comfort. It is the operating environment for AI-assisted engineering.

## Rest Of Repo

The rest of the repository is still a full desktop-dotfiles setup, not
just an AI CLI config repo. The major non-AI surfaces break down like
this.

### Shells And Shared Shortcuts

- [`dot_bashrc`](dot_bashrc) and [`dot_zshrc`](dot_zshrc) keep the
  fallback shells in sync around shared aliases, colors, and shell
  framework hooks.
- [`aliases/key_aliases.tmpl`](aliases/key_aliases.tmpl),
  [`aliases/key_dirs.tmpl`](aliases/key_dirs.tmpl), and
  [`aliases/key_files.tmpl`](aliases/key_files.tmpl) form the canonical
  shortcut layer. [`scripts/executable_sync-shortcuts`](scripts/executable_sync-shortcuts)
  regenerates shell aliases, fish abbreviations, and ranger mappings
  from those sources.
- [`fish-alias`](dot_agents/skills/fish-alias/SKILL.md) accepts an abbreviation
  followed by a command or path: `$fish-alias cbn codex-time burn day` adds
  `cbn "codex-time burn day"` in the existing work section. It previews the
  diff, comments active conflicts in place, preserves quoted hashes and spaced
  paths, normalizes pasted `/home/example` directory prefixes to `~`, and refreshes
  changed mappings. File source keys gain an `n` prefix
  in fish (`re README.md` becomes `nre`); activation follows current chezmoi
  conditions. The example is not installed automatically. See the
  [isolated checks](docs/smoke-tests.md#fish-alias-skill).
- [`dot_config/fish/config.fish.tmpl`](dot_config/fish/config.fish.tmpl)
  is the main interactive shell setup and loads the large helper surface
  under [`dot_config/fish/functions/`](dot_config/fish/functions/).

### Editor, Terminal, And Media

- [`dot_config/kitty/kitty.conf`](dot_config/kitty/kitty.conf)
  is the default terminal config, and the i3 bindings now open `kitty`
  first for normal shells and Codex. Each Kitty window has an i3 titlebar;
  Codex shows its activity indicator and a live “what are we doing?” summary
  (3–5 words, at most 36 characters), such as “Categorize card transactions”.
  Agents check their own native task name at each turn, resume, compaction
  recovery and before progress updates; they change it when the current task
  or phase differs. Pasted historical session reports do not define the active
  title. This also renames the saved conversation. These summaries depend on
  agent instruction compliance. Launch
  a new Codex process after `refresh-config` (including `codex resume`)
  to pick up the title settings/instructions; switching threads inside an existing
  TUI does not establish that the startup settings reloaded.
  If the native title tool is unavailable, use `/rename` manually. Fullscreen
  hides i3 titlebars. See the [overview checks](docs/smoke-tests.md#kitty-and-codex-overviews).
  It retains 50,000 lines with a rounded,
  draggable scrollbar and the existing 0.9 background opacity.
  Shift+PageUp/PageDown moves through history; Ctrl+Shift+End returns to the
  newest output. Codex defaults to `tui.alternate_screen = "never"`, so normal
  launches and resumed sessions keep long transcripts in native terminal
  history. Super+C uses the current shell's Codex installation and also passes
  `--no-alt-screen`. Restart or resume an existing session after applying the
  setting. The fixture uses these same Kitty settings without overrides; use
  a fresh window and the
  [scrolling smoke checks](docs/smoke-tests.md#kitty-and-codex-scrolling)
  after applying changes; tmux pane history still uses tmux copy mode.
  [`dot_config/st/config.def.h.tmpl`](dot_config/st/config.def.h.tmpl)
  remains the alternate `st` template with the repo-preferred font,
  `wal` colors, opacity, clipboard shortcuts, and selectable local
  scrollback, while the repo-owned `st-terminal` launcher still
  resolves `st` or `stterm` at runtime on hosts where the binary name
  differs.
- [`scripts/executable_apply-pywal-theme`](scripts/executable_apply-pywal-theme)
  is the repo-owned wallpaper and theme entrypoint. It wraps `wal`,
  boosts saturation, refreshes kitty, regenerates contrast-safe i3 bar
  colors, and keeps the rest of the tracked wallpaper shortcuts on one
  consistent path instead of sprinkling raw `wal -i` calls through the
  config.
- [`dot_tmux.conf`](dot_tmux.conf) is the multiplexing layer with a
  custom prefix, mouse mode, TPM plugins, a status line, and copy-mode
  mappings that push selections to `xclip`. New panes keep 50,000 history rows;
  Shift+wheel browses pane history without holding a mouse button, even in
  mouse-aware apps. Hold a left-drag at the pane's first text row to extend the
  selection through older screens without wheel events. Release, then Ctrl+Shift+C copies the persistent
  highlight while keeping the viewport in place; Escape returns to live input.
  A history-mode status hint shows the shortcuts. Plain wheel works at a shell;
  Alt+wheel remains supported. Native Kitty selection copying is preserved;
  release Shift before dragging to select tmux-owned history. Copy detection
  supports tmux sharing a foreground process group with a fish launcher.
  tmux 3.4 text dragging selects rather than moving
  a scrollbar; Kitty's native thumb cannot expose tmux-owned history. See the
  [tmux gesture checks](docs/smoke-tests.md#tmux-pane-history-scrolling) and run
  `~/scripts/tmux-scrollback-smoke` (or `--app-mouse`) in an isolated window.
  Use
  [`scripts/executable_install-tmux-tpm.sh`](scripts/executable_install-tmux-tpm.sh)
  to install or update TPM and reload an active tmux server before using
  `prefix + I` to install its plugins.
- [`dot_vimrc.tmpl`](dot_vimrc.tmpl) plus
  [`dot_config/nvim/init.vim`](dot_config/nvim/init.vim) define the main
  editing environment across Vim and Neovim. Vim keeps the shared
  editing defaults and snippet workflow, while Neovim layers a
  Python-first Blink completion and `basedpyright` LSP stack on top via
  `nvim-lspconfig`.
- [`dot_config/mpv/`](dot_config/mpv/),
  [`dot_config/zathura/`](dot_config/zathura/), and
  [`dot_config/neofetch/`](dot_config/neofetch/) round out the
  terminal-centric media and system-info stack.

### Window Manager And Desktop UI

- [`dot_xinitrc.tmpl`](dot_xinitrc.tmpl),
  [`dot_Xresources.tmpl`](dot_Xresources.tmpl), and
  [`dot_Xmodmap`](dot_Xmodmap) control X startup, DPI, fonts, keyboard
  remaps, and wallpaper theming.
- [`scripts/executable_apply-desktop-display-layout`](scripts/executable_apply-desktop-display-layout)
  saves the three-monitor desktop order used by i3: 2048px left, 4K
  middle, and 1080p right.
- [`media-screensaver`](scripts/executable_media-screensaver) adds a separate
  X11 conveyor across all three live outputs. Install with
  `./scripts/executable_media-screensaver install`, enable its local browser
  extension, then run `~/scripts/media-screensaver service` for a supervised idle monitor
  or `preview` (fish abbreviation `ss`, i3 **Alt+Shift+S** or **Super+Shift+S**) for immediate playback. i3 starts the service at login, and systemd
  restarts it after an exit. `daemon` remains available in the foreground.
  Each launch fills all three outputs with random photos/videos, then advances
  the conveyor every ten seconds.
  `--media DIR` selects a recursive photo/video library; `--seconds N` bounds a
  preview; `--report PATH` records item IDs/timestamps; `--plain` and `--details`
  control output. `status`, `probe` and `demo` expose browser coverage, codec
  checks and disposable media. Video orientation metadata is honored automatically;
  `orient` opens a separate review chooser, or `orient --file FILE` reviews one video
  and saves a private additional rotation without rewriting the original.
  Automatic activation waits five idle minutes and
  fails closed when Chrome video coverage is unavailable. See
  [installation, browser enablement and limitations](docs/media-screensaver.md).
- [`flavibot-browser`](scripts/executable_flavibot-browser) opens the FlaviBot
  music player in Chrome with a separate `~/.local/share/flavibot-chrome` data
  directory. Run `~/scripts/flavibot-browser` after `refresh-config`, then sign
  in once in that window. It takes no arguments and reuses that directory on
  later launches. Regular Chrome profile-picker profiles do not isolate media
  players. Reserve this window for FlaviBot; use your ordinary Chrome window
  for YouTube and other sites. See the [short usage guide](docs/flavibot-browser.md).
- The middle 4K music block uses
  [`now_playing_mpris`](dot_config/i3blocks/scripts/executable_now_playing_mpris)
  to follow only the dedicated FlaviBot browser, with Spotify fallback.
  Playing tracks take precedence over paused tracks; FlaviBot wins ties. It polls
  every five seconds using Python 3 and systemd's `busctl` with JSON support.
  The helper resolves each browser's D-Bus owner to its process and checks the
  exact dedicated data directory. Ordinary Chrome media, including YouTube, is
  ignored even when playing while FlaviBot is paused. If Spotify is playing and
  FlaviBot is paused, Spotify appears; with both paused, FlaviBot appears.
  No artist/title regex is required, so title-only songs remain eligible.
  With no eligible player, the block clears. Titles are displayed in full.
  Playing tracks use a compact, optically raised `▶`; paused tracks use the
  matching `‖` marker.
  This isolates the browser process, not websites within it: keep YouTube out
  of the dedicated FlaviBot window. No Discord bot or token is needed.
  Left/middle/right clicks control the displayed player when supported; stale
  or changed-track clicks do nothing. Global media keys remain Spotify-specific.
  The helper has no CLI options; run
  `~/.config/i3blocks/scripts/now_playing_mpris` to inspect its three-line output.
  `NOW_PLAYING_COLORS_FILE` overrides the pywal palette path for diagnostics;
  click state is private under `${XDG_CACHE_HOME:-~/.cache}/i3blocks/`.
  Apply tracked changes with `refresh-config` and restart i3 in place to reload
  the bar command. See the [desktop smoke checks](docs/smoke-tests.md).
- [`dot_config/i3/config.tmpl`](dot_config/i3/config.tmpl) is the main
  desktop control plane for workspace movement, app assignments,
  launcher bindings, display and audio shortcuts, and layout control.
  Hold **Super** (Windows key) or **Alt+Super** and press **1–9, then 0** for Redshift temperatures
  of **1800K, 2300K, 2850K, 3350K, 3900K, 4400K, 4950K, 5450K, 6000K, and 6500K**.
  Even kelvin steps span 1800–6500 K, rounded to the nearest 50 K.
  **Super+0** selects 6500 K. **Super+grave** or **Alt+Super+grave** removes the filter. **Alt+number** still switches workspaces;
  **Right Alt** (X11 keycode **108**, `Alt_R` in `Mod1`) uses the same **1–9, 0** shortcuts for workspaces **1–10**.
  **Super+F11** selects workspace 11.
  **Ctrl+Alt+Up/Down** increases/decreases temperature by **250 K** (cooler/warmer),
  bounded at 1000–6500 K. Presets, `rds`, `rx` and login share the saved temperature.
  The first adjustment defaults to 6500 K if no value has been saved; direct
  external Redshift commands are not tracked.
  Successful helper operations show **🌡️ Redshift — 2100 K** (using the applied
  temperature) in Dunst. Rapid adjustments edit the same two-second popup in place;
  missing or failed notifications never fail the temperature change.
- [`dot_config/i3blocks/`](dot_config/i3blocks/) plus
  [`dot_config/dunst/dunstrc`](dot_config/dunst/dunstrc) and
  [`dot_config/picom/picom.conf`](dot_config/picom/picom.conf) cover the
  status-bar, notification, and compositing layer.

### Productivity, File Management, And Scripts

- [`scripts/hdd-init-wizard.sh`](scripts/hdd-init-wizard.sh) provides an
  interactive, explicitly confirmed GPT/ext4 initialization path for a USB
  SATA disk. Run `bash scripts/hdd-init-wizard.sh --dry-run` first; then run
  `bash scripts/hdd-init-wizard.sh` as your normal user to select a disk.
  The wizard uses `sudo` for disk and fstab changes and never installs packages.
- [`yt-dl`](scripts/executable_yt-dl) downloads one YouTube video with audio at
  yt-dlp's best available quality, without a resolution cap or MP4 preference.
  Downloads default to `/mnt/linux-files-3/yt-vids`; override with `-o DIR`.
  Uses lowercase kebab-case title-only filenames without IDs or JSON sidecars.
  Shows live download percentage, speed, and ETA, then
  immediately checks the saved resolution/frame rate against fresh formats and
  reports whether 4K was verified;
  see [usage, dependencies, and offline/live checks](docs/yt-dl.md).
- [`dot_taskrc`](dot_taskrc) and [`dot_taskopenrc`](dot_taskopenrc) set
  up Taskwarrior and Taskopen with contexts, urgency tuning, sync
  targets, and note workflows.
- [`dot_config/ranger/`](dot_config/ranger/) contains the file-manager
  workflow, including custom commands, preview logic, plugins, and the
  shared key-mapping layer generated from the aliases templates.
- [`scripts/`](scripts/) holds the automation layer behind the desktop:
  wallpaper shuffling, `dmenu` helpers, audio sink changes, pass
  integration, backups, package installation, and small terminal
  utilities.
- [`dot_config/chezmoi/chezmoi-template.toml.tmpl`](dot_config/chezmoi/chezmoi-template.toml.tmpl)
  is the host-data entrypoint for machine-specific toggles that feed
  template logic across the repo.

That broader dotfiles surface is still substantial, but the README stays
centered on the four-Codex operating environment because that is the
most distinctive and actively evolving part of the repo right now.

### Desktop notification text

Dunst uses Hack Nerd Font Mono 23.25 pt, 1.5 times the previous 15.5 pt. After refresh-config, run `~/scripts/codex-notification-activate` to restart Dunst, then `~/scripts/notification-font-test` for Codex and Discord sample popups with large text throughout. Notifications render about 669 px wide on the current 135-DPI desktop (467 logical pixels plus frame and automatic scaling). Height follows the text up to 600 logical pixels, preserving readability rather than forcing a 16:9 crop. Add `--compare` to include the smaller old-size reference. Use `--app codex` or `--app discord` for one sample and `--plain` for ASCII terminal output. Samples last 15 seconds and avoid the codex-kitty audio rule. Requires Python 3 and notify-send; no sudo.

Terminal/Codex popup titles and bodies render `**bold**` as bold text; literal HTML and Markdown inside code remain literal. Run `~/scripts/notification-markdown-test --activate-all` to activate existing reachable Kitty instances and send a native bold sample. Use `--case literal` for escaping/code checks, `--case plain` for plain-text delivery, `--plain` for ASCII output and `--details` for activation diagnostics. New Kitty processes load the callback automatically. This covers strong emphasis rather than full Markdown or other apps' native notifications.

## Migrate an existing private checkout

Use [`migrate-ai-cli-workflow`](scripts/executable_migrate-ai-cli-workflow) to replace `~/linux-config` with an independent HTTPS clone of this repository on `main`. The old checkout and its linked worktrees remain private recovery material; no old Git objects, branches, hooks, or configuration are imported. Review pending edits first, rehearse with disposable fixtures, preview, apply, then verify.

The default and `--dry-run` inspect without writes. `--apply` requires reviewed content hashes supplied through a private `--review` manifest; unreviewed edits stay in the archive. `--state-dir` defaults to `~/.local/state/ai-cli-workflow-migration` (0700). `--verify` checks repository identity, accepted bytes, pending content, local settings, and archived worktree links. `--rollback` uses that recorded directory and refuses to overwrite later edits. After a failed attempt reports rollback, preserve its recovery directory and select a new `--state-dir` for retry; pass that same directory to all later verification/rollback commands. Use `--details` to identify rejected relative paths without printing their contents. `--plain` provides ASCII output; `--details` never prints rendered settings or raw diagnostics.

A review manifest has a `files` object keyed by relative destination path. Each entry contains `sha256` for the reviewed source bytes and `base_sha256` for the sanitized destination (null for a new file). An optional absolute `source` selects a privately prepared, sanitized overlay. Templates and sensitive paths cannot be imported. Hashes bind a human content review; scans do not establish that every possible secret is absent.

The migration extracts missing mail/calendar identity data privately from working local settings, then renders before cutover. Live Git/Codex, Claude integration and mail/calendar files remain local through `migrationPreservedTargets` in untracked chezmoi data. Neutral example configurations, including local project contracts, never replace working private values. Private `migrationOffline` data suppresses external-template network evaluation; installers, externals, and removals stay excluded. Review those hooks individually before any later deliberate use. Backups cover managed files, links and directory modes, not arbitrary installer effects.

No sudo is needed. Live cutover needs write access to the checkout parent, local configuration, and linked worktree Git metadata. It does not commit, push, revoke credentials, or delete the archive. Treat the recovery directory as sensitive. See [migration smoke checks](docs/smoke-tests.md#sanitized-repository-migration) and the [implementation record](plans/migrate-sanitized-repo.md).

For portable home-storage offload, see [the guide](docs/home-storage-offload.md). The reviewed helper requires an explicit `--destination` mount path; machine-specific mount settings stay outside Git.

Migration concurrency checks compare file content and logical index/recovery entries, excluding harmless Git stat-cache refreshes. New private journals retain initial and changed fingerprints; `--details` reports only changed categories/counts. The read-only preview also rejects changes observed during inventory. A clean preview covers its sampled interval; finish or pause other sessions before the live rename. Never bypass a material-change refusal.

## License

This repository is licensed under the [MIT License](LICENSE).

You may use, modify, and redistribute it, including for commercial
work, as long as the copyright and license notice stay with copies or
substantial portions of the material.
