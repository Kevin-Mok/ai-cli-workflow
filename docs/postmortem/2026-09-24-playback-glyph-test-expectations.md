# Playback glyph tests retained the old label contract

## Symptom and impact

The first full now-playing suite after adding playback glyphs reported 32 failed
assertions. The helper added `♫` or `‖` as requested, while many older assertions
still expected labels without a state prefix. This blocked verification but did
not indicate a player-selection or click-control regression.

## Evidence and root cause

Both new playing/paused glyph tests passed. The failed assertions consistently
showed a glyph-prefixed actual label versus the prior plain artist-title expected
value. The test suite's existing expectations were not updated to the newly
approved output contract before the full run.

## Resolution and verification

The short label now preserves the trusted small Pango span, with dynamic track
text escaped before assembling the markup. Both stale paused-selection
assertions expect the compact pause span. The focused now-playing suite passed
all 39 tests; Spotify and desktop layout regressions, Python AST validation,
snapshot dry-run, and `git diff --check` passed. `refresh-config` completed
without conflicts, the installed helper matches source, and live i3blocks JSON
shows `‖` in an x-small span before Ariana Grande's track title. No
player-selection or click-routing behavior changed.

## Visual-centering follow-up — 2026-09-24

The user's screenshot showed the compact pause mark still hanging below the
track baseline. A new targeted assertion requires a positive Pango `rise` to
optically center it; that regression failed as expected because the source had
not yet applied the rise. One initial combined patch was rejected because two
paused-fixture lines did not match the actual test text, so it changed no files.
After re-reading the exact contexts, the helper and all paused assertions were
updated. A later documentation patch was rejected on a stale plan context and
some earlier hunks had already applied; another attempt to reapply the guide
and smoke-test hunks was correctly rejected because that content was already
updated. Exact document tails were then re-read to avoid duplicate edits.

Verification: the centered-glyph regression and full now-playing suite passed
(39 tests). Spotify and desktop layout regressions, Python AST validation,
snapshot dry-run, `git diff --check`, and installed/source `cmp` passed.
`refresh-config` completed without conflicts; live i3blocks JSON carries
`<span size="x-small" rise="8192">‖</span>` in both labels. The visual state
has not yet been re-screenshot-tested; user confirmation remains the visual
review step.

## Playing triangle follow-up — 2026-09-24

The user requested a right-pointing triangle instead of the playing music note.
The new specific regression correctly failed against the old output. A bulk
fixture replacement then caused a Python `SyntaxError` because Pango markup
quotes were inserted into double-quoted test strings. Impact: test collection
stopped before running assertions; no installed config changed. Safely escaped
the fixture strings after verifying the transformation on a sample. One
combined documentation patch applied its plan hunk but was rejected on a stale
postmortem context; the postmortem tail was re-read and this update applied
separately.

Verification: the focused triangle test and the full now-playing suite passed
(39 tests). Spotify and desktop layout regressions, AST validation, snapshot
dry-run, and `git diff --check` passed. `refresh-config` completed with no
conflicts; the installed helper matches source. Live player state was paused at
final inspection, and i3blocks JSON showed the compact raised `‖` in both
labels. The `▶` playing markup is covered by the focused test. No playback
controls were triggered.
