# Read backup artifacts as the invoking user

Make generated archive/log/metadata files readable by the user invoking sudo, preserve backed-up home metadata, and provide a scoped repair for existing bundles.

## Context, decisions and scope

Initial status already contains recovery work and vanished-file changes; preserve all prior/unrelated work. Root archive creation and inspect_archive precede home copying, so the supplied retry log establishes those stages passed at that time, without proving restore/boot success. Sudo access here requires a password; do not request or collect it. Resolve the invoking account through pwd, never assume UID 1000. Change ownership only on the bundle directory and known generated regular files; skip symlinks and never recurse into home. Provide `access --bundle PATH --user example-user` for the authenticated local terminal. No backup restart or disk restore. Plan Mode is unavailable; use this decision-complete record.

## Checklist

- [x] Capture dirty state, read ownership/verification paths, independently review archive ordering.
- [x] Observe RED for generated-artifact ownership, preserved home metadata and symlink safety.
- [x] Implement owner resolution, creation/failure/publication ownership and scoped access repair.
- [x] Update README, recovery docs, smoke steps and record permissions incident.
- [x] Run backup regression suite, shell syntax, refresh-config, installed-byte check and ledger check.

## Verification and risks

Exact automated command: python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'. Test completed and interrupted bundles and preservation of home owner/mode/inventory. Manual: sudo ~/scripts/backup-pc access --bundle /mnt/usb-8tb/sys-backup/20261006T175918Z-927e77.incomplete --user example-user; then read log/archive without sudo. Root archive fresh readability check: tar --list --xz --ignore-zeros --file BUNDLE/system.tar.xz >/dev/null. This may take hours. No actual repair is possible here until local sudo authentication. Rollback only session changes to ownership helper/hooks/parser/docs; never revert prior recovery work. Read access does not make incomplete bundles restorable.

## Progress and review

The root-only permission policy contradicts the user’s requested access. Generated artifacts may safely change owner; recursive chown of copied home would corrupt restoration metadata. Lookup `backup permissions owner root sudo` matched ext-container-host-ownership (unresolved), applicable only as scope/UID guidance, not a verified remedy for this backup.

Final evidence: ownership helper/account tests RED with missing symbols; all 62 backup tests GREEN, exit 0. Shell syntax, access --help (source and installed), installed-byte cmp and git diff --check exited 0. refresh-config completed, exit 0. Existing bundle access repair was not applied because sudo requires the user’s local password; exact repair command documented. Root tar conclusion is based on supplied log and independently verified source ordering, not a fresh archive read. Tracked incident learning registered; targeted ledger check passed with no errors, exit 0. No commits or backup restart requested.
