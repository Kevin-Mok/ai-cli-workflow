# Full-system tar backup and guarded HDD recovery

Implement an offline Ubuntu backup containing compressed root/EFI and browsable home files, plus a standalone recovery command that validates the bundle and target before any disk write. Develop with temporary tar fixtures and mocked hardware boundaries; never erase a real disk during this task.

## Context and scope

The existing scripts/executable_backup-pc supports profile tar-root/home only and excludes persistent application state. Replace it with a Bash entrypoint embedding standard-library Python so the published copy has no repository dependency. Keep those legacy partial commands. Revise both exclusion lists, README, recovery guide and smoke checks. The supplied user plan is the intent/specification; no worktree or commit was requested. Default mode cannot be switched by tools; maintain this decision-complete ExecPlan in place.

## Decisions and interfaces

- User steering 2026-10-06: system compressed as much as practical; home must remain accessible as normal files. Bundle: system.tar.xz (maximum xz -9e single-thread preset), home/ normal files, home-index.json integrity/metadata inventory, manifest.json (schema 2), SHA256SUMS, backup-pc, RECOVERY.md, COMPLETE. Failed directories retain .incomplete suffix.
- Support only Ubuntu 24.04 amd64, conventional ext4 root/home and vfat EFI. Reject encryption, LVM, RAID, BIOS, separate essential filesystems and unsafe sources before backup/erasure.
- Require independently mounted read-only root/home/EFI from live media; exclude unrelated submounts and destination dynamically. Cache/runtime exclusion policy is embedded in the standalone script and mirrored in commented lists.
- --root-size accepts integer GiB. Layout: 1 GiB EFI, root max(64 GiB, rounded 120% archived allocated data), source swap, home remainder with 110% data capacity plus metadata allowance. Account for tar sparse extents and hardlinks.
- No unattended erase option. Checksum/structure/boot preflight precedes typed ERASE confirmation; fresh identity and safety recheck precedes first destructive operation. Never touch firmware NVRAM.
- Signed shim/GRUB artifacts preserved and copied to fallback path; Secure Boot support remains unverified until a Secure Boot VM boot test.
- Backup producer and restore consumer share schema/archive validation; tests exercise both, not just manifest claims.

## Protected state and risks

Initial git status captured before edits: aliases/key_aliases.tmpl, aliases/key_dirs.tmpl, docs/phone-ssh-public-ip.md, docs/smoke-tests.md, postmortem-memory references/api-contracts-fixtures.md, references/artifact-verification.md and sources.json are dirty; seven unrelated untracked reports/plans/prompts also exist. Preserve all. Append only scoped smoke checks; merge incident ledger additions without rewriting unrelated records. Keep hashes of protected state for refresh preflight. Disk restore is destructive by design: after erasure rollback requires a backup; failures label target incomplete and unmount only mounts made by this process. Malicious backup bundles are not trusted: check safe paths, required data and schema. Checksums detect corruption, not authenticity.

## Implementation checklist

- [x] Read source, relevant instructions, preferences and lessons; capture initial status.
- [x] Write and observe failing exclusion/source/archive/erase guard tests (12 initial RED, subsequent review regressions).
- [x] Implement offline full backup, metadata/capacity scan, transactional publication and legacy commands.
- [x] Implement read-only restore verification, disk guards, confirmation, identity recheck and restore phases.
- [x] Document exclusions/recovery/commands and create reusable disposable VM test launcher.
- [x] Run focused round trips and all guards; 29 tests GREEN and independent final review performed; fresh final syntax/diff checks below.
- [x] Final refresh after incident-knowledge updates, fresh checks, final evidence and outstanding limits.

## Verification

python3 -m unittest discover -s tests -p 'test_backup_pc*.py'
bash -n scripts/executable_backup-pc
git diff --check

Tar fixtures cover essential state, home nesting, spaces, numeric ownership, modes, ACLs/xattrs, sparse files and hardlinks. Hardware boundaries mocked in Python only; verify zero write calls on corrupt archive, insufficient capacity, running/backup/mounted/swap/holder disk, changed identity, wrong/declined input and dry-run. Disposable VM launcher must attach only virtual disks; recovery boot test disconnects original/backup and checks login, apps, data, UUIDs, swap and absent external mounts. QEMU/OVMF are unavailable locally: boot and Secure Boot tests pending, no claims of either.

## Progress and review evidence

- Initial normal exec failed before command execution: Bubblewrap RTM_NEWADDR denied. Approved scoped escalation executes read-only commands. See task incident; host sandbox repair out of scope.
- Documentation/exclusion task delegated independently; implementation/tests owned by primary. Fresh final reviewer required before completion.

## Handoff

Cursor prompt: Implement/verify plans/full-system-tar-recovery.md in place. Preserve dirty work, recovery must remain standalone, test every destructive guard, and run disk restoration only in disposable VMs. Run the three automated commands above, then the VM workflow in docs/backup-pc-recovery.md. Suggested commit: feat(backup): add full-system tar backup and guarded disk restore. Include this plan and matching docs with implementation if committing.

- First implementation: 24 tests GREEN; review corrections cover standard Ubuntu links, host-managed path escapes, private mounts and dense-inode formatting. User steering revises storage before final delivery: root/EFI tar.xz plus browsable home/; tests and docs must be revised before proceeding. No real disk write performed.

## Final implementation and review record

- Storage ruling: user steering supersedes single compressed tar: schema 2 bundle contains maximally compressed root/EFI system.tar.xz and home/ normal files; home-index.json verifies the separate tree. Cost/tradeoff: home occupies uncompressed space and needs a Linux metadata-preserving destination. Keep bundle intact; system tar alone cannot recover a disk.
- Compression: GNU xz -9e, one thread, installed manual documents ~674 MiB encoder memory. Legacy tar-root remains gzip-compatible.
- Safety review fixed: Ubuntu os-release and signed-shim alternatives links; confined host-side reads, real mount/write directories, no EFI links; private mounts; dense inode formatting; copy/inventory cache parity; literal bracketed mount exclusion; canonical nonzero-block capacity for compressed destination filesystems; bundle traversal with system archive/inventory mode 600. Root/home capacity includes a 1 GiB metadata allowance each.
- RED evidence: 12 tests failed for missing standalone engine; later RED suites exercised unsafe managed links, ELF/encryption/layout rejection, standard Ubuntu links, missing private mount, inode density, absent VM helper, split-storage interfaces, browsable permissions and literal mount exclusions.
- GREEN: python3 -m unittest discover -s tests -p 'test_backup_pc*.py' passed 29 tests (exit 0), including real tar.xz/rsync ACL/xattr/hardlink/sparse/space-name round trips and mocked complete writer/cleanup sequence. No host disk erasure or mounts were performed.
- Independent reviewer: original and split-storage reviews found no remaining clear source-level blockers after corrections. Reviewer reports corroborated by primary tests; runtime boot remains unverified.
- First fish -ic 'refresh-config' passed, exit 0, REFRESH COMPLETE. Snapshot dry-run passed and both live/tracked Codex and Git configs were byte-identical beforehand. All seven protected file hashes were unchanged afterward; subsequent intentional incident ledger edits preserve the existing records. Concurrent unrelated postmortem-memory additions remain untouched.
- README gate ./scripts/executable_readme-recruiter-sync: pass_no_change, exit 0. Targeted incident checks: both task reports registered with current SHA-256, no errors.
- Rollback: revert only task-owned file/hunk changes if desired. Published backups are additive; failed bundles remain .incomplete. After actual restore erasure, rollback requires preserved backup/original disk.
- Remaining validation: QEMU/OVMF absent locally; the actual guest restore/boot test and Secure Boot-enabled boot test remain pending in docs/backup-pc-recovery.md. Launcher tests only prove image attachment policy, not bootability. No commit/push requested or performed.

## Final verification evidence

- Final python3 -m unittest discover -s tests -p 'test_backup_pc*.py': 29 tests passed, exit 0 (2.534s). Deliberate unsafe tar path fixtures emit GNU tar warnings and are rejected; mocked writer never executes host disk commands.
- bash -n scripts/executable_backup-pc: exit 0.
- git diff --check: exit 0.
- ./scripts/executable_readme-recruiter-sync: pass_no_change, exit 0.
- Final fish -ic 'refresh-config': REFRESH COMPLETE, exit 0. Nine protected/task-owned file hashes unchanged after refresh; installed ~/scripts/backup-pc bytes exactly match tracked script. Subsequent changes are documentation/verification records only.
- Backup/restore help commands: exit 0, actual system.tar.xz and --root-size/--dry-run interface matches guide.
- Remaining boot/Secure Boot validation is explicitly deferred to the reusable disposable-VM workflow because QEMU/OVMF are unavailable. Implementation complete; no real disk recovery success claimed.

## Running-system backup extension (user steering)

The user now requests backup while the installed system is running, using source / and destination /mnt/usb-8tb/sys-backup. Preserve offline mode as default; add explicit --live accepting the current writable installation and mark every such bundle live-nonatomic. No filesystem freeze, service shutdown, snapshot claim or actual full-machine backup during development. Destination /mnt/usb-8tb is confirmed ext4 rw by findmnt; restore protections stay unchanged.

- [x] Define RED tests for live source opt-in, runtime/unrelated mount exclusions, changed/vanished file handling, live publication and warnings integrity.
- [x] Implement explicit --live, best-effort vanished-file handling (revised 2026-10-07), recorded tar/copy warnings and consistency metadata; fail on actual read/permission/I/O errors.
- [x] Update operating guide/README/smoke checks and independently review extension.
- [x] Fresh regression/syntax/diff checks, actual-machine read-only preflight, protected refresh and installed equality.

Source/live data can change across files and root/home phases; archive/home integrity only proves copied bytes are stable, not application transaction consistency. Live root tar checks required boot/package metadata as before. A checksum-protected warnings.json records noticed changes. Offline mode retains source/copy equality validation. Restore prints the live consistency limitation, then uses the same checksums/archive/home validation and destructive guards. Rollback: remove the opt-in changes without rewriting existing backups or unrelated files.

### Live extension evidence and review

- RED: missing live interfaces/warnings artifact failed; alias fixture and warning-like filename permission failure reproduced, followed by shrinking-file RED.
- GREEN: python3 -m unittest discover -s tests -p 'test_backup_pc*.py' passes 37 tests, exit 0. bash -n and git diff --check pass. Expected synthetic warnings/errors are printed by deliberately exercised failure tests.
- Actual-machine source_preflight('/', '/mnt/usb-8tb/sys-backup', live=True) and destination_preflight passed without writes. Current USB filesystem is ext4 rw. Mounted backup/unrelated disks, Snap views and Docker overlay views are excluded dynamically; underlying installed Snap/Docker state remains included. Source swap alias resolved successfully.
- Independent reviewer found warning-like filenames could conceal actual tar errors. Anchored suffix checks corrected this with RED/GREEN cases for permission and I/O failures. Live directory timestamp rescans are skipped; metadata/integrity index describes the completed copy, not a moving source.
- Live mode permits changed/shrinking/vanished root files with checksummed warnings, while real tar read errors abort. Home vanished files are accepted on rsync exit 24 in one pass; other failures abort (revised 2026-10-07). Unmounted destination fallback to source filesystem is rejected. Old schema-2 offline bundles without warnings remain readable.
- Full-machine backup was not started. --live always labels non-atomic consistency; copying running databases/services does not prove recoverable application transactions. Restore retains all disk safety guards and displays the source consistency warning.
- README gate pass_no_change; new incident/learning checks both pass with current hashes. Snapshot dry-run passes; Codex/Git live/source files byte-identical before refresh.
- Exact user command after refresh: sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup. Add --dry-run for a write-free preview.

- First live refresh passed and installed script matches source. Strict shared-ledger hash audit flagged concurrent Codex-search evidence additions; no ledger restored. Owned report checks and actual-machine preflight verify backup independently. Other checkpointed files unchanged. See docs/postmortem/2026-10-06-backup-live-protected-ledger-check.md.

- Final live extension verification: 37 tests passed (2.956s), bash syntax and git diff --check passed. Second fish refresh-config finished with REFRESH COMPLETE, exit 0; installed ~/scripts/backup-pc exactly matches source. Actual-machine live source/USB destination preflight passed again without writes. Concurrent shared-ledger additions preserved; no full-machine backup or host disk restore performed.

## Compression resource budget extension

User requests roughly 75% PC resources instead of one-thread compression. Read-only inspection shows Ryzen 5 5500 (6 cores/12 logical CPUs), 62 GiB RAM, about 39 GiB available, and an active one-thread -9e backup. Preserve that process; it cannot be retuned and must be restarted by the operator. Preserve every existing dirty edit and shared incident ledger record.

Decision: backup defaults --resource-percent 75 (integer 1..100). Derive floor(affinity CPU count * percent / 100), minimum one thread; memory ceiling is the same fraction of min(MemAvailable,MemTotal), sampled before archive creation. Retain -9e and --no-adjust; XZ may reduce threads under the memory limit, never lower dictionary/preset. Use single-thread mode on low-memory budgets; fail before bundle creation if the budget cannot fit a full -9e encoder. Isolate compression from inherited XZ_OPT/XZ_DEFAULTS. This budgets worker threads/compressor memory, not a strict aggregate CPU/RAM quota; other backup phases stay unchanged. Multithreaded XZ uses independent blocks and may produce a slightly larger archive than a single stream. Source: https://tukaani.org/xz/man/xz.1.html and installed XZ 5.4.5 tiny-input -vv check (9 threads estimates 11243 MiB).

- [x] RED resource derivation, limits, CLI validation and actual archive command tests.
- [x] GREEN implementation and real compressed fixture round trips; update docs and smoke checks.
- [x] Review, regression, syntax/diff/README checks; protected refresh and installed equality.

Verification: python3 -m unittest discover -s tests -p 'test_backup_pc*.py'; bash -n scripts/executable_backup-pc; git diff --check; ./scripts/executable_readme-recruiter-sync; installed backup --help. Manual: cancel old invocation using Ctrl-C, wait for exit, restart explicit --resource-percent 75; verify preview selects 9 threads and an available-memory ceiling. No production full-machine backup started/cancelled by development. Rollback only this task's resource additions; incomplete old bundles remain visible. Tool syntax incident is scoped and registered separately, no backup side effects.

- Resource RED: five defining tests failed for missing budget/API/CLI and inherited XZ overrides. The first GREEN attempt exposed a fixture arithmetic typo (62 GiB * 75% = 46.5 GiB); corrected hand-checked literal without relaxing requirements. Incidents and targeted evidence registrations preserve shared source records.

- Review corrections observed RED then GREEN: sanitize inherited XZ options for creation, GNU tar validation and extraction; accept only the anchored successful thread-reduction notice. Real 2 GiB-limited archive completes and records reduced threads. Fresh 44-test backup suite passed (4.451s); syntax/diff checks pass. Repository-wide discovery ran 665 tests with seven unrelated policy/hash/vault/ledger failures, named and attributed in docs/postmortem/2026-10-06-backup-resource-verification-baseline.md; this task does not claim the whole repository is green.

- Resource delivery: fish refresh-config passed, installed script matches source, backup help exposes --resource-percent75 default, actual source/USB preflight passes and selects nine workers. All refresh-boundary protected hashes unchanged; current live Codex high setting captured as specified by refresh. No backup process retuned or cancelled. Operator restart required; original partial directory stays .incomplete. Exact command: sudo ~/scripts/backup-pc backup --live --source-root / --destination /mnt/usb-8tb/sys-backup --resource-percent 75. Existing handoff/VM recovery checks remain applicable; suggested follow-up subject feat(backup): budget parallel compression resources.

## Live progress and activity log extension

User requests live root/home percentages, a progress bar and time estimate, plus a file log showing current work. Current process inspection finds no backup compressor running; do not start a real machine backup. Preserve all dirty work, including newly dirty feedback.log.

Decision: add cohesive scripts/backup-pc-progress.py for the progress UI, estimator and selector-based streaming subprocess runner; backup lazily loads it and copies it into each bundle with checksums. Recovery remains self-contained in backup-pc, compatible with prior bundles lacking the optional helper. Every real backup creates mode600 backup.log in its private incomplete bundle; timestamps, phases, copy filenames, warning/error diagnostics and periodic plain-text progress stay readable while running. Log remains an operational extra outside restore integrity hashes because it is written through completion. Dry-run never creates logs.

Root+EFI byte denominator is a fast metadata-only pre-scan, pruning the exact runtime/cache/mounted/home exclusions, deduplicating hardlinks and accounting for sparse allocation plus approximate tar metadata. GNU tar checkpoints supply uncompressed input bytes; use fixed blocking factor20 and checkpoint record count, never compressed archive size. Root percentage/ETA explicitly approximate and capped below100 until the compressor exits and diagnostics validate; stalled compression/flush must stay visibly incomplete. Home uses rsync full-list progress2 and filename output; both bars, elapsed, estimated remaining time and current activity update at a bounded interval, with periodic log snapshots. Verification stages remain explicit after copy bars finish.

- [x] RED tests for estimator parity/sparse/hardlinks, ETA edge cases, streaming/progress parsing, logged activity/error/cancellation and complete portable bundle.
- [x] GREEN streaming progress helper integration without weakening warning/exit/disk guards.
- [x] Docs/smoke/independent review; focused and broader verification; protected refresh and installed helper equality.

Risks: scan adds metadata traversal; changing live files make estimates drift, while progress must never imply application consistency. Tar buffering may stall at the end, ETA must say unknown/finishing rather than promised done. Full rsync file-list enumeration consumes memory but gives a stable denominator. Drain stdout/stderr together to avoid pipe deadlock; terminate/reap only the command's process group on interruption. Protect path-bearing logs and escape control characters. No mounts or real disks written in development.

Verification: python3 -m unittest discover -s tests -p 'test_backup_pc*.py'; bash -n scripts/executable_backup-pc; git diff --check; README gate. Disposable round trips check bytes and metadata unchanged with streamed root and home progress, current filenames and mode600 logs in failed/completed bundles; packaged backup script can verify/help from /tmp, restore without progress helper still parses legacy bundle. Manual follow-up: start user backup, observe bars and sudo tail -f exact printed backup.log; confirm final BACKUP COMPLETE after verification. Rollback only new progress integration/helper and related docs; existing backup contents/restore guards unchanged. Suggested follow-up commit feat(backup): show live copy progress and activity logs. Existing Cursor handoff remains applicable with this extension.

- Progress RED: seven tests failed for absent progress helper. Subsequent RED reproduced a log-write failure leaving the child alive; cleanup now runs even when the log is full. Root estimator initially counted home bytes and the exclusion parity test caught it before delivery. GREEN: 52 backup tests passed (3.853s), including real streamed tar/rsync publication; log600 and checksummed optional helper verified. Main script remains991 lines; progress concerns organized in separate213-line helper. Final independent review and broad regression in progress.

- Final progress review: four meaningful gaps each reproduced RED and corrected GREEN: selector setup before spawn, temporary SIGINT/SIGTERM/SIGHUP handlers reaching owned-group cleanup, accurate published-path reporting after final log failure, and home ETA calculated from elapsed/percent rather than rsync elapsed summary timestamps. Fresh 57 backup tests pass (4.382s), syntax/diff/README gate pass; reviewer recheck reports no remaining substantive blocker. Initial broad discovery ran675 tests with the same seven known unrelated baseline failures and no errors (exact IDs in /tmp/backup-progress-full-tests-summary.json and earlier scoped baseline incident); final broad rerun pending.

- Final display verification: real 80-column PTY test reproduced wrapping RED, then GREEN after rendering separate root/home/activity rows fitted to terminal cell width. Fresh 58 backup/progress tests pass (4.150s); syntax/diff and README pass_no_change. Broader run679 tests reports only the same seven unrelated baseline failures, no errors (full exact IDs stored in /tmp/backup-progress-final-full-tests-summary.json; permanent named attribution in docs/postmortem/2026-10-06-backup-resource-verification-baseline.md). Initial progress refresh completed exit0, installed script/helper matched source, real-PTY rendering and actual-machine preflight passed. One unrelated Codex-search incident document changed in the checkpoint window; its current bytes were preserved, no stale restoration. Final refresh installs the width fix. No live backup started, no host disk or mount modified.

- Final width-fix refresh: REFRESH COMPLETE, exit0; installed script and helper match source byte-for-byte, final syntax/diff checks pass. Protected checkpoint changes printed separately for any concurrent unrelated writes; no restoration attempted. Progress feature installed; 58 focused tests GREEN and known broad-suite limits remain recorded above.

2026-10-07 access revision: generated archive/log/metadata ownership follows the invoking sudo account on startup, publication and failure; copied home ownership stays intact. `access --bundle PATH --user example-user` repairs older bundles without recursion. See plans/backup-owner-access.md for evidence and current sudo-authentication limit.

2026-10-07 naming/resync revision: local MM-DD-YY bundle directories with collision suffixes; sync-home updates only incomplete home data, inventory and warnings while preserving root archive/history and incomplete status. See plans/backup-date-home-sync.md.


## Authorized delivery verification — 2026-10-08

- [x] Reproduce the missing VM progress/sync sidecars before modifying staging:
  one expected RED (`VM tools disk missing backup-pc-progress.py`, exit 1).
- [x] Copy both helpers into the virtual tools disk; four VM tests GREEN and all
  67 backup tests GREEN (10.613 seconds, exit 0). Bash entrypoint syntax passed.
- [x] Correct stale root-only ownership descriptions and document sync sidecar;
  append grouped safe smoke checks to `docs/smoke-tests.md`.
- Incident: `docs/postmortem/2026-10-08-backup-vm-sidecar-staging.md` records
  lookup, minimal fix, fixture evidence and the known shell-startup workaround.
- Remaining: root delivery integrates matching postmortem learning and runs
  final refresh/checks. Guest boot and Secure Boot acceptance remain unverified;
  launcher/staging tests do not prove either. Rollback is limited to the new
  staging loop, regression and matching documentation; preserve existing backup
  work and every published or incomplete bundle.
