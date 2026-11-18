# Screensaver media mix

Use `preview --video-only` to test three videos from a mixed library. Normal previews and automatic playback show one video and two photos after each transition when both types are available.

- [x] Define the CLI behavior with a mixed-library regression and a photo-only error case.
- [x] Filter preview candidates with the existing video extension set.
- [x] Verify installed video-only preview across a conveyor transition on the USB library and the photo-only error.
- [x] Define and implement the default mixed-library ratio across repeated transitions.
- [x] Update documentation and validate both installed modes.

Apply only the changed CLI and conveyor modules to the installed copy. Use the available media type when the library contains only one. Keep the three-monitor slide and quarantine behavior. Preserve the pre-existing screensaver renderer and motion changes and the unrelated edits in shared documentation. Roll back by restoring the previous CLI and conveyor modules in both locations.

## Verification

- The defining CLI test initially raised `SystemExit(2)` for the unknown flag. After implementation it passed, including case-insensitive recognition, both normal and video-only candidate lists, and the photo-only error.
- The defining ratio test initially observed three videos instead of one at every check. It passed after selection used the types of the cards staying on-screen. It covers the initial display, subsequent advances and skipped timer ticks.
- `/usr/bin/python3 -B -m unittest tests.test_media_screensaver tests.test_media_screensaver_cli tests.test_media_screensaver_motion tests.test_media_screensaver_bridge tests.test_media_screensaver_desktop` ran 44 tests with 42 passes and two skips in 1.249 seconds. The earlier sandbox-only lock issue is recorded in the [incident report](../docs/postmortem/2026-11-17-screensaver-preview-lock-sandbox.md).
- Installed `preview --media /mnt/usb-8tb/hevin/ --seconds 14 --video-only` admitted 1,464 videos and recorded four video entries across its first slide before input dismissal. The installed launcher rejected a photo-only fixture with exit 1 and no window. Scoped chezmoi sync of `main.py` and `core.py` matched source. The idle service reported active.
- Installed mixed preview on the same USB library admitted 5,989 media items. The report recorded one MP4 and two photos at startup and after the first slide settled at 10.858 seconds. It reached the configured duration and released all pipelines.

Follow the [manual smoke steps](../docs/smoke-tests.md#media-conveyor-screensaver) on the X11 desktop. Allow the first 750 ms slide to settle. The exiting and entering cards can both be videos during a transition.

Suggested commit: `feat(screensaver): set mixed and video-only preview modes`.

## Cursor handoff

> Review the screensaver preview flag in `main.py` and three-card media selection in `core.py`. Verify the two defining tests and repeat both installed USB-library previews through the first slide. Preserve the existing NVDEC renderer, motion detection and unrelated working-tree edits.
