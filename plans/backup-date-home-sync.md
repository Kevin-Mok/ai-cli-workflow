# Readable backup dates and home-only sync

Rename the October 6 bundle, create future bundles with readable local dates, and rerun home copying without recreating the root archive.

## Scope and settled decisions

Initial dirty state includes all prior recovery changes; preserve them. Existing bundle is example-user-owned/readable and contains a 126 GiB root archive; its log confirms root verification preceded home-copy retry exhaustion. New names use local MM-DD-YY, with -02 etc for same-day collisions, and .incomplete until full publication. Rename only the specified bundle to 10-06-26.incomplete. Add sync-home --bundle PATH --source-root ROOT [--live] [--dry-run], preserve archive/log, apply existing preflights and copy exclusions/metadata flags, accept live code24, refresh home inventory/warnings, and keep incomplete status. No --delete and no root recompression or publication of an unverified incomplete bundle. Sudo probe explicitly reports local authentication required; no password requested. Plan Mode unavailable; this record governs execution.

## Checklist

- [x] Capture dirty status, inspect actual bundle and independent home-sync review.
- [x] Observe RED for date collisions, append logging and archive-preserving sync.
- [x] Implement date naming and safe home-only sync with append logging.
- [x] Rename existing bundle with no overwrite and prove archive identity unchanged.
- [x] Update docs/smoke checks; run suite, syntax, refresh-config and installed byte checks.
- [ ] Start home sync if authentication permits, otherwise give exact installed command and report limitation.

## Verification, risks and rollback

Automated: python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'; bash -n scripts/executable_backup-pc. Defining tests: date naming and complete/incomplete collisions; appended log retains old content; sync never creates archive or COMPLETE, preserves archive bytes, rejects symlinked bundle/files/home and completed bundles, accepts vanished-source code24. Dry run makes no writes. Manual: sudo ~/scripts/backup-pc sync-home --source-root / --live --bundle /mnt/usb-8tb/sys-backup/10-06-26.incomplete. Compare archive inode/size/mtime before/after rename. No hashing of 126 GiB archive for rename; rename preserves inode. Rollback: rename back if destination absent; revert only task-owned naming/sync changes. Live sync is nonatomic and can take hours; later complete-bundle reconstruction/verification is separate work.

## Progress and review

User explicitly authorizes rename and home resync. Preserve .incomplete status because the old run lacks manifest/checksums/COMPLETE. Existing source/destination validation protects mounted HDD and prevents recursive backup. Source home ownership/ACLs remain intact. Postmortem lookup/evidence from previous backup tasks applies; no unexpected failure in this task.

Final evidence: four defining regressions RED for missing new_bundle/sync_home and append argument. Fresh full suite passed 66 tests, exit 0, including date collisions, safe destinations, dry-run nonmutation, preserved archive and log/warnings. bash syntax and git diff --check passed, exit 0. refresh-config completed, exit 0; main helper, sync sidecar and progress sidecar installed-byte cmp all passed. Installed sync-home --help passed. Actual rename completed to /mnt/usb-8tb/sys-backup/10-06-26.incomplete; archive inode 26804232, size 134882485144 bytes, device and mtime unchanged. Independent review found no blocking issues for live invocation. New home-only workflow is separated into scripts/backup-pc-sync.py because the engine already exceeds 1,000 lines; published backups ship/checksum the optional sidecar while old bundles remain compatible.

Outstanding: actual home resync is not started. Intentional sudo readiness probe returned SUDO_REQUIRES_LOCAL_AUTH. User must execute the documented sudo sync-home command in an authenticated terminal. No request for password or alternative metadata-losing unprivileged copy. Keep incomplete status until full-bundle reconstruction/verification. No commit requested. Rollback for rename is a scoped reverse rename only if the old name remains absent.
