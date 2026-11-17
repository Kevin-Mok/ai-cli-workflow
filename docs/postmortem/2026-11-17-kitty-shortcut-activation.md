# Kitty shortcut activation diagnostics

The shortcut change removes i3 grabs so existing Kitty font mappings can run. This report tracks activation checks and their environment limits.

## Symptom and impact

Initial i3 IPC inspection failed with Operation not permitted inside the sandbox. Chezmoi diff reported the live i3 config as not managed. No configuration had changed.

## Evidence and lookup

Searched postmortem memory for `i3 socket Operation not permitted chezmoi not managed`. Existing `ext-sandbox-loopback` guidance applies to restricted local IPC, but not the separate chezmoi ownership result. Elevated i3 get_version succeeds (4.23). Local chezmoi migrationPreservedTargets explicitly excludes .config/i3/config; preserve that policy and patch only the requested live lines after refresh. The live file is newer than the template; compare relevant lines and retain unrelated contents.

## Status and next steps

Resolved. refresh-config completed successfully. Both exact live binding lines were removed with a backup at /tmp/kitty-shortcut-i3-before.conf; i3 validation exited 0 with existing mouse-wheel deprecation warnings, reload returned success, and raw loaded config confirms both grabs absent. An isolated Xvfb Kitty using the installed config received real xdotool Ctrl+Alt+Up/Down events: 19.0 → 20.0 → 19.0pt. The active desktop focus and terminal sizes were not manipulated for this test. No new generalized learning; existing scoped IPC workaround and explicit migration preservation explain both diagnostics.

The first live patch deliberately stopped on an exact-content mismatch: live config uses different surrounding text. A subsequent i3 validation succeeded with existing wheel-command deprecation warnings and reload succeeded. get_config output from i3-msg is raw config, not JSON; the diagnostic decoder was incorrect. Inspect exact live lines and parse raw config on retry. No evidence of data loss.

## Learning review

No new reusable finding: existing restricted-IPC guidance applies. The initial patch guard preserved the differently formatted live file; exact-line matching and raw get_config inspection resolved diagnostic assumptions. Source assertion observed RED before removal and GREEN after. Tracked ledger registers this reviewed report; targeted coverage check is required below.
