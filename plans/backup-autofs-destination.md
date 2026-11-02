# Correct backup automount detection

Make backup preflight recognize the real filesystem beneath a systemd automount, retaining destination and source-disk safety checks.

## Scope and decisions

Update scripts/executable_backup-pc and tests/test_backup_pc.py, recovery documentation and smoke checks. Reuse mount-table selection, preferring non-autofs only on equal target lengths. Report read-only failures separately. No formatting, remount, full backup, commits or pushes. Initial dirty state: postmortem-memory ledger and five references, Vesktop settings, unrelated SSH postmortem; preserve all unrelated hunks.

## Ordered checklist

- [x] Diagnose and record incident and initial state.
- [x] Observe defining RED tests for stacked autofs and read-only diagnostic.
- [x] Correct all three containing-mount selections and diagnostics.
- [x] Run backup regression suite, syntax checks; update docs and learning.
- [x] Verify installed behavior where permissions permit and record limitations.

## Verification

Tests: python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py'. Syntax: bash -n scripts/executable_backup-pc. Manual: inspect findmnt, then operator dry-run and backup only on writable ext4. No destructive checks. RED: destination tests ran 3 with one expected error (autofs) and one expected failure (read-only diagnostic). GREEN: complete suite 71/71, exit 0 outside sandbox; sandbox had one setfacl Invalid argument error. bash -n exit 0. Installed destination validation passed against actual host rw ext4/autofs; bytes match source. Targeted chezmoi apply and refresh-config exited 0. Full sudo -n dry-run blocked by required password; operator acceptance and backup/restore remain unverified. Independent diff review found no issues.

## Risks and rollback

Sandbox mount flags do not prove host flags; do not attempt repairs from sandbox. Retain deepest mount precedence and unsupported filesystem rejection. Roll back only task hunks, preserving pre-existing work. No complete backup or boot restore acceptance is implied.

## Review and handoff

Cursor prompt: Review the automount selection regression in this plan, preserve read-only/source-disk guards, and verify with the backup suite before any live backup.
Suggested commit: fix(backup): detect real filesystem behind automounts

Final learning check: targeted postmortem-memory check passed (one report, zero errors); git diff --check passed. New finding local-backup-autofs-selection records runtime validation only. No commit or push requested or performed.

## Session commit milestone

Authorized by $commit-session after the implementation and documentation milestones. Ship one commit, `fix(backup): handle automounts and document recovery`, with both plans, the automount regression fix, quickstart, README/smoke updates and the two reviewed incidents/findings. Use direct-write fallback: session 01a199ee-c88a-7d12-b6ac-47530f859018 scope helper returned unsafe/no detected write baseline for functions.exec transport, despite observed successful writes in this conversation. Stage only the two new registry reports/findings and backup checklist block; preserve pre-existing registry changes, unrelated fish/checklist edits, Vesktop settings, five other memory references and the SSH incident.

Fresh commit-session checks: backup suite 71/71 and Bash syntax exit 0 outside sandbox. README gate initially pass_no_change; additionally corrected its restore row to disclose the verified blocker. Privacy gate and exact staged review required immediately before commit. No full restore, archive rehash or boot test performed. Interactive restore remains blocked; no fix claimed. Config refresh and installed destination validation succeeded during implementation. Next step: commit reviewed scope, then push main to origin/main once; report actual commit hash and push result in chat. Keep local commit intact if push fails.
