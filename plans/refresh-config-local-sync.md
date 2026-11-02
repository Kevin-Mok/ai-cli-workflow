# Preserve local changes during refresh

Preserve modified managed files with chezmoi re-add before applying, and retry recoverable drift. Templates and ignored machine/private settings retain chezmoi protections.

- [x] Capture dirty state; preserve unrelated sources ledger, incidents, tv shortcut and feedback.
- [x] Define regression requiring re-add before apply.
- [x] Implement synchronization and recoverable retry in refresh-config.fish.
- [x] Update README and smoke checks; verify fixture and live refresh.

Scope: helper, existing tests and docs. No force overwrite, new dependencies or history changes. Retry only drift failures; stop repeated identical failures to avoid hanging on templates or fatal errors. Rollback: restore helper. Verification: bash tests/test_refresh_config_function.sh; fish -n; deployed refresh and tv abbreviation lookup. Initial failure: mimeapps.list drift prompted on noninteractive stdin and returned EOF.

Evidence: defining test failed before implementation (missing re-add); corrected live refresh exited 0 and reloaded shortcuts. fish -n and git diff --check passed. Broad re-add was rejected after live evidence; restored incidental changes and limited import to status first-column local drift. No commit requested.

Delivery milestone: fix(fish): preserve local changes during refresh. Focused regression passed in implementation turn; live refresh exited 0. Session scope helper unavailable (no detected writes); direct conversation writes establish scope. README gate pass_no_change. Remaining work: tv expansion not confirmed; unrelated dirty work excluded. Commit/push pending.
