# Display song name before artist

Change the i3 music block to show `Title - Artist`, keeping player selection,
controls, escaped markup, title-only fallback and adaptive fitting unchanged.

## Scope and decisions

One formatting line in `executable_now_playing_mpris`, existing output assertions,
README and smoke expectations. Metadata without a separate artist remains verbatim.
No parsing of embedded artist/title strings or new dependencies. The subsequent
`commit-session` request authorizes committing and pushing this session only.

## Protected state and risks

Initial `git status --short` captured; preserve all prior changes, including README,
smoke tests and 4K wrapper/tests. Source/live helper bytes matched before edits.
Rollback: reverse the formatting line and apply configuration. Long names may
still ellipsize under workspace pressure.

## Checklist

- [x] Inspect source, config caller, tests, prior plan and relevant preferences.
- [x] Observe updated name-first assertions fail, then swap formatting operands.
- [x] Run music and layout regressions; update documentation.
- [x] Run refresh-config and inspect deployed helper output.

## Verification and review

Automated: `/usr/bin/python3 tests/test_i3blocks_now_playing_mpris.py` and
`/usr/bin/python3 tests/test_i3blocks_4k_status.py`.
Runtime: run deployed helper, compare source/live bytes and inspect a real i3blocks
frame. Manual: playing and paused songs show name first; title-only songs have no
separator; controls and long-song fitting retain their existing behavior.

## Cursor continuation prompt

Finish this plan only, preserving existing dirty changes. Verify name-first music
output and refresh-config deployment. Commit/push only this session when authorized. Suggested commit subject:
`fix(i3): display song name before artist`.

## Observed evidence

- RED: 39 now-playing tests ran; 27 failed on the expected artist-first output.
- GREEN: 39 now-playing tests and 19 layout tests passed, both exit 0.
  Cache-save diagnostic was an intentionally exercised error path.
- `fish -c refresh-config`: REFRESH COMPLETE, exit 0.
- `cmp` confirmed deployed/source helper bytes match, exit 0.
- Deployed helper emitted paused `the cure - Olivia Rodrigo` on both text lines.
  Real i3blocks JSON frame also contained that title-first text with the music
  label and expected compact fallback. Live checks exited 0.
- Scoped whitespace check passed. Reviewed production diff changes only the
  formatting operands. README/smoke changes preserve unrelated dirty hunks.
- No full-repository suite, physical clicks, screenshots or restart performed;
  polling loads the helper anew. Playing, paused, no-artist, markup and click
  behavior are covered by focused tests. No commit/push requested or performed.

## Delivery milestone: fix(i3): display song name before artist

Commit scope: helper formatting, existing output assertions, focused README/smoke
expectations and this plan. Direct-write fallback for session
`01a189f4-7b5e-7a53-900e-073253f63232`: scope helper could not detect nested tool
writes; the conversation records the initial status and each of these edits.
Only independent song-output documentation changes enter the commit; mixed layout
hunks remain with the earlier layout session. No other dirty work is included.
README gate: `./scripts/executable_readme-recruiter-sync` returned
`pass_no_change`, exit 0. Rollback is a normal revert of this focused commit.
All implementation work is complete; final privacy gate, commit and upstream push
are the delivery steps. No implementation blockers remain.

Commit-turn focused checks reran: 39 now-playing and 19 layout tests passed, exits
0. An initial Git write hit the documented read-only sandbox; approved escalation
restored scoped staging. The incident report and its no-new-learning ledger entry
are included, while other ledger modifications remain uncommitted.
