# Resolve identical refresh-config source duplicates

Make refresh-config recover automatically when ordinary and private source files are identical, preserve the private source and a rollback copy, then complete the user's refresh.

## Scope and outcome

User authorized fixing the current identical mimeapps duplicate and modifying the refresh helper. Preserve all unrelated dirty work and local configuration. No commit/push. Source/live refresh helper is byte-compared before deployment. Keep progress, emoji/CLI_PLAIN behavior and drift-import/retry behavior.

## Decisions and safety

Only the ordinary/private MIME source pair with byte-identical content may be consolidated. This narrowly fixes the actual reported conflict; unrelated duplicate types retain normal chezmoi errors. Preserve private_ source so destination permissions remain private; move ordinary duplicate into a private backup outside the chezmoi source before retrying. Refuse different contents, symlinks, templates or other attribute conflicts rather than guessing. Never import private/machine-local data into portable source as collateral. Use chezmoi source-path and the known MIME sibling names rather than scanning the whole repository or parsing diagnostic paths.

## Ordered checklist

- [x] Capture state and reproduce actual status failure.
- [x] Define failing automated duplicate-recovery and conflict-preservation tests.
- [x] Implement minimum safe recovery in refresh-config and verify GREEN/regressions.
- [x] Update README/smoke checks and incident learning.
- [x] Deploy reviewed helper and run actual refresh; preserve/resolve routine drift safely.
- [x] Verify success or exact remaining blocker and reconcile evidence.

## Evidence and rollback

Actual RED: chezmoi status --exclude scripts,externals,remove --no-tty exits1: .config/mimeapps.list inconsistent state. Two sources are identical1615bytes; ordinary dot_config/mimeapps.list untracked, private source tracked. Existing incident docs/postmortem/2026-11-16-i3-wallpaper-activation.md contains diagnosis and postmortem-memory lookup; unrelated lookup matches do not supply a cause-specific remedy. Initial status /tmp/refresh-duplicate-evidence/initial-status.txt. Backups outside source before removing duplicate. Preserve existing home i3/private settings by reviewing any drift import; only explicitly needed source changes belong to this task.

## Verification and review

Automated fixture tests must show identical duplicates backed up/recovered, differing files unchanged/failure, ambiguous/symlink cases preserved, no unnecessary normal-path changes and current existing refresh regressions. Actual refresh output must end REFRESH COMPLETE with exit0 before claiming success. Validate live i3 after any config application; avoid reload unless needed. Rollback from printed backup path. Final report links this plan, documents checks and limitations. Suggested commit: fix(fish): recover identical private source duplicates. Cursor handoff: read this plan, preserve unrelated dirty state, use the focused refresh regression tests and actual refresh result; no commit or push authorized.

Test RED observed before implementation: first identical-duplicate recovery assertion exits1 because status rejects conflicting MIME owners. Source implementation is narrowly scoped to the actual MIME pair, with symlink/nonregular/differing refusal and private XDG backup. Existing MIME handler regression now reads tracked private source, not the untracked duplicate. README/smoke describe backup path and stop behavior. Fresh lookup returned unrelated CLI/hidden-prompt findings; recorded earlier diagnosis and actual byte-equality evidence govern this fix.

## Fresh verification and activation

Initial GREEN passed identical recovery, differing/symlink refusal, normal mode, CLI_PLAIN, progress, apply retry and real chezmoi exclusion checks. Reviewer exposed malformed successful source-path output and custom state storage inside source: defining additional RED preceded boundary fixes. Final source requires one absolute existing directory; canonical backup containment rejects source descendants, including symlink aliases. Final GREEN: `bash tests/test_refresh_config_function.sh`; `bash tests/test_mimeapps_fnlb_handler.sh`; `fish --no-config -n dot_config/fish/functions/refresh-config.fish` all exit0 (/tmp/refresh-duplicate-evidence/green-final.log). No new dependencies.

Actual process19272 exit0, /tmp/refresh-duplicate-evidence/live-refresh.log ends REFRESH COMPLETE. Private underlying log /tmp/refresh-config.AvmYrbVy.log. Duplicate moved automatically to /home/kevin/.local/state/refresh-config/backups/mimeapps.McTFS2cw/mimeapps.list. Byte-equality and backup-directory0700 verified; ordinary source absent, tracked private source retained. `chezmoi source-path ~/.config/mimeapps.list` returns private_mimeapps.list; installed permissions600. Deployed helper matches source; baseline hashes show no tracked source file changed during refresh, preserving all pre-existing dirty work. Live i3 validates, reloaded once and rawIPC confirms all4whole-collection wallpaper bindings remain correct. Previous full-refresh blocker is resolved.

Rollback evidence: /tmp/refresh-duplicate-evidence/rollback stores previous helper and duplicate content; permanent duplicate backup is printed above. Restore content into canonical private source rather than reintroducing a duplicate target. No commit/push performed. Scope intentionally handles only this MIME pair; differing data, symlinks and other duplicate types still require review. Automated fixture checks cover cases without manufacturing live conflicts. Final diff check and postmortem ledger targeted check required before handoff.

Exact manual workflow checks: refresh-config emits REFRESH COMPLETE; chezmoi source-path ~/.config/mimeapps.list resolves to private canonical; stat -c '%a %n' ~/.config/mimeapps.list shows600. README and docs/smoke-tests.md document identical-backup/differing-stop behavior. No physical desktop shortcut change needed beyond existing verified i3 reload.

Final evidence review:6claims verified,0incorrect/unresolved; fresh independent focused suite/MIME/syntax checks pass, source baseline2218paths unchanged, deployed bytes/backups/permissions verified. Targeted postmortem-memory check has zero errors/new/changed/unregistered aliases and git diff --check passes. Atomic plan complete; no remaining blocker in scope.
