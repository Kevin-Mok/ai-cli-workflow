# Music playback priority

Make the i3 music block show active playback ahead of paused players, then verify selection and click routing.

## Scope and decisions
- Change `select_player` in the MPRIS helper, its existing executable tests, README music description and smoke checks.
- Playing beats paused; ties prefer Spotify, then mpv, then dedicated FlaviBot. Invalid/stopped Spotify must not hide eligible playback.
- Preserve browser eligibility, deadline and displayed-owner click validation. No media-key changes.
- Initial git status recorded: README, smoke tests, feedback, lessons, several postmortem references/ledger and other unrelated files were dirty. Preserve all pre-existing edits; commit-session subsequently authorizes this session only.

## Checklist
- [x] Inspect source, callers and existing fixtures.
- [x] Observe defining RED for paused Spotify plus playing mpv/browser.
- [x] Implement minimum selection change and update docs.
- [x] Run focused regressions and refresh-config; report deployment limits.

## Risks and rollback
Player polling remains bounded and non-atomic. mpv requires mpv-mpris. Restore only session hunks to revert; never reset unrelated work.

## Evidence and review
Prior knowledge query `i3blocks music spotify paused mpv player` matched `local-displayed-owner-control-binding` and `local-browser-source-process-identity`. Owner-binding and process eligibility apply; unconditional Spotify return is the current conflict. Verification will execute the real helper against strict busctl fixtures and attempt live deployment.

RED: 46 tests, five expected failures across playing mpv/browser and unusable Spotify cases (exit 1). Live read-only busctl probe confirmed four mpv instances (one Playing) plus paused Spotify; old selection returned Spotify. Source and live helper bytes matched before editing despite newer live timestamp. README gate: update_in_same_change for stale music priority claims; preserved existing hierarchy and unrelated edits.

GREEN: `python3 tests/test_i3blocks_now_playing_mpris.py` 46 pass; `python3 -m unittest discover -s tests -p 'test_i3blocks*.py'` 79 pass, exit 0. Expected cache-write diagnostic exercised. `git diff --check` passed.

Activation: `fish -c refresh-config` exited 1 due to pre-existing duplicate MIME sources. Preserved them. Targeted `install -m 755` succeeded; `cmp` source/live exit 0; installed helper returned playing mpv in both fields. Full refresh and physical bar/click observation remain unverified. Commit-session requested after implementation; delivery milestone below.

Review: minimal selection diff preserves bounds, browser eligibility, cache and click safety. README and smoke steps updated in place, preserving existing dirty edits. No unrelated configuration repaired.

## Handoff
Atomic plan: reproduce priority conflict, change shared selector, verify and deploy only helper (complete).
Automated check: `python3 -m unittest discover -s tests -p 'test_i3blocks*.py'`.
Manual checks: with Spotify paused and mpv playing run installed helper; with both playing Spotify wins; with both paused Spotify wins; wait five seconds and check bar; left-click controls displayed player. Retain dedicated FlaviBot identity restrictions.
Docs: README music priority, existing smoke checks, living incident and this plan.
Cursor prompt: “Review plans/music-playing-priority.md and its selector/tests/docs diff. Preserve unrelated dirty files. Verify playing-first selection and owner-bound clicks. Do not change global media keys.”
Suggested commit: `fix(i3blocks): prioritize playing media over paused Spotify`.

## Delivery milestone
`fix(i3blocks): prioritize playing media over paused Spotify`: implementation, focused tests, README music hunks, smoke music hunks, this plan, incident and its single reviewed ledger record. Scope helper reports unsafe (no writing actions recognized); direct-write fallback uses observed edits and the captured initial dirty baseline, session `01a1c678-ba1d-7560-8135-5a0e235d1947`. Mixed files stage only attributable hunks. All unrelated dirty work stays excluded.
README gate rerun: `./scripts/executable_readme-recruiter-sync` returned `pass_no_change` (exit 0). Fresh regression rerun: 79 tests passed, exit 0. Privacy check required immediately before commit. Push target: `main` to `origin/main` (`Kevin-Mok/ai-cli-workflow`). Remaining: commit, push and report; runtime limitation remains full refresh MIME conflict. Rollback is a follow-up revert of this focused commit, without rewriting history.
