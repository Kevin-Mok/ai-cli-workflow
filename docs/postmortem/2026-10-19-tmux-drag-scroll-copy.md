# tmux drag-to-edge and clipboard investigation

Reproduce the requested held-button edge selection and released-selection copy on a disposable terminal, then distinguish a configuration defect from activation or environment limitations.

## Symptom and impact

User reports blue tmux selection reaches older output but Ctrl+Shift+C does not copy it, while native Kitty selection copies only visible terminal history. Requested selection must extend across screens by holding at the pane top edge.

## Lookup and evidence

Reviewed local-tmux-released-selection-copy-ux and local-tmux-history-mouse-ownership via query `tmux scroll copy clipboard drag`. Prior fix covers released short selections after wheel browsing, not stationary top-edge multi-screen acceptance. Existing bridge must be investigated first.

Unprivileged `tmux list-clients` failed with Operation not permitted; approved read-only execution succeeded. Local process/client inspection finds Kitty -> fish -> tmux, no SSH client in inspected paths. tmux3.4, Kitty0.49.2; effective mouse on, set-clipboard external and release/User0 bindings match intended interaction. Kitty config/adapter match deployed source. Full tmux comparison differs outside the interaction block; no conclusion of stale interaction settings from that difference.

## Status and next steps

Confirmed copy cause: live Kitty no-UI inspection shows the foreground group leader is `fish -c tmux-attach ...` in both inspected clients. The existing detector checks only the leader command, missing the tmux group member. Live loaded mappings include the intended shifted/ASCII fallback and clipboard writes are permitted. One inspected window also has a native selection; it deliberately takes copy priority. No selection contents read and no production keys sent.

Baseline fourteen PTY checks pass; held first-row drag scrolls in emacs/vi without wheel. Actual isolated Kitty direct-tmux selection scrolls 60 rows, copies 2,122 bytes including complete wrapped logical lines, restores the text after reseeding clipboard, and returns to INPUT hello. Repeating with fish -c nesting gives the expected RED: drag works but clipboard copy times out. Thus no drag timer/config correction is justified. Native terminal selection cannot expose pane-owned scrollback by design.

New six-case routing test fails only for fish-owned group (expected RED). Minimal adapter change considers foreground group member commands while retaining direct group-leader lookup for empty process-map cases; all six tests pass. First GUI GREEN attempt still failed: the test loaded source kitty.conf, but relative kitten resolution used the old installed adapter. This is a harness activation gap, not evidence of a broken new detector. Before retry, use an explicit source-adapter override, then verify installed activation separately. Frozen installed Kitty modules require disassembly or official source; a guessed child.py source path was absent. A guessed test_terminal_launcher.sh was also absent; use mapped actual test files. Neither read miss changed files/sessions.

Next: full source/installed GUI checks, refresh, exact smoke docs and reviewed learning; physical desktop acceptance remains pending.

## Verification follow-up

Source-explicit GUI GREEN now passes with fish -c nesting: stationary held-edge drag scrolls 60 rows, released selection copies 2,122 bytes, wrapped text survives, repeat copy restores reseeded clipboard and Escape resumes live input. Scoped refresh-config exited0, private log /tmp/refresh-config.67rYrZ4S.log; only adapter/helper apply targets were allowed because broad status included unrelated live MIME drift and repository artifacts. Actual helper excludes chezmoi scripts/externals/removals and regenerates/reloads shortcuts. Installed/source adapter and helper now match.

Fresh regression run found 21/22 passing; new emacs stationary-edge viewport assertion sampled51 immediately after release then52 after copy (vi passes). Preserve this evidence and investigate timer quiescence before changing production behavior or loosening an assertion. Two notification tests and both existing terminal shell regressions pass. Additional guessed sync-shortcuts function file absent; stop guessing source paths and use mapped script/helper definitions.

Follow-up read-only timing establishes a second defect: after actual SGR release at the edge, selection_active is0 but scrolling continues in both modes, 51->89 over the sampled intervals and128 after further idle/copy. This is continuous, not one queued tick. Keep the failing regression. Official tmux3.4 source confirms stop-selection changes selection state without cancelling dragtimer, whereas the internal drag-release callback does cancel it. Investigate supported release event delivery before choosing a correction.

Installed vi/fish GUI passed exact wrapped clipboard comparison and reseeding after refresh. Expanded GUI app/native run failed before clipboard: after app wheel/click forwarding and Alt+C, the synthetic held drag reported active0 and only3 scrolled rows, rather than more than a viewport. Investigate event ordering separately; do not call app-edge/native GUI acceptance complete. Existing PTY app forwarding remains green.

App retry with the documented Shift-wheel entry and settled modifier release passes held-edge, exact clipboard, repeat copying and Escape/input. Native subcheck then stopped on the first xdotool window search because a normal not-yet-created window returned1; change the harness's readiness predicate to treat a missing window as pending. Raw mouse forwarding on MouseDragEnd before/after stop-selection did not stop the separate continuous timer defect in either key mode; no production change based on those experiments.

## Confirmed release cause and minimum workaround

Actual Kitty pointer events reproduce viewport64->76 over0.6s after release. tmux3.4 [server-client.c](https://github.com/tmux/tmux/blob/3.4/server-client.c#L1822-L1832) clears m.valid before mouse dispatch, calls the release callback during dispatch, and only then sets valid. [cmd.c](https://github.com/tmux/tmux/blob/3.4/cmd.c#L747-L779) rejects invalid mouse events, so [window_copy_drag_release](https://github.com/tmux/tmux/blob/3.4/window-copy.c#L5348-L5369) returns before cancelling the timer. This matches continuous observed50ms scrolling. No public stop-timer command exists.

Disposable runtime experiments show stop-selection followed by an inward cursor step preserves exact selected bytes and viewport in both key modes, at top and bottom edges. The copy cursor becomes interior so the next timer callback cannot rearm; no scrollback or clipboard mechanism added. Implemented guarded cursor-down at top / cursor-up at bottom in the existing release bindings. This is a supported-command workaround for tmux3.4, not an upstream binary repair; panes need an interior text row. Keep deterministic post-release stability regressions in both modes.

Raw native Kitty GUI now passes RAW COPY SAMPLE with the installed adapter. Live installed routing check in both original Kitty clients captures User0 in a fake window without sending real keys, demonstrating group-member detection; custom file kittens are reloaded for each invocation, so existing windows need no restart for this adapter-only edit.

## Final activation interruption

Second scoped refresh exited1 (/tmp/refresh-config.5BcMAXqL.log), before full artifact equality was established. The shell then ran the separately queued activation script despite the preceding failure: both corrected release binding bodies loaded successfully, but deployed .tmux.conf byte equality failed. Sessions/history remain intact; do not claim complete activation. Inspect private refresh diagnostics and exact tmux diff before resolving only owned target drift. Future dependent activation steps must be gated on refresh success.

Exact refresh diagnostic: .tmux.conf is not managed by this machine's current chezmoi configuration, so including it as an apply target is rejected. Preserve that machine-local exclusion; do not change ignore/settings. Required refresh will target managed adapter/helper only, then a narrowly guarded direct replacement will persist the two owned bindings in live .tmux.conf, preserving all other bytes including its pre-existing attribution comment. Source and installed interaction blocks, rather than unrelated comment bytes, must agree. Fresh 24 tests now pass; all four edge tests deliberately fail on pre-fix config (top51->56; bottom77/78->72).

## Resolution and final evidence

Scoped refresh-config now exits0 (/tmp/refresh-config.yVLknFnn.log), then guarded direct replacement persists exactly two release bindings plus their explanatory comment in live .tmux.conf. Exact inverse replacement reproduces every original byte; backup /tmp/tmux-drag-live-backup-yez9lufe. Scoped source-file reload installs both full corrected live binding bodies. Adapter/helper match installed bytes. No ignore rules or private settings changed.

Final installed actual Kitty/Xvfb/XTest checks exit0 in emacs shell and vi app-mouse cases: held stationary first-row drag grows by60/65rows in3s, release viewport remains stable for0.6s and through repeated copying; X11 CLIPBOARD contains2,107/2,108bytes exactly matching a contiguous substring of the original numbered/wrapped logical fixture text. Clipboard reseeding followed by Ctrl+Shift+C restores the selection. Escape resumes INPUT hello. Plain app wheel/click forwarding and raw Kitty RAW COPY SAMPLE copying pass. Harness /tmp/tmux_gui_final_probe.py uses installed tmux/Kitty/adapter plus existing numbered fixture, with isolated displays and clipboards. Nonfatal Xvfb keymap/compositor warnings are unrelated to verified text/state assertions.

Automated:26 scrolling/routing checks pass, two notification checks pass, two terminal shell regressions pass; syntax parsing and whitespace checks pass. One adapter fish-group RED and four pre-fix edge RED tests establish both defects. README, shared smoke instructions and the existing disposable helper now cover exact held-edge gestures, wrapping, native selection priority and clipboard replacement.

Evidence scope: copy detector verified fix; edge-release behavior verified supported-command workaround, not an upstream tmux binary repair. Requires more than two text rows. Physical shared-desktop pointer/clipboard acceptance remains pending; user can run ~/scripts/tmux-scrollback-smoke and --app-mouse, follow the updated gestures and paste into an editor. No production history/session termination, upgrade, commit or push.

Independent review identified a tiny-pane regression risk: with no interior row, cursor parking can move to the opposite edge. Add a >2-row guard and keep the known upstream tiny-pane limit explicit. Defining tiny-pane test initially failed during setup because resize-window height3 produced pane_height3, not2; corrected setup requests actual pane height2 before evaluating the intended RED. Raw test/GUI evidence is being saved for independent review of final claims.

Tiny-pane correction is complete: both defining tests first fail at the expected cursor1 vs0 assertion (/tmp/tmux-tiny-red.log); >2-row guards then preserve original tiny-pane cursor behavior. Fresh full suite26/26 exits0 in23.320s (/tmp/tmux-final-tests.log); broader checks exit0 (/tmp/tmux-broader-tests.log). Final refreshed/activated guarded bindings also pass both installed GUI runs (/tmp/tmux-final-gui-emacs.log, /tmp/tmux-final-gui-vi-app.log). Final refresh log /tmp/refresh-config.tazGZ8Mq.log. Independent reviewer confirms source/API shape, guarded edge behavior and byte-identical installed adapter/helper; only owned tmux lines/comment changed. Tiny-pane timer remains an explicit upstream limit rather than forced cursor movement.

Final independent evidence review read the raw focused/notification logs and GUI harness/results, verified all stated GUI assertions and found no remaining important code issue. Silent shell regression exit0 comes from the test executor's observed combined exit status; the log alone cannot independently prove silent command results. Physical desktop acceptance remains pending.
