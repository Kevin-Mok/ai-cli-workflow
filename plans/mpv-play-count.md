# Reusable mpv play counts

Add a Python standard-library wrapper that loops any local file with the requested
hardware decode, fast profile, and 1920x1080 scaling, persisting each started play.

## Scope and decisions

- Entry point: `scripts/executable_mpv-count`; tests: `tests/test_mpv_count.py`.
- SQLite state at `$XDG_STATE_HOME/mpv-count/plays.sqlite3` (default ~/.local/state).
- Canonical absolute file paths identify files; moving a file starts a new count.
- Count the initial successfully loaded file and each automatic replay, not seeks.
- Use single-file `--loop-playlist=inf` rather than `--loop-file=inf`: reloads
  emit file-loaded events, unlike seek-based file loops. Playback settings retained.
- `--count FILE` reads the total without playback; `--plain` removes emojis.
- No changes to the existing cg shortcut or global mpv configuration.
- Preserve all initial dirty files, including unrelated smoke-test edits.

## Checklist

- [x] Inspect existing helpers and capture initial Git status.
- [x] Clarify that loops count too.
- [x] Write and observe a failing real headless mpv loop test.
- [x] Implement wrapper; verify persistence, separate files, missing files, aliases.
- [x] Document usage and manual smoke checks; run focused regression checks.

## Verification

`python3 -m unittest discover -s tests -p test_mpv_count.py -v` exercises actual
mpv with generated short WAV media, null outputs, and finite playlist loops.
Manual: run on a real video; check displayed count, pause/seek, let it replay,
quit, query --count, relaunch. Confirm scaling and hardware output visually.

## Risks and rollback

Reloading the playlist can produce a brief gap and resets file-local settings.
A started partial play counts; old plays cannot be reconstructed. SQLite commits
serialize concurrent updates. Remove the wrapper and optional state to roll back.
Initial implementation did not request delivery; fish-alias follow-up now authorizes a focused commit and push.

## Progress and review

RED: focused unittest exited 1 because the wrapper did not exist. GREEN:
focused unittest exited 0; actual mpv looped three times on each of two launches,
persisted six plays, resolved symlink aliases, isolated another file, and rejected
a missing file. `git diff --check` exited 0. Default-state query with approved
home access returned Plays: 0, exit 0; initial sandbox limitation and reviewed
no-new-learning decision are recorded in the dated postmortem. README gate:
update_in_same_change (new entrypoint documented; existing hierarchy preserved).
Final fresh regression initially hit sandbox IPC EPERM; the same command with
approved socket access passed, exit 0. No configuration changed, so refresh-config
was unnecessary. No commit or push.
GUI playback, hardware decoding, seeking in the GUI and physical-terminal
wrapped-copy checks were not performed; mpv null audio/video was verified.

## Delivery notes

Atomic change: wrapper, focused real-mpv regression, README entry and manual
smoke checks. Suggested commit: `feat(media): persist per-file mpv play counts`.
Cursor follow-up prompt: "Review plans/mpv-play-count.md and the mpv-count
wrapper; run python3 -m unittest discover -s tests -p test_mpv_count.py -v,
then perform the Persistent mpv play counts manual smoke check. Preserve
unrelated dirty work and report actual results."


## Follow-up: most-played text list

Scope: add `--top` without a file argument, listing all positive totals in
count-descending/path-ascending order. Show a music heading, medal ranks for the
first three, numeric ranks thereafter, aligned counts and basenames. `--plain`
removes decorative Unicode. Empty state explains no plays have been recorded.
Use the existing SQLite database; no new dependencies or configuration.

- [x] Capture current dirty state and define pretty-text ranking regression.
- [x] Observe RED for missing --top behavior.
- [x] Add listing; update README and smoke checks; verify focused regressions.

Verification: same focused unittest command above; synthetic SQLite rows cover
sorting, ties, zero totals, empty state and ASCII rendering. Run actual --top
and --plain --top against saved state. GUI playback is unchanged.

Follow-up evidence: new top-only test exited 1 because the file argument was
still required. After implementation, the full focused command passed both tests
with approved local IPC access (exit 0). Default-state `--top` and `--plain --top`
each exited 0 and reported no plays recorded yet. `--help` documents the flag;
`git diff --check` passed. README and smoke checks updated in the same change.
No refresh needed: no configuration edits. No commit/push requested.
Basenames may repeat for distinct paths; counts remain separate by canonical path.
Follow-up Cursor prompt: "Review the --top listing in scripts/executable_mpv-count;
run the focused tests and verify the documented emoji and plain listings."
Suggested follow-up commit: `feat(media): list most-played files with emoji ranks`.

## Delivery: cgc abbreviation

User invoked fish-alias, authorizing focused commit and push including the
counted-playback prerequisite. cgc expands to Python plus the absolute repository
wrapper path and requested video, so it works from any current directory.
Preserve cg and unrelated dirty work, especially pre-existing smoke-test and
postmortem-ledger changes. Preview found no conflicts in applications section.

- [x] Preview and apply cgc using fish-alias helper.
- [x] Refresh configuration and verify installed abbreviation without playback.
- [x] Run focused playback tests and README gate; stage only related content.
- [x] Commit `feat(media): add counted playback and cgc shortcut`; push origin/main.

Rollback: remove cgc source mapping and refresh; saved counters remain local.
Verification commands: fish -n ~/.config/fish/key_abbr.fish; inspect cgc with
abbr --show | string match -- "*cgc*" in a fresh interactive fish; focused tests as recorded above.

Delivery evidence: refresh-config completed twice (exit 0); alias file is
migration-preserved, so only cgc was merged into the live alias source before
the second refresh. fish --no-config -n passed; generated source and fresh
interactive abbr inspection confirm the requested expansion (exit 0).
Two focused mpv tests passed. README gate pass_no_change, diff whitespace clean.
Broader fish alias tests blocked by pre-existing SyntaxError at test file line
74; no unrelated test repair included. No actual cgc playback was launched.
Refresh preserved unrelated local MIME association mode as a source rename;
that change and all initial unrelated edits are excluded from the commit.

Milestone: feat(media): add counted playback and cgc shortcut. Implementation,
rankings, docs, plan and installed shortcut are verified as scoped. No remaining
implementation work; push pending. Unverified: GUI output, physical keyboard
expansion and physical-terminal wrapping. Rollback removes cgc plus wrapper;
local counters are retained unless explicitly removed.

Prior delivery reconciliation: f8b41e5 committed the wrapper, ranked listing and
cgc shortcut, and pushed successfully to origin/main. The automatic-counting
follow-up is described and verified in plans/mpv-auto-count.md; commit-session
now authorizes delivery of that follow-up with both matching plan records.
