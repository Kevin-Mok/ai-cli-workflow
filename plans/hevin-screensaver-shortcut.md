# Hevin screensaver shortcut

Add Super+Shift+S to start the existing Hevin preview, apply it to the current desktop, and retain a repeatable manual check.

## Outcome, context and boundaries

Use `~/scripts/media-screensaver preview`, which defaults to `/mnt/linux-files-3/hevin`. Scope: the i3 template, README, media usage guide, smoke checklist and this record. No launcher, idle service, media or monitor-layout changes. Preserve all initial dirty postmortem-memory files and unrelated untracked reports/plans/prompts; initial `git status --short` was captured before edits. No commit requested.

## Decisions and implementation

- [x] Map existing launcher and bindings with a read-only search agent; Super+Shift+S is unused.
- [x] Observe defining assertion RED for absent release binding; add one binding, then observe GREEN.
- [x] Document the shortcut in README, usage guide and grouped smoke checks.
- [x] Run required refresh-config; clean no-config fish with approved home access exited 0.
- [x] Confirm live i3 config is unmanaged by chezmoi; insert only the binding, validate and reload.
- [x] Verify exactly one matching binding through raw live IPC config; preserve unrelated work.

## Risks, rollback and review

Release binding avoids launching while the S key is held. Subsequent keyboard/mouse input dismisses preview as usual. Super+S and Alt+S bindings remain present. Existing wheel_up_cmd/wheel_down_cmd deprecation warnings do not prevent validation or reload. Live i3 config differs from the sanitized tracked template and is unmanaged; avoid wholesale replacement. Roll back by removing this binding from source/live config and reloading i3; a private pre-insertion copy is `/tmp/hevin-i3-rollback.config`.

## Verification evidence

`python3 /tmp/check-hevin-binding.py`: RED assertion before change, GREEN afterward. `i3 -C -c ~/.config/i3/config`: exit 0 with existing wheel deprecations. `i3-msg reload`: success true. `i3-msg -r -t get_config` plus exact binding count: exit 0, one live Super+Shift+S preview binding. `refresh-config`: clean approved invocation exited 0, REFRESH COMPLETE. Runtime inspection errors and resolution are recorded in `docs/postmortem/2026-10-20-hevin-shortcut-refresh.md`.

Manual: press Super+Shift+S, release all keys, wait without moving mouse; preview should appear. Move mouse to dismiss. Check Super+S opens Spotify and Alt+S selects stacking. Physical keys and visual playback were not exercised in this task; existing renderer is unchanged. No broad renderer suite needed for a binding-only change.

## Atomic handoff

Keep source binding, README/usage/smoke edits, plan and incident review together. Suggested subject: `feat(i3): add Hevin screensaver shortcut`. No commit or push performed.

Cursor prompt: Read this plan and docs/media-screensaver.md. Verify Super+Shift+S starts the existing preview on release and subsequent physical input dismisses it. Preserve all unrelated settings and dirty work. Do not rewrite the launcher. Record observed manual evidence in this plan.

## Later delivery

The later commit-plan-push authorizes shipping this shortcut with the orientation implementation and matching documentation in the screensaver group. See dirty-worktree-delivery.md for commit/privacy verification and push status. Historical activation evidence and physical-key limitation above remain unchanged.
