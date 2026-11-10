# Refresh helper lookup during cure shortcut setup

This report records a read-only lookup failure and the verified helper location used to continue setup.

- Symptom/evidence: `sed` could not read `scripts/executable_refresh-config`: No such file or directory.
- Impact: one source-inspection command failed; no configuration was changed by that command.
- Lookup: searched postmortem memory for "missing script path". Installed-wrapper and README fallback findings did not apply: this was an assumed source path, not a missing dependency.
- Root cause: refresh-config is a fish autoload function, not a scripts executable.
- Resolution/verification: read `dot_config/fish/functions/refresh-config.fish` successfully; use `fish -ic refresh-config` for activation.
- Status: resolved lookup; configuration activation is verified separately in docs/task-status.md.
- Learning: no new reusable finding; existing search-before-assuming-path guidance is sufficient. No helper or behavior change required.
- Follow-up: none for this lookup. Playback remains outside verification scope.

## Configuration refresh permission failure

- Symptom: fish startup and refresh returned exit 1 with read-only filesystem errors for fnm runtime paths, universal variables and /home/kevin/aliases/.key_aliases.
- Impact: activation could not complete within the workspace sandbox.
- Lookup: searched "read-only file system sandbox refresh-config"; execution-environment guidance applies to restricted runtime/home writes, not a shortcut syntax defect.
- Status: awaiting authorized refresh with normal home/runtime write access; no playback attempted.
- Next: rerun refresh with escalated permissions and check exact abbreviation expansion.

## Pre-existing duplicate chezmoi target

- Escalated refresh reached chezmoi, which rejected inconsistent state: dot_config/mimeapps.list and dot_config/private_mimeapps.list both map to .config/mimeapps.list.
- The ordinary mimeapps source was already untracked before this session; preserve it rather than delete or commit it.
- Lookup: mimeapps inconsistent state; inspect existing local-mime-drift-reconcile guidance.
- Next: temporarily park the untracked duplicate outside chezmoi source during refresh and restore it immediately afterward; retain the tracked private target. This does not permanently repair unrelated source drift.

- Parking attempt using rename failed with EXDEV because /tmp and the repository are different filesystems; source remained intact. Use shutil.move with copy/unlink support instead. This is a file-transport limitation, not data loss.

## Activation check mismatch

- Refresh returned REFRESH COMPLETE, but the required checker failed: cure stayed literal. Generated ~/.config/fish/key_abbr.fish and ~/aliases/.key_aliases contain no cure entry while repository aliases/key_aliases.tmpl does.
- This is an activation failure, so delivery remains blocked until the source used by the generator is identified and corrected for this requested mapping.
- An additional read assumed sync-shortcuts was a fish file; inventory is required because that path does not exist.

- Root cause confirmed: aliases/key_aliases is a migrationPreservedTargets entry, so full refresh intentionally leaves the live mapping file untouched. Remedy is to merge only the authorized cure row into that preserved live file, retaining every existing row, then refresh and verify Space expansion.

## Final verification

- Final refresh exited 0 with REFRESH COMPLETE; untracked identical MIME source restored.
- Required installed checker exited 0: cure + Space expanded to the exact mpv command and was never executed.
- Known preservation behavior matches tasks/lessons.md migration-preserved-target guidance; no new general finding is needed. Lookup, EXDEV transport and sandbox limitations remain recorded here.
- Remaining: duplicate MIME source is preserved, so an ordinary future broad refresh still needs reconciliation by its owner. Playback and media availability untested.
