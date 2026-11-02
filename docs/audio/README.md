# Dual-jack audio recovery

The desktop plays the same stereo sound through front/top headphones and rear green-jack speakers. Run `~/scripts/set-dual-jack-audio` to restore the mixer switches; `ubs` and i3 startup run it automatically. The helper preserves volume and requires `alsa-utils` but no sudo.

## Saved boot mapping

`alc897-dual-jack.fw` is the working HDA retask firmware snapshot for codec `0x10ec0897`, subsystem `0x14629c95`. It was already installed at `/lib/firmware/hda-jack-retask.fw`; `/etc/modprobe.d/hda-jack-retask.conf` already loads it with:

```text
options snd-hda-intel patch=hda-jack-retask.fw,hda-jack-retask.fw,hda-jack-retask.fw,hda-jack-retask.fw
```

Pins `0x1b` (front/top) and `0x14` (rear green) share output association 1. The mixer names are `Front` and `Surround`, respectively; `Surround` here carries the same stereo stream, not separate surround content. The helper discovers the card number instead of assuming card 3, unmutes Master/Front/Surround, and does not alter pin assignments or PipeWire routing.

This snapshot is recovery evidence, not an automatic system installer. Reinstalling boot firmware on this exact motherboard needs administrator access and a reboot; do not apply it to other hardware. No system firmware or module configuration was changed in this task.

## Verification and rollback

Run the helper, then use `paplay` with the system front-left and front-right samples and listen to both devices. Repeat after a fresh i3 login. Both speakers must be powered and the rear cable must use the green output jack. Actual listening establishes audible output; an unmuted mixer alone does not.

To stop automatic unmuting, remove the `set-dual-jack-audio` call from tracked `scripts/executable_ubuntu-start` and apply that script. This leaves the existing boot mapping and volume untouched. Existing `fix-aux-speaker-audio` remains available for separate PipeWire sink-mute/routing problems.
