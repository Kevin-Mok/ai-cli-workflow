# Screensaver closed immediately after 10 AM wake

Trace the morning timer through monitor wake and playback, then verify an explicit scheduled launch stays visible while preserving normal idle safety checks.

## Symptom, impact and evidence

User found black screens around 11 AM after expecting the 10 AM screensaver. At 11:14 EDT the timer listed its last run at 10:00. All service commands exited 0, including `xset dpms force on`. Playback discovered 5803 items and closed at 10:00:02. Idle daemon logs repeatedly report unavailable browser bridge. Live X11 settings have screen blanking and DPMS timeouts of 600 seconds.

## Status and lookup

Investigating immediate scheduled-preview dismissal and display inactivity while playback is running. No display power action performed. Search `screensaver black display timer DPMS` returned mixed-card rendering and launcher-mode findings; neither directly establishes a remedy for immediate gate-driven close. Timer timing and initial monitor wake succeeded; a passing unit test did not establish sustained morning visibility.

## Next steps

Reproduce explicit scheduled launch suppressing itself because browser coverage is absent. Inspect lifecycle power inhibition, add regression coverage, implement a minimal correction and verify on the live desktop. Preserve all existing dirty work.

## Investigation and verification progress

Root cause: scheduled routed through automatic renderer policy, which dismisses whenever bridge coverage is absent. Normal X11 blanking/DPMS remains free to switch off displays after ten minutes. The correction uses manual preview policy for the explicit schedule and scoped XScreenSaverSuspend inhibition; idle activation stays conservative and lockers retain explicit control.

Eight timer tests and 58 screensaver tests passed. The latter ran under isolated Xvfb with approved desktop access; a first sandboxed run could not access X11/runtime paths. An API exploration found python-xlib has no screensaver module here, so the implementation uses installed libXss via ctypes, with extension/version validation. Primary libXss manual confirms per-connection automatic blanking/DPMS suspension and disconnect cleanup; it does not block forced locking.

Refresh passed and deployed source bytes match. First real 15-second playback check was dismissed at 0.02 seconds by physical input and its duration assertion failed; display settings remained unchanged. This is an inconclusive live-duration check, not another browser-gate failure. Retry only after a quiet input interval, distinguish duration dismissal from input, and retain this evidence.

## Resolution and remaining limits

Second desktop check waited for two quiet seconds, entered real playback with three items and no decoder errors, then input dismissed it at 1.44 seconds. Both desktop checks left `xset q` unchanged. No further retries or artificial input suppression: long live duration remains unobserved while the user is active. The isolated Xvfb test does verify inhibition beyond a one-second timeout, automatic blanking after exception cleanup and unchanged configured values. Eight timer and 58 broader tests passed; refresh and deployed-byte comparisons passed. Status: correction deployed and verified in isolated X11; next overnight/hardware acceptance remains outstanding.

Ancillary tooling failures: python-xlib screensaver-module import was unavailable; selected the documented native libXss API instead. The first sandboxed Xvfb run lacked runtime/X11 access, and the approved isolated rerun passed. One no-op report patch used incomplete paragraph context and failed; appended final evidence after reading the actual report. These do not change the playback diagnosis.

Primary evidence: [libXss manual](https://manpages.debian.org/trixie/libxss-dev/Xss.3.en.html), [X.Org screensaver protocol](https://xorg.freedesktop.org/archive/X11R7.6/doc/scrnsaverproto/saver.html). XScreenSaverSuspend is connection scoped, suspends automatic screensaver and DPMS timers, and releases on disconnect. It does not cancel forced blanking or lockers.

Learning: timer exit status 0 plus a one-time DPMS wake does not establish sustained playback. Match the explicit schedule's gate policy to user intent, and use lifetime-scoped inhibition with cleanup verification. Registered as local-scheduled-screensaver-visibility; targeted ledger check is recorded in the task plan.

Final overnight edge reproduced: starting the inhibitor on an already blanked X11 screensaver left ScreenSaverOn active (isolated regression RED). Added XForceScreenSaver(ScreenSaverReset) after acquiring inhibition, before rendering. This clears the server blank without manufacturing keyboard/mouse input or dismissing an explicit locker. Final GREEN: focused strengthened test passed, all 58 screensaver tests passed under approved isolated Xvfb, and all eight timer tests passed.
