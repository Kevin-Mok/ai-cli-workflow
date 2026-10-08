# Snapshot command inspection failure

The refresh inspection queried an executable as a fish function. This records the harmless probe failure and correction.

- Symptom and evidence: `fish -c 'functions refresh-config; functions snapshot-codex-config'` exited 1 after printing the refresh function.
- Impact: no config changes; only the inspection failed.
- Root cause: `snapshot-codex-config` is an external Python executable, not a fish function.
- Resolution and verification: read `scripts/executable_snapshot-codex-config`, which defines the executable entry point and `--dry-run` option.
- Status: resolved; run refresh using the existing function.
- Follow-up: use executable inspection for external commands.
