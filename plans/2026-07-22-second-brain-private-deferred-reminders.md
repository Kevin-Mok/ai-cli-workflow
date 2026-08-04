# Second Brain Private Deferred Reminders Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Purpose and observable outcome:** A user can defer a redacted, private reminder either to a local date or to an unscheduled someday queue; the 04:00 persistent user timer promotes due reminders to a private inbox; the CLI reports counts without disclosure; and the session skill presents full text only for an explicit focus/dismiss/pending decision.

**Architecture:** Add a `deferred.py` private-state module built on the existing XDG root, locking, private-directory, and content-redaction primitives. Extend the CLI and `vault.status_report`, then add a sibling systemd unit pair and extend the existing safe timer installer so installed runtime code and both timer pairs are checked together. Session guidance remains declarative: it calls the CLI and never writes private text to the vault.

**Tech stack:** Python 3 standard library, unittest, systemd user units, chezmoi-managed files, Markdown skill/documentation.

## Current Context and Scope

- `scripts/second_brain/vault.py` owns `status_report`, tracked vault capture, focus, and closeout.
- `scripts/second_brain/schema.py` validates versioned JSON received from stdin or a payload file; `content_security.redact` removes likely secrets.
- `scripts/second_brain/paths.py` provides `state_root`, `ensure_private_directory`, `mutation_lock`, and private-state safety checks.
- `scripts/executable_setup-second-brain-timer` safely resolves chezmoi sources, installs runtime modules/units, validates them, and enables the existing checkpoint timer.
- Existing tests are `tests/test_second_brain_command.py`, `tests/test_second_brain_timer.py`, and `tests/test_second_brain_skill.py`.
- Protected pre-existing dirty files are `aliases/key_aliases.tmpl`, `aliases/key_dirs.tmpl`, `docs/second-brain.md`, `dot_agents/skills/feedback-memory/feedback.log`, `dot_codex/AGENTS.md`, `dot_config/fish/config.fish.tmpl`, `second-brain/README.md`, `docs/second-brain-beginner.md`, `docs/second-brain-eli5.md`, `docs/second-brain-examples.md`, `docs/second-brain-for-beginners.md`, `plans/second-brain-eli5.md`, `scripts/executable_setup-second-brain-state`, and `second-brain/05 Daily Notes/2026-07-22.md`. Do not edit, stage, or overwrite them.

## Assumptions and Decisions

- The existing schema version remains `1`; deferred reminders are a new event kind, not a vault event.
- Private events are stored in a single `deferred/reminders.json` file at mode `0600` under mode-`0700` XDG private-state parents. The file contains a versioned object with a `reminders` list.
- A reminder has `event_id`, `source`, `timestamp`, `target_date`, `session_id`, redacted `text`, `state` (`someday`, `deferred`, `inbox`, or `resolved`), and optional `resolution`. Repeated identical IDs are no-ops; different content for an existing ID is rejected.
- `process-deferred` promotes `deferred` records whose target date is on or before `local_now().date()`; it never resolves, deletes, or writes the tracked vault.
- `resolve-deferred` permits only an existing `inbox` record and a `focused` or `dismissed` resolution; it is idempotent only for an identical resolution.
- The private inbox retrieval command is `second-brain list-deferred --format json`; this command is intentionally not listed in public status text and is consumed only by the session skill.
- The new timer runs locally at `04:00:00`, sets `Persistent=true`, and invokes the installed launcher without a shell or privilege escalation.
- No user-facing desktop notification, Taskwarrior integration, automatic focus creation, or tracked-vault reminder text is introduced.

## Global Constraints

- Never store or print unredacted reminder text outside the private queue; command errors remain content-safe.
- All mutations use the existing `mutation_lock` and write only after private path validation succeeds.
- Private state stays outside the Git checkout and uses `0700` directories and `0600` files.
- Existing status JSON remains backward-compatible; add counts under `private_reminders`.
- The session workflow never creates a focus without example-user’s separate confirmation and never resolves a reminder when focus is unavailable or deferred.
- Extend tests before production code and observe each focused test fail before the corresponding implementation.

---

### Task 1: Private deferred-reminder model and CLI commands

**Files:**
- Create: `scripts/second_brain/deferred.py`
- Modify: `scripts/second_brain/schema.py`, `scripts/second_brain/cli.py`, `scripts/second_brain/vault.py`
- Test: `tests/test_second_brain_command.py`

**Interfaces:**
- Produces `defer(payload)`, `process_due()`, `list_inbox()`, `resolve(payload)`, and `counts()` in `scripts.second_brain.deferred`.
- CLI commands are `defer --payload -`, `process-deferred`, `list-deferred --format json`, and `resolve-deferred --payload -`.
- `status_report()` adds `private_reminders: {"deferred": int, "inbox": int}` without exposing text.

- [x] Add failing command tests for redacted private writes, `0600` file and `0700` parent modes, duplicate/conflicting IDs, invalid dates/states, process idempotence and late promotion, focused/dismissed resolution, status counts, and a byte-for-byte vault snapshot before/after every private operation.
- [x] Run `python3 -m unittest tests.test_second_brain_command.SecondBrainCommandTest` and confirm the new tests fail because commands and private store do not exist.
- [x] Add strict deferred payload validators requiring `schema_version`, `event_id`, `source`, `timestamp`, `target_date`, `session_id`, and text; reject malformed dates, wrong types, unsafe text payloads, and unsupported resolution values without echoing content.
- [x] Implement `deferred.py` using `state_root`, `ensure_private_directory`, `mutation_lock`, `atomic_write`, `private_file_bytes`, and `redact`; preserve minimal resolved records and use canonical sorted JSON for deterministic idempotence.
- [x] Wire each CLI command through `load_payload`, print only compact JSON result metadata except `list-deferred --format json`, and extend text/JSON status counts.
- [x] Re-run `python3 -m unittest tests.test_second_brain_command.SecondBrainCommandTest` and confirm all focused command tests pass.

### Task 2: Persistent 04:00 promotion timer and safe installer integration

**Files:**
- Create: `dot_config/systemd/user/second-brain-deferred.service`, `dot_config/systemd/user/second-brain-deferred.timer`
- Modify: `scripts/executable_setup-second-brain-timer`
- Test: `tests/test_second_brain_timer.py`, `tests/test_second_brain_timer_chezmoi.py`

**Interfaces:**
- The service starts `/usr/bin/env %h/scripts/second-brain process-deferred` with `Type=oneshot`, journal output, controlled `PATH`, and `UMask=0077`.
- The timer has `OnCalendar=*-*-* 04:00:00`, `Persistent=true`, `Unit=second-brain-deferred.service`, and `WantedBy=timers.target`.
- Setup/check installs, validates, enables, and verifies the checkpoint and deferred timer pairs together.

- [x] Add failing tests that assert the exact 04:00 local persistent calendar, safe service fields, runtime package installation containing `deferred.py`, and setup/check command sequences for the additional pair.
- [x] Run `python3 -m unittest tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi` and confirm failures name the missing units or installer support.
- [x] Add the service and timer with only direct launcher invocation; update installer constants, managed targets, chezmoi source resolution, source/installed unit validation, installation, enablement, and check output for both timer pairs.
- [x] Re-run `python3 -m unittest tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi` and confirm all timer/install tests pass.

### Task 3: Session routing and public-safe documentation

**Files:**
- Modify: `dot_agents/skills/second-brain-session/SKILL.md`, `dot_agents/skills/second-brain-session/references/routing.md`, `docs/second-brain.md`, `docs/smoke-tests.md`
- Test: `tests/test_second_brain_skill.py`

**Interfaces:**
- At session start, after `status --format json`, the skill calls `list-deferred --format json` and presents each private item for `focused`, `dismissed`, or `pending` confirmation.
- It calls `resolve-deferred` only after the separate focus confirmation or an explicit dismissal; no full reminder text is added to public-safe documentation.

- [x] Add failing skill/documentation contract tests asserting the defer/process/resolve lifecycle, private boundary, timer lifecycle, and the three explicit dispositions.
- [x] Run `python3 -m unittest tests.test_second_brain_skill` and confirm failures are caused by absent deferred routing language.
- [x] Update the skill and routing reference with stdin-only payload examples, separate focus confirmation, and pending behavior; update the public Second Brain guide and smoke test with exact one-line CLI commands and expected private-only results.
- [x] Re-run `python3 -m unittest tests.test_second_brain_skill` and confirm the contract passes.

### Task 4: Integration verification, plan evidence, and focused delivery

**Files:**
- Modify: `plans/2026-07-22-second-brain-private-deferred-reminders.md`
- Verify: `tests/test_second_brain_command.py`, `tests/test_second_brain_timer.py`, `tests/test_second_brain_timer_chezmoi.py`, `tests/test_second_brain_skill.py`

- [x] Run `python3 -m unittest tests.test_second_brain_command tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi tests.test_second_brain_skill` and record the complete result and exit status below.
- [x] Run `git diff --check` and inspect `git diff --` limited to the task files; verify none of the protected dirty paths appear.
- [x] Mark every completed task and update verification/review notes in this plan in the same commit as its implementation and documentation.
- [x] Run `refresh-config` only if a tracked configuration or environment behavior change requires applying the timer/configuration to the live machine; protect unrelated dirty tracked configuration before doing so.

## Risks, Edge Cases, and Rollback

- A malformed or unsafe private store must fail before writing; rollback is to remove only the new private state file, never a tracked vault file.
- The timer may run after a missed boot; date comparison must promote all due records exactly once.
- A repeated timer execution, event, or resolution must preserve deterministic state and return `noop` where applicable.
- A confirmed focus can fail independently; do not resolve the reminder unless the subsequent explicit `focused` resolution succeeds.
- Existing protected dirty work is outside scope. If any target overlaps it, stop and ask before editing.

## Verification Evidence

- RED: record each new focused unittest command and its expected missing-command/missing-unit failure before implementation.
- GREEN: record the same command after implementation with exit status `0`.
- Regression: run the combined command from Task 4 and `git diff --check`.
- Manual: `second-brain defer --payload -`, `second-brain process-deferred`, `second-brain status --format json`, and `second-brain list-deferred --format json` using a disposable `XDG_STATE_HOME`; verify no tracked vault file changes and that the new user timer reports the 04:00 local persistent schedule.

## Progress, Verification Evidence, and Review Notes

- [x] Initial protected dirty state recorded from `git status --short` before this plan was created.
- [x] Design specification reviewed at `docs/superpowers/specs/2026-07-22-second-brain-private-deferred-reminders-design.md`.
- [x] Task 1 complete.
- [x] Task 2 complete.
- [x] Task 3 complete.
- [x] Task 4 complete.
- Verification: `python3 -B -m unittest tests.test_second_brain_command tests.test_second_brain_state_setup tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi tests.test_second_brain_skill -v` passed 83 tests with exit status 0; `git diff --check` and systemd unit validation remain part of final delivery.
- Review: live refresh was applied only to the targeted Fish config after the full refresh encountered an interactive chezmoi prompt; unrelated dirty configuration was preserved.
- Review notes: this plan intentionally uses the existing timer installer rather than adding a second installer, so runtime package and unit validation remain centralized. Rollback is a focused revert of the implementation commit plus removal of local private state only if requested.
