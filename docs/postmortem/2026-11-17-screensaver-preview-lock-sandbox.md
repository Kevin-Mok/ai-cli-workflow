# Screensaver preview lock in the test sandbox

The first sandboxed CLI regression run failed when the installed-style command attempted to open `/run/user/1000/media-screensaver/preview.lock` on a read-only filesystem. The failure occurred before the media scan.

The rerun used scoped access to the normal user runtime directory and completed with 41 passes and two skips. The focused mixed-library test also passed with an isolated temporary runtime directory and exercised the flag and photo-only error without a desktop.

The postmortem-memory query `screensaver preview.lock read-only file system sandbox` found general sandbox guidance and an unrelated scheduled playback incident. No player change was needed for the lock. Future checks can isolate the runtime directory or use the desktop session narrowly when verifying the live launcher.
