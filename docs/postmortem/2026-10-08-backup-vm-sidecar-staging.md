# Backup VM sidecar staging gap

The disposable VM launcher staged the backup entrypoint without its required progress and home-sync helpers. This report tracks the staging regression and its safe fixture verification; no real disk recovery is performed.

## Symptom, impact and evidence

During authorized push preparation, source inspection found `initialize()` copied only `executable_backup-pc` and RECOVERY.md into the VM tools disk. The current backup entrypoint imports `backup-pc-progress.py` and copies `backup-pc-sync.py` from its own directory. The staged launcher therefore cannot create a full backup from those tools alone.

## Lookup and status

Query `backup VM sidecar staged helper missing` returned general wrapper/QEMU findings, but no matching staged-sidecar remedy. `ext-qemu-isolated-capabilities` describes emulator capabilities and is not applicable to missing application files. Reproduce with real launcher initialization, mock only external QEMU image commands, and inspect staged artifacts.

The first read-only command also failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Lookup `bwrap loopback Failed RTM_NEWADDR` matched `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route`; the diagnostic is identical. Approved scoped escalation executed the required reads. Host sandbox repair remains outside scope.

## Resolution and verification

Root cause: the VM staging list predates the sidecar dependencies added to backup creation. The minimal fix copies both helpers next to the entrypoint, matching the published bundle arrangement. Ownership documentation now agrees with the invoking-sudo-user policy and lists the sync sidecar; grouped smoke checks cover automated fixtures and safe command interfaces.

Intentional RED: `python3 -B tests/test_backup_pc_vm.py VmTests.test_init_stages_required_backup_helpers_with_the_entrypoint` failed with `VM tools disk missing backup-pc-progress.py` (one expected failure, exit 1). After the fix, `python3 -B tests/test_backup_pc_vm.py` passed four tests. `python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'` passed all 67 tests in 10.613 seconds, exit 0. Bash syntax check passed. Expected fixture tar warnings exercise rejected paths/permission/I/O failures and are not new incidents.

A help probe used the wrong subcommand `exclusions` and failed with argparse exit 2. The actual inventory advertises `excludes`; corrected `./scripts/executable_backup-pc excludes` succeeded. No files were changed by either probe. This is a probe-name error, not a backup regression; the existing discover-paths/command-contract guidance remains applicable.

Status: verified_fix, code scope; root-cause confidence confirmed. QEMU commands are mocked only at the external image-creation boundary; staging, metadata writes and copies are real. No QEMU guest boot, Secure Boot verification, source mounts or host disk writes were performed. No staging, commits or push by this subtask. Root delivery owns the ledger registration and final refresh/integration checks.
