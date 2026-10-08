# Backup recovery reference lookup misses

Two read-only review searches named files that do not exist, and an optional online xz manual request was rate-limited. Use the actual repository paths and the installed xz manual; these misses did not change application files or block verification.

- Symptoms/evidence: reviewer rg calls included docs/backup-recovery.md and tests/test_backup_pc_split.py and returned exit 2. Actual files are docs/backup-pc-recovery.md and tests/test_backup_pc.py. Documentation agent's optional xz manual web lookup returned HTTP 429.
- Impact: ancillary reads only; no disk/mount/file mutations. Successful reads in the same calls still supplied source context, but failed calls are not verification evidence.
- Lookup: inspected the tracked postmortem-memory execution-environments and workflow guidance. Known sandbox workaround is separate from these misses; path existence is the distinguishing evidence.
- Root cause: speculative file names in reviewer reads and external server rate limiting.
- Resolution/status: correct paths used in subsequent source review; installed /usr/share/man/man1/xz.1.gz supplies the -9e table row (64 MiB dictionary, 674 MiB encoder, 65 MiB decoder). Reviewed code and fixture tests continued.
- Verification: actual recovery guide and split tests read successfully; installed manual table inspected by documentation agent. All 29 current backup tests pass. No live VM boot test performed.
- Follow-up: use rg --files before speculative file reads, and installed primary manuals for matching tool versions.
- Learning: no new reusable learning; this repeats existing file-discovery and primary-source verification practices. Register explicit no-new-learning decision.

During the live-backup documentation extension, an assertion caught missing explicit live-USB-only restore wording in the smoke section. The sentence was added and the scoped assertion plus diff check passed. No implementation behavior changed; this repeats keeping procedure expectations aligned with the guide.

During progress implementation, the optional official GNU tar checkpoints page timed out before content retrieval. The installed tar.1 manual supplied checkpoint, verbose quoting and totals options instead; a disposable local checkpoint probe verifies behavior. A diagnostic helper piped through head also printed BrokenPipeError when the reader closed; use structured result filtering rather than truncating the helper pipe. These ancillary reads did not change or interrupt a backup.
