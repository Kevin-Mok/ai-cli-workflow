# Idle screensaver blocked by missing browser bridge — 2026-11-17

Automatic screensaver playback is suppressed despite a running five-minute idle service. Reconnect the Chrome video detector and verify the 4K playback gate before claiming activation works.

## Symptom and impact

Live status reports browser bridge unavailable and idle monitor running. systemctl confirms active/running. DP-2 is the middle 3840x2160 monitor. No native-client state file is present in the current runtime directory. Default Chrome preferences register the expected unpacked detector, and native host manifests/launcher exist. Other profiles lack registration. Actual profiles with open windows still need discovery. A diagnostic guessed install.py, which does not exist; installer actually lives in main.py. No user data or tracked source changed from that failed read.

## Lookup and status

Read tracked postmortem-memory before remedial actions. Query `screensaver browser bridge unavailable extension Chrome`; scheduled-visibility guidance concerns explicit playback and does not permit bypassing automatic video checks. Existing inventoried-path guidance covers the mistaken source read. Root cause is not yet confirmed: missing bridge connection, profile coverage and native-host startup remain candidates. Browser auto-connect is pending.

## Verification and follow-up

Existing five-minute rule needs no source modification yet. Reconnect actual desktop Chrome, verify fresh bridge snapshots and status, then exercise 4K versus side-display video and five uninterrupted idle minutes. Preserve fail-closed behavior and earlier staged work. No new generalized learning while diagnosis remains open; known bridge prerequisite and discovery guidance apply.

## Updated diagnosis and verification

Default, Profile 7 and Profile 15 are active; only Default registers the detector. Actual Chrome lacks an available automation connection: auto-connect returned BRIDGE_NOT_READY; computer-use inventory is empty. Opened existing detector settings in actual Chrome and requested user activation in each profile. No settings or video tabs were modified automatically. Settings tabs themselves cannot be inspected by the extension, so return every window to normal pages after setup. Headless automation browser processes do not contribute native Chrome windows.

Tests: bridge 15 passed; desktop matching 3 passed; browser JavaScript passed. CLI suite initially failed one of six due read-only runtime preview.lock; rerunning under isolated mode-0700 /tmp runtime passed all six. This is the known sandbox runtime issue, not evidence of a production regression. No new generalized finding: existing per-profile bridge prerequisite, protected-tab uncertainty and isolated-runtime guidance cover this case. Current state remains blocked on manual Chrome extension activation; physical five-minute acceptance remains unverified.

## Repeat report: inactivity exceeded threshold

Fresh live status still reports browser bridge unavailable while the idle service is active/running. Recent journal lines explicitly show idle 318, 349, 379 and 409 seconds, each suppressed for the same missing bridge reason. This reproduces the user complaint beyond the 300-second threshold and rules out failure to accumulate idle time for that observation. No production change is justified until detector activation is resolved. User was asked whether the extension is enabled in every open profile; actual Chrome remains inaccessible through available controls. Previous test results are earlier-run evidence, not rerun claims for this turn.

## User-approved replacement of automatic detection

The user chose local screen watching instead of requiring Chrome, then explicitly requested i3bar exclusion. Implemented the local motion policy in `plans/screensaver-screen-motion.md`: only non-bar movement on the4K monitor resets its quiet clock, and both motion/input must remain quiet300 seconds. This does not repair the optional Chrome extension; it removes that prerequisite from automatic activation. Scoped installation/restart verified active/running with14-second screen quiet progress and actual i3bar exclusion. Isolated checks passed65 media tests before final native-capture change, final affected15 tests afterward, plus10 timer tests and JS. Full physical idle acceptance remains unobserved.
