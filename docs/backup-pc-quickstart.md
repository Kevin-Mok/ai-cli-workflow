# Back Up And Restore A Dated Bundle

Use this guide to back up the running Ubuntu PC and later restore a complete
bundle such as `/mnt/usb-8tb/sys-backup/11-01-26` onto a replacement disk.
First preview and create the backup, keep every bundle file together, then boot
a live USB to verify and restore it. Restore erases the entire selected disk.
For offline backup, implementation details and disposable-VM testing, see the
[full recovery guide](backup-pc-recovery.md).

## Current Restore Blocker

The current installed and example bundled helpers cannot accept the interactive
ERASE confirmation: their Python launcher consumes standard input, so the prompt
gets EOF and cancels before erasing. Backup and restore `--dry-run` are unaffected.
**Do not rely on this helper for a completed restore until that defect is fixed
and tested.** See the [incident and evidence](postmortem/2026-11-02-restore-confirmation-stdin.md).
The restore sections below explain the intended procedure and its prerequisites;
the final erase step is blocked in the current version. Do not bypass the prompt
or edit the checksummed helper inside an existing bundle.

## What Gets Saved

This workflow supports Ubuntu 24.04 amd64, UEFI/GRUB, ext4 root, a separate
ext4 `/home`, and FAT EFI at `/boot/efi`. Encrypted, RAID and LVM layouts are
unsupported. The backup drive must use a writable Linux filesystem; ext4 is
recommended.

| Bundle item | Keep it because |
| --- | --- |
| `system.tar.xz` | Contains root (`/`) and EFI system files; home contents are separate. |
| `home/` and `home-index.json` | Contain home files and the inventory used to verify their contents and metadata. |
| `manifest.json`, `warnings.json`, `SHA256SUMS`, `COMPLETE` | Record layout, live-copy warnings, integrity hashes and successful publication. |
| `backup-pc`, `backup-pc-progress.py`, `backup-pc-sync.py`, `RECOVERY.md` | Provide the bundled tools and recovery instructions. |
| `backup.log` | Records progress and the completion or failure outcome. |

Keep the **entire dated directory**. Copy it only with tools/options that
preserve Linux ownership, permissions, ACLs, extended attributes, hardlinks and
sparse files; a file-manager copy to exFAT is unsuitable. Do not edit the saved
home tree. Copy individual recovered files elsewhere before editing them.
`system.tar.xz` alone is insufficient for the supplied full-system restore.
The bundle contains private files and credentials and is not encrypted.

## Create A New Backup On The Running PC

Run these commands from your installed Ubuntu system, in any directory, using
the installed `~/scripts/backup-pc`. Backup commands require sudo. Check that
the USB drive is mounted before starting:

findmnt -T /mnt/usb-8tb -o TARGET,SOURCE,FSTYPE,OPTIONS

df -h /mnt/usb-8tb

Expect the real backup filesystem to be ext4 (or another supported Linux
filesystem) with `rw` options and sufficient free space. A systemd `autofs`
entry may appear alongside ext4; it is not the drive's data filesystem.

Preview without creating a bundle:

sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup --dry-run

Expect `Dry run complete; no files or disks changed`. Then create the backup:

sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup

Pass the **parent directory**, not an existing dated bundle, as `--destination`.
The helper creates a local-date `MM-DD-YY` directory; `11-01-26` means November
1, 2026. Another backup on the same day gets `-02`, then `-03`. The date is an
example, not a name to reuse. A backup spanning midnight keeps its start date.

Close write-heavy applications and finish database work first where possible.
`--live` copies changing files at different times; it does not stop services or
produce a consistent database snapshot. Prefer an offline backup from a live
USB when you need a stable filesystem copy.

Compression, copying and verification can take hours. Wait for `BACKUP COMPLETE`
and use the exact directory it prints. An unfinished bundle retains
`.incomplete` and cannot be restored by this helper. Backup creates a new bundle;
it does not resume or overwrite an earlier one.

## Inspect The Completed Example

These reads need no sudo when you are the account that invoked sudo for the
backup. Otherwise use sudo for protected artifacts. Substitute your own printed
bundle path if its date differs:

cat /mnt/usb-8tb/sys-backup/11-01-26/COMPLETE

Expect `full-system schema 2 split storage`.

python3 -m json.tool /mnt/usb-8tb/sys-backup/11-01-26/manifest.json

Check `coverage: full-system`, `storage: compressed-system+browsable-home`, and
`consistency`. `live-nonatomic` means files were copied from a running system.

python3 -m json.tool /mnt/usb-8tb/sys-backup/11-01-26/warnings.json

Review changed/vanished-file warnings. Completion means the backup passed its
creation checks, not that active application data was consistent or a restored
machine has been boot-tested. The restore dry run performs fresh bundle checks.

## Prepare For Restore In A Live USB

1. Boot an amd64 Ubuntu live USB in **UEFI mode**, using the live session rather
   than the installation you intend to replace. Connect the backup drive and a
   replacement disk with enough space for root, home, EFI and recorded swap.
2. The helper refuses the original recorded source disk, the backup disk,
   running-system disks, mounted targets and targets with active swap. It is a
   replacement-disk workflow; these commands do not overwrite your current
   source NVMe or restore only the root partition.
3. In the live session's disk utility, identify the backup partition and target
   disk by label, model, serial and size. Ensure the target's partitions are
   unmounted and its swap is inactive. Do not guess a `/dev/sdX` name.
4. Ensure the live session has Bash, Python 3, GNU tar/xz, rsync, util-linux,
   parted, udev, dosfstools and e2fsprogs. The helper reports missing tools.
   Restore uses the archived Ubuntu GRUB/initramfs tools. See the full guide's
   prerequisites if the live image lacks a tool.

The example drive is labeled `usb-8tb`. After confirming that label belongs to
the backup partition, mount it read-only at the same path used in this guide.
Skip mounting if it is already mounted there; if the desktop mounted it
elsewhere, use that actual path throughout instead. These commands require sudo:

sudo mkdir -p /mnt/usb-8tb

sudo mount -o ro /dev/disk/by-label/usb-8tb /mnt/usb-8tb

List disks and stable names; these inspection commands need no sudo:

lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,FSTYPE,MOUNTPOINTS

ls -l /dev/disk/by-id/

In the following commands, replace `REPLACEMENT-DISK-ID` with the verified
**whole replacement disk's** stable ID. Do not choose a `-part1` (partition)
entry. Leave the placeholder unchanged until you have identified the target.
The repository checkout and `~/scripts` are not needed for recovery: use the
helper inside the bundle.

## Verify And Preview Before Erasing

Run this from the live USB. It requires sudo and does not erase or format:

sudo /mnt/usb-8tb/sys-backup/11-01-26/backup-pc restore --archive /mnt/usb-8tb/sys-backup/11-01-26/system.tar.xz --target-disk /dev/disk/by-id/REPLACEMENT-DISK-ID --dry-run

The command checks bundle hashes, archive contents, home contents and metadata,
target safety and capacity, then prints the target identity and proposed layout.
Verification can take a long time: it reads the large archive and home tree,
even during dry run. A checksum-only check would not verify the home tree.
Expect `Dry run complete; zero destructive operations`. Resolve any failed
check before proceeding; do not bypass source-disk or integrity protections.

Root size is calculated automatically from the archived data. Leave the default
unless you deliberately need a larger root partition. An undersized
`--root-size` override is rejected; a generic 80 GiB example is too small for
this particular bundle's recorded root data.

## Restore And Check The Replacement

**Stop here with the current helper: its confirmation defect must be repaired
and tested first.** With a corrected, verified recovery entrypoint, the intended
procedure below **destroys every partition and all existing data on the selected
target disk.** Confirm that the preview's model, serial and size identify the
replacement, not your source or backup drive. It performs the verification again:

sudo /mnt/usb-8tb/sys-backup/11-01-26/backup-pc restore --archive /mnt/usb-8tb/sys-backup/11-01-26/system.tar.xz --target-disk /dev/disk/by-id/REPLACEMENT-DISK-ID

When prompted, type exactly `ERASE ` followed by the **resolved device path
printed by the helper**, not the by-id path from your command. An incorrect
response cancels before destructive operations. Do not bypass the prompt.

The helper recreates EFI, root, optional swap and home, extracts system files,
copies home, assigns fresh filesystem UUIDs and rebuilds initramfs/GRUB. It
installs an EFI fallback loader without modifying firmware boot entries.
Wait for `RESTORE COMPLETE`; it does not reboot automatically. If it fails,
treat the target as incomplete and preserve the backup for investigation.

Shut down, disconnect the old source and backup disks, remove the live USB,
and select the replacement in the UEFI boot menu. Verify login, important
files, applications and services before relying on it. Boot recovery and Secure
Boot compatibility require an actual boot test; successful checksums alone do
not establish either. Keep the original source and backup until these checks pass.
