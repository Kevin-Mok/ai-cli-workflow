# Daily Superpowers Release Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in systemd user timer that runs `sync-superpowers-release` every day at 05:00 local time.

**Architecture:** Chezmoi will install a oneshot service and persistent daily timer alongside the existing Superpowers sync helper. A new Python setup command will validate the exact chezmoi sources, apply only the helper and two units, reload the user manager, and enable or disable the timer without sudo. The service will use the standard `$HOME/linux-config` checkout path through `LINUX_CONFIG_SOURCE`; manual use of the existing helper remains unchanged.

**Tech Stack:** Python 3 standard library, Bash helper entrypoints, systemd user services/timers, chezmoi source-path/apply, unittest fixtures, Markdown operator documentation.

## Global Constraints

- Preserve all pre-existing dirty files: `docs/second-brain.md`, `dot_config/fish/config.fish.tmpl`, `second-brain/README.md`, the four untracked Second Brain docs, and `scripts/executable_setup-second-brain-state`.
- The timer is opt-in and user-scoped; no sudo, repository commit, or push is performed by the setup command or timer.
- The schedule is exactly `OnCalendar=*-*-* 05:00:00`, local time, with `Persistent=true`.
- The existing `sync-superpowers-release` helper remains the only release-refresh implementation.
- `--check`, `--enable`, and `--disable` are mutually exclusive and exactly one is required.
- Relevant plan progress and verification evidence remain in this file and ship with the implementation commit.

## File Map

- Create `dot_config/systemd/user/superpowers-release-sync.service`: the oneshot service that invokes the installed sync helper.
- Create `dot_config/systemd/user/superpowers-release-sync.timer`: the persistent 05:00 daily timer.
- Create `scripts/executable_setup-superpowers-release-timer`: the safe setup/check/enable/disable command installed as `setup-superpowers-release-timer`.
- Create `tests/test_superpowers_release_timer.py`: fixture-based tests for source validation, exact target application, unit verification, enable/disable behavior, and failure cleanup.
- Modify `README.md`: document the opt-in timer, command flags, schedule, and relationship to manual sync.
- Modify `dot_agents/skills/README.md`: describe the recurring external Superpowers refresh workflow.
- Modify `docs/smoke-tests.md`: add grouped manual setup, timer inspection, journal, and disable checks.
- Modify this plan: record progress and exact verification evidence.

## Implementation Checklist

### Task 1: Add the systemd user units

**Files:**
- Create: `dot_config/systemd/user/superpowers-release-sync.service`
- Create: `dot_config/systemd/user/superpowers-release-sync.timer`
- Test: `tests/test_superpowers_release_timer.py`

**Interfaces:**
- The service consumes the installed `%h/scripts/sync-superpowers-release` command and uses `LINUX_CONFIG_SOURCE=%h/linux-config`.
- The timer starts `superpowers-release-sync.service` and is wanted by `timers.target`.

- [x] Write tests that assert the service is `Type=oneshot`, invokes the expected installed helper, has journal output, and defines the standard source environment; assert the timer has the exact 05:00 calendar, `Persistent=true`, `AccuracySec=1s`, and the matching `Unit=`.
- [x] Run `python3 -B -m unittest tests.test_superpowers_release_timer -v` and observe the new unit fixtures/tests fail because the files do not exist.
- [x] Add the service:

```ini
[Unit]
Description=Refresh the external Superpowers skill bundle

[Service]
Type=oneshot
ExecStart=%h/scripts/sync-superpowers-release
Environment=LINUX_CONFIG_SOURCE=%h/linux-config
Environment="PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin"
UMask=0077
StandardOutput=journal
StandardError=journal
SyslogIdentifier=superpowers-release-sync
```

- [x] Add the timer:

```ini
[Unit]
Description=Refresh Superpowers skills at 5:00 AM daily

[Timer]
OnCalendar=*-*-* 05:00:00
Persistent=true
AccuracySec=1s
Unit=superpowers-release-sync.service

[Install]
WantedBy=timers.target
```

- [x] Run `systemd-analyze verify dot_config/systemd/user/superpowers-release-sync.service dot_config/systemd/user/superpowers-release-sync.timer` and the focused unittest; expect both to pass.

### Task 2: Implement the setup command with red-green coverage

**Files:**
- Create: `scripts/executable_setup-superpowers-release-timer`
- Modify: `tests/test_superpowers_release_timer.py`

**Interfaces:**
- `setup-superpowers-release-timer --check` validates the standard checkout’s exact sources and installed units without changing state.
- `setup-superpowers-release-timer --enable` applies the exact helper/service/timer targets, reloads the user manager, and enables/starts the timer.
- `setup-superpowers-release-timer --disable` disables and stops the timer without requiring chezmoi or a source checkout.

- [x] Extend the fixture with fake `chezmoi`, `systemctl`, and `systemd-analyze` commands that log argv and reject unexpected target lists or unit names.
- [x] Add failing tests for: required action selection; `--check` source resolution and unit verification; `--enable` exact apply ordering before daemon reload/activation; `--disable` idempotence without source resolution; rejection of symlinked or missing unit sources; and propagation of analysis/systemd failures without leaking private fixture content.
- [x] Run `python3 -B -m unittest tests.test_superpowers_release_timer -v`; confirm the behavior tests fail before the command exists.
- [x] Implement a Python standard-library command modeled on `scripts/executable_setup-second-brain-timer` with these concrete operations:
  - Require timer setup to use the standard `$HOME/linux-config` checkout and reject a missing, non-directory, symlinked, or alternate `LINUX_CONFIG_SOURCE`; manual helper behavior remains unchanged.
  - Resolve the installed helper at `$HOME/scripts/sync-superpowers-release` and the two units under `$HOME/.config/systemd/user`.
  - Use `chezmoi source-path` for the three managed targets; require each owned, regular, non-symlink result to resolve to its exact expected relative path under that checkout, and require the helper source to be executable.
  - For `--check`, run `systemd-analyze --user verify` against the installed service and timer.
  - For `--enable`, apply the exact three targets, compare each installed target’s bytes with its selected source bytes, verify installed units, then daemon-reload, enable/start, and verify again; best-effort disable on activation or final-verification failure.
  - For `--disable`, run `systemctl --user disable --now superpowers-release-sync.timer`, tolerate the already-disabled result, and do not call chezmoi.
  - Use a private lock under the existing state-root convention so concurrent setup operations fail safely.
  - Return non-zero with concise actionable errors and never print command output that could contain config or private paths beyond the intended target names.
- [x] Run the focused unittest and `python3 -m py_compile scripts/executable_setup-superpowers-release-timer`; expect all tests to pass and no generated bytecode to remain in the repo.

### Task 3: Update operator documentation and smoke coverage

**Files:**
- Modify: `README.md`
- Modify: `dot_agents/skills/README.md`
- Modify: `docs/smoke-tests.md`

**Interfaces:**
- Users discover `setup-superpowers-release-timer --check|--enable|--disable` from the documented command surface.
- Smoke checks describe the observable 05:00 timer state and cleanup path.

- [x] Add the timer to the README install/day-to-day narrative and command table, stating that it is opt-in, user-scoped, runs daily at 05:00 local time, catches up missed runs with `Persistent=true`, and leaves running Codex sessions unchanged until restarted.
- [x] Update the skills README so the external Superpowers section distinguishes the manual `sync-superpowers-release` path from the optional recurring timer.
- [x] Add a grouped `Action`/`Expected` entry to `docs/smoke-tests.md` in runnable `--enable`, `--check`, timer-list, journal, `--disable`, repeat-`--disable` order; state no sudo, 05:00 local time, `Persistent=true`, first install, and idempotent cleanup.
- [x] Verify every documented flag against `scripts/executable_setup-superpowers-release-timer --help` and keep unrelated dirty documentation out of the diff.

### Task 4: Full verification and review handoff

**Files:**
- Modify: `plans/2026-07-17-superpowers-daily-sync.md`

- [x] Run `bash -n scripts/executable_sync-superpowers-release` and `python3 -B -m unittest tests.test_superpowers_release_timer tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi -v`.
- [x] Run `systemd-analyze verify` on both tracked unit files and `./scripts/executable_sync-superpowers-release --help`; run the dry-run only if the live chezmoi external network path is available.
- [x] Run the setup command’s fixture-backed manual-equivalent checks and, on the live host if available, `setup-superpowers-release-timer --check`, inspect `systemctl --user list-timers superpowers-release-sync.timer`, then disable it if this task enabled it.
- [x] Run `./scripts/executable_readme-recruiter-sync`; resolve any `update_in_same_change` result before staging.
- [x] Inspect `git diff --check`, `git diff --stat`, and the staged diff; confirm only implementation files from this plan are included and all protected pre-existing dirty files remain unstaged.
- [x] Update this plan with observed command outputs, exit statuses, review notes, and rollback confirmation.
- [x] Commit the implementation and matching plan/docs with a concise Conventional Commit subject.

## Risks, Edge Cases, And Rollback

- A laptop powered off at 05:00 will run the persistent timer when the user systemd manager starts; an already-running Codex session will not reload skills automatically.
- Timer setup is deliberately bound to the standard `$HOME/linux-config` checkout and rejects alternate `LINUX_CONFIG_SOURCE` values; the manual `sync-superpowers-release` helper retains alternate-source support.
- Failed chezmoi, unit verification, or systemd activation must stop before later state changes where possible; tests must assert the order.
- `--disable` is recovery-safe and must continue to work when the source checkout or chezmoi is unavailable.
- Rollback is `setup-superpowers-release-timer --disable`; reverting the implementation removes future scheduling but leaves the installed bundle and manual sync entrypoint intact.

## Progress And Review Notes

- [x] Approved design recorded in `docs/superpowers/specs/2026-07-17-superpowers-daily-sync-design.md` and committed as `89c4e7e`.
- [x] Initial protected worktree state captured before repo modifications.
- [x] Existing sync helper, Second Brain timer pattern, README, skill catalog, and smoke-test surfaces inspected.
- [x] Implementation tasks complete (committed release-sync implementation and documentation were present in `1653d18`, `af79b3c`, `f51ed58`, `fc24799`, and `bd302ca`).
- [x] Focused and broader verification complete; live activation was intentionally not performed.
- [x] Final diff and protected dirty state reviewed.

### Verification Evidence

Fresh final-verification evidence on 2026-07-17:

- `bash -n scripts/executable_sync-superpowers-release` exited 0.
- `python3 -B -m unittest tests.test_superpowers_release_timer tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi -v` exited 0: 48 tests ran in 5.806s and reported `OK`. This includes fixture-backed checks for action selection, source/unit validation, exact apply ordering, idempotent disable, child-failure sanitization, private lock permissions, and no-state `--check` behavior.
- `systemd-analyze verify dot_config/systemd/user/superpowers-release-sync.service dot_config/systemd/user/superpowers-release-sync.timer` exited 0. `./scripts/executable_sync-superpowers-release --help` and `./scripts/executable_setup-superpowers-release-timer --help` each exited 0 and exposed the documented options.
- Live prerequisites were available: `chezmoi`, `systemctl`, and `systemd-analyze` resolved successfully; `systemctl --user show-environment` exited 0. A GitHub release reachability probe (`curl -sSI --max-time 15 https://github.com/obra/superpowers/releases/latest`) exited 0 and resolved to release `v6.1.1`.
- `./scripts/executable_sync-superpowers-release --dry-run` exited 0 with no output. It was run only after confirming the external release path was reachable.
- The live timer remains uninstalled and disabled: `systemctl --user list-timers --all superpowers-release-sync.timer` exited 0 with `0 timers listed`; `systemctl --user is-enabled superpowers-release-sync.timer` exited 4 with `not-found`. `./scripts/executable_setup-superpowers-release-timer --check` exited 2 with `systemd unit validation failed`; direct inspection confirmed both installed unit paths under `~/.config/systemd/user/` are absent, and `systemd-analyze --user verify` exited 1 with both units not found.
- `--enable` was deliberately not run, so no live timer state was changed. `--disable` was not run because this task did not enable the timer and must not modify a pre-existing timer. The fixture suite verifies the recovery path is idempotent; the live rollback command remains `setup-superpowers-release-timer --disable` after a user-authorized enable.
- `./scripts/executable_readme-recruiter-sync` exited 0 with `pass_no_change`; no README change is required.
- Final-review fix-wave RED: `python3 -B -m unittest tests.test_superpowers_release_timer -v` ran 18 tests and failed the alternate-checkout, out-of-root source-path, stale-target, pre-activation verification, ordering, and post-activation cleanup cases before the implementation changed.
- Final-review fix-wave GREEN: `python3 -B -m unittest tests.test_superpowers_release_timer tests.test_second_brain_timer tests.test_second_brain_timer_chezmoi -v` exited 0 with 53 tests in 5.618s. It covers standard-checkout rejection, exact three-path source mapping, deployed-byte checks before activation, pre-activation verification, and cleanup after failed final verification.
- `systemd-analyze verify dot_config/systemd/user/superpowers-release-sync.service dot_config/systemd/user/superpowers-release-sync.timer`, `bash -n scripts/executable_sync-superpowers-release`, both helper `--help` commands, `./scripts/executable_readme-recruiter-sync`, and `git diff --check` each exited 0. The README gate reported `pass_no_change`.

### Final Review Notes

- Initial protected worktree state included unrelated aliases, Second Brain files, feedback memory, Codex config/instructions, fish config, and `scripts/executable_setup-second-brain-state`; this fix wave edits and stages only the declared release-timer files.
- Final-review fix wave added standard-checkout binding, exact chezmoi source-path mapping, deployed-byte comparison, pre-activation unit verification, and best-effort cleanup after failed activation or final verification.
- The approved plan is tracked. Its checklist and final-review evidence ship in the same commit as this implementation and documentation work.
- The remaining live `--enable`, `--check`, timer inspection, and `--disable` cycle is manual and intentionally unrun to preserve the opt-in timer state.
