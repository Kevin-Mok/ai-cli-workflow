# KM's Four-Codex Operating Environment

This repo does not just configure Linux. It configures how
AI-assisted engineering runs. Under the usual `chezmoi` dotfiles
surface is a tracked operating layer for Codex: AGENTS files, runtime
defaults, reusable local skills, Graphiti-backed memory, and ExecPlans
designed for parallel terminal-agent work.

For recruiters and AI-native engineers, the point is concrete: this
repo is a public artifact of how I structure leverage. It shows
planning before edits, small reversible diffs, reproducible setup,
durable context across sessions, and verification before claiming work
is done.

<p align="center">
  <img src="media/ai-cli-workflow-samurai.png"
       alt="Multi-agent AI CLI workflow across Codex, Claude, skills, and AGENTS files"
       width="100%">
</p>

## Tech Stack And Why Chosen

| Layer | Repo evidence | Why chosen |
| --- | --- | --- |
| `chezmoi` | [`dot_config/chezmoi/chezmoi-template.toml.tmpl`](dot_config/chezmoi/chezmoi-template.toml.tmpl) | Keeps the environment reproducible across machines instead of trapping setup inside one laptop. |
| Codex CLI and tracked config | [`dot_codex/config.toml`](dot_codex/config.toml) | Versions model, reasoning, trust, MCP, and session defaults so new Codex panes start from repo policy instead of memory. |
| AGENTS instruction chain | [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md), with compact [`AGENTS.md`](AGENTS.md) and [`AGENTS.repo.md`](AGENTS.repo.md) routing layers | Keeps one inspectable policy body for planning, verification, commit hygiene, and docs sync instead of loading duplicated instructions. |
| Claude Code global config | [`dot_claude/CLAUDE.md`](dot_claude/CLAUDE.md.tmpl) and [`dot_claude/settings.json`](dot_claude/settings.json) | Wires `dot_codex/AGENTS.md` into Claude Code globally via `@path` import so both Codex and Claude share the same behavioral baseline without a separate copy. |
| Local skills | [`dot_agents/skills/`](dot_agents/skills/) and [`dot_agents/skills/README.md`](dot_agents/skills/README.md) | Packages recurring jobs into reusable local capabilities shared across Codex (`~/.agents/skills/`) and Claude Code (`~/.claude/skills/<name>/` directory symlinks) via a post-apply chezmoi script. |
| Graphiti MCP with Neo4j | [`dot_codex/config.toml`](dot_codex/config.toml), [`scripts/executable_codex`](scripts/executable_codex), and [`docs/graphiti-mcp-codex.md`](docs/graphiti-mcp-codex.md) | Adds a retrievable memory layer for multi-session work where provenance and evolving context matter. |
| Shell and terminal tooling | [`dot_config/fish/config.fish.tmpl`](dot_config/fish/config.fish.tmpl), [`dot_tmux.conf`](dot_tmux.conf), [`dot_config/st/config.def.h.tmpl`](dot_config/st/config.def.h.tmpl), [`dot_config/kitty/kitty.conf`](dot_config/kitty/kitty.conf), and [`dot_config/i3/config.tmpl`](dot_config/i3/config.tmpl) | Optimizes for terminal-first execution and multiple parallel panes, with `kitty` as the default terminal, `st` kept ready as the low-friction alternate, and tmux handling the heavier session workflow. |
| Python and Bash automation | [`scripts/`](scripts/) and [`dot_config/fish/functions/refresh-config.fish`](dot_config/fish/functions/refresh-config.fish) | Keeps repeatable operations small, inspectable, and version-controlled instead of burying them in chat or muscle memory. |
| Markdown, Obsidian, and deterministic Python | [`second-brain/`](second-brain/), [the session skill](dot_agents/skills/second-brain-session/SKILL.md), and [the command package](scripts/second_brain/) | Makes personal and project context reviewable across Codex and Claude while keeping private raw capture outside Git, confirmation-gating public event writes, and enforcing schema, containment, approval, and retry-safe checks at each mutation boundary. |

## Table Of Contents

- [Operating Model At A Glance](#operating-model-at-a-glance)
- [AI Layer Highlights](#ai-layer-highlights)
- [Core Components](#core-components)
- [Second Brain Context Layer](#second-brain-context-layer)
- [Graphiti Memory Layer](#graphiti-memory-layer)
- [Install And Bootstrap](#install-and-bootstrap)
- [Day-to-Day Use](#day-to-day-use)
- [Core Command Reference](#core-command-reference)
- [Reproducibility Through Chezmoi](#reproducibility-through-chezmoi)
- [Rest Of Repo](#rest-of-repo)
- [License](#license)

## Operating Model At A Glance

The screenshot above is the workflow. The most distinctive part of this
repo is the tracked operating surface highlighted by the left-side tree:

```text
AGENTS.md
AGENTS.repo.md
dot_codex/
dot_agents/
plans/
second-brain/
```

Those paths define how the AI layer behaves:

- [`AGENTS.md`](AGENTS.md) and [`AGENTS.repo.md`](AGENTS.repo.md) are
  compact compatibility layers that route assistants to one policy body.
- [`dot_codex/AGENTS.md`](dot_codex/AGENTS.md) is the canonical merged
  instruction document that pushes Codex toward plan-first,
  verification-heavy engineering behavior.
- [`dot_codex/config.toml`](dot_codex/config.toml) tracks model,
  reasoning, trust boundaries, MCP servers, and repo-specific developer
  instructions.
- [`dot_agents/skills/`](dot_agents/skills/) packages recurring work
  into reusable local capabilities.
- [`plans/`](plans/) is where non-trivial work becomes explicit,
  checklisted, and reviewable under the
  [ExecPlan contract](.agent/PLANS.md).
- [`second-brain/`](second-brain/) is the public-sanitized Markdown context
  layer. Private raw events and migration ledgers stay in XDG state instead of
  entering the repository.

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
- The Second Brain turns one confirmed ExampleProject outcome, deterministic
  session capture, boss-readable closeout, and copy-first migration into a
  tested cross-agent workflow instead of another unstructured note dump.

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
- Failing reproducers before bug fixes so changes are grounded in
  observed behavior instead of guesswork.
- Living postmortems for unexpected task failures so the observed evidence,
  investigation, resolution, and verification remain reviewable in one record.
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
  before committing.
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
Scroll World, UI/UX Pro Max, and Higgsfield through chezmoi externals. Its
daily refresh, bootstrap behavior, upstream links, and explicit authentication
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

- [`ai-workflow-doctor`](dot_agents/skills/ai-workflow-doctor/SKILL.md)
  turns instruction size, duplicate policy, local references, skill-catalog
  drift, and source provenance into deterministic text or JSON evidence. Its
  `--check` mode blocks objective errors while leaving semantic candidates for
  human review.
- [`metaprompt`](dot_agents/skills/metaprompt/SKILL.md) compiles plain-language
  intent into target-aware prompts and reusable `{{variable}}` templates behind
  a strict per-pass `go` gate. Conditional references add hostile-input
  hardening, agent boundaries, media guidance, and judge/rewrite/re-check flows
  while keeping the entrypoint compact.
- [`feedback-memory`](dot_agents/skills/feedback-memory/SKILL.md)
  carries forward durable user corrections through a repo-tracked
  `feedback.log`.
- [`readme-recruiter-sync`](dot_agents/skills/readme-recruiter-sync/SKILL.md)
  hard-gates commit workflows on a README that is still truthful about
  install, usage, command flags, stack rationale, and recruiter-facing
  value.
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

The tracked [Second Brain vault](second-brain/) gives Codex and Claude one
public-sanitized front door for profile context, active projects, curated
resources, and daily summaries. Its PARA-style Markdown remains directly
inspectable, while the shared
[second-brain-session skill](dot_agents/skills/second-brain-session/SKILL.md)
retrieves only the context relevant to the current session.

The engineering boundary matters more than the folder tree:

- raw session events stay in private XDG state with 0700/0600 permissions
- explicit deferred reminders can remain private in an unscheduled someday queue until example-user assigns a future local date
- confirmed tracked writes use exact versioned JSON schemas and stable event IDs
- the first confirmed ExampleProject focus is reused for the day instead of silently
  being replaced
- the doctor checks structure, privacy, ownership, imports, hard links, and LFS
- migration is copy-first, text-only, approval-bound, resumable, and
  checksum-verifiable
- protected upgrades preview one batch approval and make dated exact-byte
  backups without overwriting existing files
- the daily checkpoint refuses a dirty index, freezes and scans only the vault
  and Codex-config allowlist, uploads reachable Git LFS objects explicitly,
  and pushes only the current branch's exact configured-upstream ref without
  local hooks or unrelated tags
- an opt-in persistent systemd user timer runs that checkpoint at 16:20 local
  time and catches up after sleep or downtime without requiring sudo

This layer links to the existing canonical owners for preferences, lessons,
plans, tasks, and temporal memory; it does not duplicate them. The full
privacy, migration, recovery, and exit-code contract is in the
[Second Brain operator guide](docs/second-brain.md).

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

Treat this repository as the source of truth for most of the environment
layer, with one explicit exception: `refresh-config` snapshots the live Codex and Git configs back into the repo before running `chezmoi apply`.

1. Edit the tracked source files in this repo when the repo-managed copy
   is meant to stay authoritative.
2. Preview the resulting home-directory diff with
   `chezmoi -S "$PWD" diff`.
3. Run `refresh-config` when you want to capture the current live `~/.codex/config.toml` into `dot_codex/config.toml` and `~/.gitconfig` into `dot_gitconfig.tmpl`, then reapply the rest of the chezmoi-managed environment and generated shortcuts in one step.
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

## Core Command Reference

These are the core entrypoints the README depends on. The flags and
options listed below are verified against local CLI help or script
source in this repo.

| Command | When to use it | Flags and options that matter |
| --- | --- | --- |
| `chezmoi -S "$PWD" diff` | Preview what the checked-out source tree would change in `$HOME`. | `-S` / `--source` points chezmoi at this clone instead of the default source directory. `--reverse` flips the diff direction when you need the comparison the other way around. |
| `chezmoi -S "$PWD" apply -n -v` | Dry-run an apply with extra detail before touching files in `$HOME`. | `-S` / `--source` uses this repo as the source state. `-n` / `--dry-run` previews changes without writing them. `-v` / `--verbose` prints more detail. |
| `chezmoi -S "$PWD" apply` | Apply the tracked source state from this clone into `$HOME`. | `-S` / `--source` uses this repo as the source state. `-P` / `--parent-dirs` is useful when you apply a nested target and also want its parent directories handled. |
| `refresh-config` | Snapshot the live Codex and Git configs into the repo, force-apply those exact targets without prompts, then reapply the remaining chezmoi-managed environment layer. | No user-facing flags. It calls `snapshot-codex-config`, copies `~/.gitconfig` into its tracked source, force-applies only those two targets, runs non-interactive `chezmoi apply --no-tty --keep-going` for every other target, syncs shortcuts, and returns a partial-refresh status instead of waiting when a locally modified target needs a decision. |
| `sync-superpowers-release` | Refresh the externally managed `obra/superpowers` skill bundle from the latest GitHub release archive through chezmoi. | `--dry-run` previews the release refresh without writing files. `LINUX_CONFIG_SOURCE` points the helper at this repo when it is not checked out at `$HOME/linux-config`. |
| `sync-design-skills` | Refresh the managed public design skill sources and update UI/UX Pro Max. | `--dry-run` previews the external refresh without updating UI/UX Pro Max. `--bootstrap` installs UI/UX Pro Max on a fresh host. It never authenticates accounts, generates media, spends credits, or upgrades the Higgsfield CLI. |
| `setup-design-skills-timer` | Validate, enable, or disable the daily 05:00 design-skill refresh timer. | Exactly one of `--check`, `--enable`, or `--disable` is required. `--enable` validates and activates the `Persistent=true` user timer without sudo. |
| `setup-superpowers-release-timer` | Validate, enable, or disable the optional user-scoped release-sync timer. It runs daily at 05:00 local time and catches up missed runs with `Persistent=true`; no sudo is required. Refreshed skills are picked up by newly started Codex sessions; already-running sessions remain unchanged until restarted. | Timer setup requires the standard `$HOME/linux-config` checkout. Exactly one of `--check`, `--enable`, or `--disable` is required. `--check` validates the managed sources and installed units without changing state; `--enable` applies and activates the timer; recovery-oriented `--disable` stops it without needing chezmoi or a source checkout. |
| `./scripts/executable_ai-workflow-doctor` | Audit the repo's AI instruction and skill surface, or capture a stable before/after measurement for workflow optimization. | `--repo PATH` selects the repository. `--format text\|json` selects human or machine output. `--snapshot PATH` writes a deterministic JSON baseline; `--compare PATH` compares the current report with one. `--verify-sources` resolves declared local source archives when available. `--check` exits nonzero for objective errors while review findings remain non-blocking warnings. |
| `./scripts/executable_apply-pywal-theme <wallpaper>` | Regenerate the active `pywal` theme through the repo-owned wrapper so wallpaper changes also refresh kitty and the i3 color resources this repo depends on. | Pass an image path directly, or pass raw `wal` flags when you need that lower-level control. The wrapper runs `wal --saturate 0.8 -e`, reloads Xresources, refreshes running kitty windows when the socket is available, and regenerates the derived i3 palette file. |
| `./scripts/executable_install-chatgpt-linux` | Download and install the official ChatGPT desktop app package for a supported Linux desktop. | No flags. Supports Ubuntu 24.04/26.04, Debian 13, and Fedora 43/44 on x64 or ARM64. It prints the selected official package URL, then prompts for sudo only to run `apt install` or `dnf install`. |
| `./scripts/executable_install-tmux-tpm.sh` | Install or fast-forward the TPM plugin manager, correct the tracked tmux bootstrap path when needed, and reload an active tmux server. | `--help` prints usage. With no flags, it clones or fast-forwards TPM under `~/.tmux/plugins/tpm`; restart tmux if no server is active, then press `prefix + I` to install plugins. |
| `./scripts/executable_screenshot-all-monitors` | Save one combined `scrot` capture of the full X virtual desktop, covering every active monitor in one image. | No flags. Saves to `/home/example/Pictures/screenshots/desktop/unsorted/screenshot-YYYY-MM-DD_HH:MM:SS.png`. `SCREENSHOT_ALL_MONITORS_DIR`, `SCREENSHOT_ALL_MONITORS_SCROT`, and `SCREENSHOT_ALL_MONITORS_DATE` override the destination, capture binary, and timestamp binary for tests or alternate hosts. |
| `./scripts/executable_setup-st.sh` | Render the tracked `st` config, sync it into your `st` source checkout, and install the compiled terminal you actually want to use. | `--source-dir` points the script at a non-default `st` checkout path. `--skip-install` only refreshes `~/.config/st/config.def.h` plus the source-tree `config.def.h` and prints the exact `sudo make -C ... install` command instead of running it. `--clone-if-missing` clones the official upstream source from `https://git.suckless.org/st` into the target checkout path before syncing and building. |
| `./scripts/executable_setup-aerc-mail.sh` | Install aerc mail prerequisites or add one Gmail/Outlook.com account at a time without storing addresses, app passwords, client IDs, or OAuth tokens in Git. | `--install` may prompt for sudo to install shared packages. `--init-pass GPG_KEY_ID` initializes an empty password store. `--add-gmail` prompts for a Gmail app password; `--add-outlook` prompts for a Microsoft app client ID and launches device-code OAuth; `--status` checks configured accounts without printing credentials; `--dry-run` previews write actions without changing files or starting OAuth. |
| `sudo ./scripts/executable_setup-neovim-python-completion.sh` | Upgrade Neovim from Ubuntu's older package, install the repo's `vim-plug` Neovim stack including `nvim-lspconfig`, and install the Python language server used for strong completion and signature help. | `--neovim-version` pins a different official release. `--skip-plugins` skips `vim-plug` bootstrap and `PlugInstall`. `--skip-lsp` skips `uv tool install --upgrade basedpyright`. |
| `sudo ./scripts/executable_update-chrome.sh` | Check the installed Google Chrome apt package version and upgrade it when the Google repo has a newer build. | `--check` prints the installed and candidate versions without modifying the system. With no flags, the script refreshes apt metadata and upgrades only `google-chrome-stable` when needed. |
| `"$HOME/scripts/codex"` or `codex` when that wrapper wins on `PATH` | Start Codex in the repo so the tracked instruction chain and config take effect. The repo wrapper also ensures the Graphiti sidecar command is running first. | `-C` / `--cd` sets the repo root when you launch from another directory. `--search` enables live web search for tasks that need current external information. `CODEX_WRAPPER_GRAPHITI_CWD` and `CODEX_WRAPPER_STATE_DIR` override the wrapper's Graphiti checkout path and state directory. |
| `codex mcp list --json` | Verify which MCP servers Codex is loading from the tracked config. | `--json` emits machine-readable output that is easier to inspect or diff. |
| `second-brain status` plus `capture`, `focus`, and `closeout` | Retrieve targeted context, keep raw session text private, and persist only explicitly confirmed public-safe focus or closeout records. | `status --format text\|json`; `capture --kind raw-session\|personal-decision --payload PATH_OR_DASH`; `focus --payload PATH_OR_DASH`; `closeout --payload PATH_OR_DASH`. Payload shapes live in the [routing reference](dot_agents/skills/second-brain-session/references/routing.md). |
| `second-brain doctor` | Audit the tracked vault for structure, privacy, ownership, import-frontmatter, hard-link, and Git LFS errors without mutating it. | `--format text\|json` selects output. `--check` exits 1 when objective errors exist. |
| `second-brain migrate` | Inventory and plan selected external text, copy one explicitly approved batch into the archive, or verify its private resume ledger. | Subcommands are `inventory --source PATH` with repeatable absolute roots, `plan --inventory PATH`, `apply --plan PATH --approve SHA256`, and `verify --ledger PATH`. Follow [the copy-first procedure](docs/second-brain.md#copy-first-text-migration); no initial migration is automatic. |
| `second-brain upgrade` | Preview append-only protected-vault changes and exact-byte dated backups. | `--dry-run` prints the current batch and approval SHA. `--apply --approve SHA256` accepts only that unchanged batch; the current schema-v1 preview has zero pending operations. |
| `snapshot-codex-config` | Validate and atomically copy the live `~/.codex/config.toml` into its exact chezmoi source target. | `--dry-run` validates regular-file ownership, the strict 1,000,000-byte boundary, TOML, likely-secret content, target mapping, and filesystem boundaries without changing the tracked target. Checkpoint callers additionally bind that target to their exact repository. |
| `second-brain checkpoint` | Validate and ship one allowlisted daily Second Brain/Codex-config checkpoint on the current branch. | `--dry-run` performs candidate preflight without staging, committing, or pushing; it does not prove the later immutable-tree or shipping gates. `--no-push` commits after all gates but leaves the commit local. With no flags, the command explicitly uploads reachable LFS objects and pushes only the exact configured-upstream ref without local hooks, tags, or force. |
| `setup-second-brain-timer` | Validate, enable, or disable the persistent 16:20 systemd user checkpoint timer without sudo. | Exactly one of `--check`, `--enable`, or `--disable` is required. `--enable` applies the launcher, exact runtime-package modules, and two unit targets before daemon reload and activation; unexpected package-root files, directories, or symlinks fail closed, while an owned real `__pycache__` directory is allowed. Recovery-oriented `--disable` does not require chezmoi or a source checkout. |

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
- [`dot_config/fish/config.fish.tmpl`](dot_config/fish/config.fish.tmpl)
  is the main interactive shell setup and loads the large helper surface
  under [`dot_config/fish/functions/`](dot_config/fish/functions/).

### Editor, Terminal, And Media

- [`dot_config/kitty/kitty.conf`](dot_config/kitty/kitty.conf)
  is the default terminal config, and the i3 bindings now open `kitty`
  first so normal shells plus the Codex launcher use the feature-rich
  terminal path by default. [`dot_config/st/config.def.h.tmpl`](dot_config/st/config.def.h.tmpl)
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
  mappings that push selections to `xclip`. Use
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
- The middle 4K music block uses
  [`now_playing_mpris`](dot_config/i3blocks/scripts/executable_now_playing_mpris)
  to follow Chrome/Chromium media (including FlaviBot), with Spotify fallback.
  Playing tracks take precedence over paused tracks; Chrome wins ties. It polls
  every five seconds using Python 3 and systemd's `busctl` with JSON support
  (both available on this Ubuntu desktop). No Discord bot or token is needed.
  Chrome media qualifies when it has artist metadata or a title containing
  nonempty text on both sides of `-`, `–`, or `—` (spaces optional). This lenient
  format filter allows some non-music videos; songs with neither artist metadata
  nor a matching title cannot be recognized. Spotify still accepts title-only
  metadata. Nonmatching Chrome sessions allow another eligible player to appear;
  with none, the block clears. Matching labels are shown in full, without truncation.
  Chrome exposes its selected media session, so other tabs can replace FlaviBot.
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
- [`dot_config/i3blocks/`](dot_config/i3blocks/) plus
  [`dot_config/dunst/dunstrc`](dot_config/dunst/dunstrc) and
  [`dot_config/picom/picom.conf`](dot_config/picom/picom.conf) cover the
  status-bar, notification, and compositing layer.

### Productivity, File Management, And Scripts

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

## License

This repository is licensed under the [MIT License](LICENSE).

You may use, modify, and redistribute it, including for commercial
work, as long as the copyright and license notice stay with copies or
substantial portions of the material.
