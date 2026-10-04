# FlaviBot music window

Use a dedicated FlaviBot window so the desktop music block follows its songs
while ignoring YouTube in your normal browser. Open the launcher, sign in
and play music, then reuse the same launcher whenever you return.

Open it from a terminal:

```sh
~/scripts/flavibot-browser
```

Sign in if prompted, then play music. Use this command whenever you reopen
FlaviBot—it remembers your separate browser session. No sudo needed.

Keep this window for FlaviBot only. Watch YouTube in your normal Chrome window.
The Flavibot profile in Chrome's profile picker is **not** this separate window.

The music block updates within five seconds:

- Playing: prefixes the selected track with a small, raised `▶`, centered like
  the paused marker.
- Paused: prefixes the selected track with a small, optically raised `‖` so it
  sits centered with breathing room; paused FlaviBot keeps its song unless
  Spotify is playing.
- No song loaded: FlaviBot’s generic “FlaviBot - Music Player” metadata is
  hidden, so Spotify is shown if available and the block clears otherwise.
- FlaviBot closed: uses Spotify, or clears if Spotify is unavailable.
- YouTube in normal Chrome: never appears.

Close the FlaviBot window normally when finished. Reopen it with the same command.
