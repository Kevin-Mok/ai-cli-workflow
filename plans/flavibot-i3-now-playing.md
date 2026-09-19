# FlaviBot / browser now-playing in i3

## Purpose and observable outcome

The middle 4K i3 bar follows Chrome media, including FlaviBot, instead of always
showing Spotify. It renders `Artist - Title` using the existing icon and pywal
color. Spotify remains a fallback. No queue or playback changes during diagnosis.

## Context and scope

`bar-2` runs `i3blocks-4k.conf` on DP-2. Its current helper is Spotify-only.
Live Chromium MPRIS publishes Logic / Soul Food II; Spotify publishes Drake /
Janice STFU. Both report Paused. Chromium does not publish a source URL.
The old Spotify helper remains available; only the active 4K block changes.
Global media keys and Discord configuration are out of scope.

## Decisions and assumptions

- Use a sibling Python 3 helper backed by `busctl --user --json=short` for typed
  metadata, avoiding regex parsing of GVariant strings. Both tools are installed.
- Default is browser-wide Chrome/Chromium selection: MPRIS cannot distinguish
  FlaviBot from other tabs here. The user explicitly chose Chrome media with Spotify fallback.
- Rank Playing Chrome/Chromium, Playing Spotify, Paused Chrome/Chromium, Paused
  Spotify; ignore stopped, missing-title, disconnected, and unrelated players.
  Sort bus names for a deterministic tie between instances.
- Poll every five seconds. Fetch live metadata every time; do not display cached
  tracks when a player disappears. Paused tracks may remain visible.
- Store the last rendered player's unique D-Bus owner, track identity, and time
  in a private local cache. Clicks require a fresh matching record and current
  capability; otherwise do nothing. Never redirect a click to the fallback.
- Preserve three-line i3blocks output, a single external music icon, and color7.
  Normalize whitespace and escape markup. Emit blank lines when no player exists.
- No new Discord bot, credentials, browser extension, or playerctl dependency.

## Ordered checklist

- [x] Capture initial state: `git status --short` was empty.
- [x] Save accepted prompt and document diagnosis/tooling failure.
- [x] Confirm active bar and inspect live structured metadata.
- [x] Add regression tests and observe RED before helper/config implementation.
- [x] Implement sibling helper and switch the active 4K block.
- [x] Test selection, transitions, errors, escaping, fallback, and safe clicks.
- [x] Update README, smoke checks, postmortem, and local lesson.
- [x] Review diff; run focused regressions and runtime checks; attempt refresh-config
  and use the approved exact-target deployment after its rejection.
- [x] Record final evidence, limitations, and review notes.

## Risks and rollback

Chrome exposes its selected media session, not every tab; other browser media
can replace FlaviBot. Paused metadata is supplied by the browser and may remain
until it releases the session. Browser window presence alone proves nothing.
Missing/failed D-Bus reads must not crash the bar or reuse cached song text.
Refresh snapshots live Codex and Git config; inspect its effects and preserve
unrelated changes. No initial dirty files. Restore the 4K command to
`spotify_mpris` and refresh to roll back without deleting the old helper.

## Verification

- RED/GREEN: `python3 tests/test_i3blocks_now_playing_mpris.py`.
- Regression: `bash tests/test_i3blocks_spotify_mpris.sh` and
  `bash tests/test_desktop_display_layout.sh`.
- Validate Python syntax and `git diff --check`.
- Compare live new helper output to `busctl` properties; keep playback unchanged.
- Apply with `fish -ic refresh-config`, inspect complete log and resulting diff,
  then reload i3 configuration if needed and observe actual i3blocks JSON output.
- Manual: play FlaviBot, watch a natural track transition, pause it with Spotify
  playing, close its media session, and verify fallback. Exercise block controls
  on each selected player and verify the other player remains unaffected.

## Progress, evidence, and review

Initial investigation used read-only calls. Sandbox startup fails before commands
run; approved elevated command execution works. CUA reports no available browser,
so direct website comparison is unavailable. Exact live metadata is recorded above;
no claim that the currently paused track is actively playing.

RED: 19 new tests failed with the expected missing-helper assertion; the
layout test failed with the expected old-command assertion. Initial GREEN: all
19 tests plus existing Spotify/layout regressions passed. Independent review
found failed-state-write click risk, Pango control characters, and a hung-browser
fallback gap; four focused RED regressions reproduced these before fixes.

Deployment deviation: full `refresh-config` was attempted but auto-review rejected
it because of unrelated live Codex configuration. Follow the explicitly suggested
safer alternative: `chezmoi apply` only the 4K block config and new helper. Do not
bypass the block or snapshot unrelated configuration.

## Final evidence and handoff

- `python3 tests/test_i3blocks_now_playing_mpris.py`: 24 tests pass, including
  priority, paused fallback, track transition, removed player, malformed data,
  hung browser fallback, Pango text, deterministic instances, capability checks,
  exact-owner clicks, corrupt/expired state, failed writes, and unwritable state.
- `bash tests/test_i3blocks_spotify_mpris.sh` and
  `bash tests/test_desktop_display_layout.sh`: exit 0.
- `basedpyright --project <temporary config>`: 0 errors/warnings/notes; config
  uses `typeCheckingMode: basic` and includes the absolute new helper path.
- `bash scripts/executable_readme-recruiter-sync`: `pass_no_change`, exit 0
  after the in-scope README update. `git diff --check`: exit 0.
- Exact-target deployment succeeded:
  `chezmoi apply -- ~/.config/i3blocks/i3blocks-4k.conf ~/.config/i3blocks/scripts/now_playing_mpris`.
  This is the explicit safer alternative recommended by automatic approval
  review; full refresh did not run. No Codex/Git source files were changed.
- `i3-msg restart`: success; active 4K i3blocks PID changed from 4192 to 3026686.
- Installed helper is executable and byte-identical to the tracked source.
  A two-second capture using the installed i3blocks config emitted full text
  ` Drake - FOMO`, short text `FOMO`, color `#c9b1c0`, markup `pango`.
  A separate live D-Bus read confirms Chrome is Playing Drake / FOMO while
  Spotify is Paused on Drake / Janice STFU. Playback changed naturally during
  the task; the Logic example is not hardcoded.
- Independent review found no remaining material issue after the failure-path
  fixes. Source and docs were reviewed; the user subsequently requested
  `commit-plan-push` for the complete dirty worktree.

Remaining manual validation: compare a natural FlaviBot track transition against
its website and exercise controls using the documented smoke checks. These are
covered by fixtures but were not manually triggered because playback/queue must
not be disturbed and CUA exposes no browser. Separate MPRIS check/control calls
cannot make track transitions atomic; identity checks narrow that inherent race.
Chrome may keep paused metadata until its media session is released.

Suggested commit: `fix(i3blocks): follow Chrome media with Spotify fallback`.
Keep this plan, prompt, tests, docs, and postmortem with the implementation.
The accepted paste-ready handoff is `prompts/flavibot-i3-now-playing.md`.

## Delivery contract (2026-09-19)

All ten pending files form one coherent fix. Include the helper and active block,
regressions, README, smoke checks, lesson, prompt, this plan, and postmortem in
`fix(i3blocks): follow Chrome media with Spotify fallback`. No unrelated dirty
files or unsafe artifacts were found. Preserve the original Spotify helper.
Run the focused Python and shell tests, README gate, type check, and staged diff
check; inspect the staged content before committing. Push once afterward from
`feat/ai-workflow-optimization` to `origin/feat/ai-workflow-optimization`.
The earlier full-refresh rejection and unperformed interactive smoke checks
remain documented limitations; they do not block delivery of the tested fix.
