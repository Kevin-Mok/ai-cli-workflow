# Second Brain Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` or
> `superpowers:executing-plans` to execute this plan task by task. Every
> behavior-changing slice uses RED, GREEN, and regression evidence before it is
> committed.

**Goal:** Add a safe, personalized, plain-Markdown Second Brain to this
repository with deterministic capture, protected migration, cross-agent session
routines, and a 4:20 PM Git checkpoint.

**Architecture:** A thin `scripts/executable_second-brain` entrypoint delegates
to cohesive standard-library Python modules under `scripts/second_brain/`. A
compact repo-tracked skill routes Codex and Claude sessions to the command and
the existing canonical memory owners. Private raw capture lives under the XDG
state directory; only confirmed, sanitized material enters the tracked vault.

**Tech Stack:** Python 3 standard library, Markdown/YAML frontmatter, Git and
Git LFS, chezmoi, Fish, systemd user units, `unittest`, and shell contract tests.

## Global Constraints

- Keep `dot_codex/AGENTS.md` as the only canonical AI policy body and keep the
  root `README.md` recruiter/operator-first.
- Do not create or use a Git worktree.
- Treat the tracked repository as public. Never track raw conversations,
  credentials, proprietary source, or sensitive relationship/health details.
- Copy only explicitly selected regular text files strictly smaller than
  1,000,000 bytes. Reject binary files, nested Git repositories, containment
  cycles, symlink escapes, hard-link surprises, secrets, caches, logs, and app
  data.
- Preserve source files literally. Migration is copy-only and checksum-tracked.
- Use `America/Toronto` for default note dates with explicit test overrides.
- Lock mutations, write atomically, preserve frontmatter and section order, and
  make identical capture/closeout event IDs idempotent.
- Keep raw session capture under `${XDG_STATE_HOME:-$HOME/.local/state}` with
  private permissions. It is never staged by the checkpoint.
- Configure Git LFS for future manually selected media, but import no binary
  attachments during initial setup.
- Never run the real config snapshot or real checkpoint during implementation.
  All tests use temporary fixtures and local fake Git remotes.
- Enable the timer only after all implementation commits pass verification and
  are pushed. A `Persistent=true` catch-up is a separate runtime checkpoint.
- Record MIT provenance for `/home/example/coding/second-brain-setup` revision
  `90584269f7a4a47ea19f85a9029246873365aaf8` beside adapted material.
- Keep matching ExecPlan, tests, operator docs, smoke checks, and README changes
  in the same commits as the behavior they describe.

---

## Purpose And Observable Outcome

The completed system gives example-user one command and one shared Codex/Claude skill
for targeted context retrieval, private raw capture, confirmed tracked capture,
daily ExampleProject closeout, vault health checks, safe migrations, and protected
upgrades. Each morning the workflow proposes exactly one measurable ExampleProject
outcome with a completion criterion and evidence location. Each natural session
end drafts one nontechnical boss-readable progress record and waits for
confirmation before tracked writes.

At 16:20 local time, a systemd user timer validates the current branch and
upstream, refuses an already-dirty index, snapshots the live Codex config through
the same helper used by `refresh-config`, validates the vault and staged content,
stages only the approved allowlist, freezes and validates an immutable tree,
commits that exact tree when needed, explicitly uploads reachable Git LFS
objects, and pushes only the exact configured-upstream ref without local hooks
or unrelated tags. It never switches branches, pulls, rebases, resets, amends,
force-pushes, or consumes unrelated staged work.

## Current Context And Protected State

- Repository: `/home/example/linux-config`
- Branch: `feat/ai-workflow-optimization`
- Baseline HEAD: `d529decf48504f53825e2d977f50d1c8675bd454`
- Upstream: `origin/feat/ai-workflow-optimization`
- Approved design date: `2026-07-14`
- Baseline `dot_codex/config.toml` SHA-256:
  `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`
- Baseline relevant tests: AI workflow contract 11 passed, doctor 17 passed,
  context handoff 6 passed, refresh-config fixture passed, Claude links passed,
  and Codex wrapper passed.
- Git LFS 3.4.1 and a running systemd user manager are available.

The following paths were dirty before implementation and are user-owned. Do not
stage their pre-existing hunks; where this task also needs a file, isolate and
stage only the Second Brain hunk after inspecting the staged diff:

```text
README.md
docs/ai-workflow-optimization.md
docs/smoke-tests.md
dot_agents/skills/README.md
dot_agents/skills/metaprompt/SKILL.md
dot_agents/skills/metaprompt/agents/openai.yaml
dot_agents/skills/metaprompt/references/compilation-rules.md
dot_agents/skills/metaprompt/references/examples.md
dot_agents/skills/metaprompt/references/execution-routing.md
dot_codex/config.toml
tests/test_metaprompt_contract.py
dot_agents/skills/metaprompt/LICENSE.txt
dot_agents/skills/metaprompt/SOURCE.md
dot_agents/skills/metaprompt/references/model-profiles.md
plans/unify-metaprompt-skill.md
```

Before every implementation commit, re-run `sha256sum dot_codex/config.toml`,
compare it to the baseline above, inspect `git diff --cached --name-only`, and
prove no metaprompt or other pre-existing hunks are staged.

## Scope Boundaries And Non-Goals

In scope:

- The approved `second-brain/` Markdown and Obsidian-compatible tree.
- One compact `second-brain-session` skill shared through existing Codex/Claude
  installation wiring.
- Deterministic capture, closeout, status, doctor, checkpoint, migration, and
  protected-upgrade interfaces.
- A reusable noninteractive Codex-config snapshot helper.
- Git LFS attributes and validation for future attachments.
- Chezmoi-managed systemd user service/timer and an idempotent setup/check tool.
- Tests, public/operator documentation, smoke checks, and runtime activation.

Not in scope:

- A new database, MCP service, cloud sync provider, web UI, or Obsidian plugin.
- Automatic copying of current journals, Drive material, pictures, or code.
- Binary attachment import during this implementation.
- Automatic promotion of interests into projects or tasks.
- Global interception of online ChatGPT conversations; those require explicit
  export/import.
- Moving, editing, deleting, or auto-merging any migration source.

## Settled Decisions

- Vault language is compact, direct English with scannable technical detail.
- Public profile: education-AI developer, former Example Employer intern, University of
  Toronto CS graduate (3.84 GPA), and AI-native workflow builder. Do not publish
  the private framing that example-user has not directly read code for about one year.
- Active projects are Linux Config AI Workflow, ExampleProject, and Beginner Python
  Teaching Sites. Interests remain resources unless example-user approves promotion.
- Areas are Work and Career, AI Workflow, Teaching, Wellbeing, and Relationship.
- Resources remain flat until content justifies subfolders.
- Obsidian is enabled with Hack, black surfaces, restrained red accents, and no
  Example Employer logo or implied affiliation.
- Initial migration is preview-only. Eligible future imports are explicit text
  selections under 1,000,000 bytes; `/home/example/coding` remains reference-only.
- Eligible migration content maps by default into
  `06 Archive/Imports/SANITIZED_SOURCE`. Inventory, plan, and apply each
  recheck source policy; one SHA-256 approves the complete inspected batch.
- Migration resume state is private 0700/0600 XDG state, not a tracked vault
  artifact. New imports use descriptor-relative, no-follow, atomic
  no-overwrite creation and verification fails while any ledger entry is
  pending.
- Migration inventory and plan controls stay in a private mode-0700 state
  directory, are created under `umask 077`, and never enter Git.
- Protected upgrades use immutable append-only specifications, one batch
  approval, exact-byte dated backups, and atomic no-overwrite creation. The
  complete schema-v1 vault has no pending default upgrade.
- Task 3 configures Git LFS attributes for future explicit media imports; the
  tracked LFS object set remains empty until such an import is approved.
- Raw available session text is local/private and secret-redacted; confirmed
  sanitized summaries alone may enter Git.
- Daily briefing contains one confirmed measurable ExampleProject outcome. Closeout
  records planned, completed, evidence, and blocker in boss-readable language.

## Memory Ownership

| Information | Canonical owner | Second Brain behavior |
|---|---|---|
| Durable workflow/style preference | `dot_agents/skills/feedback-memory/feedback.log` | Link or short navigation summary only |
| Repo engineering lesson | `tasks/lessons.md` | Link only |
| Implementation state/decision/evidence | `plans/` | Project note links to the plan |
| Bounded continuation artifact | `context-handoff` | Link to the handoff owner |
| Temporal fact/relationship | Graphiti | Do not duplicate the record |
| Actionable task and task note | Taskwarrior/Taskopen | Daily note may link to the task |
| Profile, PARA navigation, Inbox, daily summary, curated context | `second-brain/` | Canonical here |

## Adoption Record

| Source capability | Decision | Target owner and adaptation |
|---|---|---|
| Resumable onboarding | adapt | This ExecPlan replaces `setup-progress.md` |
| PARA Context/Inbox/Projects/Areas/Resources/Archive | adopt | `second-brain/` |
| Session start/during/end and Daily Notes | adapt | Shared skill plus deterministic command |
| Decisions/learnings/preferences/progress | adapt | Route through the ownership table |
| One-command capture and retrieval | adopt | `second-brain` CLI |
| Claude/Codex shared behavior | adapt | Existing skill install/link wiring |
| Copy-first migration | adapt | Text-only, approved-plan hash, ledger, checksums |
| Protected reruns/upgrades | adopt | Preview, approval hash, dated backups |
| Doctor | adapt | Compose with existing AI workflow doctor |
| Obsidian | adopt | Minimal tracked config; device state ignored |
| Git history/backup/restore | adapt | Existing repo plus safe systemd checkpoint |
| Portable names/frontmatter | adopt | Deterministic sanitizer and schema tests |
| Duplicated AGENTS/CLAUDE/README policy | reject | Canonical AGENTS and recruiter README remain |
| Second preference/lesson/plan/task/temporal store | reject | Existing canonical stores remain |
| Untested source assertions | reject | Local fixtures and observable checks required |
| Additional database or MCP | reject | Markdown plus existing Graphiti are sufficient |

## File And Interface Map

### Exact tracked vault manifest

The approved initial tree contains exactly these regular files. No imported
content or binary attachment is part of Task 1:

- second-brain/README.md
- second-brain/.obsidian/.gitignore
- second-brain/.obsidian/app.json
- second-brain/.obsidian/appearance.json
- second-brain/.obsidian/snippets/example-user.css
- second-brain/00 Context/About Me.md
- second-brain/00 Context/Writing Style.md
- second-brain/00 Context/Memory Map.md
- second-brain/00 Context/Decisions.md
- second-brain/00 Context/Learnings.md
- second-brain/00 Context/AI Workflow.md
- second-brain/00 Context/Audience and Privacy.md
- second-brain/00 Context/External Locations.md
- second-brain/01 Inbox/Brain Dump.md
- second-brain/02 Projects/Linux Config AI Workflow.md
- second-brain/02 Projects/ExampleProject.md
- second-brain/02 Projects/Beginner Python Teaching Sites.md
- second-brain/03 Areas/Work and Career.md
- second-brain/03 Areas/AI Workflow.md
- second-brain/03 Areas/Teaching.md
- second-brain/03 Areas/Wellbeing.md
- second-brain/03 Areas/Relationship.md
- second-brain/04 Resources/AI Agents and Prompting.md
- second-brain/04 Resources/Education Product Design.md
- second-brain/04 Resources/CEMC Math Contest Prep.md
- second-brain/04 Resources/Beginner Programming Pedagogy.md
- second-brain/04 Resources/Software Architecture and UX.md
- second-brain/04 Resources/Linux Automation.md
- second-brain/04 Resources/Parent Facing Sales and Marketing.md
- second-brain/04 Resources/CBT and Wellbeing.md
- second-brain/05 Daily Notes/2026-07-14.md
- second-brain/06 Archive/README.md
- second-brain/06 Archive/backups/README.md
- second-brain/07 Attachments/README.md
- second-brain/07 Attachments/External Media Index.md

### Vault and skill

- Create the exact approved `second-brain/` tree from the design gate, including
  minimal `.obsidian/` settings and no unresolved placeholders.
- Create `dot_agents/skills/second-brain-session/SKILL.md` as the compact trigger
  and procedure.
- Create `dot_agents/skills/second-brain-session/references/routing.md` for
  payload schemas, owner routing, and daily briefing/closeout shapes.
- Create `dot_agents/skills/second-brain-session/SOURCE.md` with MIT provenance.
- Create `dot_agents/skills/second-brain-session/agents/openai.yaml` with only
  display name, 25-64 character description, and a prompt naming
  `$second-brain-session`.
- Modify `dot_codex/AGENTS.md` with one concise conditional route.

### Command package

- Create `scripts/executable_second-brain` as argument parsing and exit-code
  boundary only.
- Create `scripts/second_brain/cli.py` for command dispatch.
- Create `scripts/second_brain/schema.py` for JSON schema validation and safe
  errors.
- Create `scripts/second_brain/content_security.py` for shared secret-name,
  assignment, and linear netrc detection.
- Create `scripts/second_brain/paths.py` for repo/XDG resolution, containment,
  locks, permissions, and compatibility exports.
- Create `scripts/second_brain/safe_contract.py` for shared filesystem errors
  and lexical containment.
- Create `scripts/second_brain/safe_create.py` for portable exclusive creation
  and ancestor revalidation.
- Create `scripts/second_brain/safe_files.py` for descriptor-relative reads,
  Linux write leases, and checksum-bound atomic exchange.
- Create `scripts/second_brain/state_private.py` for anchored 0700/0600 private
  control-file reads.
- Create `scripts/second_brain/vault.py` for frontmatter, stable sections,
  capture, closeout, and status.
- Create `scripts/second_brain/doctor.py` for stable findings and `--check`.
- Create `scripts/second_brain/doctor_contract.py` for the static vault health
  contract used by the doctor.
- Create `scripts/second_brain/doctor_lfs.py` for Git LFS attribute inspection.
- Create `scripts/second_brain/migration_common.py` for shared source policy,
  canonical JSON, hashing, and no-follow source reads.
- Create `scripts/second_brain/migration_inventory.py` for deterministic,
  content-safe inventory and classification.
- Create `scripts/second_brain/migration.py` for sanitized destination
  planning, signed-plan validation, and stable collision handling.
- Create `scripts/second_brain/migration_apply.py` for all-source preflight,
  exclusive copy, and private resume-ledger updates.
- Create `scripts/second_brain/migration_verify.py` for strict standalone
  ledger validation and source/destination checksum findings.
- Create `scripts/second_brain/upgrade.py` for approval-bound append-only
  upgrades and protected exact-byte backups.
- Create cohesive `scripts/second_brain/checkpoint*.py` modules for Git
  validation, allowlisting, immutable-tree scans, exact commit creation,
  explicit LFS delivery, and isolated exact-ref push.
- Create `scripts/second_brain/config_snapshot.py` for shared live-to-source
  config snapshot behavior.

Stable interface:

```text
second-brain capture --kind KIND --payload PATH_OR_DASH
second-brain focus --payload PATH_OR_DASH
second-brain closeout --payload PATH_OR_DASH
second-brain status [--format text|json]
second-brain doctor [--format text|json] [--check]
second-brain checkpoint [--dry-run] [--no-push]
second-brain migrate inventory --source PATH
second-brain migrate plan --inventory PATH
second-brain migrate apply --plan PATH --approve SHA256
second-brain migrate verify --ledger PATH
second-brain upgrade --dry-run
second-brain upgrade --apply --approve SHA256
```

Every mutation payload has `schema_version`, `event_id`, `source`, and
`timestamp`. Raw-session payloads add `session_id`, `role`, and `text`.
Confirmed vault capture adds `title`, `summary`, `target`, `links`,
`visibility`, and `confirmed: true`. Daily focus adds `date`, the fixed
`ExampleProject` project, `outcome`, `done_when`, `evidence`, and
`confirmed: true`. Closeout adds `date`, `project`, `planned`,
`completed`, `evidence`, `blocker`, `decisions`, `open`, `next`, and
`confirmed: true`.

Task 1 freezes these minimum command boundaries:

- Capture kinds are `raw-session` and `personal-decision`.
- After confirmation, `focus` persists exactly one ExampleProject outcome in the
  Daily Note `Focus` section. The first confirmed focus is canonical for that
  date; repeated event IDs are no-ops and a second outcome is rejected.
- Status JSON contains `schema_version: 1`, the Toronto-local `date`, sorted
  `active_projects`, up to three descending `latest_daily_notes`, and an
  `inbox` object with a count and vault-relative path. Text status exposes the
  same information without a layout-stability promise.
- Success exits 0. Invalid input, schema, confirmation, path, or lock state exits
  2 without payload content. Mutation results are `created`, `updated`, or
  `noop`.
- Raw events live at
  ${XDG_STATE_HOME:-$HOME/.local/state}/second-brain/raw/YYYY-MM-DD.jsonl.
  The raw directory is mode 0700 and event files are mode 0600.
- `SECOND_BRAIN_REPO_ROOT` and `SECOND_BRAIN_NOW` are explicit fixture hooks;
  normal repo resolution accepts the command location only inside a real Git
  source checkout and otherwise uses `chezmoi source-path`. Standard
  `XDG_STATE_HOME`, not a Second-Brain-specific state override, controls state
  and must be absolute, non-symlinked, and outside the source repository/vault.
- Closeout writes the boss-readable result under Daily Note `Done`, confirmed
  decision strings under `Decisions`, blocker/open strings under `Open`, the
  next action under `Next`, and a compact result under ExampleProject `Progress`.
  It is rejected unless `planned` exactly matches that date's confirmed focus.
- The `interface` mapping in skill metadata has exactly display name, short
  description, and default prompt. A separate implicit-invocation policy is
  allowed so both agents can discover the conditional workflow.

### Config snapshot and timer

- Create `scripts/executable_snapshot-codex-config` as the reusable helper
  entrypoint.
- Modify `dot_config/fish/functions/refresh-config.fish` so only its first copy
  step calls that helper; chezmoi apply, shortcut regeneration, and Fish reload
  remain interactive refresh behavior.
- Create `scripts/executable_setup-second-brain-timer` with `--check`,
  `--enable`, and `--disable`.
- Create `dot_config/systemd/user/second-brain-checkpoint.service`.
- Create `dot_config/systemd/user/second-brain-checkpoint.timer` with
  `OnCalendar=*-*-* 16:20:00` and `Persistent=true`.
- Create `.gitattributes` LFS patterns for future attachment images, PDFs,
  audio, and video.
- Modify `scripts/executable_ai-workflow-doctor` to compose Second Brain
  findings without changing existing finding keys.

## Ordered TDD Checklist

### Task 1: Personalized vault and cross-agent session workflow

**Files:** approved `second-brain/` tree,
`dot_agents/skills/second-brain-session/`, `dot_codex/AGENTS.md`,
`scripts/executable_second-brain`,
`scripts/second_brain/{cli,schema,paths,vault}.py`,
`tests/test_second_brain_vault.py`, `tests/test_second_brain_skill.py`,
`tests/test_second_brain_command.py`, `dot_agents/skills/README.md`,
`docs/smoke-tests.md`, and this plan.

**Produces:** tracked vault schema, personalized sanitized notes, the minimum
stable status/capture/closeout command surface, and a shared skill that invokes
only interfaces already present in this commit.

- [x] Run a fresh subagent pressure scenario without the new skill. Record
  whether it duplicates memory owners, silently promotes tasks, or writes a
  closeout without confirmation.
- [x] Initialize a disposable `second-brain-session` skill scaffold under
  `/tmp` with the official skill initializer and inspect its generated shape.
- [x] Write vault contract tests asserting every approved path, required
  frontmatter fields, Daily Note sections, no placeholder tokens, sanitized
  public content, external/private references, and canonical-owner links.
- [x] Write skill contract tests asserting concise frontmatter, source
  provenance, metadata, Codex route, Claude discovery wiring, targeted startup
  reads, one ExampleProject task, private raw capture, confirmed closeout, and no
  session commit.
- [x] Write command tests for caller-independent source/installed discovery,
  Toronto date override, one confirmed daily focus, schema-safe errors, private
  raw capture, confirmed tracked capture, stable note sections, repeated-event
  idempotency, and matching confirmed closeout.
- [x] Run the three focused test modules and observe failure because the vault,
  command, and skill do not yet exist.
- [x] Create the minimum vault, command modules, Obsidian settings, skill,
  routing reference, provenance, metadata, and canonical AGENTS route that
  satisfy the tests.
- [x] Run all three focused tests to GREEN, validate the skill with
  `quick_validate.py`, check `SKILL.md` word count, and forward-test the same
  pressure scenario with the skill present.
- [x] Update the skill index with only this task's hunk, update this plan with
  RED/GREEN evidence, verify the protected config hash, inspect the staged diff,
  and commit `feat(second-brain): add personalized vault and session workflow`.

### Task 2: Deterministic capture, doctor, migration, and protected upgrades

**Files:** `scripts/second_brain/{cli,content_security,paths,safe_contract,
safe_create,safe_files,state_private,vault,doctor,doctor_contract,doctor_lfs,
migration_common,migration_inventory,migration,migration_apply,
migration_verify,upgrade}.py`,
`tests/test_second_brain_command.py`, `tests/test_second_brain_concurrency.py`,
`tests/test_second_brain_doctor.py`,
`tests/test_second_brain_migration.py`,
`tests/test_second_brain_migration_apply.py`,
`tests/test_second_brain_paths.py`, `tests/test_second_brain_upgrade.py`,
`docs/second-brain.md`, `docs/smoke-tests.md`, root `README.md`, and this plan.

**Consumes:** the exact vault paths, skill payload shapes, and core CLI from
Task 1.

**Produces:** the stable CLI except checkpoint, plus operator documentation.

- [x] Write command tests for caller-independent repo discovery, Toronto date
  override, schema errors, safe error text, traversal, symlink escape, invalid
  names, stable frontmatter/sections, atomic writes, lock contention, concurrent
  calls, and repeated-event idempotency.
- [x] Write capture/closeout tests using JSON from files and stdin. Assert raw
  capture uses private XDG state, confirmed capture updates authorized notes,
  and unconfirmed tracked writes fail.
- [x] Write doctor fixture tests for stable finding keys, missing paths,
  malformed frontmatter, placeholders, duplicate ownership content, sensitive
  visibility, and non-LFS attachment media.
- [x] Write migration/upgrade tests for source containment, overlapping source
  roots, nested Git repositories, symlinks, hard links, 1,000,000-byte boundary,
  UTF-8/NUL detection, secrets, deterministic collisions, interrupted resume,
  approval hash, checksum verification, source immutability, protected-file
  preview, and dated backups.
- [x] Run all Task 2 focused tests and observe expected missing-command/module
  failures.
- [x] Implement the smallest cohesive modules and entrypoint that make the
  focused suite GREEN; refactor only after GREEN while keeping modules below the
  repository's cohesion/size threshold.
- [x] Verify `--help`, text/JSON status, capture/closeout idempotency, doctor
  fixtures, and migration fixtures. Do not apply a real migration.
- [x] Add operator/recovery docs and a recruiter-README hunk grounded in actual
  `--help` output. If the pre-existing README hunk overlaps, stop the commit and
  isolate the Second Brain blob/hunk rather than staging user work.
- [x] Update this plan with evidence, verify protected paths and config hash,
  inspect the staged diff, and commit
  `feat(second-brain): add deterministic capture and migration tools`.

### Task 3: Safe config snapshot, checkpoint, LFS validation, and timer

**Files:** `.gitattributes`, `.chezmoiignore`,
`scripts/ai_workflow_second_brain.py`,
`scripts/second_brain/{cli,config_snapshot,checkpoint,checkpoint_contract,
checkpoint_git,checkpoint_scan,migration_common,paths,remove_state,safe_files,
state_private}.py`,
`scripts/executable_snapshot-codex-config`,
`scripts/executable_setup-second-brain-timer`,
`dot_config/systemd/user/second-brain-checkpoint.{service,timer}`,
`dot_config/fish/functions/refresh-config.fish`,
`scripts/executable_ai-workflow-doctor`,
`tests/test_second_brain_config_snapshot.py`,
`tests/test_second_brain_checkpoint.py`,
`tests/test_second_brain_checkpoint_{commit_failure,hook_isolation,journal,
security}.py`, `tests/test_second_brain_timer.py`,
`tests/test_second_brain_{paths,vault}.py`,
`tests/test_refresh_config_function.sh`, `tests/test_ai_workflow_doctor.py`,
`docs/second-brain.md`, `docs/smoke-tests.md`,
`docs/postmortem/2026-07-14-{shell-interpolation-early-push,
timer-runtime-parent-not-installed}.md`, root
`README.md`, `tasks/lessons.md`, and this plan.

**Consumes:** Task 2 doctor and common path/locking primitives.

**Produces:** safe daily Git shipping and final runtime setup.

- [x] Write config-snapshot tests for chezmoi target resolution, regular-file
  checks, TOML validation, expected target mapping, no-content logging, dry run,
  atomic copy, and explicit fixture overrides.
- [x] Extend the refresh-config shell contract test so the shared helper is
  required while apply, shortcut regeneration, and Fish reload remain only in
  the interactive function.
- [x] Write temporary-repository checkpoint tests for lock contention,
  non-worktree/detached/missing-upstream rejection, dirty-index abort, config
  inclusion, stable secret/sensitive-path and LFS rejection, exact allowlist,
  no-op, exact immutable commit tree, explicit reachable-LFS upload, isolated
  exact-ref push, and preserved local commit after upload or ref-push failure.
- [x] Write timer/setup tests for exact 16:20 schedule, `Persistent=true`, no
  sudo, XDG lock, content-safe journal output, exact launcher/runtime-module/
  unit installation, bytecode-cache exclusion, runtime shadow rejection, and
  source-independent disable recovery.
- [x] Run Task 3 focused tests and observe expected missing-helper/module/unit
  failures.
- [x] Implement the shared snapshot helper, Fish integration, cohesive
  checkpoint modules, setup tool, LFS attributes, systemd units, and composed
  doctor behavior.
- [x] Run the Task 3 focused suite to GREEN, then run all Second Brain tests and
  the existing relevant AI workflow/shell regression suite.
- [x] Apply the smoke-test-capture skill to add one-line Action/Expected checks.
  Apply the readme-recruiter-sync gate using verified command help and preserve
  every pre-existing README/smoke hunk.
- [x] Run `git diff --check`, focused and broader test suites, skill validation,
  AI workflow doctor before/after comparison, exact chezmoi dry-runs for every
  installed target, and temporary-repository checkpoint proof.
- [x] Reconcile final diff against the approved tree, ownership, data flow,
  adoption record, and source provenance. Run independent task and whole-change
  reviews; resolve every Critical/Important finding and re-verify.
- [x] Update this plan with final evidence, verify the protected config hash and
  staged allowlist, inspect the complete staged diff, and commit
  `feat(second-brain): add safe daily checkpoint automation`.
- [x] Record that an accidental shell interpolation pushed the already-verified
  Task 1 and Task 2 commits early; do not rewrite published history.
- [x] Push the verified Task 3 commit to the configured upstream and confirm
  local HEAD equals upstream.
- [ ] Only after the push, run `setup-second-brain-timer --enable`, inspect the
  enabled state and next trigger, and handle any persistent catch-up as a
  separate authorized `chore(second-brain): checkpoint 2026-07-14` commit.

### Task 3 activation follow-up: clean-install runtime parent

**Files:** `scripts/executable_setup-second-brain-timer`,
`scripts/second_brain/safe_files.py`,
`tests/test_second_brain_paths.py`, `tests/test_second_brain_timer{,_chezmoi}.py`,
`README.md`,
`docs/second-brain.md`, `docs/smoke-tests.md`,
`docs/postmortem/2026-07-14-timer-runtime-parent-not-installed.md`,
`tasks/lessons.md`, and this plan.

- [x] Capture the failed real activation state without enabling systemd or
  changing the repository/config.
- [x] Strengthen the fake chezmoi fixture so a missing runtime package parent
  fails; observe five defining clean-install and unsafe-parent tests fail.
- [x] Reject the initial `--parent-dirs` candidate after an independent fixture
  proves it broadens existing `0700` directories to `0775`.
- [x] Add one descriptor-relative transaction that creates only missing install
  parents, preserves existing modes, revalidates identity/ownership, rejects
  symlinks and non-directories, and rolls back all created parents on failure.
- [x] Add injected-swap, mkdir/open-failure, multi-target rollback, clean-home,
  and real-chezmoi exact-27-file regressions.
- [x] Run the timer, Task 3, Second Brain, repository, systemd, chezmoi, README,
  and protected-state gates; obtain an independent focused review.
- [x] Inspect the staged 11-path allowlist and confirm the protected config is
  unstaged.
- [x] Commit/push
  `fix(second-brain): create timer runtime parent on first install`.
- [x] Retry activation only after the fix is upstream; verify installed bytes,
  enabled/active state, next 16:20 trigger, journal output, and any separate
  persistent catch-up checkpoint.

### Task 3 activation follow-up: installed repository resolution

**Files:** `scripts/second_brain/paths.py`,
`tests/test_second_brain_{command,timer_chezmoi}.py`, `docs/second-brain.md`,
`docs/smoke-tests.md`,
`docs/postmortem/2026-07-14-{installed-runtime-relative-chezmoi-path,
refresh-config-protected-file-overwrite}.md`, `tasks/lessons.md`, and this plan.

- [x] Reproduce the installed `setup-second-brain-timer --check` failure and
  prove real chezmoi rejects the relative `second-brain/README.md` target.
- [x] Strengthen the installed-layout fake so it rejects every source-path
  argument except the absolute applied vault front door; observe RED.
- [x] Resolve the source repository from
  `$HOME/second-brain/README.md`; observe the defining test GREEN.
- [x] Restore the accidentally snapshotted protected repo config from local
  session evidence and verify its exact pre-refresh SHA-256 while preserving
  the newer live config.
- [x] Run focused, Second Brain, repository, README, doctor, diff, protected
  state, and independent review gates.
- [x] Commit/push `fix(second-brain): resolve installed source through chezmoi`.
- [x] Apply the fixed runtime module, validate the installed setup and
  checkpoint dry run, and confirm the enabled timer remains scheduled.

## Exact Verification Plan

Focused automated commands:

```bash
python3 -m unittest tests.test_second_brain_vault tests.test_second_brain_skill -v
python3 -B -m unittest tests.test_second_brain_command tests.test_second_brain_concurrency tests.test_second_brain_doctor tests.test_second_brain_paths tests.test_second_brain_migration tests.test_second_brain_migration_apply tests.test_second_brain_upgrade -v
python3 -m unittest tests.test_second_brain_config_snapshot tests.test_second_brain_checkpoint tests.test_second_brain_checkpoint_commit_failure tests.test_second_brain_checkpoint_hook_isolation tests.test_second_brain_checkpoint_journal tests.test_second_brain_checkpoint_security tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi -v
bash tests/test_refresh_config_function.sh
python3 -m unittest tests.test_ai_workflow_contract tests.test_ai_workflow_doctor tests.test_context_handoff_contract -v
bash tests/test_claude_skill_links.sh
bash tests/scripts/executable_codex_test.sh
```

Repository and integration gates:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/second-brain-session
scripts/executable_second-brain doctor --format json --check
scripts/executable_ai-workflow-doctor --format json
scripts/executable_readme-recruiter-sync
git diff --check
git lfs ls-files
chezmoi apply --dry-run --verbose
chezmoi managed
sha256sum dot_codex/config.toml
git diff --cached --name-only
```

Manual/runtime checks after implementation commits are pushed:

- [ ] Action: open `second-brain/` as an Obsidian vault. Expected: Hack-based
  dark styling loads, navigation links work, and device workspace state remains
  untracked.
- [x] Action: run `second-brain status`. Expected: active projects, Inbox state,
  and latest Daily Notes appear without dumping the full vault.
- [ ] Action: run a fixture-backed capture and repeat it. Expected: the second
  invocation reports a no-op and note sections remain stable.
- [x] Action: run `setup-second-brain-timer --check`. Expected: launcher,
  runtime-package modules, and units validate; the user manager is reachable;
  and no sudo is requested.
- [x] Action: inspect `systemctl --user status` and `list-timers` after enable.
  Expected: the timer is enabled and the next local trigger is 16:20.

## Risks, Edge Cases, And Rollback

- **Public-repo disclosure:** require sanitized `visibility` frontmatter,
  secret/sensitive-path scans, explicit confirmation, and local-only raw state.
- **Lost instructions:** raw events carry stable event/session IDs; canonical
  preferences are routed to feedback memory; confirmed closeout is idempotent.
- **Duplicate memory:** vault contracts check canonical-owner links; the doctor
  rejects copied canonical preference/lesson content.
- **Concurrent writers:** mutation lock plus descriptor-relative portable
  exclusive create and leased checksum-bound exchange; contention, an open
  editor, a changed target, or a late destination returns a nonzero result
  while preserving competing bytes or a named recovery artifact.
- **Migration damage:** preview and approval hash precede copying; sources are
  read-only and re-hashed; ledger resumes without overwrites.
- **Git contamination:** abort on staged input, stage only exact allowlist,
  inspect staged names, and never manipulate unrelated unstaged changes.
- **Push failure:** explicitly upload reachable LFS objects before the isolated
  exact-ref push; retain the local checkpoint commit and report content-safe
  recovery without a bare push, retry, pull, merge, reset, or rewrite.
- **Config damage:** validate TOML and target mapping, write atomically, keep the
  current config hash unchanged through all implementation commits.
- **Timer catch-up:** activate only after implementation push; classify an
  immediate persistent run as a separate runtime checkpoint.
- **Rollback:** run the source-independent `setup-second-brain-timer --disable`,
  revert implementation commits normally, restore approved overwrites from
  dated archive backups, and leave migration originals and private raw state
  untouched.

## Progress

- [x] Source/target discovery and baseline audit completed.
- [x] Guided interview completed and each section confirmed.
- [x] Exact tree, ownership, data flow, migration, tests, risks, and commits
  approved by the user on 2026-07-14.
- [x] Protected dirty paths and Codex config hash recorded before the first
  repository patch.
- [x] Task 1 implemented, reviewed, verified, and committed.
- [x] Task 2 implemented, reviewed, verified, and committed.
- [x] Task 3 implemented, reviewed, verified, and committed.
- [x] Full verification and final independent review completed.
- [x] Implementation series pushed and upstream equality confirmed.
- [x] Timer enabled and runtime state/next trigger verified.

## Verification Evidence

| Requirement | Command/action | Expected | Observed | Exit |
|---|---|---|---|---|
| Protected baseline | `git status --short` | Existing user paths recorded | Paths listed above | 0 |
| Config baseline | `sha256sum dot_codex/config.toml` | Stable protected hash | `3edd706e...85e2e` | 0 |
| Source provenance | `git -C /home/example/coding/second-brain-setup rev-parse HEAD` | Exact audited revision | `90584269...aaf8` | 0 |
| Baseline AI workflow | Focused baseline commands listed in Current Context | Existing behavior remains green | 11 + 17 + 6 Python tests and shell fixtures passed during discovery | 0 |
| Task 1 pressure baseline | Read-only subagent scenario without the skill | Expose the missing workflow | Correct owners were identified, but personal-decision persistence and confirmed ExampleProject closeout were unavailable | n/a |
| Task 1 initial RED | `python3 -m unittest tests.test_second_brain_vault tests.test_second_brain_skill tests.test_second_brain_command -v` | Fail because production surfaces do not exist | 24 tests failed for missing vault, skill, and command | 1 |
| Task 1 strengthened RED | Same focused suite after adversarial fixture expansion | New assertions catch real remaining gaps | 3 failures: owner links, structured provenance, and standard XDG state | 1 |
| Task 1 GREEN | `python3 -B -m unittest tests.test_second_brain_vault tests.test_second_brain_skill tests.test_second_brain_command -v` | All focused contracts pass | 27 tests passed in 1.207s | 0 |
| Skill validation | `quick_validate.py dot_agents/skills/second-brain-session` and `wc -w SKILL.md` | Valid and concise | `Skill is valid!`; 256 words | 0 |
| Task 1 forward pressure test | Read-only subagent scenario with the skill | Targeted, private, confirmation-gated handling with no Git writes | All eight behavioral criteria satisfied; no mutation performed | n/a |
| AI workflow integration | `scripts/executable_ai-workflow-doctor --repo . --format json` | No errors and skill catalog parity | Pass, 0 errors, 47 actual/catalogued skills; one pre-existing duplicate-slug warning | 0 |
| Task 1 regressions | 34 AI-workflow/doctor/handoff tests plus refresh-config, Claude-link, and Codex-wrapper fixtures | Existing integration remains green | 34 tests and all 3 shell fixtures passed | 0 |
| Task 1 hygiene | `git diff --check`; config SHA-256 | No diff errors; protected hash unchanged | Clean; exact `3edd706e...85e2e` hash | 0 |
| Task 1 independent review | Read-only senior review of the uncommitted slice | Identify correctness, privacy, and plan gaps before commit | 2 Critical, 6 Important, and 3 Minor findings; verdict not ready | n/a |
| Task 1 review RED | Expanded 38-test focused suite | Reproduce every actionable review class before fixes | 19 failures covering installed source selection, state/lock/vault containment, focus cardinality, schema/content safety, routing, and provenance | 1 |
| Task 1 review GREEN | Expanded focused suite after fixes | All reviewer-driven contracts pass | 39 tests passed in 2.474s | 0 |
| Task 1 re-review | Fresh read-only review plus routing follow-up | Every prior Critical/Important/Minor finding resolved and no new material defect | Ready to proceed: Yes; two final reference gaps were reproduced and fixed | n/a |
| Task 1 final focused | `python3 -B -m unittest tests.test_second_brain_vault tests.test_second_brain_skill tests.test_second_brain_command -v` | Complete Task 1 contract stays green | 40 tests passed in 2.745s | 0 |
| Task 1 final integration | 34 AI-workflow/doctor/handoff tests; skill validator; workflow doctor; README gate; three shell fixtures | Existing surfaces remain green and new skill is valid | 34 tests passed; `Skill is valid!`; doctor pass with one pre-existing warning; `pass_no_change`; all fixtures passed | 0 |
| Task 1 real status | `scripts/executable_second-brain status --format json` | Read source vault without mutation | Schema 1; three approved projects; Inbox 0; latest note 2026-07-14 | 0 |
| Task 1 final hygiene | `git diff --check`; protected config SHA-256 | Clean diff and unchanged protected config | Clean; exact `3edd706e...85e2e` hash | 0 |
| Task 2 command-hardening RED | Seven new command contracts against the Task 1 implementation | Expose date, event conflict, symlink, structure, rollback, and repo-alias gaps | 7 of 27 tests failed for the intended reasons | 1 |
| Task 2 command-hardening GREEN | `python3 -B -m unittest tests.test_second_brain_command -v` | All command and lock contracts pass | 28 tests passed, including held-lock rejection and retry | 0 |
| Task 2 doctor RED/GREEN | `python3 -B -m unittest tests.test_second_brain_doctor -v` | Missing surface fails, then stable safe findings pass | Initial 11 missing-command failures; final 23 passed after all-file secret, bounded-media, and bounded canonical-owner hardening | 0 |
| Task 2 migration RED/GREEN | `python3 -B -m unittest tests.test_second_brain_migration tests.test_second_brain_migration_apply -v` | Missing surface fails, then inventory/plan/apply/verify pass | Initial 15 failures; final 44 passed after canonical-path and anchored-ledger hardening | 0 |
| Task 2 upgrade RED/GREEN | `python3 -B -m unittest tests.test_second_brain_upgrade -v` | Missing surface fails, then preview/apply/backup/idempotency pass | Initial 7 failures; final 9 tests passed including injected target/backup races | 0 |
| Task 2 security review | Fresh read-only adversarial review plus executable reproducers | Identify unsafe cases before commit | 4 Important findings: source-policy bypass, no-overwrite TOCTOU, false-pass ledgers, and unvalidated imports/hard links | n/a |
| Task 2 security RED/GREEN | Doctor, path, source-policy, ledger, and late-destination regressions | Reproduce and close every Important class | Doctor 5 review failures then 16 passed; path 4 errors then 4 passed; source-policy 4 subcases rejected; ledger 9 failures then 25 passed; final apply 26 passed | 0 |
| Task 2 final adversarial review | Independent exact-diff review plus executable race, path, privacy, and resource-bound reproducers | No unresolved security blocker | Portable-create/replace races, netrc/JSON detection, all-file doctor scanning, private-ledger boundaries, and canonical paths reproduced RED then closed; post-extraction verdict READY | n/a |
| Task 2 final documentation audit | Independent operator-doc, README-table, plan-claim, and resource-bound audit | Every public claim matches code and fresh evidence | Initial verdict NOT READY; table parsing, bounded canonical-owner scanning, and duplicate-owner scope corrected; final verdict READY | n/a |
| Task 2 cohesion refactor | Split mixed-concern modules at the warning boundary | Keep each implementation module before 500 lines | Apply 292; verify 278; common 295; safe-files 497; safe-create 148; safe-contract 25; paths 216; private-state 116; doctor 499; doctor-contract 60; doctor-LFS 23; content-security 138 lines | 0 |
| Task 2 complete fixture suite | `python3 -B -m unittest tests.test_second_brain_vault tests.test_second_brain_skill tests.test_second_brain_command tests.test_second_brain_concurrency tests.test_second_brain_doctor tests.test_second_brain_paths tests.test_second_brain_migration tests.test_second_brain_migration_apply tests.test_second_brain_upgrade` | All Second Brain contracts pass | 142 tests passed in 17.088s after final security and documentation-review fixes | 0 |
| Task 2 repository regression | `python3 -B -m unittest discover -s tests -p 'test*.py'` | The complete Python test surface remains green | 187 tests passed in 19.539s | 0 |
| Task 2 real read-only CLI | Help; text/JSON status; text/JSON doctor check; migrate help; upgrade dry-run | Truthful commands, healthy vault, and no mutation | All exited 0; doctor 0 errors/0 warnings; schema-v1 upgrade operations empty | 0 |
| Task 2 integration gates | 34 AI workflow tests; skill validator; workflow doctor; README gate; three shell fixtures; `git diff --check` | Existing surfaces remain green and docs are synchronized | 34 passed; skill valid; doctor pass with one pre-existing duplicate-slug warning; `pass_no_change`; all fixtures and diff check passed | 0 |
| Task 2 chezmoi dry-run | `chezmoi apply --dry-run --force` | Resolve the existing live-config divergence without prompting and perform no writes | Exited 0; the protected config checksum remained exact afterward | 0 |
| Task 2 protected state | `sha256sum dot_codex/config.toml` | User-owned config remains literal and unstaged | Exact `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e` | 0 |
| Task 3 initial RED | Focused config-snapshot, checkpoint, and timer modules | Missing production surfaces fail before implementation | The focused suite failed on the absent helper, checkpoint modules, setup command, and units | 1 |
| Task 3 snapshot review RED/GREEN | Descriptor-bound source/target, strict-size, mode-drift, secret-content, and cross-repository mapping reproducers | Reject unsafe or changed files in dry-run and write modes without touching the protected target | Every reproduced boundary now fails closed; checkpoint callers bind chezmoi resolution to their exact repository target | 0 |
| Task 3 checkpoint review RED/GREEN | Disposable repositories covering dirty index, intent-to-add, hooks, tags, upstream selection, immutable trees, LFS upload, and ref-push failure | Ship only the frozen allowlisted tree and preserve content-safe recovery evidence | Exact reachable-LFS upload precedes an isolated exact-ref push; hooks, tags, force, push defaults, and unrelated index/worktree state cannot alter the operation | 0 |
| Task 3 timer cache RED | `test_chezmoi_ignores_runtime_bytecode_mapping_collisions` against the tracked ignore file | Generated cache entries must not collide with chezmoi directives | Failed with an inconsistent `private_state`/`remove_state` bytecode mapping | 1 |
| Task 3 runtime exactness RED | Shadow-extension, package-directory, symlink, and symlinked-cache setup tests | Every unexpected or unsafe package-root entry must abort before activation | Four subcases activated under the earlier suffix-only check | 1 |
| Task 3 timer cache/exactness GREEN | Four focused cache and runtime-root tests; real `chezmoi managed`; legacy-target dry-run | Caches are ignored, reviewed modules remain exact, and normal owned cache directories work | 4 tests passed in 0.498s; both real chezmoi commands exited cleanly with generated caches present | 0 |
| Task 3 focused GREEN | Seven config/checkpoint/failure/hook/journal/security/timer modules | Complete Task 3 contract stays green after final hardening | 83 tests passed in 6.411s | 0 |
| Early prerequisite push | Local/upstream hashes plus protected config hash after the shell-interpolation incident | No Task 3 or protected config content reached upstream | Local and upstream remained `dec36e0`; protected config stayed exact; linked postmortem records the incident | 0 |
| Task 3 complete Second Brain suite | `python3 -B -m unittest discover -s tests -p 'test_second_brain_*.py'` | All Second Brain behavior remains green | 227 tests passed in 23.606s | 0 |
| Task 3 repository regression | `python3 -B -m unittest discover -s tests -p 'test_*.py'` | Complete Python surface remains green | 274 tests passed in 26.357s | 0 |
| Task 3 integration gates | 36 AI workflow tests; refresh-config, Claude-link, and Codex-wrapper fixtures; skill validator; systemd verify; README gate; `git diff --check`; changed-surface compile | Existing workflows, docs, units, and syntax remain valid | 36 passed; all fixtures passed; `Skill is valid!`; systemd and compile passed; `pass_no_change`; clean diff | 0 |
| Task 3 live read-only health | Status, Second Brain doctor, upgrade dry-run, snapshot dry-run, and checkpoint dry-run | Healthy personalized vault and no mutation | Three projects, Inbox 0; doctor 0/0; upgrade empty; both dry-runs passed; checkpoint reported only the protected config candidate | 0 |
| Task 3 AI doctor comparison | `scripts/executable_ai-workflow-doctor --repo . --format json --compare /tmp/second-brain-task2-doctor.json --check` | No new workflow finding or active instruction growth | No added/resolved findings and zero metric deltas; only the pre-existing duplicate brand-skill warning remains | 0 |
| Task 3 chezmoi deployment | Exact 33-target and global `chezmoi apply --dry-run --force`; `chezmoi managed` with caches present | Every tracked install mapping resolves without writes or cache collisions | Exact target count 33; all three commands exited cleanly | 0 |
| Task 3 LFS policy | `git lfs ls-files`; `git check-attr` probes | No current LFS payloads; attachment media uses LFS while Markdown stays text | LFS inventory empty; PNG/PDF mapped to LFS; Markdown attributes unspecified | 0 |
| Task 3 final independent review | Fresh adversarial whole-change review and independent matrix | No unresolved Critical, Important, or Minor issue | Verdict READY; 128/128 reviewer matrix passed | n/a |
| Task 3 protected pre-stage state | Config SHA-256, cached names, status, local/upstream hashes | Protected config exact and unstaged; index empty; prerequisite refs equal | Exact `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`; cached list empty; both refs `dec36e0` | 0 |
| Task 3 staged allowlist | Cached name/status/stat inspection plus complete staged diff review | Only approved Task 3 files are staged and protected config is excluded | 37 paths, 4,594 insertions, 85 deletions; protected config remained only an unstaged user modification; staged diff check clean | 0 |
| Task 3 implementation push | `git push` followed by local/upstream hash comparison | Verified Task 3 commit reaches only its configured upstream | Both refs equal `fa80508fa1e69e194de9aa36edb5a3a00807978a` | 0 |
| Timer activation RED | Real `setup-second-brain-timer --enable`; target/type, systemd, Git, and config inspection | First install creates runtime and enables only after validation | Apply failed; launcher/units existed but runtime parent did not; timer disabled/inactive; Git refs and protected hash unchanged | 2 |
| Timer broad-parent candidate | Missing-parent tests plus independent restrictive-mode fixture | Candidate must preserve existing parent modes | Missing-parent tests passed, but fixture changed `~/scripts` and its runtime directory from `0700` to `0775`; reviewer verdict NOT READY and candidate rejected | n/a |
| Timer narrow-parent RED/GREEN | Five clean-install/unsafe-parent tests before and after the descriptor-relative helper | Create only missing parents, preserve modes, reject unsafe paths before apply | 5/5 failed against the pushed setup, then 5/5 passed in 1.039s | 0 |
| Parent transaction hardening | Injected-swap, mkdir/open-failure, foreign-owner, cross-target rollback, timer rollback, clean-home, and real chezmoi exact-inventory tests | Catch path replacement, leave no partial safe parents on failure, and install exactly 27 files | Focused path 21/21 and split timer/chezmoi 34/34 passed | 0 |
| Timer follow-up independent review | Fresh adversarial diff review plus prior-reproducer reruns | No unresolved safety, rollback, mode, or target-bounding blocker | Verdict READY; independent focused suite 54/54, restrictive-mode/swap/open/ownership/rollback reproducers passed, and diff check clean | n/a |
| Timer follow-up final gates | Task 3, Second Brain, repository, AI workflow, shell, doctor, systemd, chezmoi, README, compile, LFS, diff, and protected-hash checks | All affected and broader surfaces pass without staging or changing the protected config | Task 3 89/89; Second Brain 239/239; repository 286/286; AI workflow 36/36; all three shell fixtures, both doctors, skill validation, systemd verify, global chezmoi dry-run/managed, `pass_no_change`, isolated compile, LFS, and diff checks passed; config hash exact | 0 |
| Timer follow-up staged allowlist | Cached name/status/diff inspection plus protected hash | Only the 11 approved fix paths are staged; user config remains unstaged and exact | 11 approved paths staged; complete diff reviewed; cached diff clean; protected config absent from index with exact SHA-256 | 0 |
| Timer clean-install fix push | Commit/push plus local/upstream comparison | Fix reaches the configured upstream before activation | Commit `a300f51`; local and upstream refs equal `a300f514560afa58227872cfd747030eb52fa1fe` | 0 |
| Timer activation GREEN | Source setup enable/check; systemd state/list/status; journal; modes; Git refs | Exact installed bytes, active timer, next 16:20 trigger, preserved existing modes, and separately classified catch-up | Enable/check passed; timer enabled/active for 2026-07-14 16:20 EDT; existing `~/scripts` and config modes unchanged; new runtime `0755`; no catch-up journal; refs still `a300f51` | 0 |
| Installed repository resolution RED/GREEN | Real relative/absolute chezmoi calls plus strengthened installed-layout test | Installed runtime asks chezmoi for an absolute managed destination | Relative target exited 1 as not managed and defining test failed; absolute target mapped to the repo front door and the test passed | 0 |
| Protected config recovery | Pre/post SHA-256, local log diff evidence, and live hash | Restore exact pre-refresh repo bytes without changing newer live bytes | Repo hash restored to `3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`; live hash remained `f9e84d469f63addd863192cbadbac9145bea54872ed4526ece953efe4dc8f088` | 0 |
| Installed resolution final gates | Focused, Task 3, Second Brain, repository, AI workflow, shell, doctor, systemd, README, compile, LFS, diff, and protected-state checks | Every affected and broader surface passes without staging or changing the protected config | Focused 49/49; Task 3 90/90; Second Brain 240/240; repository 287/287; AI workflow 36/36; all three shell fixtures, both doctors, skill validation, systemd verify, `pass_no_change`, isolated compile, LFS, and diff checks passed; protected repo/live hashes remained exact | 0 |
| Installed resolution independent review | Fresh exact-diff review plus real-chezmoi and installed-layout reproducers | No unresolved correctness, security, or portability blocker | Verdict READY; all nine staged paths reviewed; real relative target failed; absolute target and a HOME path containing spaces passed; final command/path/real-chezmoi suite passed 52/52; both test-hardening recommendations were implemented | n/a |
| Installed resolution staged allowlist | Cached name/status/diff inspection plus protected hash | Only the nine approved follow-up paths are staged and the protected config remains unstaged | Nine approved paths staged; complete diff reviewed; cached diff clean; protected config absent from the index with exact `3edd706e...85e2e` checksum | 0 |
| Installed resolution fix push | Commit/push plus local/upstream comparison | The verified fix reaches the configured upstream before deployment | Commit `0bdb8c2`; local and upstream refs equal `0bdb8c20e0a4ba93b25eeb79ce268d8497e84e38` | 0 |
| Installed runtime verification GREEN | Source setup enable; installed setup check, status, and checkpoint dry run from `/tmp`; module hashes; timer state/schedule; journal; Git/config state | Installed commands resolve the source repo, dry run without mutation, and keep the verified timer scheduled | Setup/check passed; status reported three projects and Inbox 0; dry run reported only `dot_codex/config.toml`; source/installed module hashes matched; timer enabled/active for 16:20 EDT; journal empty; refs stayed equal; index empty; protected repo/live hashes stayed exact | 0 |

Task RED/GREEN, review, commit, push, and runtime evidence will be appended to
this table as each checklist item is actually completed.

## Review Notes

- The upstream source contains prose/setup assets but no tests, fixtures,
  generated-vault example, CI, or proven cross-platform runtime. Its claims are
  design input only; local tests define behavior.
- The source's three synchronized instruction files conflict with this repo's
  canonical instruction chain and recruiter README, so that pattern is rejected.
- The earlier unrelated README, smoke-checklist, skill-index, and metaprompt
  edits were committed independently. Only the protected
  `dot_codex/config.toml` diff remains user-owned and unstaged for Task 2.
- The actual checkpoint is intentionally deferred until after implementation
  commits are verified and pushed, preserving the user's live config change.
- The first Task 1 review correctly found that proposal-only daily focus was not
  durable enough for the user's lost-instruction problem. Task 1 now persists
  one confirmed ExampleProject focus per date and requires closeout to match it.
- While Task 1 was in progress, the user's pre-existing metaprompt work was
  independently committed and pushed as `dbc311d`. Task 1 did not stage or
  alter that work; the protected `dot_codex/config.toml` remains unstaged.
- Task 1 was committed as `bd3d835`; it and Task 2 reached upstream early
  only through the separately documented shell-interpolation incident.
- Initial migration remains unapplied. The initial schema-v1 upgrade registry
  intentionally has no pending operation; future operations append immutable
  specifications rather than rewriting history.
- Final Task 2 review reproduced every reported race and privacy gap before a
  fix. The behavior-neutral module extraction retained a green focused suite,
  and the independent post-extraction security re-review returned READY with no
  blockers.
- The final documentation audit found broken Markdown table pipes and an
  unbounded canonical-owner duplicate scan. The exact 1,000,000-byte regression
  failed first, then passed with a deterministic content-safe error; the final
  focused suite now passes 142 tests. Independent documentation and security
  re-reviews both returned READY after the corrections.
- A plain non-interactive `chezmoi apply --dry-run --verbose` stops at the
  pre-existing live `~/.codex/config.toml` divergence. The final read-only gate
  therefore used `--dry-run --force`; it exited 0 without writing, and the
  protected tracked config checksum remained exact.
- Task 3 review found that generated bytecode inherited chezmoi's filename
  modifiers and collided after the state-module rename. The tracked ignore now
  excludes every `__pycache__` tree and `.pyc` file; a real mapping
  regression proves the fix with caches already present.
- Installed timer runtime validation uses an exact root allowlist. It permits
  only the reviewed regular module manifest and an owned, non-symlinked
  `__pycache__` directory, rejecting native extensions, package directories,
  other files, and symlinks before systemd activation.
- Shell command substitution in a double-quoted read-only search caused the
  verified Task 1 and Task 2 commits to push before Task 3. Published history
  remains intact; the [postmortem](../docs/postmortem/2026-07-14-shell-interpolation-early-push.md)
  and repository lesson record the prevention rule.
- The pushed Task 3 dry-runs proved chezmoi mapping but not first-install
  destination creation. Real activation exposed the missing-parent gap before
  systemd enable. The broad native parent flag was rejected because it changed
  existing modes; the focused follow-up keeps exact file targets and creates
  only missing parents in a descriptor-relative rollback transaction.
- A same-UID process can still replace a home-owned path after final pre-apply
  validation because chezmoi consumes path strings, not held descriptors. That
  UID already controls these files and is not a privilege boundary; setup
  rejects pre-existing and in-helper swaps and revalidates installed types and
  bytes before enabling systemd.
- The required refresh workflow was attempted after activation, but its first
  step intentionally replaced the protected dirty repo config with the newer
  live file. Local session evidence recovered the exact pre-refresh values and
  hash without touching live state. Future protected-config deployments must
  use the snapshot dry-run and exact chezmoi targets unless overwrite ownership
  is explicitly reconciled.
