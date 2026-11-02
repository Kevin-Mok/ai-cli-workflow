# Backup destination detection

Use mount-table evidence to distinguish an unsupported destination from an automount selection defect.

## local-backup-autofs-selection

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Writable ext4 destination rejected with FAT/exFAT/NTFS error.
- Applicability: autofs and a real filesystem share a mount target.
- Diagnostics: Inspect all findmnt entries. Check host flags outside sandbox; sandbox read-only flags do not prove host failure.
- Remedy: Prefer real filesystem on equal target lengths in destination, source-disk and ancestry checks; preserve deepest-path and writable Linux filesystem guards.
- Verification: Two defining RED tests; 71 backup tests and Bash syntax pass outside sandbox. Installed destination validation passes on actual host rw ext4/autofs; source/live bytes match and refresh-config succeeds.
- Limitations: Full sudo dry-run needs interactive password; no complete backup or restored boot was tested. Sandbox ACL fixture error disappears outside sandbox.
- Source: [2026-11-01-backup-autofs-destination.md](/home/kevin/linux-config/docs/postmortem/2026-11-01-backup-autofs-destination.md) (SHA-256 `6f4538f8af807037908aa04771f8fcc471a2cd404b83b16e027c5fc8f46111e2`).
