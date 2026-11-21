# Screensaver regression blocked by desktop sandbox restrictions

The first CLI regression could not open its default preview lock in the existing desktop runtime directory because it was read-only. The first Xvfb suite also could not connect to the X11 Unix socket. The new blank-only policy tests passed, but those failures prevented running the complete desktop regression.

The lookup `screensaver preview.lock read-only filesystem Xvfb X11 socket Operation not permitted` matched the confirmed `ext-sandbox-loopback` workaround. Earlier screensaver reports independently identified the same preview-lock and socket symptoms. File and socket permission diagnostics point to the execution environment. The next step is a private temporary runtime directory and a scoped Xvfb run.

The approved Xvfb rerun with a private runtime directory passed 75 tests with one skip. The first forced-blank probe read the original root-window pixel. The corrected probe queried the XScreenSaver extension and observed `ScreenSaverOn` with `ScreenSaverBlanked`, then `ScreenSaverOff` after synthetic pointer input, with matching X11 settings before and after. The root drawable had retained its pixels while the server blanked the display. Live hardware remains a separate acceptance check.

## Refresh environment

The first refresh used `fish --no-config` to avoid unrelated startup effects. It loaded `refresh-config` directly but omitted its `cli-message` dependency, producing `command not found` and a final exit status of 127. The earlier steps reached shortcut generation. The lookup `refresh-config fish --no-config cli-message command not found` returned related shortcut verification guidance, with no exact match for the omitted dependency. Sourcing the tracked message function before refresh resolved it. Refresh exited zero and the interactive expansion checker passed without executing the mapping. The installed code matched the repo and the restarted service reported its usual 4K idle status.
