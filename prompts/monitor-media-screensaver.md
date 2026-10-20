Implement a Linux X11/i3 screensaver in /home/example/linux-config.

Media and movement:
- Recursively discover photos and videos under /mnt/linux-files-3/hevin, ignoring unrelated files.
- Randomize selection and avoid consecutive duplicates when alternatives exist.
- Build a conveyor: each item appears on the leftmost monitor, moves to the middle 4K monitor, then the rightmost monitor, then exits. A new random item enters on the left at each advance.
- Advance on a fixed 10-second cadence, using a short 750ms horizontal slide at each advance.
- Keep videos playing continuously across monitor transitions; mute audio, loop short clips, and end longer clips when they exit the rightmost monitor.
- Preserve aspect ratios with black letterboxing. Keep all three displays enabled without changing their resolutions or arrangement.
- Support the library’s JPG/JPEG, PNG, WebP, HEIC, MP4, MOV and MKV files. Verify actual decoding support; handle corrupt files without stopping the conveyor or modifying originals.

Activation:
- Provide manual preview and automatic activation after five minutes of keyboard/mouse inactivity.
- Block automatic activation specifically when Chrome/Chromium is displaying actively playing video on the middle 4K monitor.
- Audio-only playback and video confined to the other monitors must not block activation. Paused or ended video must not block it.
- Detect playing video in the active tab of a non-minimized browser window, including fullscreen playback. Use the video’s visible screen rectangle to determine whether it intersects the 4K output.
- Use a minimal local Chrome/Chromium extension and native messaging host for video state and window geometry. Generic MPRIS Playing status cannot satisfy this distinction.
- Keep browser messages limited to playback state and geometry/identifiers; omit browsing content and URLs.
- If the browser bridge becomes unavailable, suppress automatic activation with an actionable status message. Manual preview must remain available.
- Dismiss on keyboard/mouse activity, or when qualifying browser video starts. Preserve existing lock and suspend behavior.

Implementation:
1. Follow AGENTS.md and the repository’s plan contract. Inspect scripts/executable_apply-desktop-display-layout and scripts/executable_dual-monitor-slideshow, then verify live monitor geometry. Preserve the existing slideshow entrypoint.
2. Reuse installed tools where practical. Choose the smallest renderer that supports smooth movement and persistent video playback across unequal monitor sizes.
3. Write defining tests before implementation for conveyor timing, playback gating and cleanup. Test with synthetic media rather than committing personal files.
4. Add the installed launcher, idle integration and documented browser enablement. Follow repository CLI conventions, update usage/smoke documentation, and run refresh-config after tracked configuration changes.
5. Verify on the actual desktop. Report automated results separately from observed visual behavior and any unsupported browser/video cases.

Acceptance checks:
- Observe one identified item progressing through all three monitors on successive 10-second advances.
- Verify video timestamps continue through transitions without restarting.
- Test portrait photos, HEIC, short/long videos, corrupt files and an unavailable media mount.
- Test Chrome video on the 4K monitor versus either side monitor, audio-only playback, pause/resume, fullscreen, multiple windows and moving a playing video between monitors.
- Verify dismissal leaves no child players and preserves display geometry.

Finish with the working launch instructions, installation details, verification evidence and remaining limitations.
