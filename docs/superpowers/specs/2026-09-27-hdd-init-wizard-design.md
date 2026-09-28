# HDD initialization wizard design

## Purpose

Create a runnable Ubuntu Bash wizard for diagnosing and initializing one SATA
drive attached through a USB docking station. The intended drive is 8 TB (about
7.3 TiB as Linux reports binary units), but the wizard must select from actual
detected devices rather than assume a capacity or device name.

## Scope and decisions

- Add `scripts/hdd-init-wizard.sh` with `--help` and `--dry-run`.
- Begin with `lsblk`, recent kernel storage/USB messages, and optional `lsusb`
  and SMART diagnostics. Do not install packages.
- Enumerate only whole disks. Detect and prohibit the Ubuntu system disk, and
  refuse disks with mounted partitions.
- Require the exact full device path to select a disk. Existing partitions or
  filesystems require either exit or the exact `ERASE <device-path>` phrase.
- Show destructive commands and require a final explicit confirmation before
  executing them. Initialize with GPT, one full-size partition, and ext4 with
  the `64bit` feature for disks beyond 16 TiB.
- Configure the requested mount path, ownership, and UUID-based fstab entry
  only after initialization. Back up fstab first, validate with `sudo mount
  -a`, and restore the backup on validation failure.
- Dry run performs no writes, formatting, partitioning, mounting, or fstab edit.

## Non-goals

- No GUI, package installation, automatic device-name selection, data recovery,
  filesystem alternatives, or changes to existing filesystems without the
  explicit erase gates.

## Safety and rollback

The system disk and mounted disks are never eligible for initialization. The
existing-data erase phrase and final command review are independent gates.
The fstab backup is the rollback point for a failed mount validation. A failed
initialization before fstab setup may leave the selected disk partially
initialized; the script must stop and report the state rather than attempt
implicit recovery.

## Verification

- `bash -n scripts/hdd-init-wizard.sh` exits successfully.
- `bash scripts/hdd-init-wizard.sh --help` prints usage and exits successfully.
- `bash scripts/hdd-init-wizard.sh --dry-run` reaches diagnostics/planning and does not
  write to disks, create a mount directory, or edit fstab.
