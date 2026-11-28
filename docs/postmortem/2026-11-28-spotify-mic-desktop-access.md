# Spotify microphone desktop audio access

The restricted shell's baseline `pactl` calls reported “Connection refused”
and “Operation not permitted.” The session socket was present, but the probe
could not determine whether the named microphone existed.

The lookup for PipeWire, `pactl`, and socket permission errors used the earlier
[desktop-audio incident](/home/kevin/coding/virtual-mic/docs/postmortem/2026-11-25-desktop-audio-access.md)
and the reviewed scoped-socket workaround `ext-sandbox-loopback`. The scoped
host probe exited 0 on PipeWire 1.0.5 and showed that both Spotify devices were
absent. An authorized load of the original modules restored the devices and
preserved the default analog output and Blue Snowball input.

The scope is desktop audio access. This repeats the prior sandbox behavior and
adds no new remedy. The persistent configuration is tracked separately in the
[implementation plan](../../plans/spotify-virtual-mic-persistence.md).

A separate deployment check exposed a missing parent directory on first
install. Chezmoi's dry-run could display the file-only target, but applying it
exited 1 when the parent was absent. The paths-and-ownership guidance to include
missing parents applies. A preview scoped to the managed PipeWire directory
showed only its two parent directories and the intended drop-in.
The scoped directory apply then exited 0, the installed file matched its source,
and `pw-config` reported the installed path. The active audio service was left
running.
