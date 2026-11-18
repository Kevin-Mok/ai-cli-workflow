# Detect small changes on the 4K screen

Keep automatic playback suppressed while sampled pixels change outside visible
i3 bars on the middle 4K output. Reproduce a missed change, compare full-color
frames, and verify deployment and the existing idle rules.

## Scope and decisions

The journal records idle-service activation at 19:51:28 after 426 seconds without
physical input and 300 seconds without detected screen motion. The original
fullscreen frames are unavailable. Treat any captured non-bar pixel change as
activity, including a blinking caret, per the requested movement rule. Keep
the existing polling cadence, bar geometry mask, and separate physical-input
clock. Exact comparison can miss motion between samples or a fully still scene.
Retain pre-existing edits in the screensaver renderer, tests, and documentation.

## Progress

- [x] Capture initial working-tree status and identify the activation path.
- [x] Reproduce a one-pixel change getting through the quiet gate.
- [x] Compare masked native-resolution RGB frames and update usage/smoke docs.
- [x] Run focused and existing regressions, then verify the running service.

## Verification and rollback

Run the motion tests with an isolated 4K Xvfb display, including the existing
nested i3bar case, then run the existing Python screensaver suite. On desktop,
watch fullscreen video on the middle display for over five minutes and inspect
`~/scripts/media-screensaver status`; pause it with the controls hidden and
verify that the normal quiet window eventually permits playback. To revert,
restore the previous comparator hunk, then redeploy and restart the idle service.

## Results

- RED: `python3 -B tests/test_media_screensaver_motion.py MotionTests.test_single_pixel_color_change_on_4k_restarts_quiet_period` failed because the sampler returned true at 300 seconds. The same command passed after the comparator changed.
- `SCREENSAVER_MOTION_X11_TEST=1 SCREENSAVER_MOTION_4K_TEST=1 xvfb-run -a -s '-screen 0 3840x2160x24' python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py'` passed all 70 tests with scoped X11/runtime access.
- `node tests/test_media_screensaver_browser.cjs` passed. The targeted postmortem-memory check and `git diff --check` passed.
- The installed detector matched the previous baseline before deployment and the updated source afterward. The restarted service was active and reported DP-2 in the middle and quiet-time suppression. End-to-end five-minute YouTube acceptance is pending.

## Handoff

Suggested commit subject: `fix(screensaver): detect native 4K pixel changes`

Cursor prompt: Verify the running screensaver with fullscreen YouTube on DP-2
using the paired playback and pause checks in docs/smoke-tests.md. If playback
is interrupted, capture the service journal and distinguish physical idle from
screen quiet before changing the detector.

## Commit milestone

The commit named above includes the comparator, defining regression, usage and
smoke check updates, and the incident and its memory records. Session attribution
comes from observed edits because the scope helper did not detect the writes.
The mixed-file changes are limited to the screensaver hunks. The live service is
already running the fix. Fullscreen duration acceptance remains open.
