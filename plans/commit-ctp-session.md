# Commit ctp shortcut session

Record delivery of the ctp shortcut and the shared-index incident, preserving published history as the user requested. Verify the installed shortcut, check incident knowledge, then push a focused documentation follow-up.

## Context and scope

Session 01a11cfa-b056-7ef0-b9e9-dbde91247324 used direct observed-write attribution because the scope helper detected no writes. Initial status was captured before modifications. Mapping ctp to codex-time projects, its smoke check and inspection incident were intended for one scoped commit. Concurrent staging added other-session content to 5451db5. Another session then published it and follow-up f8f044e. The user explicitly chose to keep that history intact.

This follow-up includes only this plan, docs/postmortem/2026-10-08-ctp-session-staging-race.md, and its ledger/reference additions. Existing commits, README, fish skill/tests, directory mapping, and other-session documents remain unchanged. The mapped command is never executed.

## Decisions and ordered checklist

- [x] Add ctp in work with zero conflicts and run refresh-config (exit 0).
- [x] Verify syntax, installed expansion and repeat-request no-op.
- [x] Record mixed commit 5451db5 and subsequent remote publication f8f044e.
- [x] Obtain user decision: keep published history intact.
- [x] Run README gate (pass_no_change); use direct-write scope fallback.
- [x] Run fresh focused checks and inspect exact follow-up diff.
- [x] Prepared commit milestone: docs: record ctp session staging incident.
- [ ] Push focused follow-up to origin/main and verify remote equality.

## Verification

Run fish -n ~/.config/fish/key_abbr.fish (exit 0). Filter fish abbr --show to ctp (codex-time projects). Repeat installed fish-alias JSON preview (changed false, conflicts 0). Run postmortem_memory.py check --postmortem against the staging report (errors empty). Run git diff --check and inspect only the four follow-up paths. Verify resulting commit changes exactly those paths and final HEAD equals origin/main and remote main.

## Risks, rollback and review

Shared index is mutable: commit with --only and the four explicit reviewed paths so other staged files cannot enter. Preserve all existing work. No history rewrite, reset or force-push is performed. This is a documentation follow-up; no tracked configuration changes require another refresh. Rollback would remove follow-up documentation through a new reviewed commit while retaining published application changes. Staging-race prevention remains unverified; delivery is closed by user decision, not a claim that the race was repaired.

## Commit milestones and current overview

5451db5 — ctp installed and verified; commit also contains concurrent session changes, an acknowledged scope error.

f8f044e — another session published fish verification and the preceding mixed commit; kept intact by user request.

Follow-up docs: record ctp session staging incident — completed documentation, ledger and guidance reconciliation. Verified: README gate pass_no_change; fish syntax exit 0; installed expansion codex-time projects; repeat preview changed false with conflicts 0; targeted incident check errors empty; scoped diff passes whitespace checks and contains only the intended documentation. Remaining: create and push the focused follow-up. Blockers: none for authorized delivery. Next: verify, commit explicit paths and push normally.
