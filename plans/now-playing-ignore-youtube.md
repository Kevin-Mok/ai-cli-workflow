# Isolate FlaviBot from ordinary Chrome media

## Purpose and scope
The i3 music block follows only the dedicated FlaviBot Chrome process, with Spotify
fallback. YouTube in ordinary Chrome is ignored regardless of title or playback state.
Files: media helper and tests; new flavibot-browser launcher and its test; README,
smoke checks, lesson and matching postmortem. No profile copying or playback control.

## Initial state and context
Initial git status was clean on 2026-09-20. Subsequent dirty files belong to this task.
Chrome exposes no origin URL for either FlaviBot or YouTube. Channel names appear
as artists, so title/artist heuristics cannot implement website exclusion.
Chrome profile-picker Flavibot (Profile 28) still shared PID 4159 / owner :1.50.
A distinct user-data-dir proved independent: PID 626513 / owner :1.152959.

## Decisions
- Launcher opens https://flavibot.xyz/music-player with the exact persistent
  ~/.local/share/flavibot-chrome directory. No arguments; sign in once.
- Resolve each unique D-Bus owner via GetConnectionUnixProcessID; inspect its
  /proc/PID/cmdline. Accept exactly one matching user-data-dir argument.
- Support NUL-separated arguments and Chrome's observed flattened process title.
  Reject malformed PID responses, vanished processes and ambiguous directory flags.
- Revalidate before clicks; retain original metadata for track identity.
- Remove title regex: all valid songs from this process qualify, including title-only.
- Playing tracks precede paused; dedicated FlaviBot wins ties with Spotify.
  Ordinary Chrome is never a fallback. No eligible player clears text/cache.

## Checklist
- [x] Inspect source, live metadata and initial worktree.
- [x] Verify ordinary Chrome profiles do not isolate media.
- [x] Create and test dedicated-data-directory launcher; refresh and open it.
- [x] Verify distinct media owner after user sign-in/playback.
- [x] Observe failing source-filter regressions before implementation.
- [x] Implement source filtering and retain control safety.
- [x] Update README, smoke checks, lesson and postmortem.
- [x] Run regressions, independent review, refresh and installed/rendered checks.

## Risks and rollback
This is process isolation, not website detection. Reserve the dedicated window for
FlaviBot: YouTube inside it would still qualify. Flat process titles with ambiguous
quoting or a moved data directory may fail closed to Spotify. Titles remain full;
this change deliberately does not implement truncation. No credentials were copied.
Rollback: restore the previous helper and refresh. The isolated browser directory
can remain; do not delete personal profile data as part of rollback.

## Exact verification and evidence
- python3 tests/test_flavibot_browser.py: initial RED missing script (127), then
  GREEN 1 test verifying stable directory, exact URL, and repeat-launch arguments.
- python3 tests/test_i3blocks_now_playing_mpris.py: initial source-filter RED had
  six assertions for ordinary Chrome acceptance/title-only rejection; parser test
  failed with missing is_flavibot. Final GREEN: 33 tests, exit 0. Includes playing
  ordinary YouTube versus paused dedicated FlaviBot and paused Spotify.
- bash -n scripts/executable_flavibot-browser: exit 0.
- bash tests/test_i3blocks_spotify_mpris.sh: exit 0.
- bash tests/test_desktop_display_layout.sh: exit 0.
- bash scripts/executable_readme-recruiter-sync: pass_no_change, exit 0.
- git diff --check: exit 0.
- fish -ic refresh-config: REFRESH COMPLETE, exit 0; full log inspected at
  /tmp/refresh-config-20260920-084930-638805.log. Codex snapshot already current;
  no unrelated tracked changes resulted.
- cmp source versus installed launcher/helper: identical; launcher executable.
- Installed helper emits Logic - Under Pressure / Under Pressure / #c9b1c0;
  cache selects dedicated owner :1.152959, chromium.instance626513.
- Three-second installed i3blocks capture renders music icon + Logic - Under
  Pressure, short text Under Pressure, pywal #c9b1c0, alongside volume and clock.
- Read-only independent review found no blocking issue; process-source limitation
  is documented. No live playback or queue controls were sent.

## Review and manual follow-up
The user saw YouTube while paused before the tested helper had been deployed;
source/installed mismatch confirmed this, then refresh installed the fix.
The actual live check had both browser players paused; the playing-YouTube case
is covered by the explicit automated regression. Follow docs/smoke-tests.md for
interactive transitions and button checks; these were not manually triggered.
The implementation is a launcher plus one source-identity predicate; no browser
extension, artist heuristics, credentials or persisted PID configuration is needed.

## Handoff
Manual entrypoint: ~/scripts/flavibot-browser (no sudo), sign in once, play a song.
Suggested commit: fix(i3blocks): isolate FlaviBot from ordinary Chrome media.
Keep launcher/helper, tests and all related documentation in the same commit.
Cursor prompt: Review this plan and its source-identity limitation, run the exact
checks above, then use the documented manual transitions without changing user
playback automatically. Delivery is authorized by the 2026-09-22 commit-plan-push request.

## Short usage guide
Added docs/flavibot-browser.md at the user's request: exact launch command, sign-in,
normal-Chrome YouTube separation, pause/fallback behavior, and closing/reopening.
Linked from README and smoke checks; keep it in the implementation commit.

## Delivery verification — 2026-09-22
The explicit commit-plan-push request now authorizes delivery of all dirty work.
Initial status contained exactly the ten implementation, test, and documentation
paths listed by this plan; there were no staged changes. Keep those paths in one
atomic `fix(i3blocks)` commit, followed by a separate documentation commit for
[this delivery's sandbox incident](../docs/postmortem/2026-09-22-commit-inspection-sandbox.md).
Push the completed series once to origin/feat/ai-workflow-optimization.

- [x] Review all initial dirty paths and preserve the existing implementation.
- [x] Fresh `python3 tests/test_i3blocks_now_playing_mpris.py`: 33 tests, exit 0.
- [x] Fresh `python3 tests/test_flavibot_browser.py`: 1 test, exit 0.
- [x] `bash -n scripts/executable_flavibot-browser`,
  `bash tests/test_i3blocks_spotify_mpris.sh`, and
  `bash tests/test_desktop_display_layout.sh`: all exit 0.
- [x] `./scripts/executable_readme-recruiter-sync`: pass_no_change, exit 0;
  `git diff --check`: exit 0.
- [x] `fish -ic refresh-config`: REFRESH COMPLETE, exit 0. Full log inspected at
  /tmp/refresh-config-20260922-102238-834010.log. No additional configuration
  changes appeared in Git status. Both installed scripts match source via cmp.

The media test's cache-write diagnostic is an intentionally exercised failure
path. Interactive playback transitions and controls were not repeated during
this delivery; the existing smoke checks remain the manual verification path.
The original RED evidence above belongs to implementation; this delivery ran
fresh GREEN/regression checks without altering production code. Rollback remains
a revert of the atomic fix followed by refresh-config, preserving profile data.

Independent delivery review found no blocking correctness, security, or documentation
issue. Its stale authorization-note finding is corrected above.
