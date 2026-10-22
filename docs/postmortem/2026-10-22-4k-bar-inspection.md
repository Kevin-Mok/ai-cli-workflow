# 4K bar inspection required live-session access

Initial read-only inspection could not reach the live i3 socket from the
sandbox. Elevated inspection succeeded; no configuration or audio state was
changed by those queries.

## Symptom and impact

`i3-msg -t get_bar_config` and `get_outputs` returned `Operation not permitted`.
Two exploratory lookups also referenced a nonexistent historical report name
and a nonexistent test glob; the actual media tests and report were then read.
These failures delayed inspection only.

Required activation then stopped: `fish -ic 'refresh-config'` exited 1 during
chezmoi apply. Its private log is `/tmp/refresh-config.XsNNudZZ.log` and names
unrelated live drift in `scripts/audio-mute`. Preserved that helper and applied
only the reviewed 4K bar target; i3 reload returned success.

## Cause and resolution

The desktop socket requires access outside the sandbox. Repeating the read-only
queries with the normal escalation returned three bars and active DP-2 at
3840x2160. The historical report is `2026-09-24-flavibot-empty-state.md`, and
the media test is `tests/test_i3blocks_now_playing_mpris.py`.

## Verification and follow-up

Elevated IPC returned exit 0. Live i3blocks emitted volume `36%`, song with
invisible compact text, and calendar in the requested order. Full refresh
remains incomplete; the bar is activated. Lookup `refresh-config chezmoi apply
conflict` matched `local-refresh-snapshot-ownership`; its exact-owned-target
workaround applies to the confirmed unrelated conflict. No new reusable
learning: existing permission/ownership guidance covers this incident.

The first delivery attempt was blocked by the privacy gate's `home_path`
category in the new ledger alias. Replace that alias with the repository's
existing `/home/example` convention before retrying; preserve the report hash.

The follow-up adaptive layout found live i3 config is intentionally not managed
by chezmoi (`chezmoi diff` reports `not managed`). Deploy the new managed status
helper normally, and replace only its reviewed status_command line in the live
i3 config. Preserve other session edits and all other live settings.

Final screenshot initially retained the earlier artist-first output: an i3
reload does not restart an unchanged status_command. Make the system Python
interpreter explicit in that command (the helper uses system GI/Pango), then
reload so i3bar starts the final helper. Standalone final-helper output already
showed `Stitches -…`; compare the actual running bar after activation.

The restarted bar retained unadapted text even after its first media poll,
although a standalone process with the running helper's environment adapted
correctly. Startup fallback was permanent, so a transient initialization failure
during reload could leave raw i3blocks output forever. Add an executable
transient-startup regression and retry measurement initialization on subsequent
status updates while preserving raw output until it succeeds.

Resolution: the defining transient-startup regression now passes and the running
bar screenshot shows centered volume `36%` with `Stitches -…` beside it. Source
and installed helper match. A fallback test originally asserted JSON whitespace;
it now parses the preserved status frame and checks the actual volume value.
Later full-refresh attempts stopped on unrelated Kitty font-helper drift;
preserved that work and deployed only this task's helper and live status line.
