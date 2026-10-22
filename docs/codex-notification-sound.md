# Codex notification sound

Play your own MP3 for Codex notifications, with optional offline speech of the exact saved conversation title or a short sentence about a queued question afterward. Configure a clip, install the voice, deploy the completion and question callbacks, resume affected conversations, then explicitly enable speech. MP3 sound stays disabled until you configure a path; speech is separately disabled by default. The checkout includes a short "Sire" intro; selected paths remain machine-local. The older question MP3 is not bundled.

## Do Not Disturb

Right-click the i3blocks `Notis`/`DND` indicator to pause notifications and
suppress automatic Codex, Discord and Grok audio. Left-click restores delivery.
The shared player checks Dunst pause before starting, after waiting for its
playback lock, and before each clip or speech stage. Suppressed hook audio is
discarded; Dunst still displays its queued notifications when resumed. A phrase
already playing may finish. Explicit `preview` commands remain available during
DND. If Dunst is unavailable or its one-second query fails, audio retains its
usual behavior. No settings change or daemon restart is needed for this gate.
Use `codex-notification-sound smoke tagged` for a synthetic Codex popup without
TTS when Codex speech is enabled; DND queues that popup until resumed.

## Choose, preview and disable

These commands require no sudo. After applying the GUI dotfiles, select the bundled `~/scripts/sire.mp3`, which says only "Sire" in Ryan's voice before the notification message is read. It was generated offline with `en_US-ryan-high` at pace 0.95 from the text `Sire.`. On an existing installation, the older question clip may also be available at `~/scripts/can-i-ask-you-a-question.mp3`; selecting Sire leaves it intact. Quote filenames containing spaces:

```sh
~/scripts/codex-notification-sound status
chezmoi apply "$HOME/scripts/sire.mp3"
~/scripts/codex-notification-sound set "$HOME/scripts/sire.mp3"
~/scripts/codex-notification-sound preview
~/scripts/codex-notification-sound disable
```

The targeted `chezmoi apply` installs only the bundled clip. Refresh excludes chezmoi script hooks, not ordinary executable files or assets under `~/scripts`; verify the active ignore rules for the host. Keep your selected clip outside the checkout so repository moves or cleanup do not invalidate its path. Refresh cannot restore an audio file absent from source. The local JSON is excluded from repo artifacts.

If popups appear but both the clip and speech are silent, run `~/scripts/codex-notification-sound status --details` first. A missing selected clip stops the whole clip-then-speech sequence before synthesis starts. Use `set` with an existing local copy, then `preview --title "Notification audio check" --details` to verify both stages. No daemon restart or speech toggle is needed for a path correction. Historical errors remain in `status --details`; compare their timestamps with the new preview rather than deleting the log.

`set` accepts an existing local file, resolves its absolute path, and writes an atomic, mode-0600 JSON setting. `disable` removes only that setting and leaves your MP3 intact. To switch clips, run `set` again. The editable setting is `${XDG_CONFIG_HOME:-$HOME/.config}/codex-notification-sound/sound.json`:

```json
{"path": "/absolute/path/to/your clip.mp3"}
```

The daemon and your shell must use the same XDG config location. Missing configuration means disabled. A missing/invalid file or unavailable `mpv` skips audio without breaking the popup. Errors go to `${XDG_STATE_HOME:-$HOME/.local/state}/codex-notification-sound/errors.log` and appear on stderr with `--details`; default warnings give a short recovery action. Player failures make `preview` exit 1; the Dunst hook always exits 0. Playback has a 60-second limit; use a short notification clip.

## Audition ten local voices

Run the numbered audition script to compare ten offline Piper alternatives, hear the question clip before each test, then replay a favorite with different lines. These auditions leave your selected notification voice and speech switch unchanged. No sudo or cloud service is needed.

```sh
~/scripts/codex-voice-auditions --list
~/scripts/codex-voice-auditions
~/scripts/codex-voice-auditions --voice 1 --sample celebrate
~/scripts/codex-voice-auditions --voice 1 6 --sample technical
~/scripts/codex-voice-auditions --voice 6 --text "All done! The tests passed, and your changes are ready."
~/scripts/codex-voice-auditions --voice 1 --sample celebrate --length-scale 0.9 --offline
```

Numbers are stable: **1 Amy, 2 Bryce, 3 HFC Female, 4 HFC Male, 5 Joe, 6 Ryan, 7 Alan, 8 Alba, 9 Cori, 10 Jenny Dioco**. The first six are US voices; the final four are UK voices. Ryan and Cori use high-quality models; the others use medium. These single-speaker IDs were verified in the [upstream voice catalog](https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json). `--voice` also accepts a full name (quote names with spaces) or model ID. `--samples` displays the shared `short`, `celebrate` and `technical` lines; default `all` reads all three. `--text` supplies literal custom wording, up to 4,000 characters.

Install the existing speech environment first using `setup-codex-notification-speech --install` if needed. The first audition downloads only selected missing models into the existing XDG data voices folder; subsequent runs reuse them. Ten model downloads require substantial local storage. `--offline` prohibits downloads. Generation and playback are local; naturalness and upbeat delivery depend on the individual voice. The audition pace is slightly brisk at `--length-scale 0.95`; `1.0` is normal and `0.9` faster. This pace does not change notification playback settings.

Before every audible sample, the script displays its number/name, starts speech generation while the included "Can I ask you a question?" clip plays, then prints the remaining gap and plays the voice. The gap measures process handoff after clip completion, rather than physical speaker onset. It reflects cold-process synthesis, not a cached recording. `--clip PATH` lets you use another question clip. Actual notification playback also synthesizes while its configured MP3 plays, reducing the remaining gap while preserving strict MP3-then-speech order and serialized sequences. Synthesis retains a 30-second deadline and MP3 failure cleans up its owned synthesis process.

WAVs and a manifest containing sample text, pace, voice IDs and timings are saved under `${XDG_DATA_HOME:-$HOME/.local/share}/codex-notification-speech/auditions`. Each run replaces samples for selected voices and the manifest; failed generation preserves earlier valid WAVs. Use a separate `--output-dir PATH` to keep multiple wording/pace comparisons. `--render-only` exports WAVs without audio or clip timing. `--dry-run` prints the selected numbers and wording without dependencies or downloads. `--plain` is ASCII; `--details` reveals full paths/diagnostics. Slow subprocess phases report elapsed activity every five seconds. Interrupting stops owned workers and retains completed samples. Ryan (number 6) is now the selected notification voice at pace 0.95. Auditions remain independent of notification settings.

For direct checks from the checkout (no sudo), substitute `./scripts/executable_codex-voice-auditions` for the installed command above. Run `python3 -B tests/test_codex_voice_auditions.py` and `python3 -B tests/test_codex_notification_sound.py` for automated coverage; subjective voice choice needs listening.

## Speech-only preview

Use `~/scripts/codex-notification-sound preview --speech-only --title "Your task title" --plain`
to hear a title without the question clip. This uses local Piper with Ryan high
at pace 0.95 and leaves notification settings unchanged. A nonblank title and
installed voice are required; synthesis failures return nonzero. No saved
introduction/celebration recording or replay wrapper is included in this checkout.

## Optional offline title speech

The default notification voice is **6 — Ryan (US, high)** at pace **0.95**.
Install the pinned Piper 1.8.0 runtime and `en_US-ryan-high` voice, then check it:

```sh
~/scripts/setup-codex-notification-speech --install
~/scripts/setup-codex-notification-speech --check
~/scripts/codex-notification-sound preview --title "Smoke-test VPS backup"
```

No sudo is needed. Installation needs internet and Python's `venv`/pip support. The isolated environment, voice, download cache and temporary installation files stay under `${XDG_DATA_HOME:-$HOME/.local/share}/codex-notification-speech`. `--check` synthesizes a temporary WAV offline and deletes it; playback contacts no service. `status` uses aligned, width-aware output with helpful icons; add `--plain` for ASCII or `--details` for full paths and recent diagnostics. Both notification commands accept these display flags and emit no ANSI colors, respecting `NO_COLOR`. `status` reports speech activation, selected Ryan model/pace and voice file readiness; `--check` verifies the pinned runtime and actual synthesis.

After explicitly deploying the reviewed event scripts and hook configuration, start or resume affected Codex conversations to load them, then enable speech:

```sh
~/scripts/codex-notification-sound speech enable
```

Completion audio follows **user-facing completed answers**, including focused and background completions. The event must contain a nonblank `last-assistant-message`, and exact matching transcript metadata must identify a top-level `cli` or `vscode` conversation. Ordinary helper-agent completions, copied results on agent spawn, empty/missing answers, parent-linked sessions and unknown/ambiguous provenance stay silent. Permission requests and automatic approval reviews remain silent in speech mode, so a task does not repeatedly announce its title during work. Desktop popup content, actions and focus behavior remain unchanged. Dunst's sound callback becomes a no-op, preventing a second MP3. Existing sessions may still have the former PermissionRequest hook loaded; the updated bridge rejects its calls before launching audio. The deployed hooks file removes that permission handler, and no `/hooks` trust is required for completion speech.

The [event bridge](../scripts/executable_codex-notification-event) resolves completion `thread-id`. The transcript must resolve inside `${CODEX_HOME:-$HOME/.codex}`. A filename's rollout UUID need not equal its conversation ID. The latest matching `thread_name` in `session_index.jsonl` is captured before detached audio queues; visible terminals, answer text and other conversations are never title fallbacks. All spawned agents and internal system/reviewer threads are silent; their parent announces the final user-facing answer. Missing, malformed or inconsistent identity/provenance stays silent. A verified user-facing answer with an unavailable saved title still plays MP3 only.

One per-user state-directory lock serializes each complete MP3 → synthesized title or question WAV sequence. Piper begins while the MP3 plays and receives the exact title through private temporary stdin with a 30-second limit; each mpv playback retains its 60-second limit. Temporary WAVs are deleted. Failed synthesis leaves the already-played MP3 as the notification, without retrying it or affecting Codex. Legacy permission-hook calls return immediately with no audio or approval decision. Scheduler order between simultaneous sequences is unspecified.

For immediate speech rollback, preserving the selected MP3:

```sh
~/scripts/codex-notification-sound speech disable
```

Dunst's existing MP3-on-popup behavior resumes immediately. `disable` still removes only the MP3 setting; use `speech disable` separately when returning to popup audio. The machine-local speech switch is `speech.json` beside `sound.json`, atomically written with mode 0600. No setting, voice or virtual environment is tracked in Git.

The contracts are described in [Codex hooks](https://learn.chatgpt.com/docs/hooks) and [Piper 1.8.0](https://pypi.org/project/piper-tts/1.8.0/). Transcript metadata is a defensive local integration and can change; unavailable or unfamiliar provenance fails silently.

## Queued-question speech

When the TUI shows “Queued follow-up inputs · 1 question”, the question hook plays your selected “Can I ask you a question?” MP3 once, then Ryan speaks one concise sentence about the actual question. For example, “The checks passed. Should I deploy now?” becomes “Codex asks: Should I deploy now?” The task title and answer choices are not read.

The [question hooks](../dot_codex/hooks.json) use `PostToolUse` for `request_user_input_async` after its response confirms `accepted=true`, so rejected requests stay silent. Blocking `request_user_input` uses `PreToolUse`, before waiting for an answer, and validates required question fields first. Both require matching top-level cli/vscode transcript identity under CODEX_HOME. Helper/internal conversations, permission reviews, empty/malformed prompts and secret questions stay silent. The bridge accepts the native async `title` or blocking `question` fields, keeps at most three prompts plus a remaining-question count in one sentence capped at 280 characters, strips controls, and prefers the actual ask over preceding context. This is local text extraction and Piper synthesis, with no cloud summarization.

After applying, start/resume affected Codex conversations so they load the question hooks. On a new installation or after changing the hook command, open `/hooks` and enable/trust only the two question entries running `python3 /home/example/scripts/codex-notification-event`. Codex stores their exact trusted hashes and enabled state in its config; completion `notify` does not need hook trust. Speech and sound must both be enabled/configured. Questions announce in focused and background conversations, through the same serialized clip-then-speech player. Hardware listening and a genuine queued question are the final acceptance checks.

Run these silent direct probes from `~/linux-config`; no sudo or voice download is needed:

```sh
python3 -B scripts/smoke_codex_question_events.py --installed --case question --plain
python3 -B scripts/smoke_codex_question_events.py --installed --case multi-question --plain
python3 -B scripts/smoke_codex_question_events.py --installed --case question-blocking --plain
python3 -B scripts/smoke_codex_question_events.py --installed --case question-worker --plain
python3 -B scripts/smoke_codex_question_events.py --installed --case question-empty --plain
python3 -B scripts/smoke_codex_question_events.py --installed --case question-secret --plain
```

The first three verify one clip then one exact question sentence with two silent fixture-player calls. Worker, empty and secret cases verify zero calls. They copy deployed handlers into disposable directories and do not change your settings or play real audio. Native hook timing is covered separately by an isolated local fake-provider app-server probe; [the implementation plan](../plans/codex-queued-question-audio.md) records the observed runtime evidence and remaining live-session loading requirement. The hook coverage contract is documented in [Codex tool hooks](https://learn.chatgpt.com/docs/hooks#tool-coverage).

## Installation and activation

Repository sources are [Kitty's callback](../dot_config/kitty/notifications.py), [Dunst's rule](../dot_config/dunst/dunstrc) and [the playback command](../scripts/executable_codex-notification-sound). Apply with the normal `refresh-config` workflow after reviewing source changes and local differences privately. The current refresh function excludes chezmoi script hooks, externals and removals, and stops on conflicts; ordinary managed files under `~/scripts` can still be applied. Review live settings and managed-file differences before applying.

Run the activation helper once after initial installation, or after changing the Kitty notification callback or Dunst rule:

```sh
~/scripts/codex-notification-activate --open-kitty
```

You do **not** need to run it for every Kitty launch. Each new Kitty process loads the installed callback automatically, and the selected sound path persists across terminal launches and reboots. Open Kitty normally afterward. Changing the MP3 with `set` takes effect on the next playback without activation or a restart. Normal desktop startup loads Dunst's installed rule after a reboot.

It identifies the current session's notification-bus owner, verifies that it is your Dunst process, restarts only that daemon, and opens a fresh Kitty process. It preserves existing Kitty/Codex terminals and does not change the sound setting. Omit `--open-kitty` to restart Dunst only. Startup diagnostics are saved alongside the sound error log in `dunst.log`.

Dunst 1.9.2 reads its configuration at startup and requires a restart. It has no config reload command. Restarting clears its in-memory history and queues. Start a **fresh Kitty process** to load `notifications.py`, or run `~/scripts/notification-markdown-test --activate-all` to reload only the callback in reachable existing instances and send a native bold sample. A new tab or config reload alone does not reload the callback. Existing terminals, notification IDs and native actions are preserved by the no-UI activation path.

## How it works

Codex already uses OSC 9 with `tui.notifications=true`. The callback resolves the notification's channel ID to its originating Kitty window and examines that window's foreground processes. It tags a local executable named `codex` as application `codex-kitty`. Origin tagging never matches notification text or falls back to the active window. The callback never launches a player or sends a second popup. Separately, terminal titles/bodies render Markdown `**bold**` as safe Pango bold; literal HTML and code/escaped markers remain literal. The official npm launcher runs the native Codex child in the same foreground process group.

Dunst matches that exact application name and double-forks the sound helper, so waiting for mpv does not block Kitty, Codex or Dunst. Playback uses argument lists without a shell and passes the entire filename after `--`. mpv ignores user configuration and opens no video window. The callback formats strong-emphasis text; timeout, actions and click-to-focus remain native; Codex/Kitty's existing focus suppression remains in place.

`always_run_script=false` is global in Dunst 1.9.2. One notification_audio rule invokes the shared callback once; Python classifies Codex, Grok and Discord. Overlapping script rules would each run and cause duplicate audio. It prevents sound for empty-format suppressed notifications and repeated calls for already-sounded objects. Native duplicate stacking remains enabled: an identical displayed notification adds no immediate sound or popup. Most history recalls stay silent; Dunst replaces a stacked duplicate with an unsounded object, which can sound once when later recalled or restored. Notifications queued while Dunst is paused sound only when displayed. Future `skip_display=true` rules would require separate review because Dunst invokes scripts before that suppression.

This is local process identification, not a security boundary. SSH and tmux foreground clients cannot reliably expose remote/nested Codex origin and remain ordinary Kitty notifications. Every popup that local Codex actually emits is eligible, including approvals; this does not enable notifications that Codex itself suppresses. With speech disabled, the deployed completion callback and permission bridge are no-ops; Dunst retains this behavior. With speech enabled, the event bridge owns audio as described above.

The inspected contracts are documented in [Kitty's callback configuration](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.filter_notification), [versioned Kitty notification code](https://raw.githubusercontent.com/kovidgoyal/kitty/v0.49.2/kitty/notifications.py), [Dunst scripting](https://dunst-project.org/documentation/#SCRIPTING) and [Dunst 1.9.2 script delivery](https://raw.githubusercontent.com/dunst-project/dunst/v1.9.2/src/notification.c).

## Checks

```sh
python3 -B tests/test_codex_notification_sound.py
python3 -B tests/test_codex_question_notification.py
python3 -B tests/test_codex_notification_speech_setup.py
basedpyright --level error scripts/executable_codex-notification-sound scripts/executable_codex-notification-event scripts/executable_setup-codex-notification-speech
xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py
```

Unit tests cover fake completion/approval origins, channel isolation, text lookalikes, disappearing processes, absent/invalid local settings, safe filenames, one player invocation, failures and a real empty-home chezmoi install. The daemon check uses private DBus/Xvfb and a fake mpv; it verifies exact app matching, delivery timing, duplicates, history, pausing and empty-format suppression without audio or changes to your desktop daemon.

Check event eligibility without playing real audio or changing settings (no sudo):

```sh
python3 -B scripts/smoke_codex_notification_events.py --plain
python3 -B scripts/smoke_codex_notification_events.py --installed --plain
python3 -B scripts/smoke_codex_notification_events.py --installed --case worker --plain
```

The probe copies checkout handlers (or deployed `~/scripts` handlers with `--installed`) into a disposable home, feeds actual JSON events to the CLI and records calls to a silent fake mpv. Default `--case all` checks completion, worker, empty, missing, unknown, ambiguous, parent and permission events plus async, multiple, blocking, worker, empty and secret question cases. Completion records one playback; valid questions record one clip then one spoken sentence (two calls); all rejected/silent cases record zero. Each case prints progress and a PASS count; a mismatch exits 1. This validates eligibility and deployment bytes, while actual hardware listening and subsequent real Codex completion remain separate acceptance checks.

After selecting a clip, run the reusable live checks:

```sh
~/scripts/codex-notification-sound smoke tagged
~/scripts/codex-notification-sound smoke kitty
```

With speech disabled, the first should show one synthetic popup and play once. With speech enabled it displays the popup silently because synthetic Dunst events do not invoke Codex hooks. The second emits Codex-looking OSC 9 text from an unrelated process and should remain silent. It exercises Kitty origin filtering; it does not simulate real Codex. Follow the [shared completion/approval, focus and rollback smoke checks](smoke-tests.md#codex-notification-sound) for actual Codex behavior.

## Rollback

For immediate speech rollback, run `~/scripts/codex-notification-sound speech disable`. To disable all configured audio, run `~/scripts/codex-notification-sound disable`; popups continue normally. For complete removal of all shared audio (including Grok and Discord), remove the `notification_audio` rule. Keep `always_run_script=false` for remaining script rules. Remove the completion `notify` entry and the two question entries in `hooks.json`, then remove this task's Kitty callback, event bridge, sound helper, setup helper and activation helper from both the tracked and installed paths. Apply the remaining config, restart Dunst and start a fresh Kitty process. Do not reset unrelated dirty files. Your MP3 is never deleted.

## Optional source outline

During player playback, the optional source module outlines the verified Kitty window or tmux pane without changing focus. Capture occurs before worker detachment; process start times, ancestry, server and pane identity are rechecked before display. Missing support or ambiguous/stale identity leaves audio available without an outline.

The outline is present only while the player runs. Errors and handled termination restore the prior display style, and cleanup preserves concurrent tmux style edits. On X11 the click-through ring requires optional python3-xlib and SHAPE 1.1. A temporary preview from the source terminal exercises capture; a real completion or question event also checks pre-detachment provenance.

## Grok Bot speech

The Dunst rule for app name `Grok Bot` uses the same local player. It speaks the
nonblank notification body, falling back to its title, with Ryan after any
configured clip. This route is independent of the Codex speech switch; disable
or change its Dunst rule separately if needed. `smoke grok` emits a real desktop
notification and can play audio, so use it only when ready to listen.

## Speech volume

Notification speech defaults to 75% mpv software volume; intro clips keep
their existing level, and browser/system volume stays unchanged. The default was selected by listening alongside Twitch after comparing live-stream
and Ryan sample levels.
It is a fixed gain, so stream loudness and future browser volume changes can change
the balance. Set it with `codex-notification-sound speech-volume 75` (0–100);
omit the number to show the current value. The setting is saved privately and
applies to future speech across Discord, Codex and Grok. mpv uses a nonlinear
scale: 50% is about −18 dB, rather than half the signal amplitude.
Check while watching with `codex-notification-sound smoke discord-isolates`.

## Discord channel-message speech

Read desktop channel messages and Vesktop direct messages locally with Ryan as `SENDER says MESSAGE`, without
an introductory clip. Deploy the helper and Dunst rule, restart Dunst once, then
explicitly enable this independent switch (no sudo):

```sh
~/scripts/codex-notification-sound discord-speech enable
~/scripts/codex-notification-sound status --plain
~/scripts/codex-notification-sound smoke discord
~/scripts/codex-notification-sound smoke discord-unicode
~/scripts/codex-notification-sound smoke discord-isolates
~/scripts/codex-notification-sound smoke discord-dm
~/scripts/codex-notification-sound smoke discord-unrelated
```

The three synthetic probes use app `FormatProbe`: `(A) Alex (#normie, Active)` /
`hai`, `Alex (#😊normie, Another Server)` / `hello`, and `Voice: listening` /
`nerd-dictation is ready`. Expect normal popups, speech `(A) Alex says hai`,
`Alex says hello`, and silence respectively. These test the installed desktop
path; subjective listening and a real incoming Discord message are separate checks.

Matching requires the complete title `SENDER (#CHANNEL, SERVER)` plus a nonblank
body. Sender parentheses, Unicode and emoji are preserved; actual notification
markup is removed and whitespace normalized. Escaped literal markup remains text.
Discord's invisible Unicode direction isolates (U+2066–U+2069) are removed before
matching, so channel/server metadata stays out of speech. The `smoke discord-isolates`
probe uses Vesktop identity and reproduces this client format; it should speak `Alex says hello` exactly once.
Notifications containing links announce only `SENDER sends link`; X/Twitter
status links announce `SENDER sends tweet`. Link destinations in markup count,
even when their visible labels contain no URL. URL-only messages also announce
the kind. SaucyBot nonblank notifications always announce `SaucyBot sends tweet`.
No URL, tweet contents, caption or engagement counters are spoken. Ordinary text
messages still use `SENDER says MESSAGE`. Nothing is fetched from the network.
Use `smoke discord-links` and `smoke discord-link-only` to hear `Alex sends link`,
and `smoke discord-saucybot` to hear `SaucyBot sends tweet`.
The normalized sender `Twitter Cap Bot` remains excluded case-insensitively
for channels and DMs. Use `smoke discord-twitter-cap-bot` to check silence.
All these popups remain visible.
The app name is deliberately unrestricted, so another app using the same format
also speaks. Sender-only titles are accepted for exact appname `vesktop`, observed
in live Dunst history. The `smoke discord-dm` fixture uses that app with title
`Alex` and body `hello from a direct message`, speaking `Alex says hello from a
direct message`. Unidentified sender-only titles remain silent. Vesktop status
notifications with nonblank title/body may also speak; appname is routing metadata,
not authentication. Other clients require their own observed identity. Codex and Grok retain their own
routes. Message text is passed as data to Piper, never shell commands or logged.

The machine-local `discord-speech.json` beside `speech.json` is atomically written
with mode 0600 and defaults to disabled when absent or malformed. The independent
switch does not change Codex speech or the selected clip. Discord uses the existing
shared playback lock and voice, with no cloud service. Dunst pause/suppression and
its documented duplicate/history behavior still apply; messages that never reach
Dunst cannot speak. A queued message checks the switch when its callback runs.

Rollback immediately with `~/scripts/codex-notification-sound discord-speech disable`.
Popup delivery continues normally. Install the changed helper explicitly with
`chezmoi apply "$HOME/scripts/codex-notification-sound"`; run `refresh-config`
for tracked config, then `~/scripts/codex-notification-activate` for the new rule.
The restart clears Dunst history/queues; it preserves terminals and audio workers.
