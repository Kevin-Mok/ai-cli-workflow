# i3 wallpaper activation evidence

Keep the all-wallpaper bindings and history activation accurate while preserving unrelated local configuration.

## Symptom, impact and status

An exploratory read of the optional .chezmoi.toml.tmpl returned exit2 because that file is absent. No files were changed. Installed i3 configuration has a newer timestamp than the source template; compare rendered source before any installation. Earlier task established that full refresh stops on duplicate MIME targets; preserve both files if that conflict persists.

## Evidence and next steps

Use successful `chezmoi execute-template` output to compare installed config, apply only reviewed binding changes, back up local config/scripts, validate and reload once. Tests intentionally failing before implementation are TDD RED and not incidents. Prior postmortem-memory lookup identifies duplicate MIME targets as an unrelated existing activation blocker; don't infer full activation from scoped success.

Full refresh attempt exited1; /tmp/refresh-config.w5sHsxNl.log confirms the same duplicate .config/mimeapps.list targets. No local drift import or global apply completed. Rendered-source/local comparison found additional local shortcuts and private machine data; preserve them by changing only matching wallpaper-selection lines. Source template keeps its portable existing values; private values are not imported. Scoped install/reload is next.

Scoped install validated candidate i3 config (exit0), installed scripts and restored the current theme (exit0), including history hook. The subsequent verification command incorrectly JSON-parsed `i3-msg -t get_config`'s default human output and raised JSONDecodeError. This is verification parsing failure after activation, not evidence of reload/application failure. Preserve the successful installed state; inspect local i3-msg help and request raw JSON for verification, without another reload.

Raw IPC verification succeeded with `i3-msg -r -t get_config`; installed manpage confirms default GET_CONFIG output is plain config, while -r returns JSON. Four active random-selection bindings now use full-root image mode; candidate validation and current-theme restore both exited0. History default/plain and duplicate suppression work. Actual shuffler selected a valid collection image without applying it or recording a selection as usage.

New isolation issue exposed by live history inspection: three entries point to pywal test fixtures (/tmp/.../dim.ppm, one-color.ppm and two-color.ppm). Existing readable-suite fixtures override HOME/cache but inherit XDG_STATE_HOME, so the new automatic wrapper hook can write caller history during tests. Preserve current history before cleanup; reproduce with a poisoned disposable parent state, then override XDG_STATE_HOME in the fixture and verify no external writes. Remove only these exact session-created test records; keep the real current-wallpaper entry. This is test pollution, not actual historical wallpaper use.

Memory lookup `PYWAL_CACHE_DIR XDG_STATE_HOME isolation history` returned a prior tracker runtime-fixture isolation finding (local-tracker-validation-runtime); general home/state isolation applies, though that remedy concerns locks/sockets rather than this history hook. Defining poisoned-parent reproducer:11/11suite tests pass but writes wallpaper-history/history.jsonl and nvim/log to caller state. Fix adds explicit fixture XDG_STATE_HOME override; fresh externally poisoned run must leave parent state absent.

## Resolution and verification

Scoped activation verified: installed3scripts match source, i3 candidate validates0, current theme restore0 and rawIPC confirms4active full-root image bindings. History default/plain and consecutive-duplicate suppression work live; selection alone does not record an application. Snapshot and rollback script are in /tmp/i3-all-wallpapers-evidence/rollback. No source images changed. Full refresh still blocked by unrelated MIME duplicate targets.

Test-isolation fix verified GREEN:11pywal tests pass with a fresh poisoned parent XDG_STATE_HOME left empty; shuffler4/history9andexistingBash checks pass. The3exact fixture rows were removed under flock after preserving a backup; the real current-wallpaper record remains. Local lesson appended to tasks/lessons.md. Existing isolation and IPC-contract guidance applies; no additional generalized finding. Independent source review found no material defect. Direct wallpaper setter success is not proven because upstream pywal starts feh asynchronously; no different live wallpaper or physical shortcut was exercised. Rollback syntax checked but not executed.

## Follow-up diagnosis: user refresh run

The user's refresh log /tmp/refresh-config.7axnaIlY.log confirms the same exact duplicate target before any apply. Read-only comparison: untracked dot_config/mimeapps.list and tracked dot_config/private_mimeapps.list are byte-identical (1615bytes each), with no unique lines in either. Both map to ~/.config/mimeapps.list; the private_ attribute controls target permissions rather than a distinct destination. Diagnosis only: neither duplicate was removed or changed. Consolidating the untracked duplicate into the tracked private source would preserve all content, but cleanup was not requested in this question. Lookup `chezmoi mimeapps inconsistent state` returned unrelated CLI/hidden-prompt findings; no remedy from those was applied. Existing incident still records the unresolved global refresh blocker; no new generalized learning.

## Authorized duplicate recovery

User now explicitly authorized fixing the current duplicate and updating refresh-config to handle identical duplicates automatically. Fresh pre-change reproducer exits1 with the same inconsistent MIME target; byte equality and untracked ordinary/tracked private ownership reconfirmed. Defining regressions and safe backup/recovery are next; differing contents and ambiguous targets must remain untouched.

## Duplicate blocker resolved

Updated refresh-config automatically consolidates only the byte-identical ordinary/private MIME pair. It requires a valid source directory, rejects differing contents and symlinks, verifies canonical backup storage is outside source, moves the ordinary copy into a0700private state backup and keeps private_ ownership. Defining RED followed by fresh GREEN verifies recovery and fail-safe cases, progress/plain output and real chezmoi exclusions. MIME source test now uses tracked private source. Boundary review caught successful-but-invalid source output and inside-source state storage; additional REDs preceded fixes.

Actual refresh process19272 exited0 and emitted REFRESH COMPLETE (/tmp/refresh-duplicate-evidence/live-refresh.log, underlying /tmp/refresh-config.AvmYrbVy.log). Permanent backup /home/kevin/.local/state/refresh-config/backups/mimeapps.McTFS2cw/mimeapps.list matches retained private source exactly. Source-path resolves correctly, installed MIME permissions600, deployed helper matches source. Whole-source baseline hashes confirm no tracked source changes during apply; unrelated work preserved. Live i3 validates/reloads once and fullpool bindings remain correct. Earlier blocked-refresh statements above are historical; this blocker is now resolved. Local engineering lesson recorded; existing state/attribute/conflict preservation learning applies, no new generalized finding. Scope excludes other duplicate types and never auto-merges differing data.

## Local-first generalization follow-up

User reiterated copying local managed updates into the repo before rf continues. Installed chezmoi2.61.0 isolated experiments show normal re-add already does this, but both-edited/local-only statuses are both MM; re-add can overwrite concurrent repo edits, and templates are skipped without error. A real integration fixture confirms ordinary local-first order. New defining regressions require recoverable repo backups before local-priority imports and explicit refusal for changed templates, retaining portable placeholders and local values. No actual user's config was overwritten in these isolated probes.

Local-first follow-up verified: explicit source backup precedes local re-add, ordinary local version wins while concurrent repo content is recoverable; changed templates stop before apply preserving rendered changes and placeholders. Real CLI regression passes for local-only, both-edited, and template cases. Independent source-only check confirms no re-add and correct repo→HOME apply. One diagnostic fixture initially imposed a local-edit equality gate on a source-only case and exited88; corrected fixture passed, no production issue inferred. Current deployed helper equals source and actual refresh exits0 with REFRESH COMPLETE (/tmp/refresh-duplicate-evidence/local-first-live-refresh.log); no local imports were needed on that real run. Reviewer6claims verified/0unresolved. Scope does not auto-merge templates or import ignored secrets; source-only status differences may remain. Existing isolation/conflict/data preservation guidance covers this; local source-backup lesson appended.
