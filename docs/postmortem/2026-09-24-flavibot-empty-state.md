# FlaviBot empty-state metadata appeared in i3

## Symptom and impact

With no song loaded in the dedicated FlaviBot window, the 4K i3 music block
could show `FlaviBot - Music Player` as if it were a track. This hid the useful
Spotify fallback and misrepresented an empty player as active media.

## Evidence and root cause

The FlaviBot page publishes generic MPRIS metadata. The displayed label can come
from a single `xesam:title` (`FlaviBot - Music Player`) or from artist `FlaviBot`
and title `Music Player`. The now-playing helper accepted both shapes as real
songs. Focused regressions reproduced each representation, plus the no-Spotify
case, before the fix.

## Resolution and verification

The helper now excludes only the two exact generic metadata representations from
the dedicated FlaviBot source. Spotify remains the fallback, and the block clears
when no eligible player remains. Real title-only and paused tracks remain valid.

Verification: the focused generic-title and screenshot-shaped metadata cases
failed before the fix and pass afterward. The fresh now-playing suite passed all
36 tests; the Spotify shell regression,
desktop layout regression, Python AST syntax validation, and `git diff --check`
all exited 0. The Codex snapshot dry-run passed. `fish -ic 'refresh-config'`
printed `REFRESH COMPLETE`, exited 0, and its full log showed no conflicts. The
installed helper is byte-identical to the tracked source and currently emits the
live Spotify artist, title, and color on three lines. The live player did not
provide the FlaviBot placeholder during final verification, so that state is
covered by the automated fixture.

## Follow-up

The FlaviBot usage guide and smoke checklist now cover the empty state. No browser
profile data or playback state was changed. The block polls every five seconds,
so restarting i3 was unnecessary.
