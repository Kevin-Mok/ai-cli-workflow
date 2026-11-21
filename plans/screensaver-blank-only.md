# Blank the displays without playing the idle screensaver

Use `ssof` to select black screens after five minutes of physical input and middle 4K screen inactivity. Restore the usual idle playback from the same launcher.

## Scope and decisions

Reuse the existing X11 idle daemon, physical input clock, 4K capture and i3 bar mask. Keep the selection in the private runtime directory so restarting the daemon preserves it and reboot clears it. Explicit previews and schedules are independent. The blank action uses the X11 server, which handles input-to-wake. Preserve the server's configured timers and the existing lock checks.

## Implementation and verification

- [x] Record the starting state. Existing changes to aliases, README, smoke tests, i3 and other files are protected.
- [x] Run the defining CLI and idle-loop regressions before and after the patch.
- [x] Add the blank action, mode commands, `ssof` under power options and usage/smoke documentation.
- [x] Verify actual X11 blanking on a disposable display, refresh installed shortcuts, verify fish expansion and deploy the updated launcher.
- [x] Prepare an isolated commit candidate and verify `origin/main` as the configured upstream.

## Risks and rollback

The daemon treats sampled pixel changes outside the bar as activity, so stationary playback can still time out. An unavailable 4K capture suppresses idle actions. Use `~/scripts/media-screensaver idle-playback` to restore the default. The existing manual and scheduled commands retain their behavior. Keep unrelated baseline hunks outside the commit.

## Evidence and review

The defining tests first failed because the launcher rejected `blank-only` and the idle loop never called the blank action. Both passed after implementation. With an isolated `XDG_RUNTIME_DIR`, the CLI suite passed 11 tests. `SCREENSAVER_MOTION_X11_TEST=1 xvfb-run -a python3 -B -m unittest discover -s tests -p 'test_media_screensaver*.py'` passed 75 tests with one skip under scoped X11 access. The timer suite passed all 10 tests. The display probe observed `ScreenSaverOn` with `ScreenSaverBlanked` while the idle inhibitor was held, then `ScreenSaverOff` after pointer input, with identical configured X11 settings. See the [sandbox incident](../docs/postmortem/2026-11-21-screensaver-sandbox-regression.md) and the [XScreenSaver API](https://xorg.freedesktop.org/archive/X11R7.5/doc/man/man3/XScreenSaverUnregister.3.html).

For hardware acceptance, follow the `ssof` entry in the shared smoke checklist. Verify five quiet minutes, input-to-wake and a playback interval on the 4K output. The shortcut checker verifies expansion without activating the mode. Manual desktop behavior and panel power draw remain separate from the Xvfb check.

Atomic delivery subject `feat(screensaver): add blank-only idle mode`. Include the launcher, two regressions, public usage and smoke notes, the new alias and the matching incident and plan. Preserve the unrelated baseline hunks in the shared files. The README check passed with `pass_no_change`.

Live deployment finished with `REFRESH COMPLETE`. `python3 -B scripts/executable_check-fish-abbr ssof '~/scripts/media-screensaver blank-only'` confirmed the exact Space expansion. The installed launcher module matched the source. The restarted service reported `Idle mode: play media`, `i3 bar excluded` and `Idle monitor: running`. The shortcut is ready to select blank-only mode from the desktop, and hardware acceptance remains open.

Cursor prompt for desktop validation: “Follow the `ssof` smoke check in `docs/smoke-tests.md`. Verify that moving video on the middle 4K display keeps the displays awake, then pause it until the displays go black and confirm mouse movement wakes them. Restore idle playback and record the observed result in this plan.”
