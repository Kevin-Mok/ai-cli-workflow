# Screensaver launch black box

Investigate the intermittent black rectangle at the upper-left of the screensaver, reproduce its cause, and verify a minimal renderer correction alongside randomized media on all three outputs at launch.

## Symptom and impact

The user reports an intermittent black box at the upper-left during playback. They also request a random image on each screen when launching the screensaver. Existing startup creates only one card on the left; other screens fill over twenty seconds.

## Evidence and status

Status: verified workaround for a reproduced GTK3/X11 mixed-card presentation defect; the exact partial mask in the user's photo remains unconfirmed. The user clarified that the box persists over the picture. An isolated red-photo probe did not reproduce it. GTK initially maps a tiny `(-1,-1,1,1)` surface before allocation, disproving the proposed large default-surface cause; no geometry-order patch was applied.

Initial reads attempted unmapped filenames (a renderer test, refresh executable and skill directory) and exited 1; no files or running playback changed. The mapper/catalog identified the correct paths. Broad temporary-file inventories encountered protected system-directory permission diagnostics; subsequent probes used owned fixtures.

A native synthetic pixel probe exceeded its intended three-second duration while repeatedly capturing/encoding full-desktop PNGs. Stop only its exact owned PID; investigate callback blocking before repeating. This is diagnostic instrumentation failure, not evidence of a screensaver defect. Narrow or capture once on subsequent probes. The unrelated small Chrome/Vesktop windows at the root's upper-left are unmapped and therefore do not explain a visible box.

Ledger registration initially rewrote unrelated Unicode escape formatting. Restoring that formatting with Python's `unicode_escape` briefly produced non-JSON `\x` escapes; corrected them to JSON `\u00` escapes and parsed the full ledger successfully before further use. Use the existing JSON encoder settings for subsequent ledger changes; this was an editing-helper error, not a runtime failure.

Postmortem lookup: `screensaver black box upper left random image launch` found orientation-fixture guidance (`local-video-rotation-fixture-metadata`), which applies to rotation test setup, not the reported rectangle. No applicable rectangle remedy was found. Preserve GTK initialization and verified fixture metadata for regression checks.

## Root cause and workaround

A video alone renders correctly, but a red MP4 between photo siblings renders black while playback advances. Bypassing GTK3 double buffering only on the video widget restores direct X11 screen pixels, including after movement/resizing, without obscuring green photo neighbors. This localizes the reproduced defect to GTK's buffered presentation of mixed widgets; the upstream implementation defect was not repaired. `ensure_native`, changing the layout container, forced redraw, and Cairo save/restore were insufficient and were excluded.

GDK child/parent screenshots changed or omitted native-child presentation; some apparent native-window successes depended on capture side effects. The defining test instead synchronizes GDK and reads actual root pixels through a separate Xlib connection. An Xlib data string caused one diagnostic test TypeError; the fixture normalizes that library return to bytes. Direct X11 baseline fails with red channel0, whereas the buffering workaround passes with red253 and neighboring green255.

GTK documents the setter as deprecated, with possible flicker, stacking and performance costs: [GTK3 buffering contract](https://docs.gtk.org/gtk3/method.Widget.set_double_buffered.html). Keep this workaround limited to the existing GTK3/X11 video sink and re-evaluate it when changing renderers. Original media and orientation filters remain untouched.

## Verification and remaining acceptance

- Startup RED: two new tests failed because only slot0 was populated. GREEN: all three slots contain random media immediately, single-file repetition works, ten-second cadence and adjacent non-repeats remain covered.
- Renderer RED: `test_video_remains_visible_beside_photo_windows` showed black video despite advancing playback and intact photos. GREEN includes literal screen pixels before and after resizing/moving that same video.
- Fresh focused runtime9/9 and full screensaver57/57 pass; browser CJS and display-layout shell checks exit0. Expected GTK deprecation and Xvfb DRI2 diagnostics remain; Python Xlib also emits an upstream Xauthority ResourceWarning.
- A bounded real desktop probe used only green PNG/red MP4 fixtures on the actual three-output geometry. All three screens had correct colors at startup and after an accelerated slide; playback timestamps advanced, duration dismissal occurred at1.604s, final cleanup reported players0, exit0. No capture side effects or full-screen PNG encoding were needed.
- Source/live comparison found no newer installed work; explicit installer exited0. Final installed-byte and runtime checks are recorded in the plan.

The required `refresh-config` attempt exited1 on a protected `scripts/media-screensaver` changed-target prompt/EOF, rather than the historical mimeapps conflict. The installed launcher and twelve package files match the reviewed repository bytes. No forced adoption or overwrite was attempted; explicit installation succeeded separately. Preserve changed-target protection and report this refresh limitation. Existing refresh-conflict guidance applies; no additional remedy was attempted.

The user's photograph shows a partial upper-left rectangle; that exact historical frame was not reproduced. Recheck the installed screensaver on the original content, including a full-resolution multi-video session. This limitation is separate from the proven mixed-widget presentation workaround. Keep all personal media and screenshots outside Git.
