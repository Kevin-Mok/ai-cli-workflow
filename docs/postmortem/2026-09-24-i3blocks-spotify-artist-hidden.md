# i3blocks Spotify artist hidden by short text

## Symptom and impact

The 4K i3 bar showed only `twilight zone` for a Spotify track by Ariana Grande,
even though the helper knew the artist. This made Spotify's now-playing label
incomplete whenever i3blocks selected its short-text field.

## Evidence and root cause

The installed helper emitted three lines: `Ariana Grande - twilight zone`,
`twilight zone`, and the color. The live i3blocks JSON confirmed those became
`full_text` and `short_text` respectively; the screenshot matched the short text.
The renderer correctly used the shorter field when space was constrained.

## Resolution and verification

The helper now emits the artist-title label for both full and short text, so
either rendering choice retains the artist. The focused regression failed before
the change. The fresh now-playing suite passed all 37 tests; Spotify and desktop
layout regressions, Python AST validation, and `git diff --check` exited 0.
`refresh-config` completed with no conflicts and the installed helper matches the
tracked source. A fresh live i3blocks status line now shows `Ariana Grande -
twilight zone` in both `full_text` and `short_text`.

## Follow-up

The smoke check and active plan now state the artist-preserving output contract.
The change does not alter player selection or click routing.
