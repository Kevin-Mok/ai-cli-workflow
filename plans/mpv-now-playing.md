# Show mpv in the music block

Add mpv to the existing MPRIS block, install the distro bridge, and verify existing players remain eligible.

## Outcome and scope
The 4K bar shows mpv title/artist and state and routes supported clicks to its displayed owner. Reuse busctl, rendering, cache, and controls. No new IPC protocol or global media-key changes.

## Decisions and context
`source_rank` currently allows dedicated Chrome and Spotify only. Live mpv PID 2449138 has no MPRIS name; Ubuntu offers mpv-mpris 0.7.1-1build2. Prefer playing over paused; equal states rank mpv, FlaviBot, Spotify. Base and instance-suffixed mpv names qualify. Existing running mpv must reopen to load the plugin.

## Checklist
- [x] Capture dirty state and inspect helper, tests, docs and live bus.
- [x] Add mpv selection/control tests and observe RED: 42 tests, 3 expected failures.
- [x] Extend source ranking; install user-local Ubuntu bridge; update README and smoke checks.
- [x] Run focused regressions, refresh-config, runtime checks and review diff.

## Risks and rollback
Protected pre-existing work: sources.json edits and two untracked archived-repository/repository-deletion postmortems. Preserve them. No video restart or playback changes. Sudo needs a password, so extract Ubuntu’s package and install its plugin user-locally; no binary enters Git. Revert helper/docs changes to restore selection; removing distro bridge is optional. Live file timestamp is newer by deployment but compare contents before refresh.

## Verification
Run `python3 -B tests/test_i3blocks_now_playing_mpris.py` RED then GREEN. Verify base/suffixed names, playing/paused priority, stopped/empty fallback, click ownership and vanished players. Run refresh-config and inspect installed three-line output. Manually reopen mpv, check title within five seconds, pause/resume and supported clicks; close mpv to verify fallback.

## Progress and review
Initial busctl was denied by sandbox; scoped approved inspection succeeded. No mpv MPRIS bridge currently loaded. No commit requested.

## Final evidence
- This turn: 42 MPRIS tests GREEN; 19 status tests and 1 overflow test GREEN (62 total). Initial RED had 3 expected mpv selection failures.
- User-local Ubuntu plugin installed at ~/.config/mpv/scripts/mpris.so; all ldd dependencies resolved. Not tracked; reinstall the distro mpv-mpris package on other machines.
- refresh-config applied the helper (source/live cmp exit 0) but stopped later on unrelated .config/mimeapps.list conflict. Full refresh is incomplete; do not overwrite unrelated local MIME preferences.
- Host runtime: isolated silent/headless mpv opened the screenshot video and published its filename; real installed helper displayed ▶️, BLOCK_BUTTON=1 produced MPRIS Paused, PlayPause resumed, closing test mpv restored paused FlaviBot `the cure - Olivia Rodrigo`. Original video untouched.
- git diff --check passed. Live i3bar appearance and original-window reload remain manual; no i3 restart needed because the helper is polled.
- Atomic delivery: helper + regression tests + README + smoke checks + this plan + incident learning record. No commit/push requested. Suggested commit: `feat(i3blocks): include mpv playback`.
- Cursor follow-up prompt: “Review plans/mpv-now-playing.md, run python3 -B tests/test_i3blocks_now_playing_mpris.py and the two 4K tests, then verify the installed bar after reopening mpv; preserve pre-existing work and unrelated MIME choices.”
- Review: minimal shared rank change reuses existing sanitization, deadlines and owner-bound clicks; existing Chrome/Spotify regression checks pass. Rollback is restoring the helper; optional removal of user-local mpris.so disables mpv publication.

## Commit milestone — feat(i3blocks): include mpv playback
User requested commit-session. Scope helper found no logged writes/baseline, so use directly observed session writes and the initial status captured in chat. Include helper, tests, README, smoke checks, plan, incident and only the mpv report entry in the mixed sources.json. Leave the two pre-existing reports and their ledger entries dirty. README gate: pass_no_change. Prior live evidence remains valid; rerun focused tests for commit. No implementation blockers; broad refresh MIME conflict remains unrelated. Next: commit and push origin/main, then preserve filename endings on overflow as requested.

## Follow-up — preserve filename endings
User confirmed long mpv filenames should keep their ending and extension, with an ellipsis at the beginning. The helper exposes text only, so detect a filename extension in the shared fitting function rather than adding source metadata. Other labels retain existing truncation. Scope: 4k_status, its layout tests, README and smoke checks. Existing live wrapper equals source (cmp exit 0).
- [x] Observe filename truncation RED: 21 layout tests, two expected filename failures.
- [x] Keep common audio/video filename suffixes in the existing measured binary search; preserve icons/markup and tiny-width handling.
- [x] Run regressions, refresh, and verify live Pango layout with a constrained filename.
Initial milestone committed as a8cddb3 and pushed to origin/main. Rollback: restore fit_song and restart the wrapper. No change to playback selection or controls.

Follow-up evidence: 42 MPRIS + 21 layout + 1 overflow tests passed (64 total). Installed wrapper cmp equals source. /usr/bin/python3 live_layout used live DP-2/Pango configuration: long filename retained cigarette-smoke.mp4 after leading ellipsis, short.mp4 remained intact, ordinary song ended with ellipsis. i3-msg restart activated the updated wrapper. refresh-config retried and stopped at the same unrelated MIME conflict after applying the wrapper; no unrelated files were adopted. Source diff check passed. The follow-up is applied; the user subsequently authorized committing and pushing it. First milestone a8cddb3 pushed to origin/main. Suggested next commit: fix(i3blocks): preserve media filename endings. Remaining manual check: inspect a long filename on the physical bar. Known scope: recognized common audio/video extensions trigger suffix fitting, regardless of MPRIS source; titles without such extensions retain existing fitting.

## Commit milestone — fix(i3blocks): preserve media filename endings
Scope helper again lacks logged writes; direct-write evidence identifies wrapper, tests, README, smoke checks, plan, incident update and only its hash update in the mixed ledger. Pre-existing two reports and their ledger entries remain excluded. README gate pass_no_change; targeted postmortem check and diff check pass. Focused test suites rerun before commit. Completed: applied suffix fitting and docs; remaining: local commit and origin/main push. No task blocker; full-refresh MIME conflict remains unrelated. No configuration edits during this commit-only turn, so prior refresh/deployment evidence applies. Rollback and Cursor follow-up remain as above; next step is ship the verified follow-up.
