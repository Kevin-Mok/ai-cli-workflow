# Preserve local changes during refresh

Preserve modified managed files with chezmoi re-add before applying, and retry recoverable drift. Templates and ignored machine/private settings retain chezmoi protections.

- [x] Capture dirty state; preserve unrelated sources ledger, incidents, tv shortcut and feedback.
- [x] Define regression requiring re-add before apply.
- [x] Implement synchronization and recoverable retry in refresh-config.fish.
- [x] Update README and smoke checks; verify fixture and live refresh.

Scope: helper, existing tests and docs. No force overwrite, new dependencies or history changes. Retry only drift failures; stop repeated identical failures to avoid hanging on templates or fatal errors. Rollback: restore helper. Verification: bash tests/test_refresh_config_function.sh; fish -n; deployed refresh and tv abbreviation lookup. Initial failure: mimeapps.list drift prompted on noninteractive stdin and returned EOF.

Evidence: defining test failed before implementation (missing re-add); corrected live refresh exited 0 and reloaded shortcuts. fish -n and git diff --check passed. Broad re-add was rejected after live evidence; restored incidental changes and limited import to status first-column local drift. No commit requested.

Delivery milestone: fix(fish): preserve local changes during refresh. Focused regression passed in implementation turn; live refresh exited 0. Session scope helper unavailable (no detected writes); direct conversation writes establish scope. README gate pass_no_change. Remaining work: tv expansion not confirmed; unrelated dirty work excluded. Commit/push pending.

## 2026-11-16: explicit local-first refresh

User reaffirmed that local managed-file updates must enter this repo before continuing rf. Keep prior milestones above; this follow-up preserves existing ordinary-file import and adds source backups before local-priority import, with explicit template refusal rather than silent re-add skipping.

Scope: refresh-config.fish, existing real/fake refresh regression fixture, README/smoke, durable public-safe feedback and incident evidence. Initial dirty state is recorded at /tmp/refresh-duplicate-evidence/local-first-initial-status.txt; protect all unrelated and earlier-session work. No commit/push requested.

- [x] Inspect installed chezmoi semantics and existing helper; record user preference.
- [x] Verify actual local-only managed update reaches source before apply (real CLI fixture).
- [x] Observe RED for missing source backups/concurrent edits and template refusal.
- [x] Back up prior repo source before local-priority import; stop local template conflicts safely.
- [x] Run focused and real CLI checks; deploy and refresh.
- [x] Align docs, review evidence and record final limitations.

Evidence: chezmoi2.61.0 first status column compares actual with last-written state, second with target. Local-only and both-edited files both report MM, so source cannot be protected by status alone. Existing re-add imports ordinary local changes but replaces source-only concurrent edits, and skips templates. Real local-first regression passed before production changes; the new requirements preserve repo copy outside source first. Templates retain placeholders and local edits; merge is required before apply rather than copying rendered values into portable source. Ignored secrets/machine-local settings remain excluded.

Verification commands: bash tests/test_refresh_config_function.sh; bash tests/test_mimeapps_fnlb_handler.sh; fish --no-config -n dot_config/fish/functions/refresh-config.fish; actual refresh must complete0. Use isolated real chezmoi fixture for local-only, source-only, both-edited and template cases; do not manufacture live conflicts. Rollback: restore helper from /tmp/refresh-duplicate-evidence/rollback, source backups are private XDG state. Suggested commit: fix(fish): preserve source copies before importing local updates. Cursor continuation: read this plan and preserve dirty work, rerun real CLI checks with temporary HOME/state, preserve template placeholders and source backups; no commit/push authorized.

Defining RED: local-first-red.log fails “repo content must be backed up before local import” before production changes. Helper now resolves each locally modified source, preserves a private outside-source repo copy, then re-adds the local file. Changed template sources stop explicitly before apply. CLI phases now identify copying local updates before apply. Common existing backup containment guard applies to local backups as well as MIME recovery.

Final GREEN: local-first-green.log covers real local-only and both-edited imports, repo backup before apply and template refusal. Separate isolated source-only check passes with no re-add, repo content preserved and applied to HOME (source-only-check.log). Its first diagnostic wrapper used the local-first equality gate incorrectly for source-only data and exited88; corrected guard rejects only re-add and verification passes. No production defect inferred from that fixture error. MIME guard and fish syntax pass. Independent reviewer6claims verified/no issues.

Deployed after checking live helper matched the previous reviewed version; rollback helper stored /tmp/refresh-duplicate-evidence/local-first-rollback/refresh-config.fish. Actual refresh exits0 and prints explicit copy-local→apply phases and REFRESH COMPLETE (/tmp/refresh-duplicate-evidence/local-first-live-refresh.log, private /tmp/refresh-config.S7Xx8X4E.log). This actual run had no local files to import; data-flow claims are proved by isolated real CLI fixtures, not invented live imports. Ignored/private values stay excluded. Global status includes source-only differences; do not equate successful refresh with whole-tree status empty. Source-only handling is verified separately.

User preference saved append-only in canonical feedback.log. No commit/push. Current policy is local-priority for ordinary managed files with prior repo version recoverable; changed templates stop for manual merge to retain placeholders, and untracked/ignored private data is not blindly imported. Relevant docs updated and final diff/incident ledger checks complete before handoff.

## Session delivery milestone

Subject: feat(desktop): soften palettes and preserve local config. Complete session scope includes muted wallpaper palettes/verifier, full-pool i3 selection/history, safe MIME duplicate recovery and local-first source backups/template refusal with matching tests/docs/plans. Scope helper could not detect tool writes for thread01a1e5d4-be1c-72d3-b7bd-1836fa29179d; direct conversation writes plus initial dirty baseline establish eligible hunks. Shared README/smoke/feedback/lessons/ledger use attributed partial snapshots; unrelated privacy/night/Lavish/CTO work remains untouched. Reviewed dependencies exist in HEAD; accepted saved pywal prompt included as required spec.

Fresh delivery checks:45Python tests across palette/verifier/XCF/shuffler/history/i3 suites and3Bash workflows all pass. Earlier fresh667-image full-library result, source/cache unchanged evidence and actual terminal/i3/refresh activation remain recorded in their plans. Final candidate privacy gate and exact staged diff are required before commit; push origin/main after the verified commit. Exact scope/remaining paths are recorded in docs/handoffs/2026-11-16-desktop-session.md. No implementation work remains; commit/push is the current delivery step.
