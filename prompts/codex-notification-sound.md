# Verify Codex notification sound

Continue verification of the implemented optional Codex sound hook. Read the linked plan, run the automated checks, then use a user-selected clip to verify completion, approval and focus behavior. Preserve unrelated work and do not commit or push unless requested.

```prompt
In /home/example/linux-config, follow dot_codex/AGENTS.md and read
plans/codex-notification-sound.md and docs/codex-notification-sound.md.
The Kitty callback tags local foreground Codex popups as codex-kitty;
Dunst invokes scripts/codex-notification-sound. Sound is disabled until
configured. Preserve OSC 9, original content/timing/click focus and
native duplicate stacking; do not add completion-only notify or text matching.
Run python3 -B tests/test_codex_notification_sound.py and
xvfb-run -a dbus-run-session -- python3 -B tests/scripts/codex_notification_daemon_check.py.
Check deployed bytes and use docs/smoke-tests.md#codex-notification-sound
for real completion, approval, focused suppression, unrelated origin and audio.
Use ~/scripts/codex-notification-activate --open-kitty after applying changes.
Dunst needs restart; Kitty needs a fresh process. Preserve pre-existing
Codex model/source differences before refresh-config. The selected clip is
stored as scripts/can-i-ask-you-a-question.mp3 with a Git LFS attribute.
Keep only the machine-local sound-path JSON out of Git. Update plan/docs with observed results and limits.
Do not commit or push without authorization.
```

Suggested eventual Conventional Commit: `feat(notifications): add optional Codex popup sound`.
