# Full-system Backup And HDD Recovery

Use `backup-pc` to save your Ubuntu installation and restore it onto a
replacement disk. Offline backups are the default: boot a live USB and mount
the installed filesystems read-only. You can also explicitly back up the
running machine with `--live`, accepting that changing files may come from
different times. Preview, create and keep the complete backup bundle, then
restore from a live USB using its included script. System files are compressed;
home files remain browsable. Restoration erases the selected whole disk.

## Supported System And Prerequisites

The recovery layout supports Ubuntu 24.04 amd64 with UEFI/GRUB, a conventional
ext4 root partition, a separate ext4 `/home`, and a FAT EFI partition mounted
at `/boot/efi`. Recovery rejects BIOS, encryption, RAID, LVM and device-mapper
layouts. A separate `/boot` is outside this layout. Keep the source disks
available until the replacement boots and your files have been checked.

Use an amd64 Ubuntu live USB for offline backup and every restore. Live backup
runs on the installed machine. Backup and restore require `sudo`, Python 3,
GNU tar, GNU xz, rsync and standard Linux disk utilities. Restore also needs GPT partitioning,
FAT32/ext4 formatting and the Ubuntu installation's GRUB/initramfs tools.
The standalone recovery script embeds its implementation and exclusion policy;
it does not require this checkout or your installed dotfiles.

## Prepare And Create An Offline Backup

Shut down the installed system and boot the live USB. Use the live session's
disk utility to identify the source partitions and the backup disk by model,
serial and capacity. Mount the source root read-only at `/mnt/source`, its
separate home read-only at `/mnt/source/home`, and its EFI partition read-only
at `/mnt/source/boot/efi`. Mount the backup disk read-write at `/mnt/backup`.
Use a Linux backup filesystem, preferably ext4, with sufficient space for the
normal home files plus the compressed system archive. The helper verifies copied
home data and metadata; FAT, exFAT and NTFS destinations are rejected.
Do not boot the installation being archived or allow it to write during backup.
Without `--live`, the helper rejects writable source mounts and missing
required mounts. This remains the default backup mode.

Preview the source, coverage and exclusions:

```bash
sudo ./scripts/executable_backup-pc backup --source-root /mnt/source --destination /mnt/backup/system-backups --dry-run
```

Create the full backup using the same arguments without `--dry-run`:

```bash
sudo ./scripts/executable_backup-pc backup --source-root /mnt/source --destination /mnt/backup/system-backups
```

## Back Up The Running Machine

Use explicit `--live` when you want to back up the running supported Ubuntu
system. Root, separate `/home` and EFI must still be mounted in their expected
locations; live mode permits them to be writable. The backup destination must
still use a supported Linux filesystem and have enough space. These commands
use the installed `~/scripts/backup-pc` entrypoint and your backup HDD path:

```bash
sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup --dry-run
sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup
```

Every live backup is labeled `consistency=live-nonatomic` in its manifest,
even if no file-change warning occurs. Root, home and service data are copied
at different times while the system can continue changing them. This is not a
filesystem snapshot or a guarantee of application/database consistency. You
may close applications and pause your own write-heavy jobs before starting;
the helper does not stop services automatically.

The helper records tar warnings for files that changed or vanished in a
checksummed `warnings.json`. For home, rsync exit 24 is accepted after one
best-effort pass, with vanished-file warnings saved in the same file. Inspect
recorded warnings before relying on the backup.
Read, permission and I/O errors remain failures: they leave a visibly
incomplete backup rather than publishing a successful bundle. A live copy
does not provide a consistent point-in-time image of active applications.

Live backups retain the same compressed system archive and normal browsable
home files as offline backups. A completed bundle's checksum and home-index
checks prove that its saved files remain intact; they do not turn a live copy
into an application-consistent snapshot. Recovery prints the manifest's live
consistency warning before restoring it. Restore still runs from a live USB
with the same whole-disk protection and erase confirmation.

## Backup Bundle And Browsable Home

The completed backup directory contains:

| File or directory | Purpose |
| --- | --- |
| `system.tar.xz` | Compressed root and EFI files, with an empty home mount directory. |
| `home/` | Normal browsable home files, copied with rsync. |
| `home-index.json` | Per-path integrity, metadata and hardlink information for the home copy. |
| Recovery manifest and checksums | Describe and verify the complete schema-2 bundle, including its consistency mode. |
| `warnings.json` | Checksummed file-change/vanishing warnings for a live backup. |
| `backup-pc` and recovery instructions | Standalone recovery entrypoint and operating notes. |
| `backup-pc-progress.py` | Checksummed backup progress helper; recovery remains embedded in `backup-pc`. |
| `backup-pc-sync.py` | Checksummed helper for updating an incomplete bundle’s home copy. |
| `backup.log` | Private timestamped activity log, readable by the account invoking sudo. |

Keep the whole bundle together. `system.tar.xz` alone is a partial backup and
cannot restore the system. Failed backups remain visibly incomplete and are
rejected for recovery. The manifest identifies full-system coverage with
`compressed-system+browsable-home` storage.

System compression uses GNU xz's maximum preset, `-9e`. By default,
`--resource-percent 75` selects 75% of the CPU threads available to the process,
rounded down with a minimum of one, and caps compressor memory at 75% of the
smaller of available and total RAM at startup. For example, 12 available CPU
threads select nine compression threads. Set an integer from 1 to 100 to change
this budget; the dry-run preview and compression progress show the selected
thread count and memory ceiling.

The percentage sets a thread count and memory ceiling, rather than keeping
actual CPU and RAM usage at exactly that percentage. GNU xz may reduce the
thread count to fit its memory limit, but `--no-adjust` keeps the `-9e` preset.
Budgets below 700 MiB are rejected before creating a bundle; below 1280 MiB,
the helper selects single-thread mode. If XZ cannot fit its encoder within the
ceiling, the backup remains incomplete rather than reducing compression quality. Maximum compression can still take hours,
and already compressed files may shrink little. Parallel XZ compresses independent
blocks, so the archive may be slightly larger than one continuous stream.
See the [XZ manual](https://tukaani.org/xz/man/xz.1.html) for memory and threading details. Home rsync is unchanged by
this setting. Home is deliberately uncompressed: browse
`BACKUP/home/USERNAME/` with ordinary file tools without extracting an archive.
Original ownership and permissions remain intact, so some files require sudo
to inspect from a live session.

An already running compressor keeps its original settings. To replace an older
single-thread run, stop that backup with Ctrl-C, wait for it to exit, then start
a fresh invocation, for example:

```bash
sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup --resource-percent 75
```

The interrupted directory remains marked `.incomplete`; the new invocation
creates a separate bundle and does not resume or overwrite it.

The home copy uses `rsync -aHAXS --numeric-ids`, preserving ownership,
permissions, ACLs, extended attributes, hardlinks and sparse files. It omits
only known home caches and unrelated mounts beneath home. The system archive
preserves the same metadata for root and EFI. Both components restore to their
usual paths; home files appear exactly once beneath the restored `/home`.

Browse the backup without editing it. Recovery compares the normal home files
against the checksummed `home-index.json` before any disk write; missing,
modified or mismatched files make the bundle invalid. Use a separate copy when
you want to edit a recovered file.

The published directory permits traversal, while each home file keeps its
original ownership and permissions. The system archive and home inventory are
restricted to the account invoking sudo; direct root invocations remain root-owned.
Browse your own home files normally; use sudo for files you could not originally
access. Reading home files
is safe; editing them invalidates recovery verification.

Checksums detect corruption, not a maliciously replaced backup. Store the
backup safely: it contains private user files and system credentials.

## Watch Progress And Read The Activity Log

Backup displays separate root/EFI and home progress bars by default, with
elapsed time, an estimated remaining time and the current file. Root/EFI first
scans the selected source data to estimate GNU tar input bytes, accounting for
sparse files and hardlinks. The root percentage is an estimate: live files can
change after the scan, compression speed varies, and XZ can still be finishing
output after tar has read its last file. Root stays below 100% until the archive
process succeeds; a stalled or finishing compressor has an uncertain ETA.

Home uses rsync’s whole-transfer progress with a full initial file list, plus
current-file output. Home ETA is estimated from elapsed time and the reported
percentage, since rsync completion timestamps show elapsed transfer time.
Sparse files, hardlinks and changing live files can affect
its percentage and ETA too. These bars describe copying; archive readability,
checksums and home integrity checks still follow. Wait for the final
`BACKUP COMPLETE` message before relying on the bundle.

Ctrl-C, SIGTERM and SIGHUP stop and reap the active copy process group; the
unfinished bundle stays marked incomplete.

The backup prints its bundle/log path at startup and writes `backup.log` there
throughout the run. The log includes timestamped phases, filenames and
warnings/errors. The directory retains its `.incomplete` suffix until all
checks succeed, then the log moves with the published bundle. To follow it
from a second terminal, replace the example directory with the printed path:

```bash
tail -f /mnt/usb-8tb/sys-backup/BACKUP.incomplete/backup.log
```

The log’s mode is `600` because filenames and diagnostics may reveal private
information. Generated artifacts (archive, log, indexes and instructions) belong
to the account invoking sudo, so that account can read them without sudo. Root
invocations without a sudo user remain root-owned. The copied `home/` tree keeps
its original ownership, permissions and ACLs. `--dry-run`
creates neither a bundle nor a log. Installing a new version does not change
an existing backup process: stop the old invocation with Ctrl-C, wait for it
to exit, then start a fresh backup to get these progress displays and logging.
The old incomplete bundle stays available for inspection.

### Repair access to an older bundle

Older backups may have root-owned mode-600 archives/logs inside a mode-700
incomplete directory. Run this scoped repair with sudo to assign the bundle
and its generated artifacts to example-user; it does not recurse into copied home
files or modify archive contents:

```bash
sudo ~/scripts/backup-pc access --bundle /mnt/usb-8tb/sys-backup/10-06-26.incomplete --user example-user
```

Then example-user can list the bundle and read `backup.log` and `system.tar.xz` without
sudo. This does not complete or resume an incomplete backup. The root/EFI tar
is created and fully inspected before home copying begins, so a later home-copy
failure means those archive checks passed at the time. Fresh archive readability
can be checked without extracting files (this may take a long time):

```bash
tar --list --xz --ignore-zeros --file /mnt/usb-8tb/sys-backup/10-06-26.incomplete/system.tar.xz >/dev/null
```

Exit zero confirms compressed archive readability; it does not verify a complete
recovery bundle or prove a restored machine boots. A live archive is nonatomic.

The checksummed `backup-pc-progress.py` helper is packaged beside the standalone
script for future backups. The restore implementation remains embedded in
`backup-pc`; legacy completed bundles without the helper remain readable.

## Exclusion Policy

Print the built-in policy without root privileges:

```bash
./scripts/executable_backup-pc excludes
```

The same policy is documented in
[the main exclusion list](../txt/exclude-dirs-backup.txt.tmpl) and
[the full exclusion list](../txt/exclude-dirs-backup-full.txt). Patterns use
GNU tar's relative `./PATH` names with `--anchored --wildcards`. Comment lines
explain intent and must be stripped when using a list directly with tar.

| Category | Treatment |
| --- | --- |
| `/dev`, `/proc`, `/sys`, `/run`, `/tmp` | Omit runtime contents; preserve or recreate directories and permissions. |
| Users' default `.cache` directories | Omit contents; include configuration, data and persistent state. Nonstandard cache locations remain included. |
| APT archives/indexes, pacman package downloads, Snap cache | Omit these known caches; retain package databases and installed state. |
| `/opt`, Snap/Docker state, browser profiles, Android files, projects and games | Include. |
| Logs, crash dumps, `/var/tmp`, recovered files in `lost+found` | Include. |
| Backup destination and unrelated mounted filesystems | Exclude dynamically and show them in the preview. |
| Ordinary local files beneath `/mnt`, `/media` or `/backup` | Include when they are not beneath a dynamically excluded mount/destination. |

The [XDG specification](https://specifications.freedesktop.org/basedir/0.8/)
distinguishes disposable caches from configuration, application data and state.
A directory containing installed packages or personal data is not a cache
merely because it is large.

## Restore Onto A Replacement HDD

Boot the live USB and mount the backup disk. Leave every partition of the
replacement disk unmounted and deactivate any swap on that disk. Identify the
whole disk using a stable `/dev/disk/by-id/` path. Substitute your completed
backup directory for `BACKUP` and the replacement HDD's identifier for
`TARGET-HDD` in these commands.

Preview recovery with the standalone script included in the backup:

```bash
sudo /mnt/backup/BACKUP/backup-pc restore --archive /mnt/backup/BACKUP/system.tar.xz --target-disk /dev/disk/by-id/TARGET-HDD --dry-run
```

Run recovery:

```bash
sudo /mnt/backup/BACKUP/backup-pc restore --archive /mnt/backup/BACKUP/system.tar.xz --target-disk /dev/disk/by-id/TARGET-HDD
```

Before writing, the script verifies checksums, system archive
readability/completeness, the intact browsable home tree against its index,
supported architecture and boot setup, and capacity. For a live backup, it
prints the manifest's `live-nonatomic` consistency warning. Legacy partial
archives are rejected. It blocks the source/backup disk, running-system disks, mounted
targets, active swap, and RAID/LVM/device-mapper holders. The preview identifies
the resolved disk path, model, serial, capacity, existing partitions/filesystems
and proposed layout. Any partition table or filesystem signature means the
disk has existing data.

**Every partition and all existing data on the selected HDD will be lost.**
Type exactly `ERASE <resolved-device-path>` when prompted, using the path printed
by the script. An incorrect response, cancellation or dry run performs no
destructive operations. The script rechecks disk identity immediately before
erasing it. Never use a real user disk for development or recovery testing.

Recovery creates this GPT layout:

| Partition | Size and format |
| --- | --- |
| EFI | 1 GiB FAT32. |
| Root | ext4; archived root data plus 20% headroom and 1 GiB metadata allowance, rounded up to GiB, minimum 64 GiB. |
| Swap | Source's recorded capacity, when present. |
| Home | ext4; remaining space, sufficient for copied home data plus 10% headroom. |

Capacity calculations account for sparse files and hardlinks. To override the
root size, append `--root-size 80` (GiB) or `--root-size 80GiB` to the preview
and restore commands. An override that cannot hold the archived root data and
required headroom is rejected before disk writes.

After extracting the system archive and copying home files, the helper writes
fresh root/home/EFI/swap UUIDs into `fstab`,
updates resume references, rebuilds initramfs and GRUB, and adds `nofail` to
unrelated external mounts. It preserves the available signed Ubuntu boot files
and installs an EFI fallback loader without changing the live machine's
firmware boot entries. Ubuntu documents the relevant firmware and removable
loader options in [grub-install](https://manpages.ubuntu.com/manpages/noble/man8/grub-install.8.html).
This workflow does not claim verified Secure Boot support.

On failure, treat the replacement disk as incomplete. The helper cleans up
only mounts it created; inspect the error and retry from the preserved backup.
On success, it syncs and unmounts the restored filesystems and prints boot
instructions. It never reboots automatically. Shut down, disconnect the old
source and backup disks, select the replacement disk in the UEFI boot menu,
and verify login, applications and important files before retiring the source.

## Legacy Partial Commands

The existing profile names remain `nzxt`, `arch-2`, `x1`, `ubuntu` and
`ubuntu-h7`. For example:

```bash
sudo ./scripts/executable_backup-pc ubuntu-h7 tar-root
sudo ./scripts/executable_backup-pc ubuntu-h7 home
```

`tar-root` archives root without `/home`; `home` copies only home data using
rsync. These are partial backups and cannot be passed to the whole-disk restore
command. Use the new `backup` command for a complete recovery artifact.

## Verify Recovery In A Disposable VM

The reusable [VM recovery check](../scripts/backup-pc-vm-check) prepares and
walks through a disposable UEFI VM scenario. Read its help before running it:

```bash
./scripts/backup-pc-vm-check --help
```

On a host with `qemu-system-x86`, `qemu-utils` and OVMF installed, initialize
a fresh disposable directory. Replace the ISO/source-image paths with real
regular files. The source must be a powered-off standalone raw or qcow2 Ubuntu
24.04 amd64 image with the supported root/home/EFI layout. Use a matching OVMF
code/variables pair from your installation; the paths below are examples.
Choose target and backup capacities that fit your source; the 160/256 GiB
values below are examples. No host command in this workflow requires sudo or
accepts a host block device.

```bash
./scripts/backup-pc-vm-check init --work-dir /tmp/backup-pc-vm --source-image /path/to/ubuntu24-source.qcow2 --iso /path/to/ubuntu24-live.iso --firmware-code /usr/share/OVMF/OVMF_CODE_4M.fd --firmware-vars /usr/share/OVMF/OVMF_VARS_4M.fd --target-size 160 --backup-size 256 --dry-run
./scripts/backup-pc-vm-check init --work-dir /tmp/backup-pc-vm --source-image /path/to/ubuntu24-source.qcow2 --iso /path/to/ubuntu24-live.iso --firmware-code /usr/share/OVMF/OVMF_CODE_4M.fd --firmware-vars /usr/share/OVMF/OVMF_VARS_4M.fd --target-size 160 --backup-size 256
./scripts/backup-pc-vm-check backup --work-dir /tmp/backup-pc-vm
./scripts/backup-pc-vm-check restore --work-dir /tmp/backup-pc-vm
./scripts/backup-pc-vm-check boot --work-dir /tmp/backup-pc-vm
```

Run each phase after closing the previous VM. Initialization creates a source
overlay, backup image and nonempty replacement disk, and stages `backup-pc`,
`backup-pc-progress.py`, `backup-pc-sync.py` and this guide together on a
read-only virtual tools disk. The backup VM attaches the source
and backup images; the restore VM attaches backup and replacement; the boot VM
attaches only the replacement. The original source image remains backing
storage for its overlay.

In the live guest's disk utility, identify disks by `SOURCE_SYSTEM`,
`BACKUP_STORE` and `RESTORE_TARGET`. Format only the disposable `BACKUP_STORE`
image as ext4, mount it at `/mnt/backup`, and mount the source partitions
read-only beneath `/mnt/source`. Mount the read-only tools disk at
`/mnt/tools`, then run its staged script inside the guest:

```bash
sudo /mnt/tools/backup-pc backup --source-root /mnt/source --destination /mnt/backup/system-backups --dry-run
sudo /mnt/tools/backup-pc backup --source-root /mnt/source --destination /mnt/backup/system-backups
```

Browse the resulting home files and confirm caches are omitted while important
personal files remain.

In the restore guest, mount `BACKUP_STORE`, select the whole `RESTORE_TARGET`
disk and use the standalone restore command above. Verify the existing-data
warning, decline or enter an incorrect erase phrase once, then perform a
confirmed restore. Before completing the check, verify cancellation, protected
targets and changed device identity with the automated guard suite as well.
The isolated boot must reach login with both source and backup disks absent.
Verify applications, representative home files, separate fresh root/home UUIDs,
swap/resume and successful boot with external disks absent. Record the firmware,
commands, observed results and screenshots in `/tmp/backup-pc-vm/RESULTS.md`.
Test Secure Boot separately with it enabled before claiming compatibility.

Automated checks from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_backup_pc*.py'
bash -n scripts/executable_backup-pc
git diff --check
```

The fixture suite exercises tar round trips and destructive-operation guards.
It cannot prove firmware boot or physical disk recovery. QEMU and OVMF were
unavailable in the implementation environment, so the disposable-VM boot check
and a Secure Boot-enabled boot check remain required validation.

Capacity estimates use canonical nonzero 4 KiB data blocks plus per-entry
metadata rather than backup-filesystem compression ratios. Ext4 formatting uses
one inode per 4 KiB so many small files fit. Home file integrity uses a
versioned sparse-aware SHA-256 digest of logical size and positioned nonzero
blocks; the inventory itself is covered by SHA256SUMS.

## Readable dates and rerunning only home

New bundles use local `MM-DD-YY` directory names, such as `10-07-26`.
Additional backups on the same day use `10-07-26-02`, then `-03`. The
`.incomplete` suffix remains until the full backup passes publication checks.
The manifest retains its exact UTC creation timestamp.

To update the existing October 6 home copy, run this installed helper with sudo:

```bash
sudo ~/scripts/backup-pc sync-home --bundle /mnt/usb-8tb/sys-backup/10-06-26.incomplete --source-root / --live
```

Add `--dry-run` for source/destination preflight without writes. This command
reuses the existing root tar, appends to `backup.log`, copies home with the
same exclusions and metadata preservation as a backup, and refreshes the home
inventory and warning file. Existing warnings are preserved. Vanished live
files (rsync exit 24) are accepted; other copy failures remain fatal. It does
not delete destination files that disappeared from the source. example-user can
follow the log without sudo:

```bash
tail -f /mnt/usb-8tb/sys-backup/10-06-26.incomplete/backup.log
```

A successful home-only sync leaves the bundle `.incomplete`: this old bundle
still lacks the full recovery manifest, checksums and publication marker.
Home resync does not recreate the root archive or claim a complete recovery
backup. Keep all files for later recovery verification.
