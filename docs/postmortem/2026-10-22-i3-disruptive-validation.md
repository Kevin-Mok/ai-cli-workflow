# Disruptive i3 validation during Kitty setup

Keep development checks off the active desktop. Inspect i3 read-only, use an
isolated display for layout tests, and batch any necessary activation reload.

## Symptom and impact

The user reported disorienting desktop refreshes and a disappearing middle bar
after monitor-font setup. Their screenshot records the affected desktop. Prior
validation reloaded i3 for activation and repeatedly moved disposable windows
and a temporary workspace on the real desktop. Cleanup restored snapshots, but
those actions can still interrupt ongoing work and overwrite newer focus choices.

## Evidence and diagnosis

- The font watcher's only i3 subprocess queries are `get_tree` and
  `--get-socketpath`; it subscribes to events. It issues no reload, restart,
  workspace-move or bar-visibility command.
- Its service restart is triggered by i3's `exec_always` entry. The direction is
  i3 reload -> watcher restart, not watcher loop -> i3 reload.
- Read-only live inspection found three dock-mode bars and one registered dock
  window on each output. DP-2's bottom dock is121px high, DVI-D-0's77px and
  HDMI-0's121px. This does not prove visible pixels or the screenshot's cause.
- All three i3bar processes started at13:49:42; i3 itself started onOctober20.
  This supports a recent bar restart, not continuous i3 process restarts.
- Separate concurrent bar work also involved i3 reloads. Exact ownership/cause
  of the screenshot's missing bar is not established; do not guess or reload
  again as a diagnostic shortcut.
- Lookup `i3 reload bar disappears focus` returned adjacent bar/renderer and
  desktop-access guidance, with no verified explanation for this screenshot.

## Resolution and limitations

No desktop configuration or live placement changed in this follow-up. Stop
disruptive active-desktop testing and use isolated validation. Record the user's
workflow correction in the canonical feedback log. Necessary future activation
reloads should be batched and explicitly described; ordinary watcher operation
needs none. The missing-bar cause remains unresolved without further evidence.
No claimed repair, automatic reload, force refresh or process restart occurred.
