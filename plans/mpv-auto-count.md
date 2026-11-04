# Automatic mpv playback counts

Make ordinary mpv launches update existing per-file totals automatically by
installing a quiet Lua script. Continue using --top for the emoji ranking.

## Context and decisions

- Existing counter: scripts/executable_mpv-count; SQLite state unchanged.
- Add dot_config/mpv/scripts/play-count.lua; auto-loaded on new mpv sessions.
- Add --record FILE to the existing counter for the Lua-to-SQLite boundary.
- Keep cgc and the wrapper; wrapper marks its subprocess so the automatic hook
  skips it, avoiding double counts. Wrapper playlist events remain exact.
- Native loop-file in mpv 0.37 is a seek, with no distinct loop event. Detect
  near-end to near-start wraps (a one-second EOF window, wider proportionally for subsecond media) without changing native looping or player options.
  This is a documented heuristic: a rewind within the detection window may count; unusually
  fast playback or short clips may miss a wrap. No polling process daemon needed.
- Count local files only; ignore network URLs and nonmedia/failed opens.
- Helper path defaults to ~/linux-config/scripts/executable_mpv-count, overridable
  by mpv script-opts play-count-helper for other repository locations.
- Background helper failures log a concise error; never erase existing totals.

## Checklist

- [x] Capture initial dirty state and inspect source and official mpv0.37 docs.
- [x] RED: real mpv auto-script initial load and native file loops do not count.
- [x] Implement hook, --record and wrapper exclusion; verify real mpv behavior.
- [x] Update README and smoke checks; refresh and verify deployed auto-load.

## Verification

Focused tests: python3 -m unittest discover -s tests -p test_mpv_count.py -v.
Use isolated XDG state/config and generated WAV media. Exercise initial launch,
finite native loop-file, infinite loop-file stopped after observed counts,
seek/pause, multiple files, concurrency, and wrapper with automatic hook loaded.
Direct runtime: ordinary installed mpv with null outputs and temporary XDG state;
query resulting count. Config update requires refresh-config with approved access.

## Protected state, risks and rollback

Preserve all initial unrelated dirty files, including smoke tests and the ledger.
The subsequent commit-session invocation authorizes a focused commit and push. Remove installed/source play-count.lua to disable
automatic recording; existing totals remain. --no-config/--load-scripts=no bypass
normal autoload. Existing sessions do not acquire new scripts. Short notification
sounds also count because the request covers every mpv local-file playback.

## Evidence and review

Native loop implementation: https://github.com/mpv-player/mpv/blob/v0.37.0/player/playloop.c#L813-L849
No option or playback semantics changes were made. Verification and deployment results follow.

TDD evidence: initial RED exited1 for absent auto hook. First implementation
recorded initial load but not native loops; the new test stayed RED (expected3,
observed1). An instrumented real0.8s WAV showed native seeks at reported positions
0.385 and0.355 because audio was queued ahead, followed by0 and negative positions.
Expand the end window to account for buffering and apply it only when native
looping was enabled at load; keep pause/seek tests on ordinary nonloop playback.
This remains explicitly heuristic for native loop-file, not an exact mpv API.

GREEN: python3 -m unittest discover -s tests -p test_mpv_count.py -v passed
all4tests, exit0 (~10seconds) with approved IPC access. Native finite repeats
and infinite repeats, pause/seek, wrapper auto-load duplicate prevention,
concurrent recording and existing rankings passed. Added dedicated usage and
limits document before the completed deployment recorded below.

Deployment evidence: approved fish -ic refresh-config exited0 (REFRESH COMPLETE).
Installed ~/.config/mpv/scripts/play-count.lua matches repository bytes. A normal
mpv launch (no explicit --script/config-dir) with --loop-file=2, null outputs,
a temporary WAV and isolated XDG_STATE_HOME recorded exactly Plays:3 and exited0.
Actual user totals were unchanged by this probe. README gate pass_no_change;
git diff --check passed. Documentation describes buffering heuristics, disable
paths and wrapper exclusion. Independent evidence review verified installed bytes, all4tests, duplicate
prevention, transactional recording, structured subprocess safety, unchanged
player settings and matching heuristic qualifications. Its pending default-config
check is satisfied by the completed runtime probe above (Plays:3, exit0).

## Handoff

Atomic plan: this hook, helper boundary and wrapper exclusion, focused tests,
README/usage/smoke documentation, and matching plans. Commit-session now authorizes delivery.
Suggested commit: feat(media): count ordinary mpv playback automatically.
Cursor prompt: "Review plans/mpv-auto-count.md and docs/mpv-play-counts.md; run
python3 -m unittest discover -s tests -p test_mpv_count.py -v with local socket
access, then verify ordinary mpv auto-load using isolated counter state. Preserve
unrelated work and report the native-loop heuristic honestly."
Manual test: query the supplied concert clip's count; reopen with the original
mpv command, allow2replays, quit, query count and --top. Prior sessions do not
acquire the hook. Physical video/hardware output and terminal copy wrapping were
not tested. Existing unrelated fish-alias test syntax failure was not revisited.

## Commit-session delivery milestone

Session: 01a1a8ab-a016-7773-8601-a4d14d7f6be1. Scope helper returned unsafe:
no successful repo writes detected in its supported log actions. Use direct-write
evidence from the active conversation and the initial git status baseline.
Eligible: automatic Lua hook, existing counter's --record and wrapper exclusion,
focused tests, README row, mpv-only smoke hunks, usage docs and both matching plans.
Exclude initial unrelated Fish/Vesktop edits, all unrelated postmortem knowledge
and the SSH report. Also exclude the refresh-preserved MIME source mode rename.
No staged work existed before staging this candidate.

Fresh delivery checks: python3 -m unittest discover -s tests -p test_mpv_count.py
-v passed4tests, exit0 (~9.72s), with approved local socket access. README gate
pass_no_change. Installed hook and null-output ordinary-launch verification from
the prior implementation turn remain applicable; no implementation changes since.

Milestone subject: feat(media): count ordinary mpv playback automatically.
Implementation and deployment complete; review and focused verification passed.
Known limits remain native-loop heuristic and untested physical GUI/hardware.
Next: exact candidate privacy gate, commit, then push configured origin/main.
