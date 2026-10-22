# Keep 4K volume visible

Keep volume near the center of DP-2 and fit song text into the remaining bar
space with an ellipsis. When workspace buttons extend beyond the center, move
volume right only as needed. Preserve playback, audio settings and block clicks.

## Scope and decisions

The initial milestone below records the first shipped implementation. The
follow-up replaces song disappearance with an adaptive status wrapper; the
invisible compact form remains only its safe native-i3blocks fallback.

Only the 4K block config changes. Use an empty Pango span as `short_text`
on the second line of the existing song helper in this config only. Installed
i3blocks 1.4 discards truly empty output lines, so a blank line alone does not
set `short_text`; the span preserves an explicit invisible compact form.
Keep volume's full and short percentage identical. Preserve other monitors,
song controls, colors, and calendar. No new dependencies or helper options.

## Checklist

- [x] Capture initial dirty state; unrelated README, smoke-test, notification,
  postmortem and plan edits are protected.
- [x] Read config, installed protocol, helper, tests, lessons and feedback.
- [x] Observe scheduler regression RED, reorder blocks and empty song short text.
- [x] Verify regression and related desktop/media checks.
- [x] Update README/smoke check, run refresh-config, reload and inspect live bar.

## Verification and risks

Run `python3 tests/test_i3blocks_4k_overflow.py` against installed i3blocks with
disposable output helpers: volume stays nonempty, song collapses completely,
order and song color survive. Run desktop-layout and MPRIS regressions.
Manual: play a long song; crowd DP-2 with workspace buttons, confirm song hides
before volume, then remove pressure and confirm song returns. No audio mutations.
Native i3bar still has a physical limit if workspace buttons alone consume the
whole monitor; this change removes the song's contribution before clipping.
Rollback: restore only the 4K config hunk, refresh, then reload i3.

## Evidence and review

Postmortem lookup `i3bar volume spotify overflow` found media-selection/theme
guidance, not overflow fixes; those do not apply. Installed protocol and upstream
i3bar source confirm compact text is used before clipping. Initial
live IPC access needed sandbox escalation; elevated read succeeded. No live
configuration or audio state was changed during discovery.
RED: real i3blocks emitted `spotify, volume, calendar`, failing the requested
`volume, spotify, calendar` assertion with one failure and zero errors.
First GREEN attempt exposed the installed 1.4 behavior: a blank second line
omits `short_text`. A disposable real-scheduler probe confirmed an empty Pango
span is preserved; revised the compact-form assertion to that representation.
GREEN: overflow scheduler test (1), MPRIS tests (39), desktop-layout shell
regression, Spotify shell regression, and `git diff --check` all passed.
Live installed config matches source; targeted apply exited 0 and `i3-msg reload`
returned success. Live scheduler emitted volume 36%, song with compact
`<span></span>`, calendar. Full refresh stopped on unrelated audio-mute drift;
preserved that file and activated only this config. Physical workspace-pressure
and click checks remain manual; no playback or audio changes were made.
README and existing smoke entries now describe song-first collapse.

Suggested commit: `fix(i3blocks): preserve volume before collapsing 4K song`.
Cursor handoff: "Read plans/4k-volume-visibility.md. Review the 4K config and
real-i3blocks regression; preserve unrelated dirty work. Manually verify a long
song under workspace pressure, restore the workspace layout, and report any
clipping. Do not change audio settings."

## Delivery milestone — fix(i3blocks): preserve volume before collapsing 4K song

Session `01a164a7-4838-70b0-90c4-4064956d45b7`: scope helper could not detect
writes through the tool wrapper, so use directly observed edits and the captured
pre-write baseline. Include the config, scheduler regression, this plan, README
and smoke-test hunks, inspection incident and only its new ledger report.
Exclude all unrelated notification, Kitty, prompt and plan edits. README gate
returned `pass_no_change`. Verified behavior is active; physical pressure remains
manual and full refresh remains blocked by unrelated audio-mute drift. Commit
and upstream push are the remaining delivery steps; no product work remains.

## Follow-up — fit song text and center volume

The user's screenshot shows unused space after the song disappears. Replace
the blank compact song with adaptive ellipsized text. Keep volume centered on
DP-2 where workspace buttons allow, then move it right only as those buttons
require. Preserve all block clicks, polling, colors, and other monitor bars.

Use a small 4K-only status-stream filter around existing i3blocks. Measure text
with installed system Python GI/Pango at the live bar font and Xft DPI, reserve
volume/calendar/workspace space, fit the song with a Unicode ellipsis, and use
song min_width to hold volume's position even for short tracks. Pass click input
straight to i3blocks. Fall back to a minimal song marker if IPC is unavailable.
No packages are installed; GTK/Pango bindings are present in /usr/bin/python3.

- [x] Add defining tests for long/short/Unicode titles, crowding, and click stream.
- [x] Observe RED, implement the filter and wire only the DP-2 bar.
- [x] Verify tests, live geometry and installed output; update docs and refresh.
- [ ] Deliver the verified follow-up with the original commit; push once.

Risk: native workspace buttons can exhaust the physical display. Reserve volume
first and collapse calendar/song as needed; when no text can fit, retain native
clipping as the physical limit. DPI/font and exact separator calculations need
live verification. Rollback: restore original 4K status command and block config.

### Delivery milestone — feat(i3blocks): fit song text beside centered volume

Prerequisite commit: `1960ab3` (local, pending series push). The final adaptive
wrapper reserves volume, centers it where workspaces allow, ellipsizes title
first, preserves click input and metadata, and retries transient startup failures.
Defining RED observed for missing filter, title priority, no-song position,
startup fallback and startup recovery. GREEN: 10 layout tests, 1 scheduler test,
39 MPRIS tests and both shell regressions; diff whitespace check passed.
Independent review found empty-song and startup-fallback issues; both corrected
with regressions. Live source/installed identity and actual bar screenshot
`/tmp/4k-bar-recovered.png` confirm volume 36% near screen center with
`Stitches -…`. No audio or playback changes. Extreme workspace pressure and
click actions are fixture-covered; the user's workspace layout was preserved.
README and smoke tests describe the final behavior. Repeated required refresh
attempts preserved unrelated audio/Kitty conflicts; exact owned deployment
succeeded. Live i3 config is preserved from broad chezmoi management, so only
the reviewed status_command line was changed there. Runtime requires system
Python GI/Pango; if unavailable, the original volume-priority stream survives.
Scope helper remains unavailable; stage only directly observed current-session
hunks, including the new learning/ledger entry, and exclude Kitty work.
