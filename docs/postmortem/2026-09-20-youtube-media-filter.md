# YouTube media passes song-format filter — 2026-09-20

## Symptom and impact
Long YouTube titles still filled the bar after a lenient artist/title filter.
The user requested excluding YouTube while keeping all FlaviBot songs.

## Evidence and root cause
YouTube reported the concert title as title and Bounceific On Twitch as artist.
The artist exception admitted it despite no title regex match. A second YouTube
session reported Fireship / Anthropic researchers are quitting... and now we know
why. Neither it nor FlaviBot publishes source URL; both originally shared Chrome
PID 4159 / D-Bus owner :1.50. Artist metadata can describe an uploader, not music.

## Investigation failures and resolution
- Ordinary Chrome profile Flavibot (Profile 28) still shared the process. The
  recommendation omitted the distinct --user-data-dir requirement; corrected
  with a dedicated launcher, without copying or modifying existing profiles.
- Initial dedicated launch returned PID 626513, but an exact argv scan missed it.
  Chrome rewrote /proc/PID/cmdline into one space-separated entry. Explicit
  inspection confirmed startup; parser now supports both representations.
- Optional discovery searches referenced absent directories/globs; corrected
  source inventories succeeded. No modifications resulted from those failures.
- User saw YouTube again while FlaviBot was paused before the new helper was
  installed. Source/installed mismatch confirmed deployment was pending after
  interruption. refresh-config subsequently installed the tested source.

## Final resolution
~/scripts/flavibot-browser opens the supplied music-player URL using
~/.local/share/flavibot-chrome. User sign-in/playback proved independent owner
:1.152959 / PID 626513. The helper resolves the actual D-Bus owner to its process
and requires that exact directory before selection and clicks. Original metadata
and click identity remain intact; title regex removed, so title-only songs qualify.
Ordinary Chrome is ignored; Spotify remains fallback. Reserve the dedicated
browser for FlaviBot because websites inside one process remain indistinguishable.

## Verification and current status
Resolved and deployed. Launcher RED failed with missing file, then its test passed.
Source-filter RED exposed six expected failures; parser RED showed missing helper.
Final: 33 media tests plus 1 launcher test pass. Spotify/layout regressions, launcher
syntax, README gate and diff checks pass. Independent review found no blocker.
refresh-config returned REFRESH COMPLETE, exit 0; log inspected and no unrelated
tracked changes resulted. Installed files match source. Actual i3blocks output is
music icon + Logic - Under Pressure, with cache selecting dedicated owner :1.152959.
No live playback controls were sent. Playing-YouTube/paused-FlaviBot isolation is
covered by regression; live inspection at deployment had both browsers paused.

## Follow-up
Use the [desktop smoke checks](../smoke-tests.md) for interactive transitions and
controls. Keep YouTube in ordinary Chrome. See the [plan](../../plans/now-playing-ignore-youtube.md)
for exact commands, evidence, risks and rollback. Process identity replaces the
failed assumption that artist metadata identifies a music source.
