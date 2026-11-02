# Document dated backup bundles

Provide an operator quickstart for creating a backup under /mnt/usb-8tb/sys-backup and restoring a complete dated bundle such as 11-01-26. Reuse the existing CLI and detailed recovery guide; do not modify scripts or backup files.

## Context and decisions

The existing docs/backup-pc-recovery.md covers the full implementation but lacks a focused dated-bundle walkthrough. Add docs/backup-pc-quickstart.md, link it from that guide and README.md, and capture its manual check in docs/smoke-tests.md. No new CLI or options. Use installed helper for backup and bundled helper for recovery. Restore from a live USB to a replacement whole disk; retain original-source protection.

Initial dirty state includes earlier backup fix/source/tests/docs, postmortem-memory records/references, Vesktop settings, and unrelated SSH incident. Preserve all of it. No commit/push requested. Documentation-only work requires no behavioral RED/GREEN test or configuration refresh.

## Ordered checklist

- [x] Capture status; read current guide and relevant CLI implementation.
- [x] Confirm target restrictions, dry-run ordering, root sizing and confirmation via focused search agent.
- [x] Write the dated-bundle quickstart and navigation links.
- [x] Update grouped smoke checks without duplicating existing backup checks.
- [x] Verify documented flags with installed/bundled --help; inspect relative links and diff.
- [x] Record review results and unverified live actions.

## Verification plan

Run ~/scripts/backup-pc backup --help and the example bundle's backup-pc restore --help; both must exit 0 and expose the documented arguments. Read its manifest, COMPLETE and RECOVERY.md without rehashing the large archive. Run git diff --check and validate local links in edited documentation. Review all destructive steps for target placeholders and whole-disk warnings. Do not run backup, restore, mount, package installation or live-USB actions.

## Risks and rollback

Never substitute a guessed target device. The source NVMe and backup drive are protected. Live backup is nonatomic; published metadata does not prove current archive integrity or bootability. Keep the whole bundle with metadata intact. To roll back, remove only this quickstart and its new links/checks, preserving prior changes in the recovery/smoke docs.

## Review and delivery

Documentation, README link and grouped smoke check completed. README gate outcome: update_in_same_change; the existing backup command row now links the quickstart and its documented arguments still match help. Existing recruiter-first hierarchy and command/setup coverage were preserved.

Verification this turn: installed backup --help and bundled restore --help exit 0; local documentation links resolve; example COMPLETE marker and manifest match full-system split storage; git diff --check exits 0. No behavior tests were rerun for prose-only changes. No configuration or runtime-script change; no refresh-config required.

Independent review discovered a pre-existing interactive restore defect: Python stdin is consumed by the heredoc before input() reads ERASE confirmation. Reviewer and root isolated reproductions confirm EOF without touching disks. Scope revised to document the blocker prominently in quickstart and detailed guide, record docs/postmortem/2026-11-02-restore-confirmation-stdin.md, and register unresolved finding local-backup-restore-stdin-confirmation in postmortem-memory. Targeted learning check passed, zero errors. No fix is claimed; backup and dry-run are unaffected. No complete restore can be claimed until repaired and boot-tested.

No mount, package installation, backup, restore, archive rehash, boot acceptance, commit or push performed. Do not alter the existing checksummed bundle. Unrelated dirty files preserved. Documentation/source formatting was reviewed; actual wrapped selection/paste in a fresh fish TUI remains unverified. Suggested commit: docs(backup): add dated-bundle backup and restore quickstart

Cursor prompt: Review docs/backup-pc-quickstart.md against scripts/executable_backup-pc, check the replacement-disk and full-bundle requirements, preserve prior dirty changes, and run the documented help/link checks without executing a restore.

## Session commit milestone

Authorized by $commit-session after the implementation and documentation milestones. Ship one commit, `fix(backup): handle automounts and document recovery`, with both plans, the automount regression fix, quickstart, README/smoke updates and the two reviewed incidents/findings. Use direct-write fallback: session 01a199ee-c88a-7d12-b6ac-47530f859018 scope helper returned unsafe/no detected write baseline for functions.exec transport, despite observed successful writes in this conversation. Stage only the two new registry reports/findings and backup checklist block; preserve pre-existing registry changes, unrelated fish/checklist edits, Vesktop settings, five other memory references and the SSH incident.

Fresh commit-session checks: backup suite 71/71 and Bash syntax exit 0 outside sandbox. README gate initially pass_no_change; additionally corrected its restore row to disclose the verified blocker. Privacy gate and exact staged review required immediately before commit. No full restore, archive rehash or boot test performed. Interactive restore remains blocked; no fix claimed. Config refresh and installed destination validation succeeded during implementation. Next step: commit reviewed scope, then push main to origin/main once; report actual commit hash and push result in chat. Keep local commit intact if push fails.
