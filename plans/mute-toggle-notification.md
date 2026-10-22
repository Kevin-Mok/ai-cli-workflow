# Mute toggle notification

Add one desktop popup that updates in place when Super+M or the audio mute key toggles speaker mute. Preserve the existing PulseAudio mixer and i3blocks refresh.

## Scope and decisions

Use a shared `scripts/executable_audio-mute` helper from both i3 bindings. Read the applied state from amixer's toggle output; Dunst's existing stack-tag mechanism replaces the popup, independently of Redshift. Notification failure must not undo successful audio changes. No volume adjustment changes or new dependencies. Follow-up commit-session authorizes one scoped commit and upstream push.

## Checklist

- [x] Capture initial `git status --short`; preserve all existing dirty files/hunks, especially README and smoke tests.
- [x] Inspect bindings, Redshift helper/tests, feedback and lessons.
- [x] Write executable behavior tests; observe missing-helper RED.
- [x] Implement helper and update bindings, README, smoke checks.
- [x] Verify tests; attempt refresh-config, deploy only requested live bindings/helper, validate and reload i3. Full refresh remains blocked by an unrelated conflict.
- [x] Exercise two live Super+M toggles and popup replacement, restoring initial mute state.

## Risks and rollback

Live i3 config is migration-preserved and contains private settings; change only the two mute bindings. Preserve unrelated tracked and live content. Revert these bindings and remove the new helper to roll back. Audio probes must restore starting mute state. Dunst stack tags are daemon-specific, matching this desktop's existing Redshift behavior.

## Verification

Automated: `python3 -B tests/test_audio_mute.py` and `python3 -B tests/test_redshift_control.py`. Tests invoke real helper with fake external mixer/notifier commands; cover on/off notifications, replacement tag, failed audio and failed notification. Manual: run installed audio-mute twice and synthesize Super+M twice; inspect Dunst history/state and audio state. Run `fish -c refresh-config`, `i3 -C -c ~/.config/i3/config`, then `i3-msg reload` before live shortcut probes.

## Progress and review

Initial worktree has extensive unrelated dirty work; unrelated existing changes will not be staged or committed. Implementation and scoped activation complete. RED: 4 tests/6 assertions failed because helper was absent (exit 1). GREEN: audio helper 4 tests, Redshift 6 tests, volume block 1 test, all exit 0. Targeted diff whitespace check passed.

`fish -c refresh-config` exited 1 because unrelated live `scripts/tmux-scrollback-smoke` differed and noninteractive chezmoi could not answer its overwrite prompt. Preserved it; see `docs/postmortem/2026-10-22-mute-notification-refresh.md`. Installed the authorized helper and merged only the two live i3 mute lines with approved host access. i3 validation exited 0, reload returned success true.

`python3 /tmp/verify-mute-notification.py` exited 0: synthetic Super_L+m changed Mute: no -> yes -> no, displayed notification counts stayed equal and positive, and after expiry exactly one new Audio history entry contained Unmuted. Finally restored original mute state. This confirms live replacement without reading unrelated notification content. Physical keypress, subjective listening, and entire repo suite not checked; media key uses the same verified helper.

## Handoff

Atomic change: helper plus both bindings, regression test, README/smoke updates, this plan and incident record. Session-only delivery authorized; see the milestone below. Commit subject: `feat(i3): show mute notifications in place`.

Cursor prompt: "Review plans/mute-toggle-notification.md and the audio-mute helper; preserve unrelated dirty work. Re-run the three focused Python test files listed here, then verify two Super+M presses update one Audio popup and restore initial mute state. Do not overwrite the unrelated tmux refresh conflict."

Automated checks: `python3 -B tests/test_audio_mute.py`; `python3 -B tests/test_redshift_control.py`; `python3 -B tests/test_i3blocks_volume.py`. Manual checks are recorded in docs/smoke-tests.md under Audio. Remaining risk: full refresh remains blocked by unrelated user work, while scoped live activation is verified.


## Delivery milestone — feat(i3): show mute notifications in place

Ready to commit the verified helper, both bindings, tests, README/smoke updates and incident records together. Fresh checks: audio-mute 4 tests, Redshift 6 tests, volume block 1 test; all exit 0. README gate: pass_no_change. Scope helper could not detect writes for session 01a16472-14a9-7c12-a6df-6cbdc9722015, so use conversation-observed writes and the captured initial status. README/smoke current diffs contain only this session's changes. Stage only the two new report entries from the mixed ledger; leave all other dirty changes and :memory:.ses untouched. Privacy check and exact staged diff are mandatory before commit. Push destination: origin/main. Remaining limitation: unrelated full-refresh conflict; scoped live mute feature verified. Next step after local commit: push the verified commit.
