# Screensaver playback scaling

Reduce the size of video frames going through orientation filters and into GTK to address remaining stutter in mixed playback. Use GStreamer's existing scaler to bound the decoded raster to 1920×1080 without upscaling ordinary square-pixel clips. Preserve the source file, frame rate, orientation, aspect ratio, NVIDIA selection and software fallback.

- [x] Record the reported stutter and test the GTK input size before implementation.
- [x] Scale in the shared video card before its orientation filters.
- [x] Verify actual negotiated sizes, rotation, hardware selection and software fallback.
- [x] Update README, playback docs and the manual smoke check. Sync the installed renderer and CLI modules and run a desktop playback check.

The cap applies after the decoder, which still processes the source resolution. A rotation may swap the capped dimensions. The test measures what GTK receives, while perceived smoothness needs live playback. To roll back scaling, restore the prior renderer at source and apply that one managed target. Preserve the user's prior GPU, motion and preview changes.

## Verification

- `xvfb-run -a /usr/bin/python3 -B tests/test_media_screensaver_runtime.py RuntimeTests.test_large_video_is_scaled_before_reaching_gtk` failed first with 3840×2160 received. It passed with the 1920×1080 cap.
- `xvfb-run -a /usr/bin/python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py'` passed with 71 passes and two skips, including rotation pixels and forced software fallback. `node --test tests/test_media_screensaver_browser.cjs` passed.
- Before and after isolated seven-second runs used the same USB clip and synthetic photos. Both selected NVDEC and reached the duration. The first rendered 107 frames and the second rendered 158. For the rotated clip, GTK received 2160×3840 before and 1080×1920 after. This is a single paired comparison, including startup.
- A real three-output desktop run of the installed renderer completed at 14 seconds, kept the one-video, two-photo mix, moved the capped NVDEC clip to the center output, and released every pipeline. Sustained perceived smoothness on the original clip is unverified.
- Scoped chezmoi applied only `main.py` and `renderer.py`. Both installed files matched their sources, the idle service reported active, and `git diff --check` passed. The [incident](../docs/postmortem/2026-11-17-screensaver-mixed-playback-stutter.md) records the related missing-flag regression and its targeted ledger check.

Follow the [manual smoke test](../docs/smoke-tests.md#media-conveyor-screensaver) with a 4K source in a mixed folder and leave the desktop untouched through the first slide.

Suggested commit: `perf(screensaver): scale video before display`.

## Cursor handoff

> Review the video scale and caps filter before orientation in `renderer.py`. Run the focused 4K sink-cap test, the full Xvfb screensaver suite and the mixed-library preview through the first slide. Verify that the source stays untouched, the rotated clip preserves aspect and NVDEC still falls back on error. Preserve earlier working-tree changes.
