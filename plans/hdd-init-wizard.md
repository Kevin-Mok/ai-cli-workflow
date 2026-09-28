# HDD initialization wizard

## Purpose and observable outcome

Provide a runnable Ubuntu CLI wizard at `scripts/hdd-init-wizard.sh` for
diagnosing a USB-attached SATA disk and, only through explicit safety gates,
initializing and mounting it. The intended drive is 8 TB (about 7.3 TiB in
Linux binary units); detection must remain dynamic.

## Current context and scope

- Design: `docs/superpowers/specs/2026-09-27-hdd-init-wizard-design.md`
- Canonical policy: `dot_codex/AGENTS.md`
- Scope: one Bash script, README usage, a grouped smoke check, this plan,
  a Bash prompt lesson, and postmortems for observed workflow failures.
- No existing wizard was found in `scripts/`.
- Update README and smoke checks because this adds a reusable operator command.
  No tracked machine configuration changes are needed.

## Assumptions and settled decisions

- Use `lsblk`, `findmnt`/root-source resolution, kernel logs, `lsusb`, and
  `smartctl` only when available. Never install tools.
- Show only whole disks and prevent the root/system disk and any disk with
  mounted child filesystems from being selected for initialization.
- Existing partition/filesystem metadata stops the default flow. Erasure needs
  exact `ERASE /dev/...`; all destructive commands are displayed before a
  separate final confirmation.
- GPT, one full-size partition, ext4, label default `Storage`; mount default
  `/mnt/storage`; fstab uses UUID and `defaults,nofail`.
- `--dry-run` may run read-only diagnostics but performs no writes or mounts.
- User requested creation and the exact three verification commands, which
  establishes the execution method.

## Ordered implementation checklist

- [x] Record initial state: `git status --short` was clean before changes.
- [x] Define result, scope, and safety decisions in the design spec.
- [x] Define this implementation plan and exact requested verification.
- [x] Add executable `scripts/hdd-init-wizard.sh` with safe diagnostics,
  selection, confirmation, initialization, and mount/fstab flows.
- [x] Document invocation and a read-only manual smoke check.
- [x] Add a dated postmortem for the initial shell sandbox startup failures;
  record successful elevated read-only access as resolution.
- [x] Record and fix the interactive prompt failure found by the dry-run test.
- [x] Record and resolve the ext4 option patch context mismatch.
- [x] Run `bash -n scripts/hdd-init-wizard.sh`.
- [x] Run `bash scripts/hdd-init-wizard.sh --help`.
- [x] Run `bash scripts/hdd-init-wizard.sh --dry-run` and inspect that it
  performs no writes.
- [x] Review final diff, plan evidence, and remaining limitations.

## Risks, edge cases, rollback, and protected state

- Device enumeration and root-source resolution must account for mapper/LVM
  roots and parent whole disks; if system-disk identification is uncertain,
  fail closed and prohibit initialization.
- Partition table changes and formatting are irreversible. The selected path,
  existing-data phrase when applicable, visible commands, and final
  confirmation are separate barriers.
- If `mount -a` fails after fstab modification, restore the exact timestamped
  backup. Earlier disk initialization may already have occurred and must be
  reported without pretending it was rolled back.
- The initial Git state was clean. Preserve all subsequent user changes and
  touch only the listed deliverables.

## Verification plan and evidence

| Check | Expected | Observed |
|---|---|---|
| `bash -n scripts/hdd-init-wizard.sh` | Exit 0, no output | Exit 0, no output |
| `bash scripts/hdd-init-wizard.sh --help` | Usage, exit 0, no disk changes | Exit 0; usage and flags printed |
| `bash scripts/hdd-init-wizard.sh --dry-run` | Diagnostics and intended plan, exit 0; no writes, mounts, or fstab edits | Exit 0; detected `/dev/sdd` as 7.3 TiB USB disk, blocked `/dev/nvme0n1`, printed preview, and made no writes |
| Interactive `--dry-run`: choose `/dev/sdd`, confirm path, decline SMART, accept default label/mount | Command preview, exit 0, no writes | First run exited 1 from prompt variable shadowing (RED); after fix, exit 0 with `No writes were made` (GREEN) |
| `lsblk -nr -o PATH,TYPE /dev/sdd` after dry run | Only the whole disk remains | Exit 0; `/dev/sdd disk`, no partition |
| `git diff --check` | Exit 0 | Exit 0 after final script and docs changes |

## Progress and review notes

- Spec reviewed and approved by the user; script location clarified as
  `scripts/`.
- Initial restricted shell startup failed twice with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No commands
  ran in those attempts. A reviewed elevated read-only command then succeeded.
- The interactive dry-run failure exposed a prompt variable shadowing bug;
  its [postmortem](../docs/postmortem/2026-09-27-hdd-wizard-prompt-unbound.md)
  records the RED/ GREEN evidence and repair.
- A patch for explicit ext4 `64bit` support initially failed to match its
  `printf` source line. The [postmortem](../docs/postmortem/2026-09-27-hdd-wizard-patch-context-mismatch.md)
  records the corrected match and successful interactive preview.
- `shellcheck` was unavailable, so static verification used `bash -n` plus
  both dry-run paths. No partitioning, formatting, or fstab edit was exercised.
- Final review found only the requested wizard and its matching README, smoke
  check, design, plan, lesson, and failure records. The script is executable.
  The actual destructive path remains untested by design until the user runs
  and explicitly confirms it on the intended disk.
- User explicitly requested the implementation and checks; proceed with this
  plan after plan review.
- Rollback for repository changes is reverting the wizard and its matching
  README, smoke check, design, plan, lesson, and postmortems. Runtime rollback
  for fstab uses the generated backup; disk repartitioning/formatting cannot
  be rolled back.
