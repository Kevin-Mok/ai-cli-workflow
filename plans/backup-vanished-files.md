# Best-effort live home backup

Accept files disappearing during a live home copy, preserve warning evidence, and continue integrity verification and publication.

## Scope and decisions

The user explicitly accepts missing files after copying starts. Accept only rsync exit 24 in live mode; other errors and offline strictness remain. Existing dirty backup source/tests/docs and all unrelated work are protected. No disk writes or backup restart are requested. Plan Mode is unavailable in this session; this document records the implementation plan.

## Checklist

- [x] Capture initial status and inspect copy/publication paths.
- [x] Observe RED for a single best-effort pass and published warning evidence.
- [x] Remove vanished-file retries, update docs and smoke expectation.
- [x] Run all backup tests, shell syntax, sync configuration, inspect installed bytes.
- [x] Record evidence and review notes.

## Verification and risks

Automated: python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'; bash -n scripts/executable_backup-pc. Mock code 24 with and without progress, and retain code 23/offline rejection. Manual: next authorized live backup should finish despite code 24, save warnings.json, and verify its copied-home inventory. No real backup or restored boot will be run. Live data remains nonatomic. Rollback: restore the previous copy_command and associated tests/docs only, preserving pre-existing work.

## Progress and review

Root cause: three whole-home retries cannot converge while applications rotate LevelDB files. Accepting documented vanished-source status preserves copied-data checks. Initial status contained extensive prior recovery work; no commit is requested.

Verification: defining direct-copy test RED with 2 calls instead of 1; progress test RED with retry exhaustion. Full backup suite GREEN: 58 tests, exit 0. Shell syntax, git diff --check and installed-byte cmp each exited 0. refresh-config completed with REFRESH COMPLETE, exit 0. Incident learning registered in tracked ledger and artifact-verification guidance; both targeted postmortem checks exited 0 with no errors. No actual backup restarted.
