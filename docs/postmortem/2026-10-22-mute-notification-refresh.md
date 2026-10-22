# Mute notification refresh conflict

Track the refresh-config failure encountered while activating in-place mute notifications, then deploy only the requested helper and bindings.

## Symptom, impact and current status

`fish -c refresh-config` exited 1: chezmoi apply stopped at an unrelated, pre-existing dirty `scripts/tmux-scrollback-smoke` target. The noninteractive conflict prompt reached EOF. Private log: `/tmp/refresh-config.Azvy0uUD.log`. Broad refresh remains incomplete; the conflicting helper is preserved. The requested mute feature is active and verified through the live key binding.

## Evidence and lookup

Before desktop activation, searched postmortem memory for `X11 display pulse Operation not permitted` and read the existing mute-shortcut desktop-access report. It documents restricted desktop sockets and migration-preserved i3 configuration; approved host execution and a narrowly scoped live merge apply here.

Before remediation, searched `refresh-config conflict EOF changed` and read [local-refresh-snapshot-ownership](../../dot_agents/skills/postmortem-memory/references/paths-ownership.md#local-refresh-snapshot-ownership). Its exact-owned-target workaround applies because the log names `scripts/tmux-scrollback-smoke`, which was already dirty before this task. The log ends with `chezmoi: scripts/tmux-scrollback-smoke: EOF`. No overwrite or adoption of that unrelated target is authorized or needed for mute notifications.

## Cause and resolution

Cause confirmed: unforced broad apply correctly protected divergent helper content, then failed because a noninteractive session could not answer its conflict prompt. Preserve the unrelated helper and activate only the authorized audio helper and mute binding changes. This mitigates task-local activation without resolving the broad refresh conflict.

## Verification and remaining work

Scoped installation deployed `~/scripts/audio-mute` and changed only the live `Mod4+m` and `XF86AudioMute` bindings. `i3 -C` exited 0 and `i3-msg reload` returned success true.

`/tmp/verify-mute-notification.py` exited 0: two synthetic `Super_L+m` presses changed `Mute: no` to `yes`, then back to `no`. Displayed notification counts were equal and at least one; after expiry, exactly one new Audio history entry remained with body `Unmuted`. The original audio state was restored. These observations verify the scoped workaround and in-place notification replacement, not completion of broad refresh.

Do not retry broad refresh with force; the owner can reconcile the unrelated helper separately.

## Learning review

No new general learning: the existing refresh ownership/conflict guidance already requires preserving unrelated content and using exact owned deployment targets. Register this report's reviewed hash and alias in the tracked ledger; retain broad refresh as unresolved even if the scoped desktop checks pass.
