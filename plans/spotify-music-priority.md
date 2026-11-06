# Prioritize Spotify on the middle monitor

Resume Spotify from the music block whenever its MPRIS service is open; use local mpv only after Spotify closes. Add executable regression coverage, update existing usage and smoke checks, and refresh configuration.

## Scope and decisions

Change `dot_config/i3blocks/scripts/executable_now_playing_mpris`, its existing test module, and the matching README/smoke entries. Spotify service presence defines open. An open Spotify with unreadable/stopped metadata clears the block instead of selecting local playback. Existing displayed-owner click safeguards remain. Without Spotify, preserve mpv/FlaviBot ranking. No global media-key changes.

## Protected state and risks

Initial git status contained unrelated README, smoke, feedback, postmortem ledger/guidance, Fish progress, Vesktop, privacy approvals, lessons and Firstmate work. Preserve all unrelated changes. The later commit-session request authorizes committing and pushing this session only. Installed helper is newer but byte-identical to source (cmp exit 0). Runtime audio playback needs manual verification. Rollback: restore only this task's priority branch and documentation hunks, then refresh.

## Checklist

- [x] Inspect block, callers, tests, docs and local managed helper.
- [x] Observe RED for Spotify priority/resume with local players open.
- [x] Implement first-choice Spotify, preserve fallback and click protections.
- [x] Update README and smoke checks.
- [x] Run focused regression checks, refresh-config and inspect installed helper.

## Verification and progress

Planned automated command: `python3 -B tests/test_i3blocks_now_playing_mpris.py`. Test real executable with a strict fake external D-Bus boundary; cover Spotify paused alongside playing/paused mpv, closed Spotify fallback, stopped/unreadable Spotify and cached owner safety.
Manual: with Spotify paused and mpv open, inspect block and left-click to resume Spotify; close Spotify and verify mpv selection; open Spotify with no loaded track and confirm local is not selected. Preserve current audio while testing automatically.

## Review notes

Smallest implementation is an early return for the already-first-discovered Spotify service. No dependency or new command. Companion command-discovery incident records an absent guessed executable path; existing reviewed knowledge covers Fish function discovery.

RED: 44 tests ran, 7 expected failures (both Spotify-vs-mpv statuses, three unavailable/stopped metadata cases, Spotify-vs-playing browser and both-paused browser). Existing browser/mpv regressions now explicitly close Spotify. README gate: update_in_same_change; repaired stale music priority claims while preserving unrelated README work.

GREEN: now-playing 44 tests, 4k status 21 tests, 4k overflow 1 test, all exit 0. Tests were delegated to the tests agent; its results and command reports were reviewed. `git diff --check` exit 0. `refresh-config` ran in Fish without normal startup, sourced the tracked functions and existing shortcut script, and exited 0 with REFRESH COMPLETE. Installed helper byte comparison exit 0. A live read-only poll emitted a paused song and pywal color; cache confirmed `org.mpris.MediaPlayer2.spotify`. No actual audio resume/close/open action was performed. The block polls every five seconds, so no restart is required.

Discovery incident targeted ledger check returned no errors, changed or unregistered aliases, exit 0. Initially no commit/push was requested or performed; commit-session subsequently authorized scoped delivery. Remaining manual check: pause Spotify, open mpv, click the middle block; then close Spotify and repeat. Actual TUI wrapped command copy/paste was not exercised; no rendering settings changed.

Atomic delivery: test selection/click routing, add early Spotify return, align README/smoke documentation, refresh and compare installed helper. Suggested commit: `fix(music): prefer open Spotify over local playback`. Cursor follow-up prompt: “Read plans/spotify-music-priority.md; manually verify Spotify resume with mpv open, then local fallback after Spotify closes, preserving unrelated dirty work.”

## Commit milestone: fix(music): prefer open Spotify over local playback

Completed: priority selection, executable tests, README/smoke documentation and configuration activation. Scope helper returned unsafe because it detected no successful writes in this tool transcript; use directly observed writes from session `01a1b298-7551-7de0-b65a-7fd346b3550d`. Stage only music hunks from baseline-dirty README/smoke files and this incident's ledger record; all unrelated work remains unstaged. No prerequisite code changes are needed against HEAD. README gate command `./scripts/executable_readme-recruiter-sync` returned pass_no_change, exit 0. Verification and privacy gate are required before the commit. Target: main -> origin/main. Remaining: manual audio acceptance only; push result reported after commit. Rollback is a normal revert plus refresh, without rewriting history.

Fresh commit-session verification: reran all three focused suites (44 + 21 + 1 tests), all passed, exit 0. Expected cache-write warning belongs to the intentional failure-path test. All session code is already installed; commit-only work adds documentation/ledger state and requires no further configuration activation.
