# Backup destination rejected behind systemd automount

Diagnose the live backup preflight rejection without changing disks or starting a backup.

## Symptom and impact

The operator ran `sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup` and received the FAT/exFAT/NTFS error. No successful backup was reported.

## Lookup and evidence

Postmortem-memory searches: `backup-pc filesystem exfat` returned unrelated live-copy findings; `autofs` returned no matches. No prior remedy applies.
`findmnt -T /mnt/usb-8tb/sys-backup -o TARGET,SOURCE,FSTYPE,OPTIONS` shows systemd autofs followed by /dev/sdd1 ext4 at the same target. /etc/fstab enables x-systemd.automount. The destination check uses max(target length), selecting the first equal-length mount (autofs). path_disks and live source preflight repeat that selection.
The sandbox observes ext4 as ro; that does not establish the host mount is read-only.

## Status and next steps

Confirmed selection defect; reproduce using an automount plus writable ext4 fixture, select the real filesystem on ties, retain read-only and unsupported-filesystem guards. Do not format, remount, or run a full backup. Live acceptance remains pending.

## Investigation tooling note

An attempted read of scripts/executable_refresh-config failed because no such tracked script exists. Locate the fish refresh-config function before activation; no configuration was changed by that read.

## Verification progress

Outside-sandbox findmnt confirms /dev/sdd1 ext4 is rw on the host; no remount is needed. Two defining tests failed as expected before the fix. The first full suite ran 71 tests with one environment error: setfacl returned Invalid argument in the ACL roundtrip fixture. A postmortem-memory search for `setfacl Invalid argument` returned generic unrelated matches, not an applicable remedy. Retry the suite outside the sandbox without changing tests. Additional path lookup for dot_config/fish/config.fish failed; the real refresh function was located successfully in dot_config/fish/functions/refresh-config.fish. Neither failed read changed files.

## Activation and further verification

The complete suite passed outside the sandbox: 71 tests, exit 0; Bash syntax passed. Independent diff review found no concrete issues. Installed backup-pc matched pre-session HEAD before targeted chezmoi apply, which succeeded. A sudo -n installed dry-run could not start because an interactive password is required; no backup was started. refresh-config inside the sandbox stopped on read-only home/runtime paths; preserve the private log /tmp/refresh-config.Vr5wO5sT.log and retry only outside the sandbox. This is an environment activation boundary, not a backup validation failure.

## Resolution and final evidence

All three containing-mount selections now prefer non-autofs on equal target lengths; deepest mount remains primary. Read-only and unsupported filesystem errors are separate. The installed destination_preflight executed outside the sandbox against the actual mount table and passed (exit 0); installed bytes equal the tracked source. Host drive is writable ext4. refresh-config succeeded outside sandbox (exit 0). No complete backup or restored boot was performed; interactive sudo is still required for the full dry-run. The ACL fixture passes outside sandbox. No formatting or remounting was performed.

## Learning

Record local-backup-autofs-selection as verified_fix with runtime scope limited to destination validation; retain full backup/restore limitations. Recovery guide and smoke checklist document the corrected behavior. README already accurately requires writable Linux destination; no command interface changed.
