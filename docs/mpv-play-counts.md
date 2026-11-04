# Automatic mpv play counts

New mpv sessions automatically save local-file playback totals. Launch mpv as
usual, let files play or loop, then use the counter's text ranking to see your
most-played files. No separate daemon or special launch command is needed.

## Use

From the repository, run `python3 scripts/executable_mpv-count --top` for the
emoji ranking, or add `--plain` for ASCII text. Use `--count /path/to/file.mp4`
to inspect one file. The existing cg command is tracked automatically; cgc
continues to use the wrapper and records each playlist reload exactly once.

The auto-loaded script is `~/.config/mpv/scripts/play-count.lua`. It calls the
Python helper at `~/linux-config/scripts/executable_mpv-count`. Other checkouts
can supply `--script-opts=play-count-helper=/absolute/path/to/executable_mpv-count`.
The helper's `--record FILE` option saves one play and is normally called only
by the script. It validates that FILE exists; no shell evaluates filenames.

## Counting and limits

- A successfully loaded local file adds one, including a partially watched play.
  Loading another playlist entry adds a play for that entry.
- Native --loop-file repeats are detected by playback wrapping from near the
  end back to the beginning. mpv0.37 exposes no distinct native-loop event.
  Audio buffering requires a one-second detection window; for subsecond clips,
  most of the clip is in that window. A manual rewind in the same window can
  add a play. Very short or fast playback can miss wraps. This is a heuristic.
- Pauses and ordinary seeks outside that window add no plays. Native looping
  and player options are unchanged. Loop mode is sampled when the file loads;
  changing loop-file interactively takes effect for tracking at the next load.
- Native playlist loops and the wrapper use file-loaded events instead of the
  native-file-loop heuristic. Wrapper launches are excluded from automatic
  recording to prevent duplicates.
- Network URLs are skipped. Every local-file mpv session includes notification
  audio and other background players, not just songs opened from a terminal.
- Already-running sessions must be reopened to load the script. --no-config,
  --load-scripts=no and custom config directories can bypass auto-loading.

## Storage and recovery

SQLite totals remain at `$XDG_STATE_HOME/mpv-count/plays.sqlite3`, defaulting to
`~/.local/state/mpv-count/plays.sqlite3`. Canonical absolute paths identify files,
so symlinks share totals and moved files start new totals. Concurrent updates
are serialized. Errors leave existing totals in place and print a concise mpv
error; check helper availability and directory permissions.

To stop auto-counting temporarily, move play-count.lua out of the mpv scripts
directory before opening new sessions. Restore it to enable recording again.
Configuration refresh can reinstall the managed script. No totals are erased.

## Verification

Run `python3 -m unittest discover -s tests -p test_mpv_count.py -v`. Tests use
isolated SQLite state and real null-output mpv playback for native finite and
infinite loops, ordinary pause/seek, wrapper duplicate prevention, concurrent
recording, file aliases and ranking output. Sandbox execution may require local
socket access for the wrapper's IPC.

For a manual check, query a clip's count, open it with ordinary mpv and
--loop-file=inf, let it replay twice, quit, and query its total again. Expect
three additional plays. Reopen once without looping and expect one additional
play. This also verifies that the installed script auto-loads.
