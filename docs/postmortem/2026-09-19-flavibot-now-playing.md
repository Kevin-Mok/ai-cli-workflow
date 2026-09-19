# FlaviBot missing from the i3 music block

## Symptom and impact

The user saw FlaviBot playing Logic — Soul Food while i3 displayed Spotify's
Drake — Janice STFU. The middle 4K music block could not follow browser media.

## Root cause and evidence

The active block called `spotify_mpris`, which explicitly queries Spotify only.
Live Chromium MPRIS already exposed Logic / Soul Food II, so a Discord bot was
unnecessary. Chromium supplied no website URL; the user explicitly selected
browser-wide Chrome support with Spotify fallback.

## Resolution

Added a separate `now_playing_mpris` helper using Python and structured busctl
JSON, preserving the old Spotify helper. Playing tracks win over paused tracks;
Chrome/Chromium wins ties. The helper reads fresh metadata every poll, clears
absent tracks, preserves pywal/Pango formatting, and binds clicks to the last
rendered unique connection with current capability and identity checks.

Independent review found cache-write failure could retain an old click target,
and unresponsive browser calls could hide a healthy Spotify fallback. New RED
regressions reproduced these cases plus invalid Pango controls. The fixes
invalidate old click state, require successful state consumption before controls,
guard cleanup, read fallback first, and remove XML-invalid controls.

## Tooling and deployment failures

- Sandbox startup failed before the initial read-only command and again during
  a patch: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
  Approved elevated commands worked; the failed implementation patch created
  no helper. A file-existence probe returned exit 1 as confirmation.
- Optional source searches included nonexistent `.github`, `packages*`, and
  fish snapshot-wrapper paths, producing inspection-only exit 2 outcomes. The
  real snapshot entrypoint is the tracked Python script. No runtime impact.
- Automatic approval review rejected full `refresh-config`: broad snapshot/apply
  could overwrite unrelated Codex configuration. No bypass was attempted.
  The review-recommended exact-target alternative deployed only
  `~/.config/i3blocks/i3blocks-4k.conf` and
  `~/.config/i3blocks/scripts/now_playing_mpris`. Codex/Git config stayed untouched.

## Verification and current status

Implemented and deployed. All 24 new regression tests, the existing Spotify
regression, and desktop layout checks pass. Basic basedpyright reports no
errors/warnings; README gate and whitespace checks pass.

`i3-msg restart` succeeded, replacing the 4K status process. The installed helper
matches source and is executable. Capturing the installed i3blocks config emits
` Drake - FOMO` with one icon and pywal color `#c9b1c0`. At that time live Chrome
reported Playing Drake / FOMO while Spotify was Paused on Drake / Janice STFU.
No test altered playback or the queue. The initial Logic example was dynamic,
not a literal string to pin in the bar.

## Follow-up and rollback

Use the updated desktop smoke checks for a natural FlaviBot transition and
interactive click validation; those were fixture-tested but not manually
triggered. CUA exposed no browser for direct website inspection. Chrome's media
session can switch tabs or retain paused metadata, and MPRIS check/control calls
are not atomic. Restore the active block command to `spotify_mpris`, apply that
config, and restart i3 in place to roll back. Preserve the original helper.

See [implementation plan](../../plans/flavibot-i3-now-playing.md) for exact commands
and evidence; the completed postmortem belongs in the same commit as the fix.
