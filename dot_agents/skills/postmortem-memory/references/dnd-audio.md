# DND and automatic audio

Use the existing desktop pause state for direct event audio as well as daemon-triggered notification playback.

## local-dnd-direct-event-audio

- **status**: verified_fix
- **symptoms**: ['i3blocks DND pauses notifications but direct Codex TTS still plays.']
- **applicability**: Shared notification players invoked both by Dunst and direct Codex event hooks.
- **diagnostics**: ['Trace the block to dunstctl set-paused, then trace event-play directly to the shared player without a pause check.']
- **confidence**: confirmed
- **remedy**: Query Dunst pause with a bounded timeout before automatic audio, after the playback lock and before each stage. Explicit previews bypass DND; unavailable Dunst retains previous audio behavior.
- **verification**: Expected RED3; GREEN DND6, sound89, question12 and private Dunst1; typecheck0. Installed live Dunst pause/resume probe with silent player passed; source/live bytes equal and original pause restored.
- **verification_scope**: runtime
- **limitations**: Already playing audio may finish; natural incoming event and listening remain manual. Full refresh stopped on unrelated Kitty drift; targeted helper apply succeeded.
- **Report**: [DND TTS](../../../../docs/postmortem/2026-10-22-dnd-tts.md)
