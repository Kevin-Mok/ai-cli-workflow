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

## Empty FlaviBot state follow-up — 2026-09-24

- [x] Reproduce generic `FlaviBot - Music Player` metadata appearing as a song,
  both as one title and as artist `FlaviBot` plus title `Music Player`; focused
  regression tests failed against the old selection logic.
- [x] Exclude those exact generic metadata values from the dedicated FlaviBot
  source while retaining
  real paused tracks, title-only tracks, and Spotify fallback.
- [x] Update the user guide and manual smoke check for the empty-player state.
- [x] Run focused and adjacent now-playing regressions; refresh the tracked
  configuration and inspect the installed helper.

Evidence: the generic-title tests failed before the fix, showing page metadata
instead of Spotify and leaving the placeholder visible when Spotify was absent.
The screenshot-shaped metadata regression also failed before its matching filter
was added. The fresh
`python3 -B -m unittest tests.test_i3blocks_now_playing_mpris -v` run passed all
36 tests. `bash tests/test_i3blocks_spotify_mpris.sh`,
`bash tests/test_desktop_display_layout.sh`, Python AST syntax validation, and
`git diff --check` all exited 0. `fish -ic 'snapshot-codex-config --dry-run'`
passed; `fish -ic 'refresh-config'` printed `REFRESH COMPLETE` and exited 0; its
full log showed no conflicts. `cmp` confirmed the installed helper matches the
tracked source. Running the installed helper produced the current live Spotify
song, title, and pywal color on three lines. No manual FlaviBot metadata fixture
was available in the live player, so placeholder behavior is verified by the
three automated cases. Rollback is to remove the exact-placeholder predicate and
its regression cases; no profile data changed.

Review note: the filter is scoped to Chrome/Chromium (the isolated FlaviBot
source); Spotify titles are unaffected. Exact match preserves legitimate
title-only and paused songs. No i3 restart is needed because the block polls every
five seconds. The final refresh log at
`/tmp/refresh-config-20260924-110307-1293793.log` reported no conflicts. No
unrelated tracked files appeared after refresh.

## Spotify artist visibility follow-up — 2026-09-24

- [x] Capture the live helper output and active i3blocks stream to confirm why
  the artist was missing: full_text contained `Ariana Grande - twilight zone`,
  while short_text contained only `twilight zone`.
- [x] Add a regression requiring Spotify's short_text to retain its artist and
  make both text fields use the same artist-title label.
- [x] Run now-playing and adjacent regressions, refresh configuration, and
  compare the installed helper and live i3blocks output.

The short-text-only regression failed before implementation because it observed
`Janice STFU` where the bar-visible label must include `Drake`. This changes no
player selection or click routing. Rollback restores title-only short_text and
the previous expectation; the artist remains present in full_text.

Verification: the fresh `python3 -B -m unittest
tests.test_i3blocks_now_playing_mpris -v` run passed all 37 tests. Spotify and
desktop layout shell regressions and Python AST syntax validation exited 0.
`fish -ic 'snapshot-codex-config --dry-run'` passed; the final
`fish -ic 'refresh-config'` emitted `REFRESH COMPLETE`, exit 0, with no conflicts
in `/tmp/refresh-config-20260924-111055-1306171.log`. Installed helper matches
the tracked source. Its live output contains `Ariana Grande - twilight zone` in
both text lines; a fresh live i3blocks status line also contains that label in
both `full_text` and `short_text`. `git diff --check` exited 0.

## Playback-state glyph follow-up — 2026-09-24

- [x] Add RED regressions for playing and paused labels using the approved
  `♫` and `‖` glyphs.
- [x] Prefix both full and short text with the playback-state glyph and leave
  the no-player output blank.
- [x] Document the state indicators in the FlaviBot guide and manual smoke test.
- [x] Run the now-playing and adjacent regressions, refresh configuration, and
  inspect the installed helper and live status output.

RED evidence: both new cases failed because the current output omitted the state
marker. No player priority, metadata filtering, or click behavior changes.
Rollback removes the glyph prefix and restores the unprefixed label expectations.

Verification: `python3 -B -m unittest tests.test_i3blocks_now_playing_mpris -v`
passed all 39 tests. Spotify and desktop layout regressions, Python AST syntax
validation, and `git diff --check` passed. Snapshot dry-run passed and
`fish -ic 'refresh-config'` printed `REFRESH COMPLETE`, exit 0; full log
`/tmp/refresh-config-20260924-112812-1332655.log` showed no conflicts. The
installed helper matches the tracked source. Live Spotify output while paused
contains `‖ Ariana Grande - twilight zone` in both text lines; live i3blocks
JSON likewise shows the pause mark in both `full_text` and `short_text`. Playing
state is covered by the `♫` fixture. No player or click behavior was triggered.

## Compact pause marker follow-up — 2026-09-24

- [x] Render only the paused `‖` marker at x-small Pango size; keep track text
  at its regular size and preserve the markup in both i3blocks label fields.
- [x] Update paused-output assertions and document the compact marker.
- [x] Re-run focused and adjacent checks, refresh configuration, and inspect
  installed/live output.

The first paused-size regression run exposed three verification failures: the
short label escaped trusted Pango markup, and two existing paused assertions
still expected a plain glyph. The correction escapes dynamic track text before
adding markup, emits the same safe assembled label to both fields, and updates
those assertions. Keep this follow-up in the implementation commit.

Verification: `python3 -B -m unittest tests.test_i3blocks_now_playing_mpris -v`
passed all 39 tests. Spotify and desktop layout regressions, Python AST syntax
validation, `git diff --check`, and `fish -ic 'snapshot-codex-config --dry-run'`
passed. `fish -ic 'refresh-config'` printed `REFRESH COMPLETE`, exit 0; full
log `/tmp/refresh-config-20260924-113750-1347865.log` showed no conflicts. The
installed helper matches source. Live helper and i3blocks status JSON both show
the paused marker as an x-small Pango span before `Ariana Grande - twilight
zone`. No player controls were invoked.

## Pause marker vertical alignment follow-up — 2026-09-24

- [x] Reproduce the low-hanging pause glyph in the user screenshot and capture
  the expected baseline adjustment in a failing label regression.
- [x] Raise only the small Pango pause mark while preserving track size and
  label spacing; document the centered treatment.
- [x] Run focused/full now-playing tests, refresh configuration, and inspect
  installed/live output.

The initial focused assertion failed because the helper emitted no `rise`
attribute, confirming the missing vertical alignment. One combined patch had a
stale test context and changed no files; the exact locations were re-read and
patched successfully. Verification: the focused centered-glyph test and full
`python3 -B -m unittest tests.test_i3blocks_now_playing_mpris -v` both passed
(39 tests). Snapshot dry-run and `refresh-config` passed; full log
`/tmp/refresh-config-20260924-114255-1355876.log` showed no conflicts. Installed
helper matches source and live i3blocks JSON carries
`<span size="x-small" rise="8192">‖</span>` in both labels. The raised compact
marker has not been visually re-screenshot-tested; user confirmation is the
remaining visual review. No playback controls were triggered.

## Playing triangle follow-up — 2026-09-24

- [x] Replace the playing music note with a compact right-pointing triangle.
- [x] Match the triangle's Pango size and vertical rise to the paused marker;
  update tests, README, guide, and smoke-test instructions.
- [x] Run the focused/full suite, adjacent checks, refresh config, and inspect
  installed/live output.

RED: `test_playing_state_adds_compact_triangle_to_both_labels` failed against
the existing note output. A mechanical fixture rewrite initially produced a
Python syntax error from unescaped attribute quotes; escaping the quotes fixed
collection. Verification: the focused test and all 39 now-playing tests passed;
Spotify and desktop layout regressions, AST validation, snapshot dry-run, and
`git diff --check` passed. `refresh-config` printed `REFRESH COMPLETE`, exit 0;
log `/tmp/refresh-config-20260924-115151-1370829.log` had no conflicts. The
installed helper matches source. Live player status was paused during final
inspection; live JSON shows the compact raised pause marker in both labels.
Playing triangle output is covered in the focused test. No playback controls
were triggered.
