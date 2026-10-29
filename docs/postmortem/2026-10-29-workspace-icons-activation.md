# Workspace icon activation boundaries

Track deployment of colorful workspace labels while preserving local i3 configuration and shortcuts.

## Symptom and impact

Initial read-only `i3-msg -t get_workspaces` could not connect: Operation not permitted. `chezmoi cat ~/.config/i3/config` reported not managed; piping its empty output into diff produced a misleading whole-file deletion diff. No file changed. Live activation needs approved host IPC and scoped editing because the installed i3 config is unmanaged and contains private differences.

## Status and next steps

Inspect live IPC through approved execution; compare only workspace definitions, retain all other local bytes, validate before one reload, and rename existing workspaces without moving windows or focus. Required refresh-config will still be attempted. Never overwrite the installed config with the public template.

## Lookup

Search postmortem memory for i3 IPC sandbox and unmanaged config before remedies; record applicability and completed evidence below.

Lookup found `local-i3-probe-ipc-unicode`: literal UTF-8 and isolated focus-safe diagnostics apply. Approved read-only host IPC succeeded and captured original workspace/tree identities. A later ordinary fish startup inspection also attempted normal home/runtime writes blocked by the sandbox; use no-config fish with explicitly sourced helpers for refresh under approved host permissions. No product defect or repair to desktop access is claimed.

Focused regression found a pre-existing stale assertion in `tests/test_desktop_display_layout.sh:39`: expects `label=` while the baseline-dirty i3blocks config already uses `label=🎵`. Workspace source was initially clean, i3blocks was dirty before this task. Preserve those unrelated changes and report this check as failing rather than rewriting its expected output. Other workspace/Redshift/4K/voice checks passed; isolated Xvfb exercised 27 real select/move combinations successfully.

Further boundary evidence: default-sandbox `i3 -C` failed creating `/run/user/1000/i3/errorlog.2` and exited 139; validate under approved host permissions. A no-config fish refresh omitted `cli-message` from PATH and printed command-not-found, though underlying apply proceeded. Inspect its completion before retrying and provide the existing helper PATH; never alter the product helper to accommodate this diagnostic shell. Legacy wheel directive warnings predate this task.

Refresh then completed cleanly with the normal function directory loaded, exit 0. Approved syntax validation passed (legacy wheel warnings only). Activation updated only the 13 installed label lines, reloaded once, and renamed existing workspaces. Live label/shortcut checker passed. The immediate identity/output/focus assertion failed after reload; investigate current state against the captured baseline before declaring preservation. Do not change focus or move windows as a remedy without evidence.

A window-number comparison diagnostic omitted its recursive helper return and raised TypeError; correct the diagnostic only. Live desktop state changed during this task (workspace IDs and focus changed); do not claim the original focus/IDs were preserved. Running icon and Redshift shortcut checkers pass.

Compact activation used rename-before-reload and its workspace-ID/output/visibility/focus assertion passed. Its strict full-window-set comparison failed, preventing the planned original-output restoration. Inspect added/removed window classes and original XID-to-workspace mappings before interpreting live application churn as a moved-window regression. Live compact and overlapping Redshift shortcut checkers both passed.

## Resolution and final verification

Normal helper-path refresh succeeded. Guarded live updates retained all unrelated installed bytes. Compact activation preserved workspace IDs, outputs, visibility and focus. The overstrict window-set assertion compared restarted i3bar dock windows as if they were application windows; follow-up XID comparison retained all 32 original non-bar windows on the same numbered workspaces. Three original i3bar windows were replaced, and a new mpv window appeared. Restore-only-hidden-output operation returned workspaces 2/4/11 to their original monitors while preserving then-visible workspaces and focus. No original application moved to another numbered workspace.

Final user refinement uses native minimum button widths: 144 logical pixels on 50pt bars and 95 on the 30pt bar. Screenshot after startup shows a 202px one-digit button with a 173px label: about 15px per side. Full-cell Unicode spaces would each add 56px at current font/DPI, so labels remain compact. Existing 4K measurement now accounts for native minimum width.

Fresh final source tests: 16 layout, one scheduler, workspace checker, Redshift checker and voice binding all exit 0. Installed and running workspace/Redshift checks exit 0; installed i3 syntax exit 0 with pre-existing wheel deprecation diagnostics. Deployed 4K helper equals source, cmp exit 0. Final padding-only activation preserved every workspace ID, output, visible state and focus. The unrelated stale desktop-layout music-label assertion remains failing; no whole-repository suite or physical keyboard firmware acceptance claimed. No commit/push requested.

## Learning

Use rename-before-reload when changing workspace labels: loaded old assignment names cannot match the new labels. Preserve exact UTF-8 names. Compare application window assignments separately from i3bar dock windows, which restart on reload. Verify live minimum widths and actual rendered dimensions; retain focused regression checks. The sandbox itself remains restricted; approved execution was a scoped workaround.
