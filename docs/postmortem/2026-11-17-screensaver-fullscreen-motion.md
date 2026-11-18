# Fullscreen YouTube interrupted by screensaver

The idle service started the media conveyor while fullscreen YouTube was
reported on the desktop. The journal shows 296 seconds of screen quiet at
19:51:24 and activation at 19:51:28 after 426 seconds of physical input idle.
This confirms automatic idle activation. No incident-time frames were retained.

The motion detector reduced the masked 4K frame to 160×90 grayscale and
required at least eight cells to change by eight levels. This can classify
real visible changes as quiet. The next step is to reproduce that false quiet
result and verify a native-resolution color comparison.

Postmortem-memory lookup used “screensaver fullscreen YouTube idle pointer
i3 bar”. The scheduled-visibility finding concerns scheduled playback and
does not apply to this idle launch. The service journal and local detector
source provide the diagnostic evidence.

## Resolution and verification

The 4K regression changed one non-bar pixel between two almost-equally bright
colors. The old sampler allowed activation at 300 seconds. Comparing masked
native-resolution RGB frames made the same regression pass. The subscription
to physical input remains separate. This confirms a false-quiet mechanism,
while the exact incident-time frame sequence remains unknown.

The initial sandboxed checks could not reach X11 or the user systemd bus, and
the suite could not write its runtime lock. Scoped desktop access allowed the
same checks to run. All 70 Python screensaver tests passed on a disposable
4K Xvfb display, including real X11 capture and i3bar masking. Browser
geometry checks passed. The live service was restarted with only the installed
detector replaced after a baseline comparison. Source and installed files
matched. Live status saw DP-2 as the middle monitor and reported the quiet
gate suppressing activation. An unattended five-minute fullscreen YouTube
session is still a manual acceptance check.
