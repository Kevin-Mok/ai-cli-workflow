# Restore Vesktop theme dimming

Keep the current wallpaper, fonts and orange accents while restoring readable shading with one active full theme.

## Context and decisions
Scope: settings/settings.json and quickCss.css under dot_config/vesktop, regression check, README/smoke documentation and incident learning. Preserve pre-existing settingsSyncVersion and all unrelated dirty changes. Live CSS matches source; source files are newer. No automatic app termination.

## Checklist
- [x] Capture dirty state and inspect live/source configuration.
- [x] Reproduce conflicting themes and transparent overlay with executable assertions.
- [x] Enable ClearVision alone and restore a dark overlay.
- [x] Run regression checks and refresh-config; compare deployed files.
- [x] Record runtime limits and manual restart checks.

## Verification and risks
Run focused Python unittest; RED must identify conflicting themes and transparent overlay. GREEN must validate both. Run refresh-config and compare deployed settings/CSS. Manual: reload Vesktop, inspect channel and member-list readability, then restart and check launch. Remote upstream imports can still cause grey launch while loading or offline; startup behavior is not proven by config tests. Rollback only this task's settings/CSS hunks; preserve other work.

## Review notes
Commit-session now authorizes a scoped commit and upstream push. Runtime visual verification pending.

## Results
Two focused unittest checks failed before the edit and passed afterward. Official current main.css fetched successfully outside sandbox and consumes background-shading via hsl conversion. refresh-config exited 0; cmp confirmed source/live CSS and settings match (exit 0 each). Refresh also removed the initially clean private_mimeapps.list source file; that helper-only change was restored to HEAD without touching live MIME settings. No visual reload/restart observed. Existing settingsSyncVersion preserved.

Suggested commit: fix(vesktop): restore wallpaper shading
Cursor follow-up: Read this plan, reload Vesktop, verify chat/member/popout shading and cold launch; investigate remote CSS only if grey styling persists.

## Delivery milestone: fix(vesktop): restore wallpaper shading
Completed: configuration, regression tests, docs and incident learning. Verified: 2 focused tests pass; refresh-config and deployed comparison passed in the implementation turn; targeted ledger check clean. README gate pass_no_change. Scope helper returned unsafe (no writes detected), so staging uses directly observed session edits and excludes pre-existing mixed-file hunks. Remaining: visual reload and cold launch, grey-launch diagnosis if persistent. No implementation blocker; next step is the authorized upstream push after commit.
