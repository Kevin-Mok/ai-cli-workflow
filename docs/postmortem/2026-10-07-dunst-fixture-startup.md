# Dunst fixture readiness activated a competing daemon

This report tracks an isolated integration fixture that started a second notification daemon during readiness checking. Fix the probe before trusting its notification-rule results.

## Symptom and impact

The defining Dunst RED check reported no sound, but stderr also showed DBus activating `org.freedesktop.Notifications` and a competing daemon losing the name. Its `dunstctl is-paused` readiness probe can activate the default daemon before the explicitly configured fixture daemon acquires the bus name. No production daemon or audio was touched: the test used a private DBus session, Xvfb and fake mpv.

## Evidence and lookup

`xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py` exited 1; DBus logged activation and name-acquisition conflict. Search `dbus Name acquired dunst fixture startup readiness` found generic unrelated readiness/deployment findings, which do not establish a remedy here. Systematic-debugging inspection identifies the activating destination as the boundary at fault. The initial failure is not credited as defining RED until fixture ownership is proved.

## Status and next steps

Investigation: replace readiness polling with DBus `NameHasOwner` addressed to the bus itself, then verify the fixture daemon is still running before any `dunstctl` call. Rerun without production rule to observe valid RED; add the rule and confirm GREEN. Register a reusable finding after verification.

## Subsequent evidence

The nonactivating NameHasOwner probe obtained valid RED (missing production rule, no DBus race). With the rule installed, completion and approval each played once, and identical duplicate stacking was silent. A following history-pop played a third sound, contradicting the inspection's blanket claim of no replay. Search `dunst history script replay always_run_script` found unrelated results; inspect duplicate replacement of script_run before changing code or expectations. This is an isolated fixture observation; no production activation yet.

## Resolution and verification

NameHasOwner checks addressed to org.freedesktop.DBus do not activate a notification service. The fixture verifies its explicitly started daemon remains alive before any notification command. Corrected defining RED had no DBus activation/name-conflict output; final isolated integration exited 0 and cleaned its own daemon/display/bus.

The history expectation was also corrected after source inspection confirmed Dunst 1.9.2 transfers duplicate count/icon but not script_run when stacking duplicates. Normal already-sounded history remains silent; a silently stacked replacement can sound once on its first later display. Preserve that native behavior rather than deduplicate by text or persist arbitrary notification IDs.

Final command: `xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py`: exit 0, one integration test; fresh completion/approval sound once, unrelated apps and immediate duplicates remain silent, queued audio waits for display, empty-format suppression remains silent, normal and stacked history cases match the installed contract. The player is mocked; live MP3 acceptance is outside this evidence.

## Learning and follow-up

Record local-dbus-readiness-no-activation and local-dunst-stacked-script-state in tracked memory. Use nonactivating ownership checks for private service fixtures and verify mutable-object replacement state before making blanket replay guarantees. No production Dunst patch or persistent dedup cache is needed. Retain the explicit native-history limitation in docs and tests.
