# AUX Speaker Audio Repair Implementation Plan

**Goal:** Add a safe Bash utility that diagnoses PipeWire/PulseAudio playback and restores application audio to the active AUX speaker sink.

## Atomic plan

- [x] Capture the current audio evidence and preserve unrelated working-tree changes.
- [x] Add a failing shell regression test using a fake `pactl` executable.
- [x] Add the minimal repair script: diagnose, unmute the default sink, and move active playback streams to it.
- [x] Run the regression test, shell syntax validation, and the real repair command; then verify the live sink is unmuted.

## Design

`scripts/executable_fix-aux-speaker-audio` will use the PulseAudio compatibility API provided by PipeWire. `--diagnose` is read-only. `--fix` identifies the default sink, unmutes it, and moves every active sink input to that sink. `--restart` is opt-in and restarts only the three user-scoped audio services before applying the same repair.

## Review

- Verified July 12, 2026: the default analog AUX sink was unmuted and active Spotify/Chromium streams were routed to it.
