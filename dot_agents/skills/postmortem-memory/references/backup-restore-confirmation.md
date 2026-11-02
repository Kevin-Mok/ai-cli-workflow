# Backup restore confirmation

Check interactive confirmation separately from archive integrity and dry-run readiness.

## local-backup-restore-stdin-confirmation

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: ERASE prompt receives EOF and cancels before destructive operations.
- Applicability: Embedded Python supplied through a stdin heredoc, followed by input().
- Diagnostics: Inspect launcher and confirmation; use an isolated heredoc reproducer, never a real disk erase.
- Remedy: Pending implementation to separate source transport and confirmation input; retain explicit erase consent and test through the actual launcher.
- Verification: Reviewer and root isolated reproductions establish EOF. Installed and dated-bundle source have the same pattern. Dry-run/help do not exercise input.
- Limitations: No fix or actual restore performed. Preserve checksummed bundle; do not bypass confirmation. Boot acceptance remains separate.
- Source: [2026-11-02-restore-confirmation-stdin.md](/home/kevin/linux-config/docs/postmortem/2026-11-02-restore-confirmation-stdin.md) (SHA-256 `1d3dd7eb6140d1fbb8c7a583ab7a5e82aacf4fc0a98d75afc95add8fc8720e1f`).
