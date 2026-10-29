# Redshift live activation checks

This report tracks activation checks after adding the Redshift block: isolate Fish startup and restart the affected bar when an unchanged status command retains old configuration.

## Symptom, impact and evidence
A read-only `fish -c 'functions refresh-config'` emitted read-only fnm, universal-variable and alias-write diagnostics although its final command exited 0. No intentional live writes succeeded. A subsequent isolated, approved `fish --no-config` refresh completed successfully.
The first successful i3 reload retained the prior running status command and scheduler: a DP-2 screenshot still showed volume/song/calendar without Redshift even though installed files matched the new source. Activation was therefore not yet established.

## Lookup and applicability
The existing 2026-10-23 agent-policy-fish-inspection report describes the same startup side effects; use no-config and explicit function paths. Search `running i3bar unchanged status command reload` matched `local-i3bar-layout-startup-recovery`; the 2026-10-22 4K inspection report confirms unchanged status commands survive reload. Both apply; no new product defect is inferred.

## Current status and next steps
Refresh passed. i3 validation exited 0 with pre-existing wheel_up_cmd/wheel_down_cmd deprecation warnings. Restart only the affected bar, then verify rendering, wheel events and Windows+2, restoring the original temperature and pointer.

## Learning
Pending final evidence; existing environment-isolation and unchanged-status-command guidance cover the observations.

## Rapid-wheel failure
Actual DP-2 Windows+2 showed 2300 K, wheel-up showed 2550 K, and wheel-down returned 2300 K. Eight wheel-up events at 25 ms spacing reached only 2800 K instead of 4300 K. Original 2850 K, pointer and focus were restored. This is a new product bug: i3blocks 1.4 drops clicks while the block command runs; controller locks cannot recover events never delivered. Use a serial click reader in the existing wrapper to handle Redshift wheels before i3blocks scheduling; preserve the rest of the protocol. Add an executable rapid-click regression with the real scheduler before implementation.

## Resolution and final verification
The wrapper now reads click input serially, intercepts only Redshift wheel events before the busy scheduler, invokes the block/shared controller for each and forwards all other input unchanged. Queued output (including errors) overlays the next frame; signal 2 requests an immediate refresh, with one-second polling retained. The defining rapid-click regression failed before implementation and passed afterward.
After refreshing and restarting only DP-2, the actual bar showed the thermometer. Windows+2=2300, up=2550, down=2300, eight 25-ms up ticks=4300, other three clicks=4300, reset=6500 all passed. Original target2850, pointer and focus were restored. Screenshot `/tmp/redshift-live-up.png` shows2550. Focused suites passed24tests before final fixture strengthening; final evidence is in the plan. Status: verified fix (runtime); physical human-wheel/keyboard testing and crowded live workspaces remain manual, with synthetic actual-X11 events and isolated layout coverage established.

New learning: controller concurrency tests cannot detect scheduler-dropped input. Test click delivery through the installed scheduler, and intercept queued events before its busy-block boundary when necessary. Existing startup/isolation guidance still covers the other observations; no broad configuration or workspace changes were needed.
