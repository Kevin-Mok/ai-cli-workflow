# First NVDEC frame in the orientation test

The first full Xvfb suite after enabling NVDEC ran 69 tests with one failure and two skips. The first landscape orientation fixture produced an all-black capture after a fixed 350 ms wait. Other orientation assertions and the focused NVDEC playback and fallback check passed. A sandboxed attempt could not initialize X11 and did not provide playback evidence.

The earlier `screensaver video lag 4K` lookup returned `local-gtk3-mixed-card-presentation`. The known GTK stacking issue occurs beside photo siblings after video playback has started. This failure occurred on the first card in a video-only window. The pixel test assumed the decoder had rendered by 350 ms. It now waits up to three additional seconds for the sink to report a rendered frame and retains the same color assertions.

On rerun with scoped Xvfb and device access, 67 tests passed and two skipped. The original failure did not recur. This supports the readiness hypothesis. Exact first-frame latency from the failed run was unavailable. The browser suite passed separately.

An ancillary sandboxed Fish startup probe also emitted read-only errors while trying to initialize fnm and regenerate home shortcuts. The lookup `fish fnm_multishells read-only file system sandbox` did not return a match specific to that startup path. Deployment uses the exact managed renderer target with chezmoi and does not depend on Fish initialization.
