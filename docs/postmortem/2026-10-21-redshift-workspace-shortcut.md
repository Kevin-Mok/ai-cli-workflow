# Redshift preset captured workspace shortcut

Restore workspace 11 navigation without removing the combined-modifier Redshift preset.

## Symptom and evidence

The user reported Windows+1 controls Redshift instead of workspace 11. Both tracked and installed i3 bind Mod4+1 to set 1800 K; Alt+Super+1 duplicates that preset. The existing checker explicitly enforced that previous behavior. Memory search for redshift/Super/workspace returned IPC diagnostic guidance, not a shortcut remedy.

## Impact and status

Workspace navigation requires Super+F11 until the single binding is restored. Resolved: source and live binding now select workspace 11; Alt+Super+1 remains 1800 K.

## Diagnostic limitations

A broad initial search included a nonexistent sxhkd glob and returned exit 2; subsequent searches used known paths. An attempted helper read used a nonexistent scripts path; the actual helper is a fish function. Inspecting the function through interactive fish triggered startup writes denied by the read-only home sandbox; use no-config fish with explicit function sources for scoped commands. These diagnostic failures changed no requested configuration.

## Next steps

Update the existing checker first, observe RED, change only Super+1, preserve all other live bytes, refresh and reload i3, and verify tracked/installed/running configuration.

## Source verification

Updated checker first failed as expected on the old Super+1 preset, then passed after the one-line mapping change. Sandboxed i3 syntax validation exited 139 after failing to create its error log under /run/user/1000; no live change occurred. Retry only with scoped home/runtime access.

## Refresh checkpoint

Required refresh-config ran with scoped access but stopped on an existing changed scripts/media-screensaver target (noninteractive EOF). It did not complete. An attempted unnecessary sync-shortcuts function source was missing; sync-shortcuts is an executable. Preserve this unrelated local target instead of forcing global apply. Proceed with guarded i3-only activation.

## Resolution and verification

The previous preset-only design occupied Super+1. Removed that preset binding in source and assigned Super+1 to workspace 11. Kept Alt+Super+1 and every other preset/reset/workspace binding. Installed change was an exact one-line replacement with a byte-preserving backup and concurrency guard; i3 syntax validation exited 0 with existing wheel-command deprecations. Reload returned success true; installed and running checker both exited 0. Source checker passed and 13 focused tests passed. Physical keypresses remain untested; full refresh remains blocked by the unrelated local screensaver conflict.

## Learning decision

No new general troubleshooting rule: this is a user-directed reversal of a previously intentional binding. Existing IPC guidance and source/installed/live checks cover verification. Sandbox and managed-file conflicts are existing environment limitations; do not force unrelated overwrites. Reviewed current report in the tracked ledger with an explicit no-new-learning decision.

## Delivery privacy check

The staged privacy gate blocked the machine-specific home path in this report ledger alias. The committed ledger uses the established public-safe example path; the machine-specific alias stays only in local dirty state. Restage the reviewed entry and rerun the unchanged gate before committing.
