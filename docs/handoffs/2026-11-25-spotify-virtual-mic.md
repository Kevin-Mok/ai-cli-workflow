# Spotify virtual microphone handoff

Use Firefox to send Spotify into the Vole account's microphone in Chrome Discord. Check the live Firefox and Chrome routes before changing devices, then test Spotify playback and pause in the call.

## Use the route on Vole

1. Play Spotify in Firefox. In PulseAudio Volume Control, the active Firefox Spotify stream should play to **Spotify Cable**. Keep Chrome playback on the ordinary output so call audio cannot loop back into the call.
2. In the Vole account in Chrome Discord, select **Spotify Virtual Mic** in **User Settings → Voice & Video**. After joining, check that the mic is unmuted. Use Voice Activity with noise suppression, echo cancellation, and automatic gain control off if music gets cut or distorted.
3. Check the current routing with `pactl list short sinks`, `pactl list short sink-inputs`, `pactl list short sources`, and `pactl list short source-outputs`. IDs change between sessions. If Chrome shows the virtual mic but is silent after reconnect, compare recording streams before and after rejoining to identify the new Discord capture. In PulseAudio Volume Control under **Recording**, move only that capture to **Monitor of Spotify Cable**.
4. Pause Firefox Spotify to stop feeding music. To return to the physical microphone, select the **Blue Snowball** or **System Default** in Discord and rejoin if the capture still uses the virtual input.

## Install and persist the devices

Chezmoi installs the [PipeWire Pulse drop-in](../../dot_config/pipewire/pipewire-pulse.conf.d/50-spotify-virtual-mic.conf)
under `~/.config/pipewire/pipewire-pulse.conf.d/`. From the linux-config checkout,
apply the managed PipeWire directory with the command below. Sudo is unnecessary.

chezmoi -S "$PWD" apply --include=dirs,files -- ~/.config/pipewire

PipeWire Pulse reads the file at startup. The next login or restart recreates
both devices automatically. To activate immediately on a fresh install, restart
the user `pipewire-pulse.service` when audio can be interrupted. Reload Discord
Web if its microphone list still shows the old devices. WirePlumber can restore
Firefox's previous output assignment. If Firefox plays on the regular output,
move its Spotify stream back to **Spotify Cable** in PulseAudio Volume Control.

To remove the setup, select your physical microphone in Discord and move
Firefox back to the regular output. Remove the drop-in from both chezmoi source
and home, then restart `pipewire-pulse.service` when audio can be interrupted.

## Vole Chrome verification

The active Vole Discord account was connected and unmuted. The named virtual mic carried Spotify in all 60 one-second samples and was silent when Spotify paused. Chrome playback stayed on analog output, and the system default input remained the Blue Snowball. Spotify was left playing. See the [migration plan](../../plans/spotify-virtual-mic-vole.md) for the current checks and the [continuity incident](../postmortem/2026-11-25-vole-spotify-continuity-check.md) for the interruptions observed in Firefox.

## Source workspace

`/home/kevin/coding/virtual-mic` contains the original work and its evidence.

- [Original request](/home/kevin/coding/virtual-mic/prompt.md)
- [Setup, verification, reconnect, and rollback](/home/kevin/coding/virtual-mic/plans/spotify-discord-cable.md)
- [Desktop and iPad smoke checks](/home/kevin/coding/virtual-mic/docs/smoke-tests.md)
- [Monitor fallback incident](/home/kevin/coding/virtual-mic/docs/postmortem/2026-11-25-spotify-mic-silent-with-chrome-playback.md)
- [Intermittent static investigation](/home/kevin/coding/virtual-mic/docs/postmortem/2026-11-25-spotify-discord-intermittent-static.md)

## Original handoff evidence

Firefox Spotify played into a temporary PipeWire cable. The Discord alt in Chrome recorded directly from the cable monitor after the named remap source went silent on reconnect. Chrome playback and the system defaults stayed on their original devices. The desktop probe measured signal in all 60 one-second samples. The iPad listener confirmed music and voice.

Discord's Automatic Gain Control was switched off after a report of intermittent static. The listener later said the audio sounded clearer and thought it sounded good. A controlled gain-toggle or tab-share comparison remains open. The final live setup in this record was session-local.

## Resume

1. Read the [runbook](/home/kevin/coding/virtual-mic/plans/spotify-discord-cable.md) and inspect the current audio routes before changing them. Stream and module IDs can change.
2. If the alt is silent after reconnecting, identify its new recording stream and use the documented monitor fallback. If static returns, check the [smoke checks](/home/kevin/coding/virtual-mic/docs/smoke-tests.md) and verify on the iPad before making broader audio changes.
3. Follow the [restart smoke check](../smoke-tests.md#spotify-through-the-vole-chrome-microphone) after a reboot to confirm the devices return and the Discord Web input still receives Spotify.

Git was initialized locally in the source workspace before the task changed to this handoff. The source repository has an unborn `main` branch and no remote. Its source documents live in that local workspace.

## Suggested skills

- `postmortem-memory` for renewed static or a silent mic after reconnecting.
- `superpowers:systematic-debugging` for isolating the audio fault with a live reproducer.
- `superpowers:verification-before-completion` before claiming a repair or a persistent setup works.
