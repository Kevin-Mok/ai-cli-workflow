# Screensaver stutter with one video

The user reported that one video beside two photos improved playback but still stuttered. The specific clip and exact timing were unavailable. The renderer preferred NVDEC for compatible clips, and the shared video card sent full-size frames through orientation filters and GTK.

The lookup `screensaver 4K 1080p NVDEC GTK video lag` returned `local-gtk3-mixed-card-presentation`. Its GTK setup applies, but the black-region fix did not measure sustained smoothness. The earlier [decode benchmark](2026-11-17-screensaver-video-stutter.md) and [NVDEC check](../../plans/screensaver-gpu-decoding.md) do not isolate the remaining single-card bottleneck.

The defining test rendered a synthetic 4K clip and observed 3840×2160 at GTK before the change and 1920×1080 afterward. The cap applies before rotation. A seven-second isolated comparison using the same USB clip, two photos, and NVDEC rendered 107 full-sized frames versus 158 capped frames. This clip had rotation metadata, so GTK saw 2160×3840 before and 1080×1920 after. Each comparison used a single run and the counts include startup.

The first full regression run reached 73 tests with one error and two skips. Its manual-preview bridge-failure fixture passed an argument namespace predating the video-only option. The scan tried to access the missing field and raised AttributeError before playback. The query `manual preview AttributeError SimpleNamespace video_only bridge runtime` found no applicable cause. The scan now defaults to mixed mode for callers that omit the flag. The scaling test had already passed.

The installed renderer played the capped clip with two photos for 14 seconds on the desktop. NVDEC remained selected and the clip advanced through the first slide. The run ended as the sample was looping, so its terminal counters did not measure the entire preview. The isolated measurements support lower display work for the sample. Subjective smoothness on the originally reported clip remains unknown.
