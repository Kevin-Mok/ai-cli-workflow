# Fit music across the i3 bar

Use the space between workspace buttons and the right edge for status blocks,
with smaller music text and an ellipsis when artist and title cannot fit.

## Scope and decisions

- Remove the DP-2 volume-centering constraint in `executable_4k_status`.
- Render only music at 70% of the bar font (35 points with the current 50-point font).
- Preserve artist-title order; shorten music before compacting/hiding the calendar.
- Preserve volume/Redshift, click identities, padding, Unicode and escaped markup.
- Empty/short songs must not reserve an artificial expanding width.
- Update existing tests, README and smoke checks; no commit/push requested.

## Protected state and risks

Initial `git status --short` was captured before edits. README, smoke tests,
feedback, postmortem knowledge, Codex instructions and concert-video work were
already dirty; preserve their unrelated hunks. Live/source wrapper bytes match.
Workspace buttons plus fixed controls can exceed physical display capacity.
Rollback: restore the previous wrapper and apply/restart the bar.

## Ordered work

- [x] Inspect live metadata, font, DPI, configuration and existing fitting logic.
- [x] Observe defining tests fail against centered/title-first behavior.
- [x] Change fitting, smaller rendering and documentation.
- [x] Run focused and neighboring regression checks and review.
- [x] Run required refresh-config, activate the wrapper and verify a live frame.

## Verification

- RED/GREEN: `/usr/bin/python3 tests/test_i3blocks_4k_status.py`.
- Regression: i3blocks layout, scheduler, now-playing, calendar and volume tests.
- Runtime: actual i3blocks frame measured through Pango at live font/DPI; confirm
  full current song, valid markup, bounded width and shortening under synthetic
  workspace pressure without changing real workspaces.
- Manual: inspect DP-2 with a long track and additional workspace buttons;
  controls stay readable, song shrinks first, short songs do not center volume.

## Progress and review

RED: 19 focused tests ran with 10 expected assertion failures before production
edits. Initial GREEN exposed three independently verified fixture arithmetic
errors; corrected from independent sums, then all 19 focused tests passed. Production now uses the whole available width,
measures the 70% music span, preserves order and omits expanding min_width.

## Cursor continuation prompt

Read this plan and the canonical instructions. Preserve pre-existing changes.
Finish only the DP-2 adaptive music fitting change, run the listed automated
and runtime checks, and update this plan with observed evidence. Do not commit
or push unless requested. Suggested subject: `fix(i3): fit smaller music across bar`.


### Final evidence (this turn)

- `/usr/bin/python3 tests/test_i3blocks_4k_status.py`: 19 passed, exit 0.
- Neighboring checks: overflow scheduler 1, now-playing 39, calendar 1 and volume
  2 tests passed; Spotify shell check exited 0. Now-playing deliberately exercised
  a cache-save diagnostic and still passed. No unrelated full-repository run.
- `fish -c refresh-config`: REFRESH COMPLETE, exit 0.
- `i3-msg restart`: success true, exit 0. Installed/source wrapper bytes match.
- `/usr/bin/python3 /tmp/i3-music-fit-probe.py`: exit 0. Actual live track was
  `Olivia Rodrigo - the cure`; smaller marked-up text measured 1243 px versus
  1694 px originally. At synthetic workspace width 1000 px, the song ellipsized
  while retaining the full calendar; measured total stayed within the bar budget.
  Empty music had no expanding width. Real workspaces were not changed.
- Read-only independent review found no concrete implementation bugs.
- Targeted incident-memory check passed after recording fixture resolution.

### Remaining limits and delivery

Physical pointer clicks and actual crowded workspace rendering were not exercised
in this turn; click forwarding was unchanged and its regression checks passed.
No screenshots or full-repository test run. No commit or push requested/performed.
The temporary read-only runtime probe remains at `/tmp/i3-music-fit-probe.py` for
rechecking during this desktop session; it requires a track loaded in a player.
README and smoke expectations now match the implementation, preserving prior edits.
The minimal production diff removes centering/reordering and measures one smaller
music span. Existing fixed-control physical-capacity limits remain.

Global `git diff --check` reported a pre-existing blank line at EOF in
`dot_agents/skills/postmortem-memory/references/api-contracts-fixtures.md:726`;
that unrelated dirty file was preserved. Scoped change whitespace check passed.

## Authorized delivery, 2026-10-30

Explicit commit-plan-push supersedes prior no-commit notes. Fresh 19 focused tests passed; required refresh-config exit 0. Physical interactions not repeated. Deliver code, tests, matching README/smoke hunks and helper-discovery incident together.
