# Discord speech refresh permission conflict

Refresh stopped safely on a known launcher mode conflict. Preserve identical launcher contents while reconciling only its reviewed permission mode, then retry unforced refresh.

## Symptom, impact and evidence

Guarded exact-target chezmoi apply prompted for media-screensaver overwrite and hit EOF (exit 1); the subsequent required refresh also stopped on that target. Preflight proved live/rendered content identical, live0755 versus target0775. No force or adoption was used. Discord deployment remains pending final activation.

## Lookup and cause

Before remediation read plans/refresh-config-screensaver-conflict.md and searched screensaver launcher mode drift. Reviewed local-screensaver-launcher-mode-drift, verified_workaround: exact same explicit-installer0755 versus chezmoi umask002 target0775 conflict. Exact-target apply itself still prompts when last-write state differs; matching bytes alone do not bypass mode conflicts.

## Resolution plan and rollback

Guard content equality again, set only the exact target mode to the rendered0775, then verify/reconcile state and run unforced refresh. Preserve every unrelated byte and listener. Rollback to0755 restores the conflict. No installer policy change. Verification pending.

## Observed resolution

Guarded live/render equality again; set only live launcher mode0775, verify exited0 with bytes preserved. Unforced refresh then completed apply, sync-shortcuts and source-shortcuts, exit0 (private log /tmp/refresh-config.GZO6qqz3.log). No unrelated source file content was changed by reconciliation. Local Ryan --check exited0; activation restarted only Dunst; Discord enable succeeded while global speech and selected sire.mp3 remained enabled. No new reusable finding beyond the existing mode-drift workaround; preserve its installer recurrence limitation.
