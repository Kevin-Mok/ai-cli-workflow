# Persist the Spotify virtual microphone

Restore the named input for Discord Web and recreate it automatically whenever
the user's PipeWire Pulse server starts. Spotify runs in Firefox so Chrome's
Discord playback remains on the regular speakers.

## Scope and decisions

The original experiment is in the [Vole handoff](../docs/handoffs/2026-11-25-spotify-virtual-mic.md).
Reuse its node names and stereo 48 kHz configuration in a managed PipeWire
drop-in. Apply only the audio target if a full refresh would include unrelated
changes. Keep the desktop audio service running during installation. Spotify
stream assignment and Discord's microphone selection remain per-app settings.

## Checklist

- [x] Capture the dirty checkout and inspect historical and current audio routes.
- [x] Restore the missing live source and verify the existing default devices.
- [x] Reproduce missing devices in a fresh isolated PipeWire server.
- [x] Add the drop-in and verify clean starts and an isolated Pulse restart.
- [x] Install the drop-in and update README, handoff, and manual smoke instructions.

## Verification and rollback

Run `dbus-run-session -- bash tests/test_spotify_virtual_mic.sh` with permission to start local Unix
listeners. Confirm the installed file equals the source and inspect live device
descriptions and default routes. In Chrome Discord Web, select Spotify Virtual
Mic, route only Firefox Spotify to Spotify Cable, then use Mic Test during play,
pause, and unrelated Chrome audio. Repeat after a desktop restart.

To roll back, select the physical microphone in Discord and restore Firefox's
regular output, then remove the drop-in from both source and home and restart
the audio service when free to interrupt audio.

## Progress and review

The original modules were absent from the current PipeWire graph. Scoped
desktop access reproduced the missing source and recreated module IDs 536870913
and 536870914. The default source stayed Blue Snowball and the sink stayed
analog. Browser selection and receiver audio are separate manual checks.

- RED: The isolated test without the drop-in exited 1 at the missing-sink assertion.
- GREEN: `dbus-run-session -- bash tests/test_spotify_virtual_mic.sh` exited 0 and found the exact sink and source names on two private Pulse starts.
- Deployment: `chezmoi -S "$PWD" apply --include=dirs,files -- ~/.config/pipewire` exited 0, `cmp` verified the installed file, and `pw-config -n pipewire-pulse.conf paths` found the override. Used scoped apply because a full refresh showed unrelated pending targets. The current audio service was left running.
- Live check: Pulse listed the cable, monitor, and named mic. The saved WirePlumber Firefox output target is `spotify_cable`. A full desktop reboot, Discord Web device selection, and receiver-side Spotify playback were not exercised this turn.

Cursor handoff: “Keep the existing Spotify cable and microphone names stable. Verify both on isolated Pulse starts, then use the Discord Web restart and reconnect smoke checks to confirm Spotify playback and silence when paused.”

Suggested commit subject: `fix(audio): restore Spotify virtual mic at startup`

## Delivery milestone

The `fix(audio): restore Spotify virtual mic at startup` commit is scoped to
this plan, the PipeWire drop-in, the restart test, the setup and smoke docs,
and the desktop-access incident and its ledger entry. The session scope helper
could not attribute the tool writes, so the candidate was reconstructed from
observed edits and reviewed against the upstream tip in a separate checkout.
The original checkout contains divergent commits and mixed local edits. Publish
only the scoped commit to `origin/main`; leave the original checkout in place.
The remaining functional check is a Discord Web Mic Test after a real restart.
