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
