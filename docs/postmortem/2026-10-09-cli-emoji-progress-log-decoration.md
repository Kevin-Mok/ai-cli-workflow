# Backup progress decoration reached saved logs

Review found an output-boundary regression during the emoji rollout. Keep terminal decoration separate from persisted progress records, then verify both default and plain modes.

## Symptom and impact

The new backup progress icon was added before the same text was written to `[progress]` log records, changing generated log content. No live backup was run for this review.

## Lookup and evidence

Lookup: `decorative emoji generated logs`; the reviewed `local-terminal-report-readable-projection` guidance applies to terminal presentation, while the canonical output policy explicitly preserves generated files. The agent inspected the shared `parts` text and confirmed the contamination with a defining executable regression (expected RED).

## Resolution and verification

Status: verified_fix, code scope. Keep `parts` plain and decorate only the terminal row. The regression now passes for default output and CLI_PLAIN=1; three existing percentage/ETA, terminal-width and home-log checks pass (four targeted checks total). Session renderer assignment also moved after its docstring; 14 renderer tests passed. Live disk synchronization and backups were not exercised.

## Learning and follow-up

No new reusable finding: existing terminal-projection guidance and the explicit generated-file preservation policy cover this boundary. Include the regression with the fix. During scope inspection a recursive /tmp search encountered protected systemd directories; use explicit known artifact paths instead. No protected content was accessed or changed.
