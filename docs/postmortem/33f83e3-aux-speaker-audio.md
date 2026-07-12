# Postmortem: AUX Speaker Audio Outage

**Incident date:** 2026-07-12  
**Repository fix:** [`33f83e3`](https://github.com/example-user/ai-cli-dotfiles/commit/33f83e3)  
**Severity:** Low — local workstation playback only  
**Status:** Resolved

## Summary

Spotify and Chromium were playing audio streams, but no sound came from the
AUX speakers. PipeWire, PipeWire PulseAudio, and WirePlumber were all running.
The active analog output was the correct AUX sink, but it was muted.

## Impact

Playback was silent through the workstation's AUX speakers while applications
continued to report active streams. The microphone and unrelated audio inputs
were unaffected.

## Detection and evidence

The initial `wpctl status` output showed:

- PipeWire, `pipewire-pulse`, and WirePlumber: active
- Default sink: `alsa_output.pci-0000_30_00.6.analog-stereo`
- Analog sink: `Family 17h/19h HD Audio Controller Analog Stereo [vol: 0.58 MUTED]`
- Spotify and Chromium: active playback streams routed to `ALC897 Analog`

This ruled out a missing service, missing device, or application-level pause.

## Root cause

The default analog sink used by the AUX speakers had its mute state enabled.
The existing audio helper could switch sinks, but there was no focused recovery
command to inspect the complete state, clear the mute flag, and re-route active
streams in one operation.

## Resolution

Commit `33f83e3` added
[`scripts/executable_fix-aux-speaker-audio`](../../scripts/executable_fix-aux-speaker-audio),
which:

1. Reports service, default-device, and PipeWire output state with `--diagnose`.
2. Reads the default sink through the PipeWire PulseAudio compatibility API.
3. Clears the sink mute state with `pactl set-sink-mute @DEFAULT_SINK@ 0`.
4. Moves every active sink input to the selected sink.
5. Supports an explicit sink with `--sink` and an opt-in service restart with
   `--restart`.

The live repair was run with `--fix`. Afterward, `wpctl status` showed the
analog sink at 58% without `MUTED`, and Spotify and Chromium remained active on
the analog playback paths.

## Verification

The following checks passed:

- `bash tests/test_fix_aux_speaker_audio.sh`
- `bash -n scripts/executable_fix-aux-speaker-audio`
- `fish -n dot_config/fish/functions/gen-pass.fish`
- `git diff --check`
- `./scripts/executable_readme-recruiter-sync`
- Live `wpctl status` after the repair

The regression test uses a fake `pactl` server and verifies both unmuting and
moving an active playback stream.

## Prevention and follow-up

- Keep `--diagnose` read-only so future incidents can gather evidence safely.
- Use the shared audio smoke test in [`docs/smoke-tests.md`](../smoke-tests.md)
  after changes to the desktop audio workflow.
- Use `--restart` only when service health evidence indicates a restart is
  warranted; the common mute-state failure does not require one.
- Consider adding a desktop keybinding later if this recovery becomes frequent.

## Lessons learned

Active application streams and healthy audio services do not prove that sound
can reach a physical output. The sink mute flag must be checked explicitly
before escalating to service restarts, driver changes, or package changes.
