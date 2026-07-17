# Daily Superpowers Release Sync Design

## Goal

Run the existing `sync-superpowers-release` helper once per day at 05:00 local
time so the installed `obra/superpowers` skill bundle stays current without
requiring a manual command.

## Scope

The change adds an opt-in systemd user timer and a repo-local setup command.
The timer invokes the existing release-sync helper, which remains the single
place that knows how to refresh the chezmoi external archive. The workflow does
not modify tracked repository files, commit changes, push changes, or restart
running Codex sessions.

## Design

`setup-superpowers-release-timer` manages one user service and one user timer:

- `superpowers-release-sync.service` runs `sync-superpowers-release` with the
  repository path supplied through `LINUX_CONFIG_SOURCE` when needed.
- `superpowers-release-sync.timer` uses `OnCalendar=*-*-* 05:00:00` and
  `Persistent=true`, so a missed 05:00 run is performed when the user systemd
  manager next becomes active.
- The setup command supports exactly one of `--check`, `--enable`, or
  `--disable`, validates the managed unit sources, installs them through the
  existing chezmoi source, reloads the user manager, and enables or disables
  the timer without sudo.

The timer is intentionally opt-in. Enabling it is an explicit local-machine
operation, while the checked-in service, timer, setup command, documentation,
and smoke checks make the behavior reproducible.

## Alternatives

Cron was considered but rejected because the repository already uses systemd
user timers and systemd provides a clear user-scoped lifecycle plus
persistent catch-up after missed laptop wakeups. A login-triggered randomized
window was also considered but does not meet the requested fixed 05:00 local
schedule.

## Error Handling And Safety

- A failed refresh leaves the existing installed skill bundle in place because
  chezmoi refreshes the external target as one operation.
- The service uses the existing helper and exits non-zero on refresh failure;
  systemd records the failure in the user journal.
- Setup refuses missing, symlinked, or unexpected unit sources and does not
  require root privileges.
- Disabling the timer stops future runs but does not remove the installed
  Superpowers bundle.

## Verification

- Validate the setup command with `bash -n` or the repository's applicable
  Python test harness.
- Run `setup-superpowers-release-timer --check` and verify both units with
  `systemd-analyze --user verify`.
- Run `sync-superpowers-release --dry-run` to confirm the existing refresh
  path remains safe and functional.
- Enable the timer, inspect `systemctl --user status` and
  `systemctl --user list-timers`, then disable it as cleanup when testing on a
  live machine.
- Update the root README, skill catalog, and `docs/smoke-tests.md` with the
  setup command, 05:00 schedule, flags, and expected results.

## Rollback

Run `setup-superpowers-release-timer --disable` to stop future refreshes. If
the implementation is reverted, the existing manual
`sync-superpowers-release` command and installed bundle remain available.
