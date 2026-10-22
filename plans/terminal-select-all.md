# Select full terminal history

Make Ctrl+A select all retained text in Kitty or the active tmux pane, including offscreen history. Ctrl+Shift+C copies the highlight; Escape returns tmux to live input.

## Scope and decisions

Use the existing Kitty/tmux copy adapter for foreground detection. Keep the Ctrl+Space tmux prefix. Ctrl+A replaces application line-start behavior. Only retained history (50,000 configured lines) can be selected; deleted history is unavailable. Native Kitty selection needs its embedded Screen API because Kitty has no public select-all action. Do not add dependencies or change existing copy behavior.

Files: Kitty config/adapter, tmux config, focused existing tests, README, shared smoke tests. Preserve all pre-existing dirty changes recorded at turn start. Local tmux config differs only in a contact comment; retain the public-safe tracked placeholder rather than importing contact information.

## Checklist

- [x] Inspect configuration, docs, preferences and existing tests; capture initial dirty state.
- [x] Add defining RED tests for full retained selection, repeated selection, and native/tmux routing.
- [x] Implement minimal binding/adapter changes and run focused regressions.
- [x] Update README/smoke checks, run refresh-config and verify deployed behavior.
- [x] Record final evidence and remaining limits.

## Verification

Use real Kitty embedded Screen with more lines than the viewport to assert first/last markers and wrapping survive selection. Use existing isolated tmux PTY fixture to press Ctrl+A, copy full history and compare logical content; repeat in both copy tables, then Escape and type. Run existing Kitty routing and tmux scrolling regression suites. Deploy with `fish -c refresh-config`; verify deployed bytes and reload live config where accessible. Manual: generate 200 numbered lines in Kitty, repeat inside tmux, press Ctrl+A then Ctrl+Shift+C, paste and check first/last lines.

## Risks and rollback

Kitty Screen API is internal and must be checked against installed 0.49.2. No history beyond retained limits can be restored. Revert only this task's adapter/bindings to roll back; preserve unrelated edits. Commit-session now authorized; include this plan with the implementation.

## Evidence and review

Initial versions: Kitty 0.49.2; tmux 3.4. Kitty remote-control socket `/tmp/kitty` unavailable; live activation needs actual socket discovery. Initial mistaken refresh-script path was diagnostic only (see path-probe incident); correct helper is the Fish function. RED: Kitty routing suite had 6 passes and 2 expected failures; real tmux PTY Ctrl+A test failed waiting for selection (after permitted host execution). GREEN: `python3 -B tests/test_kitty_tmux_copy.py` passed 8 tests; `python3 -B tests/test_tmux_scrolling.py` passed 22 tests using host socket access. `kitty +runpy "import runpy; runpy.run_path('tests/kitty_select_all_check.py', run_name='__main__')"` passed real Screen selection with 200 lines, evicted history, a single line, wrapping and repetition.

`fish -c refresh-config` exited 0. Both deployed Kitty files matched source, and load-config succeeded on 13 actual sockets. A temporary real Kitty tab selected exactly CHECK 0001 through CHECK 0200; it was closed afterward. `.tmux.conf` is migration-preserved/ignored, so refresh intentionally skipped it: merged only the four-line binding/comment block into the live file, preserving all other local content. Live root/copy-mode/copy-mode-vi Ctrl+A bindings verified. See the activation incident for diagnostic failures and the preserved-target learning.

Focused review found no correctness issues. README and shared smoke checks describe retained history, copy/Escape behavior and Ctrl+A replacement. Commit-session authorized for current-session hunks only. Manual physical-key and clipboard-paste inspection remains unperformed; tmux native PTY input and real Kitty selection were exercised. Kitty selection relies on internal Screen APIs verified on 0.49.2; rerun the embedded check after upgrades. Rollback removes the task's binding blocks and select-all branch, then refreshes Kitty and merges the matching removal into preserved tmux config.


## Delivery milestone — feat(terminal): select full history with Ctrl+A

Implementation, regression checks, activation, README and smoke documentation are complete. No behavior work remains; physical keyboard/clipboard acceptance is manual. The scope helper could not detect tool-composed writes for session `01a1645f-264b-7053-9f91-390850db70e1`; use direct-write evidence from this conversation and the initial pre-write status. Stage whole session-owned files and only the select-all/activation additions in mixed README, smoke tests, lessons, operational guidance and ledger files. Leave every unrelated dirty hunk unstaged. README gate passed. Next: verify scoped candidate, run privacy gate, commit and push once to origin/main. Push outcome will be reported with the resulting commit hash.
