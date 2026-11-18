# Screensaver video stutter

The user reported stutter during screensaver video playback. The affected clip and number of active video cards were unknown.

The installed renderer matched the checkout. It raises the rank of software libav decoders and draws through GTK's system-memory video sink. The conveyor can run three video pipelines concurrently. A metadata sample of 20 library videos contained five 3840 × 2160 H.264 clips at 30 fps.

On the Ryzen 5 5500, a bounded FFmpeg benchmark decoded and converted up to 120 frames per clip to BGRx. One sampled 4K stream ran at 28.1 fps. Three distinct sampled 4K streams tested concurrently ran at 12.1, 12.0 and 12.3 fps. This measures local file reading, software decoding and pixel conversion outside the application. It excludes GTK drawing and conveyor movement. The workload fell below the clips' 30 fps target under concurrency.

The sandboxed status command exited 1 because it could not read X11 monitors. Scoped read-only execution returned three monitors and a running idle monitor. This is the X11 access limitation documented in the [earlier X11 investigation](2026-10-20-screensaver-x11-sandbox.md).

The postmortem-memory query `screensaver video lag 4K` surfaced `local-gtk3-mixed-card-presentation`. Its GTK3/X11 setup matches, while its remedy addresses black regions and leaves sustained smoothness unverified. The benchmark supports software processing load as a contributor when several 4K videos play, and live frame timing on the affected clip remains open. No player settings or media were changed.

If live isolation is needed, compare the affected original with a 1080p copy at the same frame rate in equivalent conveyor runs and measure dropped frames.
