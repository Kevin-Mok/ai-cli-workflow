# Screensaver GPU decoding

Use NVIDIA hardware decoding for compatible H.264 and HEVC cards on the GTX 1070. Preserve GTK presentation, looping, orientation, and software playback where hardware is unavailable.

## Scope and decisions

The installed GStreamer 1.24 NVIDIA decoder advertises system-memory output on the desktop. Prefer those factories above libav when they advertise that output. Retry with software once when a selected NVIDIA pipeline errors. Keep the current player and original files. Preserve unrelated dirty files and existing live settings.

## Checklist

- [x] Verify a real H.264 card selects NVIDIA when available and returns to playback after a simulated decoder failure.
- [x] Update card decoder selection, README, operator documentation and smoke checklist.
- [x] Run the Xvfb renderer and orientation regressions and verify NVIDIA selection on three concurrent 4K cards on the desktop.
- [x] Sync the installed renderer and verify the idle service.

## Risk and rollback

GPU frames still cross into system memory for GTK and GPU capability varies by codec/profile. The desktop test must confirm actual decoder use rather than registry presence. To roll back, restore the previous renderer in source and its installed copy, then restart the user service.

## Verification and review

- `xvfb-run -a /usr/bin/python3 -B tests/test_media_screensaver_runtime.py RuntimeTests.test_h264_prefers_nvdec_and_retries_failed_hardware_in_software` exited 1 before the change because it observed `avdec_h264`. It exited 0 after the change and again after final signal-handler cleanup. With `CUDA_VISIBLE_DEVICES=-1` and a fresh GStreamer registry, the hardware test skipped and the software movement/cleanup test passed.
- `xvfb-run -a /usr/bin/python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py'` ran 69 tests with two skips and no failures after the orientation test waited for its first rendered frame. This suite ran before the final signal-handler cleanup. `node --test tests/test_media_screensaver_browser.cjs` passed. The earlier orientation test failure and its evidence are recorded in the [incident report](../docs/postmortem/2026-11-17-screensaver-nvdec-orientation-test.md).
- Scoped `chezmoi apply` updated only `~/scripts/media_screensaver/renderer.py`. `cmp` confirmed its bytes match source and `systemctl --user is-active media-screensaver.service` returned `active`. The idle daemon launches each preview in a fresh process. No service restart was needed.
- A temporary probe wrapping the installed preview measured actual 4K H.264 playback. All three real desktop cards selected NVDEC and delivered frames. Input dismissed playback after 3.4 seconds and cleanup released every pipeline. An isolated 14-second run with simulated monitor geometry reached the conveyor transition and released all pipelines. Three original cards had valid playback positions at that transition. Sustained visual smoothness on the real desktop and live HEVC playback remain unverified.
- To repeat the manual check, follow the [media conveyor checklist](../docs/smoke-tests.md#media-conveyor-screensaver). Validate the `dec` column against an idle baseline and use a folder limited to a known-compatible clip.

Suggested commit: `feat(screensaver): prefer NVIDIA hardware decoding`.

## Cursor handoff

> Review the screensaver's NVDEC selection and software retry in `scripts/media_screensaver/renderer.py`. Confirm only NVIDIA H.264 and HEVC factories advertising system-memory output outrank libav. Verify the same card resumes in software after a simulated NVDEC error, then follow the GPU smoke check on the three-monitor X11 desktop. Preserve unrelated working-tree changes and record measured results in this plan.
