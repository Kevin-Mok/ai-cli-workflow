# Workspace spacing desktop access

This report records desktop inspection constraints encountered while adjusting workspace spacing.

## Symptom and impact
Sandboxed i3-msg failed with Operation not permitted on the desktop socket. A login fish inspection also attempted startup writes outside the workspace and printed read-only errors. One chezmoi diff without an explicit source reported the live config unmanaged. No workspace spacing changes had been applied.

## Evidence and lookup
Searched postmortem memory for i3 socket Operation not permitted; ext-sandbox-loopback describes the approved host-execution route, applicable as a permission boundary workaround, not a repaired sandbox. Host i3-msg get_version succeeds (i3 4.23). Fish confirms chezmoi source /home/kevin/linux-config. Avoid login fish for probes and use explicit chezmoi source.

## Status and next steps
Use approved scoped host execution and fish --no-config for activation. Preserve newer live edits by comparing explicit rendered config before refresh. No independent engineering learning beyond existing sandbox execution guidance.

## Activation evidence
Explicit source rendering differs substantially from local private config; i3/i3blocks are intentionally ignored by chezmoi. Applied only matching workspace and measurement edits directly, preserving local content. refresh-config succeeded. i3 config validation exited 0 with existing wheel command deprecation warnings. Live label checks pass; all three bars hide numeric prefixes and disable minimum widths. An order-sensitive before/after list assertion failed after rename; current focus remains workspace 6, and no move/focus commands were issued. Status filters survived the first reload; adding shell exec to their commands forces updated code to load on the final reload. A missing explicit sync-shortcuts source was harmless because fish autoload resolved it and refresh completed.

## Resolution and final verification
All three live bar configs report the intended prefix/minimum-width settings. Updated status processes restarted at 18:55:51, source/live smoke checks pass, 18 regressions pass, and Pango measurements confirm requested spacing at current DPI. Scoped deployment preserves local private content. git diff --check reports an unrelated pre-existing blank line at api-contracts-fixtures.md:726; left untouched. Sandbox remains restricted; no host repair is claimed.
