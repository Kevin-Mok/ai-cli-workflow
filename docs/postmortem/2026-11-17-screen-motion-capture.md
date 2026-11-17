# Screen motion X11 capture compatibility — 2026-11-17

A disposable-Xvfb acceptance test exposed a capture type mismatch while implementing local screen motion detection. Reuse the established Xlib conversion and verify actual i3bar nesting before deployment.

## Symptom and impact

`SCREENSAVER_MOTION_X11_TEST=1 xvfb-run -a python3 -B -m unittest discover -s tests -p test_media_screensaver_motion.py` failed when a bar-only update should allow playback at t=300. The detector reported capture unavailable. No actual desktop was modified and no screenshot was saved.

## Lookup, cause and resolution

Tracked postmortem-memory and existing X11 runtime tests were consulted before further remedies. Existing runtime.py test line 164 already converts Xlib image data with Latin-1 encoding. The installed Xlib returns image data as a Latin-1 string, while Pillow requires bytes. Reusing that conversion repaired the capture. The same Xvfb command then passed four tests. Third-party Xlib emitted an xauth ResourceWarning; there was no production capture failure.

Live metadata inspection additionally found i3bar beneath i3-frame rather than as a direct root child; the middle 4K bar is 3840x112 at the lower edge. A nested synthetic bar regression is being added before extending discovery. No bar pixels or personal screen images were persisted.

## Status and learning

Capture conversion fixed in source; live deployment and final nested-bar regression are pending. No new generalized lesson: existing Xlib compatibility and inspect-actual-window-topology guidance apply. Keep status distinct from live acceptance; automatic motion policy was explicitly authorized by the user.

## Live 4K performance finding

A read-only in-memory diagnostic using python-Xlib full-resolution capture remained CPU-bound for over two minutes; only that owned diagnostic process was terminated. Pillow native ImageGrab captured the same 3840x2160 rectangle in 0.17 seconds. Switch large capture to native Pillow and retain Xlib only for bar/window metadata; pass an explicit X display so Pillow cannot fall back to screenshot commands that may create temporary files. Add a disposable large-frame regression and rerun tests before deployment. The old diagnostic never wrote image files. Native live probe succeeded; integration deployment is still pending.

## Native capture verification

Source now uses explicit-display native Pillow capture. Final disposable3840x2160 Xvfb motion tests: seven pass, including a bounded10-second capture regression and simulated native failure proving no temporary-image fallback. CLI integration tests: eight pass. Live source probe returned3840x2160, bar mask(0,2048,3840,2160), in0.278s. No image file was saved. Source fixes verified; scoped installation/service restart and full physical idle acceptance remain separate. Existing third-party Xlib xauth ResourceWarning is not a test failure.

## Installed resolution

Only main.py and motion.py were deployed after verifying the previous installed main matched committed source. Scoped refresh completed, the idle service restarted active/running, and fresh installed status showed14 seconds quiet out of300 with i3bar excluded. Installed bytes match tested source. No screenshot was persisted or uploaded. Physical five-minute acceptance is still separate; source and live capture/idle monitoring are verified.
