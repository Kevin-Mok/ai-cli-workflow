# Redshift 150 K live-probe interruption

This report records an interrupted display-session check while a concurrent session was changing the same bars. Inspect the live bar before replaying input, then verify both directions and restore the original target.

## Symptom and evidence
The150 K probe observed Windows+2=2300 and wheel-up=2450, but a subsequent wheel-down left2450 instead of2300. The captured DP-2 bar region was blank, and concurrent colorful-icon changes were present in the shared configuration, scripts and tests. Original target2300, pointer and focus were restored. No product fix is inferred from a missing-bar click.

## Lookup and status
Search `i3bar disappears during reload live probe` matched existing live-bar initialization/activation guidance. Applicability: a running visible bar is required for click acceptance; standalone controller checks cannot establish that. Status: investigate bar geometry/readiness before replay. Possible concurrent restart is a hypothesis, not a proven cause. The focused current-worktree tests passed12Redshift and13layout tests plus keyboard smoke.

## Next steps and learning
Capture current bar geometry, verify visible thermometer coordinates, rerun150 K checks after readiness and restore state. No new reusable learning yet; existing observed-runtime-readiness guidance covers this diagnostic.

Second probe: the bar was visibly present before launch, but wheel-up did not change2300 K. The original pointer/focus/target were restored again. A shared-pointer race remains possible during concurrent UI tests; the fixed-coordinate click path is not reliable evidence here. Next: send synthetic button events directly to the observed DP-2 bar window coordinates, avoiding the shared pointer, and compare saved state.

The direct-window probe's Python Xlib transport tried the absent filesystem `/tmp/.X11-unix/X1` socket and stopped before any target or UI mutation. Existing xdotool/libX11 queries still work via the abstract X11 socket. Lookup `Xlib abstract socket missing X11-unix` precedes switching only the disposable probe transport to that abstract socket. This is a diagnostic-environment issue, not a block failure.

The pointer-independent event also left2300 unchanged. Active i3bar config still names the4k_status wrapper, but process inspection found neither its live Python process nor its i3blocks child. The bar's cached text is insufficient evidence of status-process readiness. Inspect installed config/scheduler startup before retry; do not classify this as an adjustment-size failure. Original2300 restored.

## Root cause established
The private restarted-bar log reports `ERROR parse_bar:162: malformated line: SHORTFMT=+📅 %H:%M`, followed by child EOF. The user screenshot independently shows `status_command process exited unexpectedly (exit 0)`. A concurrent calendar change added uppercase SHORTFMT as an i3blocks1.4 property; this version rejects it. The wrapper exhausted the failed scheduler stream and returned0, leaving the visible error. The150 K mapping itself was not responsible. Move SHORTFMT into the calendar command's environment rather than a config property; retain the new calendar appearance. Reproduce via the installed scheduler test before fixing.

The scheduler reproducer failed for the exact malformed SHORTFMT line. Before this session edited that stanza, concurrent work removed the unsupported property from shared source. Preserve that correction and do not restore unrelated calendar changes. Apply the now-valid source and confirm scheduler startup; no additional configuration patch is needed from this session. Lookup returned no directly matching SHORTFMT guidance; the installed scheduler error is the primary evidence.

A full refresh attempt then exited1 at chezmoi apply (`/tmp/refresh-config.uTysWM4S.log`). No force apply or overwrite is authorized by this failure. Inspect the named target and preserve newer local/shared changes; use exact-target deployment for this session's block if unrelated live drift cannot be reconciled safely.

The valid-installed-config restart was followed by another failed coordinate-click probe;2300 remained2300. Pointer and target were restored, but original focus differed afterward, so do not claim focus restoration in this run. Inspect its private `/tmp/redshift-bar-150-final.log` before any further live retry.

## Resolution and verification
The installed scheduler config no longer contains the unsupported property. After restarting only DP-2, process inspection confirmed both4k_status and its i3blocks child running, the private log was empty and a screenshot showed the normal bar instead of the reported error. A pointer-independent probe against that live bar passed Windows+2=2300 (after first setting3000), up=2450, down=2300, eight25-ms up events=3500. It restored original2300 without moving the pointer. Exit0. Earlier coordinate probes remain inconclusive because of missing status processes and shared-pointer interaction; do not reuse them as successful checks.

Full refresh initially succeeded for150 K, then a later broad refresh stopped on unrelated calendar-label source/live drift. Source was newer than live; preserved both and used the valid installed configuration for recovery. That unrelated difference remains uncommitted. No additional product patch beyond150 K mapping was needed from this session. Status: recovered and150 K runtime verified; physical wheel testing remains manual.

Learning decision: no new reusable rule beyond existing version-specific configuration validation, live-process readiness and scoped drift handling. The installed-scheduler RED and observed log establish this report's specific unsupported-property cause; the concurrent source correction is preserved rather than attributed to this session.
