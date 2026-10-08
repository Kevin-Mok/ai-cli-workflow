# Codex notification sound

Play your own MP3 for Codex notifications, with optional offline speech of the exact saved conversation title afterward. Configure a clip, install the voice, deploy the completion callback, resume affected conversations, then explicitly enable speech. MP3 sound stays disabled until you configure a path; speech is separately disabled by default. The selected [can-i-ask-you-a-question.mp3](../scripts/can-i-ask-you-a-question.mp3) is stored in this repo; the setting remains machine-local.

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

The daemon and your shell must use the same XDG config location. Missing configuration means disabled. A missing/invalid file or unavailable `mpv` skips audio without breaking the popup. Errors go to `${XDG_STATE_HOME:-$HOME/.local/state}/codex-notification-sound/errors.log` and appear on stderr with `--details`; default warnings give a short recovery action. Player failures make `preview` exit 1; the Dunst hook always exits 0. Playback has a 60-second limit; use a short notification clip.

## Optional offline title speech

Install the pinned Piper 1.8.0 English `en_US-lessac-medium` voice, then check it:

```sh
~/scripts/setup-codex-notification-speech --install
~/scripts/setup-codex-notification-speech --check
~/scripts/codex-notification-sound preview --title "Smoke-test VPS backup"
```

No sudo is needed. Installation needs internet and Python's `venv`/pip support. The isolated environment, voice, download cache and temporary installation files stay under `${XDG_DATA_HOME:-$HOME/.local/share}/codex-notification-speech`. `--check` synthesizes a temporary WAV offline and deletes it; playback contacts no service. `status` uses aligned, width-aware output with helpful icons; add `--plain` for ASCII or `--details` for full paths and recent diagnostics. Both notification commands accept these display flags and emit no ANSI colors, respecting `NO_COLOR`. `status` reports speech activation and voice file readiness; `--check` verifies the pinned runtime and actual synthesis.

After `refresh-config` deploys the completion callback, start or resume affected Codex conversations to load it, then enable speech:

```sh
~/scripts/codex-notification-sound speech enable
```

Audio follows **completed turns only**, including focused and background completions. Permission requests and automatic approval reviews remain silent in speech mode, so a task does not repeatedly announce its title during work. Desktop popup content, actions and focus behavior remain unchanged. Dunst's sound callback becomes a no-op, preventing a second MP3. Existing sessions may still have the former PermissionRequest hook loaded; the updated bridge rejects its calls before launching audio. The deployed hooks file removes that permission handler, and no `/hooks` trust is required for completion speech.

The [event bridge](../scripts/executable_codex-notification-event) resolves completion `thread-id`. The transcript must resolve inside `${CODEX_HOME:-$HOME/.codex}`. A filename's rollout UUID need not equal its conversation ID. The latest matching `thread_name` in `session_index.jsonl` is captured before detached audio queues; visible terminals, answer text and other conversations are never title fallbacks. Ordinary spawned agents use their own saved title. Internal system/reviewer threads are silent. Missing, malformed or inconsistent identity/title means MP3 only.

One per-user state-directory lock serializes each complete MP3 → synthesized title WAV sequence. Piper receives the exact title through stdin with a 30-second limit; each mpv playback retains its 60-second limit. Temporary WAVs are deleted. Failed synthesis leaves the already-played MP3 as the notification, without retrying it or affecting Codex. Legacy permission-hook calls return immediately with no audio or approval decision. Scheduler order between simultaneous sequences is unspecified.

For immediate speech rollback, preserving the selected MP3:

```sh
~/scripts/codex-notification-sound speech disable
```

Dunst's existing MP3-on-popup behavior resumes immediately. `disable` still removes only the MP3 setting; use `speech disable` separately when returning to popup audio. The machine-local speech switch is `speech.json` beside `sound.json`, atomically written with mode 0600. No setting, voice or virtual environment is tracked in Git.

The contracts are described in [Codex hooks](https://learn.chatgpt.com/docs/hooks) and [Piper 1.8.0](https://pypi.org/project/piper-tts/1.8.0/). Transcript metadata is a defensive local integration and can change; unavailable metadata fails to MP3 only.

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

This is local process identification, not a security boundary. SSH and tmux foreground clients cannot reliably expose remote/nested Codex origin and remain ordinary Kitty notifications. Every popup that local Codex actually emits is eligible, including approvals; this does not enable notifications that Codex itself suppresses. With speech disabled, the deployed completion callback and permission bridge are no-ops; Dunst retains this behavior. With speech enabled, the event bridge owns audio as described above.

The inspected contracts are documented in [Kitty's callback configuration](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.filter_notification), [versioned Kitty notification code](https://raw.githubusercontent.com/kovidgoyal/kitty/v0.49.2/kitty/notifications.py), [Dunst scripting](https://dunst-project.org/documentation/#SCRIPTING) and [Dunst 1.9.2 script delivery](https://raw.githubusercontent.com/dunst-project/dunst/v1.9.2/src/notification.c).

## Checks

```sh
python3 -B tests/test_codex_notification_sound.py
python3 -B tests/test_codex_notification_speech_setup.py
basedpyright --level error scripts/executable_codex-notification-sound scripts/executable_codex-notification-event scripts/executable_setup-codex-notification-speech
xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py
```

Unit tests cover fake completion/approval origins, channel isolation, text lookalikes, disappearing processes, absent/invalid local settings, safe filenames, one player invocation, failures and a real empty-home chezmoi install. The daemon check uses private DBus/Xvfb and a fake mpv; it verifies exact app matching, delivery timing, duplicates, history, pausing and empty-format suppression without audio or changes to your desktop daemon.

After selecting a clip, run the reusable live checks:

```sh
~/scripts/codex-notification-sound smoke tagged
~/scripts/codex-notification-sound smoke kitty
```

With speech disabled, the first should show one synthetic popup and play once. With speech enabled it displays the popup silently because synthetic Dunst events do not invoke Codex hooks. The second emits Codex-looking OSC 9 text from an unrelated process and should remain silent. It exercises Kitty origin filtering; it does not simulate real Codex. Follow the [shared completion/approval, focus and rollback smoke checks](smoke-tests.md#codex-notification-sound) for actual Codex behavior.

## Rollback

For immediate speech rollback, run `~/scripts/codex-notification-sound speech disable`. To disable all configured audio, run `~/scripts/codex-notification-sound disable`; popups continue normally. For complete removal, remove only the `codex_notification_sound` rule, restore `always_run_script=true` if there are no intervening script-rule changes, and remove the completion `notify` entry, then remove this task's Kitty callback, event bridge, sound helper, setup helper and activation helper from both the tracked and installed paths. Apply the remaining config, restart Dunst and start a fresh Kitty process. Do not reset unrelated dirty files. Your MP3 is never deleted.
