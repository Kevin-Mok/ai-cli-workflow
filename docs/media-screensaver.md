# Three-monitor media screensaver

Show a media conveyor across the existing X11/i3 desktop without changing display configuration. Install the launcher and native messaging host, enable the local extension in every Chrome/Chromium profile, then preview it and start the idle monitor. Missing browser coverage suppresses automatic activation; manual preview remains available.

## Requirements and installation

Use an X11 desktop with exactly three horizontally arranged outputs and XInput2.1 support. Automatic activation requires a middle output at least 3840×2160. The launcher reads live `xrandr --listmonitors` geometry, including vertical offsets; it never calls the display-layout script or disables an output. The older `dual-monitor-slideshow` entrypoint remains unchanged and retains its older behavior.

Required Ubuntu packages: `python3`, `python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`, `gir1.2-gstreamer-1.0`, `gstreamer1.0-gtk3`, `gstreamer1.0-plugins-good`, `gstreamer1.0-plugins-bad`, `gstreamer1.0-libav`, `python3-xlib`, `libxi6`, `x11-xserver-utils`, and ImageMagick with HEIC reading support. The synthetic demo additionally uses `ffmpeg` and `python3-pil`. Package installation requires sudo; the screensaver installer and runtime do not.

From the checkout, run `./scripts/executable_media-screensaver install`. This copies the package and launcher into `~/scripts/`, creates `~/scripts/media-screensaver-native`, and writes the native-host manifest under both Chrome and Chromium's per-user `NativeMessagingHosts` directories. Re-running updates only the owned package files and preserves other files in that directory. Nonstandard browser configurations need the same native-host manifest in their documented host lookup location.

The installer adds only its startup line to an existing i3 config and preserves every other setting. The i3 template also starts `~/scripts/media-screensaver daemon` on the next i3 session. Run `refresh-config` after tracked configuration changes. Its current implementation applies reviewed chezmoi files, regenerates shortcuts and reloads fish; it excludes chezmoi scripts, externals and removals. The explicit installer above installs the screensaver even when scripts are excluded from a general refresh. To start in the current session, run the daemon from a terminal; it stays in the foreground and reports status every 30 seconds. Duplicate daemon starts exit harmlessly.

## Enable the browser bridge

1. Open `chrome://extensions` in each Chrome/Chromium profile used on this desktop.
2. Enable Developer mode, choose **Load unpacked**, and select `~/scripts/media_screensaver/browser`.
3. Confirm ID `fpologomejgfmlemideffbaallaejhbb`. Enable **Allow in incognito** if you use incognito, and **Allow access to file URLs** if you play local browser files.
4. Reload tabs that were open before the extension was enabled. Load a normal web page and run `~/scripts/media-screensaver status` from a desktop terminal.

The extension inspects each window's active tab, including non-focused windows and fullscreen playback. It traverses frame and shadow-root video elements and reports only playback state, numerical window/video rectangles and window IDs. It sends no URLs, page titles, media names or browsing content to the host. Native JSON is strictly validated; per-host files are private (0700 directory, 0600 files) and expire after four seconds. State lives under `$XDG_RUNTIME_DIR/media-screensaver`, with a private `/tmp/media-screensaver-UID` fallback. Clean native-host disconnect removes its state file.

The gate uses the visible video rectangle rather than generic MPRIS status. Playing video intersecting the middle output blocks automatic activation. Paused/ended video, audio-only playback and video confined to either side output do not. Every native Chrome window, including hidden/minimized windows, must match one reported extension window; only mapped windows contribute video, so another profile without the extension suppresses activation. Status messages explain unavailable coverage. A browser with no bridge connection suppresses automatic activation even when no video is playing.

## Daily commands

Run `~/scripts/media-screensaver preview` for the real media library at `/mnt/linux-files-3/hevin`. Use `--media DIR` for another recursive library. Supported extensions are JPG/JPEG, PNG, WebP, HEIC, MP4, MOV and MKV, case-insensitively. Symbolic links and unrelated files are ignored. Originals are opened read-only. Individual corrupt/unavailable files are skipped and quarantined until the preview restarts; an unavailable mount or no decodable media produces an actionable error.

The first item starts on the left. Every ten seconds, a new random item enters and existing items move one output right with a 750ms slide. The same video pipeline survives movement and resizing; short clips seek to the start at end-of-stream, and long clips stop when their card exits. Video audio is disabled. Photos and videos preserve their aspect ratio against black. Adjacent selections differ whenever another usable file exists.

Run `~/scripts/media-screensaver daemon` for activation after 300 seconds of keyboard/mouse inactivity. It tracks raw XInput2 keyboard/mouse activity from daemon startup, ignoring software screensaver resets from players, without resetting X11 idle, changing DPMS, taking input grabs or inhibiting lock/suspend. Locked sessions and unavailable lock state suppress activation. Any keyboard/mouse activity dismisses a preview. Qualifying browser video starting during preview also dismisses it; manual preview remains available without a healthy bridge. Stop the foreground daemon with Ctrl+C; it releases its owned preview. To stop an i3-started daemon, send TERM to the PID shown in the private runtime status file. Never kill unrelated players or browser processes.

Run `~/scripts/media-screensaver probe --media DIR` to decode one frame of every supported candidate and report per-format successes/skips. It does not start a preview or alter originals. It can take time for a large library; use a small test directory first. `~/scripts/media-screensaver demo` generates disposable portrait photos and short/long videos, probes them plus a corrupt MP4, then shows one identified long synthetic video for 35 seconds. The demo does not generate HEIC because the installed libheif has reading support but no HEVC encoder plugin.

Options shared by commands: `--seconds N` bounds preview duration (0 waits for dismissal); `--report PATH` writes a new private JSONL preview report with item IDs, slots and playback timestamps, never personal filenames; `--plain` produces ASCII CLI output (`CLI_PLAIN=1` also works); `--details` includes raw diagnostics. `--help` describes the commands. Report paths must not already exist. `NO_COLOR` does not remove emojis; output does not require ANSI color.

## Verification and limitations

Automated and observed desktop evidence are recorded separately in [the implementation plan](../plans/monitor-media-screensaver.md). Repeatable manual checks, including browser geometry and cleanup, live in [the smoke checklist](smoke-tests.md#media-conveyor-screensaver).

Browser page zoom is supported on X11. Uniform browser UI scale (including the measured 1.40625 scale) is converted into native X11 pixels and checked against real window bounds. Unreconciled mixed display scaling, ambiguous transforms/CSS zoom, noncenter video positioning, picture-in-picture, restricted browser tabs, inaccessible frames and incomplete snapshots suppress automatic activation. Canvas/WebCodecs renderers without an HTML video element are not detectable. The bridge is for Chrome/Chromium; it cannot distinguish playing video in other browsers. Custom Chrome builds/host lookup paths and site-specific players require separate acceptance. A status of ready proves current bridge coverage, not every site's video implementation. i3 may ignore conventional browser minimize requests; a still-viewable playing video continues to block. Moving an owned browser to a non-viewable i3 workspace/scratchpad excludes its video after native window reconciliation.

The CPU GTK video sink prefers installed libav decoders to avoid incompatible CUDA-memory negotiation. High-resolution simultaneous videos may consume significant CPU; smoothness must be checked on the actual GPU/desktop. No personal images or videos are committed. Roll back by stopping only this daemon, removing its i3 startup line and uninstalling the named package/host manifests; the old slideshow and existing lock/suspend configuration remain available.

## Automated and manual test plan

Automated: `xvfb-run -a python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py' -v` exercises the conveyor, strict native framing/state, complete native-window matching, installation, real GStreamer continuity/loop/cleanup, portrait pixels, software idle resets, keyboard grabs and manual bridge failure. `node tests/test_media_screensaver_browser.cjs` runs real content-script initialization plus geometry, frame relay, shadow roots, UI scale and audio-only regressions. `bash tests/test_desktop_display_layout.sh` checks existing display integration. These require no sudo; an environment blocking X11 sockets needs its approved scoped execution route even for Xvfb.

Manual: follow the grouped smoke entries for the full35-second conveyor, browser matrix, unavailable mount/corruption and five-minute activation. A real suspend/resume cycle and five uninterrupted idle minutes are separate acceptance checks; automated threshold/cleanup evidence does not establish those observations. Browser tests in an isolated profile do not enable the extension in ordinary user profiles.
