# i3blocks 1.4 rejected a calendar format property

Record and fix a config-parser incompatibility encountered while keeping emoji visible in compact calendar output.

## Symptom and impact

The focused scheduler regression rejected `SHORTFMT=+📅 %H:%M` as malformed config input. The same property had been refreshed into live bar configs before that final test finished, so bar startup was temporarily affected. No user data or audio state changed.

## Evidence and status

`python3 -m unittest discover -s tests -p 'test_i3blocks*.py' -v`: 61 tests, one scheduler failure; the remaining tests passed. Redshift's 12 tests passed. Root cause: i3blocks 1.4 accepts defined config properties, not arbitrary script environment variables. Status: resolved and live activation verified. Removed the rejected property from live configs immediately and restarted i3 successfully (IPC success true); user screenshot confirms the bars recovered. Calendar-script protocol and scheduler regressions then passed: 62 i3blocks tests and 12 Redshift tests, exit 0. Final suite (62 i3blocks +13 Redshift tests) passed before final activation; refresh-config and i3 restart exited 0. Final bar-only screenshots show calendar/full and clock/compact output with colored playback buttons and no status-command error.

## Next steps

Resolved by removing unsupported config keys and using the existing calendar script: calendar icon in full text, clock icon in compact text, HOME-based palette path. The isolated protocol test and actual scheduler regression pass; live bars render successfully. No new dependency or schema migration.

## Lookup and resolution

Query: `i3blocks malformed config property`; no i3blocks-specific match. The general `ext-boundary-error-contracts` finding recommends matching installed contracts; the actual scheduler is the decisive evidence here. Use a script-level default LABEL for both text lines and the existing HOME-based palette pattern. Do not introduce arbitrary uppercase environment keys in i3blocks 1.4 configs. A separate user refinement chooses calendar/full and clock/compact icons.

## Follow-up

Run the actual scheduler and complete relevant suite before applying config changes. Keep immediate recovery separate from final activation. Reviewed learning: local-i3blocks-config-properties; final hash registered in the tracked ledger and targeted coverage check recorded in the task plan. Final evidence: /tmp/i3blocks-compact-final-dp2.png and /tmp/i3blocks-compact-final-secondary.png. Physical laptop rendering was not exercised.

## Verification reporting correction

A test-agent summary parser assumed unittest's summary was on stdout and failed after the expected RED suite finished (unittest reports on stderr). It changed no files and reran no application action. The agent read the original output and reported counts and mismatches directly; reuse the complete process output rather than parsing only stdout.

## Asymmetric padding follow-up

A read-only mapping report incorrectly inferred i3blocks config support from i3bar protocol docs. Actual scheduler rejected border before activation (62 other tests passed). Live config was untouched. Apply border fields in the existing JSON wrapper instead. Review also found i3bar min_width includes border and border sizes scale with DPI; account for both. A reviewer xrdb probe was sandbox-denied; no retry/state impact. Existing local-i3blocks-config-properties guidance applies: verify actual scheduler, not downstream protocol.

Verification follow-up: terminate the persistent scheduler probe after a frame rather than waiting for normal exit. A concurrently added workspace_button_width test briefly failed before its separate implementation existed; preserve that work and isolate padding checks. Review found a trailing separator still rendered before an empty calendar entry; budget it using original array positions.

Padding resolution verified: generic wrapper emitted numeric borders after initial unnamed frames, exited0 with empty stderr; 15 relevant layout checks passed. Full block run earlier passed63; a later concurrent workspace-only test was excluded while its implementation was pending. Refresh completed and i3 restart exited0. Live /tmp/i3blocks-asymmetric-secondary.png and /tmp/i3blocks-asymmetric-4k.png show correct bars and asymmetric gaps with unrelated workspace icons preserved.

Icon-gap verification follow-up: the busy-scheduler error assertion still expected raw `🌡️ ERR` after output gained the requested Pango spacer. The actual error remained present and all eight wheel events were delivered. Update the assertion to the exact JSON-encoded padded error, preserving both the error and new formatting contract. No production error handling changed. Prior boundary-contract guidance applies; no new reusable failure pattern.

Icon-gap follow-up resolved: all66 i3blocks checks passed exit0 with the exact padded-error assertion. Pango verified20px at96/135DPI; refresh/restart succeeded and both live bar screenshots show the requested spacing. No production error-handling defect; no additional reusable learning beyond the recorded protocol-boundary guidance.
