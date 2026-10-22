# Keep 4K volume visible

Move volume immediately before the song on DP-2 and let i3bar hide the song
when workspace buttons crowd the status area. Apply the config and verify the
real scheduler output without changing playback or audio settings.

## Scope and decisions

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
