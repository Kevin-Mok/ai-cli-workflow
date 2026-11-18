# Screensaver settled layout

Stop asking GTK to rearrange all three cards on every frame while their positions are fixed. Keep the current slide, video size cap, NVIDIA decoding and input behavior.

- [x] Reproduce redundant layout changes outside the transition.
- [x] Update geometry during transitions and once when they settle.
- [x] Compare the same 4K clip before and after, run the X11 regressions, and sync only the renderer.

The cap and one-video mix stay in place. A slide still requires real geometry updates. Restore the previous renderer to roll this change back.

## Verification

- `xvfb-run -a /usr/bin/python3 -B tests/test_media_screensaver_runtime.py RuntimeTests.test_conveyor_moves_cards_during_slide_and_leaves_settled_geometry_alone` originally observed 112 calls by the first slide tick instead of seven. The defining regression passed after the change.
- `xvfb-run -a /usr/bin/python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py'` finished with 72 passes and two skips, including direct-screen mixed-card pixel checks.
- With the same 4K USB clip, two photos and NVDEC, paired 14-second isolated runs counted 120 then zero moves in the stationary interval. GTK video draw callbacks increased from 79 to 163 in seconds 2–9 and from 22 to 61 in seconds 11–14. The sink reported 378 versus 377 buffers. This checks GTK activity and does not count unique pixels presented on the monitor.
- The installed preview ran for 14 seconds on the real desktop and advanced the video to the middle display, with NVDEC and cleanup of all pipelines. The service was inactive during the check. The manual preview did not require restarting it. The user's original stutter remains visually unconfirmed. See the [incident report](../docs/postmortem/2026-11-17-screensaver-settled-layout-stutter.md).

Follow the [manual smoke check](../docs/smoke-tests.md#media-conveyor-screensaver) with a 4K clip in a mixed library. Compare its motion before, during and after the first slide.

Suggested commit: `perf(screensaver): stop relayout between slides`.

## Session delivery

- Commit milestone `perf(screensaver): improve video playback` packages NVDEC and fallback, the one-video mix and video-only preview, frame scaling, and the settled-layout fix with their tests and plans.
- The scope helper could not identify the session's writes. The delivery uses directly observed edits, with only the screensaver hunks in shared documentation and only the five incident records and one finding in the postmortem ledger. Unrelated dirty files and hunks remain in the worktree.
- The playback regression suite and live preview verified the implementation. Perceived smoothness on the originally reported clip remains open.

## Cursor handoff

> Review the settled-state geometry guard in the screensaver frame loop. Run the settled-layout regression and verify that geometry updates still occur for initial placement, slides and their final frame. Use the X11 smoke check with one 4K video and two photos. Compare video widget draw callbacks separately from GStreamer sink counters. Preserve the installed GPU decoding and video size cap.
