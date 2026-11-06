# Three notification modes

Add full notifications, visuals only, and DND to the existing i3blocks indicator.
Keep left/right click behavior and use middle-click for visuals only. Test the
block and shared player, update usage, then apply the reviewed configuration.

## Scope and decisions

- Block: `dot_config/i3blocks/scripts/executable_dnd`; audio gate:
  `scripts/executable_codex-notification-sound`.
- A local `codex-notification-sound/audio-muted` marker under XDG config persists
  the visuals-only setting. Clip, voice and volume settings remain intact.
- Left clears the marker before resuming Dunst; middle creates it before
  resuming; right pauses Dunst. DND wins over the marker in the display.
- Existing playback gates also check the marker, including queued/staged audio.
  Explicit previews still work. Already playing audio may finish.
- Initial git status captured: README, smoke tests, task status, feedback,
  postmortem references, fish progress, Vesktop, privacy approvals, lessons,
  and Firstmate files already dirty. Preserve all unrelated changes; no commit
  or push requested. Live block and player contents match source despite newer
  deployment timestamps.

## Checklist

- [x] Inspect block, callers, audio gate, tests and live copies.
- [x] RED: test middle-click, left-click restore, persistent rendering, and
  automatic clip/speech suppression while Dunst is unpaused.
- [x] GREEN: implement marker and shared playback gate; run related regressions.
- [x] Update README, notification usage and grouped smoke checks.
- [x] Run refresh-config and verify installed copies and live state restoration.

## Verification and review

Automated: `python3 -B -m unittest discover -s tests -p 'test_*dnd.py'` and
`python3 -B -m unittest discover -s tests -p 'test_codex_notification*.py'`.
Manual: left/middle/right click should render Notis/Silent/DND; synthetic
Codex/Grok/Discord notifications should display and sound according to the mode.
Verify queued audio and explicit-preview exceptions with isolated player fixtures.
Do not restart Dunst or clear its queue. Restore the starting pause/mute state
after live probes. Rollback: restore the two scripts and remove the local marker
if returning to the old player. Desktop sound/visual acceptance remains manual
unless directly observed. No new dependency or audio configuration migration.

Cursor continuation prompt: Read this plan, preserve unrelated dirty work, finish
unchecked items, run the two exact unittest commands, refresh configuration and
record observed results. Suggested commit: `feat(i3blocks): add silent notification mode`.

## Observed evidence

- RED: DND discovery ran 17 tests, 5 expected failures for missing middle-click,
  marker clearing and automatic audio suppression.
- GREEN: DND discovery 17/17; notification discovery 113/113; both exit 0.
  Warning-path fixtures emitted their expected diagnostics.
- `bash -n dot_config/i3blocks/scripts/executable_dnd` and `git diff --check`:
  exit 0. Reviewed implementation diff: marker affects every existing DND
  checkpoint and leaves explicit preview bypass unchanged.
- `fish --no-config -c 'source dot_config/fish/functions/cli-message.fish;
  source dot_config/fish/functions/refresh-config.fish; refresh-config'`:
  approved deployment exit 0, REFRESH COMPLETE. Private log:
  `/tmp/refresh-config.R7vPFrpM.log`.
- Installed block and player byte-match source. Live block invocations with
  BLOCK_BUTTON=3/2/1 rendered DND (1), Silent, Notis, with correct real Dunst
  pause state and local mute marker. Original paused=false/mute-absent state
  restored in a finally block.
- Full repository suite, physical clicks and desktop listening/visual acceptance
  were not run; 130 focused tests cover related playback and event contracts.
  No Dunst restart, commit or push. Shell startup sandbox incident is recorded
  in `docs/postmortem/2026-11-06-notification-fish-inspection-sandbox.md`.

Manual follow-up: click left/middle/right and send a normal notification in each
mode; expect configured sound+popup / popup only / neither (Dunst queues popups).
Explicit previews remain audible in any mode. Already playing audio can finish.

## Delivery milestone: feat(i3blocks): add silent notification mode

Session commit requested on 2026-11-06. Scope helper returned unsafe/no detected
writes for session `01a1b297-126a-7831-b4af-ef5dd2b2c211`; direct conversation write
evidence establishes the two scripts, two test files, notification usage, this
plan, notification Fish incident, and only the notification-specific README,
smoke-test and ledger hunks. Other dirty work stays excluded. No prerequisite
outside this set is required; the existing DND checkpoints and configured Dunst
callback already exist in HEAD.

Fresh commit-turn verification: 17 DND tests and 113 notification tests passed,
exit 0; README gate returned pass_no_change. Earlier live verification and refresh
remain as recorded above. Stage via an isolated index, inspect its exact diff,
run the privacy gate immediately before committing, then push main to origin/main.
Completed: implementation, docs, configuration application, focused checks.
Remaining at milestone: commit and one upstream push; no known blocker.
Physical click/listening acceptance remains manual. Rollback restores the two
scripts and removes the local audio-muted marker; no saved audio preference is lost.

Exact isolated candidate (HEAD plus the 10 scoped file/hunk changes) was exported
under `/tmp/notification-commit-rjoa7klg/tree`: the same 17 DND tests and 113
notification tests passed, and README gate returned pass_no_change, combined
exit 0. Targeted postmortem check also exited 0 with no errors/stale hashes.
