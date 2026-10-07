# Codex notification sound

Play your own MP3 when a local Codex completion or approval popup appears. Apply the hook, start a fresh Kitty process, choose a clip, then preview it and check real notifications. Sound stays disabled until you configure a path. The selected [can-i-ask-you-a-question.mp3](../scripts/can-i-ask-you-a-question.mp3) is stored in this repo; the setting remains machine-local.

## Choose, preview and disable

These commands require no sudo. The current clip lives at `/home/example/linux-config/scripts/can-i-ask-you-a-question.mp3` and is tracked through Git LFS. Quote filenames containing spaces when choosing another clip:

```sh
~/scripts/codex-notification-sound status
~/scripts/codex-notification-sound set "$HOME/linux-config/scripts/can-i-ask-you-a-question.mp3"
~/scripts/codex-notification-sound preview
~/scripts/codex-notification-sound disable
```

On GUI hosts, `refresh-config` also installs the repo clip at `~/scripts/can-i-ask-you-a-question.mp3`; the selected path can point to either copy. The clip is stored through Git LFS, while the local JSON is excluded from repo artifacts.

`set` accepts an existing local file, resolves its absolute path, and writes an atomic, mode-0600 JSON setting. `disable` removes only that setting and leaves your MP3 intact. To switch clips, run `set` again. The editable setting is `${XDG_CONFIG_HOME:-$HOME/.config}/codex-notification-sound/sound.json`:

```json
{"path": "/absolute/path/to/your clip.mp3"}
```

The daemon and your shell must use the same XDG config location. Missing configuration means disabled. A missing/invalid file or unavailable `mpv` skips audio without breaking the popup. Errors go to `${XDG_STATE_HOME:-$HOME/.local/state}/codex-notification-sound/errors.log` and stderr. Player failures make `preview` exit 1; the Dunst hook always exits 0. Playback has a 60-second limit; use a short notification clip.

## Installation and activation

Repository sources are [Kitty's callback](../dot_config/kitty/notifications.py), [Dunst's rule](../dot_config/dunst/dunstrc) and [the playback command](../scripts/executable_codex-notification-sound). Apply with the normal `refresh-config` workflow after checking its live-to-source Codex/Git snapshots against protected work.

Run the activation helper once after initial installation, or after changing the Kitty notification callback or Dunst rule:

```sh
~/scripts/codex-notification-activate --open-kitty
```

You do **not** need to run it for every Kitty launch. Each new Kitty process loads the installed callback automatically, and the selected sound path persists across terminal launches and reboots. Open Kitty normally afterward. Changing the MP3 with `set` takes effect on the next playback without activation or a restart. Normal desktop startup loads Dunst's installed rule after a reboot.

It identifies the current session's notification-bus owner, verifies that it is your Dunst process, restarts only that daemon, and opens a fresh Kitty process. It preserves existing Kitty/Codex terminals and does not change the sound setting. Omit `--open-kitty` to restart Dunst only. Startup diagnostics are saved alongside the sound error log in `dunst.log`.

Dunst 1.9.2 reads its configuration at startup and requires a restart. It has no config reload command. Restarting clears its in-memory history and queues. Start a **fresh Kitty process** to load `notifications.py`; a new tab, config reload or window attached to an existing Kitty process does not load this callback. Leave your existing Codex sessions open and launch a new ordinary Kitty instance when ready.

## How it works

Codex already uses OSC 9 with `tui.notifications=true`. The callback resolves the notification's channel ID to its originating Kitty window and examines that window's foreground processes. It tags a local executable named `codex` as application `codex-kitty`. It never matches notification text, falls back to the active window, launches a player or sends a second popup. The official npm launcher runs the native Codex child in the same foreground process group.

Dunst matches that exact application name and double-forks the sound helper, so waiting for mpv does not block Kitty, Codex or Dunst. Playback uses argument lists without a shell and passes the entire filename after `--`. mpv ignores user configuration and opens no video window. The original notification content, timeout, actions and click-to-focus remain unchanged; Codex/Kitty's existing focus suppression remains in place.

`always_run_script=false` is global in Dunst 1.9.2. There are no other active script rules in this repo. It prevents sound for empty-format suppressed notifications and repeated calls for already-sounded objects. Native duplicate stacking remains enabled: an identical displayed notification adds no immediate sound or popup. Most history recalls stay silent; Dunst replaces a stacked duplicate with an unsounded object, which can sound once when later recalled or restored. Notifications queued while Dunst is paused sound only when displayed. Future `skip_display=true` rules would require separate review because Dunst invokes scripts before that suppression.

This is local process identification, not a security boundary. SSH and tmux foreground clients cannot reliably expose remote/nested Codex origin and remain ordinary Kitty notifications. Every popup that local Codex actually emits is eligible, including approvals; this does not enable notifications that Codex itself suppresses. Codex's completion-only `notify` hook is unused.

The inspected contracts are documented in [Kitty's callback configuration](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.filter_notification), [versioned Kitty notification code](https://raw.githubusercontent.com/kovidgoyal/kitty/v0.49.2/kitty/notifications.py), [Dunst scripting](https://dunst-project.org/documentation/#SCRIPTING) and [Dunst 1.9.2 script delivery](https://raw.githubusercontent.com/dunst-project/dunst/v1.9.2/src/notification.c).

## Checks

```sh
python3 -B tests/test_codex_notification_sound.py
xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py
```

Unit tests cover fake completion/approval origins, channel isolation, text lookalikes, disappearing processes, absent/invalid local settings, safe filenames, one player invocation, failures and a real empty-home chezmoi install. The daemon check uses private DBus/Xvfb and a fake mpv; it verifies exact app matching, delivery timing, duplicates, history, pausing and empty-format suppression without audio or changes to your desktop daemon.

After selecting a clip, run the reusable live checks:

```sh
~/scripts/codex-notification-sound smoke tagged
~/scripts/codex-notification-sound smoke kitty
```

The first should show one synthetic popup and play once. The second emits Codex-looking OSC 9 text from an unrelated process and should remain silent. It exercises Kitty origin filtering; it does not simulate real Codex. Follow the [shared completion/approval, focus and rollback smoke checks](smoke-tests.md#codex-notification-sound) for actual Codex behavior.

## Rollback

For immediate rollback, run `~/scripts/codex-notification-sound disable`; popups continue normally. For complete removal, remove only the `codex_notification_sound` rule, restore `always_run_script=true` if there are no intervening script-rule changes, and remove this task's callback, sound helper and activation helper from both the tracked and installed paths. Apply the remaining config, restart Dunst and start a fresh Kitty process. Do not reset unrelated dirty files. Your MP3 is never deleted.
