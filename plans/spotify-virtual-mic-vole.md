# Spotify through the Vole Chrome microphone

Reuse the live Spotify cable, identify the Vole Discord input, and verify that it receives Firefox Spotify while desktop playback stays on analog.

## Scope and decisions

The [handoff](../docs/handoffs/2026-11-25-spotify-virtual-mic.md) and the original runbook in `~/coding/virtual-mic/plans/spotify-discord-cable.md` describe the session-local cable and the direct monitor fallback. Use Vole Chrome Profile 7, the most recently used Vole profile and the one with Discord microphone permission. Keep Spotify in Firefox, where PipeWire can isolate its playback. Preserve existing Git work, audio defaults, and other streams.

## Checklist

- [x] Read the source handoff and runbook. Identify Vole and capture the live PipeWire baseline.
- [x] Resume the identified Spotify stream and compare the cable and current Chrome capture.
- [x] Check the need for the direct monitor fallback. The current Chrome capture receives the named source, so leave its route in place.
- [x] Verify the routed playback and capture, signal and pause behavior, and the system defaults. Record any remaining call checks.

## Verification and rollback

Compare `pactl get-default-sink` and `pactl get-default-source` before and after. Inspect `pactl list short sinks`, `sources`, `sink-inputs`, and `source-outputs` to match stream device indices. Probe the selected source while Spotify is playing and paused. Verify delivery with Discord's Mic Test or a listener when available.

For rollback, pause Spotify and move only the changed Discord stream back to its original source or select the desired physical microphone in Discord. The existing cable is session-local. See the original runbook to remove it by its current module IDs.

## Progress

- Baseline on `ubuntu-h7`: analog default output, Blue Snowball default input, Spotify Cable present, Firefox Spotify on the cable and paused. Chrome capture is on the named remap, with Chrome and Vesktop playback on analog.
- Controlled pause and play: both virtual sources measured a peak of 0 while paused and 10180 while playing. `pw-link -l` showed both mapped channels flowing from Firefox through the named input into Chrome. Discord showed the Vole account voice-connected with its microphone unmuted.
- Firefox paused during the first two continuity probes. Starting from Spotify's own Play button, the next probe exited 0 with signal in all 60 one-second samples (minimum peak 7150) and confirmed the routes at 1, 15, 30, 45, and 60 seconds. Spotify still reported Playing at the end. See the [continuity incident](../docs/postmortem/2026-11-25-vole-spotify-continuity-check.md).
- The live call was left connected and unmuted. This run verified the desktop audio path to Chrome's capture and the Discord call state. Receiver-side listening and a new leave/rejoin were not exercised.

## Delivery milestone

- `docs(audio): document Vole Spotify microphone routing` records the handoff, smoke check, and continuity incident with its reviewed ledger entry. The scope follows the observed session edits and the original handoff they extend. Publish the scoped changes on the upstream tip because local `main` already contains unrelated commits and has diverged.
