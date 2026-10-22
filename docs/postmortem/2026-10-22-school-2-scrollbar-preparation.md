# school-2 scrollbar preparation

Diagnose the missing scrollbar and prepare a separate tmux upgrade while preserving all running sessions.

## Symptom and impact

The school-2 session has no draggable scrollbar. Live default server reports tmux 3.4, with school-2 (13 windows) and five other sessions. Native pane scrollbars require tmux 3.6 or later. No production session has been restarted.

## Lookup and evidence

Search `tmux scrollbar` returned `local-tmux-history-mouse-ownership`: applicable because live server and client both report 3.4. Existing plans/tmux-kitty-scrolling.md already documents this limitation. Upstream https://github.com/tmux/tmux/issues/4699 confirms support added in 3.6.

Initial sandboxed tmux queries returned `Operation not permitted`; the approved scoped host query succeeded. Search `tmux sandbox socket Operation not permitted` returned existing execution-environment guidance; this was an access boundary, not a broken tmux socket. A diagnostic shell returned status 2 because optional versioned binary paths were absent. Development-header probes confirmed libevent/ncurses development packages are absent; this is a preparation prerequisite, not a tmux runtime fault.

## Authorized scope

User chose: prepare the upgrade and keep all current sessions running. Prepare a versioned binary and isolated scrollbar configuration, verify on a separate disposable socket, leave the default executable and server untouched. Migration and physical scrollbar acceptance remain pending.

## Build prerequisite failure

The first 3.8 configure exited 1 with `yacc not found` after accepting the extracted libevent headers and runtime library. No installation or session modification occurred. Next: retrieve a local bison package and point configure at its yacc-compatible parser; keep all prerequisites under /tmp.

The first bison extraction used a relative archive glob from the source subdirectory and failed before extraction. Corrected to the absolute downloaded archive path; no external state changed. Search for yacc found no applicable parser-build guidance.

The absolute `YACC` value including `-y` still failed configure's executable lookup. Inspection confirmed its program-name lookup; corrected to PATH pointing at extracted binaries, YACC=bison and YFLAGS=-y. This is build configuration only.

## Preparation progress

Configure succeeded after putting the extracted bison executable on PATH with YACC=bison and YFLAGS=-y. Build exited 0; binary reports tmux 3.8 and links only existing host runtime libraries. Versioned install: ~/.local/opt/tmux-3.8/bin/tmux with matching man page. /usr/bin/tmux and server PID 28315 (3.4) remain unchanged. The optional refresh-config source-file probe used an incorrect path and returned status 2; repository mapping located dot_config/fish/functions/refresh-config.fish. No refresh is required because no tracked configuration changed; only the preview script is deployed directly.

The initial disposable runtime probe checked only window-local option overrides (`show-options -wv`) after setting a global default and failed its assertion. Corrected the probe to query the configured global option (`-gwv`); no production changes or speculative repair.

## Resolution and limits

Prepared tmux 3.8 from the official release tarball, SHA-256 e79c699c7e949dccd0a4a125e17b8d1261e311b16979dbc8eb34542f3966d82e. Installed binary SHA-256 a381d2f56dcdd582e5dd5c2d153dbbe7cf983e19e611bc670770ca282b4a8c39. Install and matching manual live only under ~/.local/opt/tmux-3.8. Build prerequisites remain extracted under /tmp; no apt packages were installed.

Added --scrollbar to the existing tmux-scrollback-smoke helper and deployed its exact source to ~/scripts/tmux-scrollback-smoke. It pins the versioned binary, uses its existing unique disposable socket, enables pane-scrollbars on only there and retains cleanup isolation. No default PATH, launcher or tmux configuration was changed.

Defining tests first failed twice for the absent --scrollbar option, then both passed. Real attached PTY scrollbar drag passed on the prepared binary: history_size 3579, scroll_position 3578, copy mode entered and INPUT hello accepted after cancel. Physical Kitty mouse acceptance is not established by PTY events. The original school-2 server remains PID 28315, version 3.4. Migration to give that existing session a scrollbar remains intentionally deferred by user choice.

## Compatibility regression discovered

Fresh combined regression suite (preview + scrolling): tmux 3.4 passes all 24 tests; tmux 3.8 passes 20 and fails 4. Both emacs and vi cases of stationary top-edge selection and bottom-edge scroll movement time out. The prepared scrollbar itself passes separate real PTY drag checks in shell and mouse-aware fixtures. Do not treat 3.8 as a drop-in replacement for the existing 3.4 selection gestures. Current status: preview prepared, activation deferred; root cause of the older edge-gesture differences remains unresolved. No production configuration adjustment is authorized or required for preparation.

## Learning record

Registered local-tmux-38-edge-drag-compatibility as unresolved, supported confidence and runtime evidence: preview scrollbar works, but four existing edge-selection checks fail on 3.8 and pass on 3.4. Root cause remains unconfirmed; this finding does not claim a repair. Existing capability and socket-boundary guidance remains applicable. The report hash and reciprocal source links are updated in tracked postmortem-memory knowledge; targeted check must pass before handoff.

Final live read still reports PID 28315 / tmux 3.4; school-2 now has 14 windows after earlier identical 13-window snapshots. Concurrent session activity is not attributed to this task: no production create/kill/respawn commands were issued. Final helper installed bytes match tracked source (cmp exit 0).

## Preview Kitty launch failure

User's actual preview opens Kitty configuration errors at line 30: --allow-fallback=shifted,ascii is unknown. Host has /usr/bin/kitty 0.32.2 and ~/.local/bin/kitty 0.49.2. The helper launches bare kitty, allowing inherited PATH to select the incompatible system version. Prior verification covered the tmux PTY path but omitted real Kitty launch and therefore missed this boundary. Search `kitty allow-fallback shifted ascii unknown` returned previous selection-copy findings requiring shifted/ASCII fallback; preserve that mapping and target the modern installed Kitty. Defining regression will simulate PATH choosing /usr/bin/kitty while ~/.local/bin/kitty exists.

Graphical verification with forced PATH=/usr/bin:/bin confirmed modern Kitty parses the configuration, but exposed a TPM returned-1 overlay. The helper pins its direct tmux calls, while plugins inherit old system tmux through PATH. Investigate matching child PATH before claiming the graphical preview is clean. The isolated display also reports expected unavailable compositor/settings portal warnings.

## Kitty launch resolution and verification

Confirmed exact parser baseline: /usr/bin/kitty 0.32.2 reports the line-30 allow-fallback error and unknown scrollbar config keys; ~/.local/bin/kitty 0.49.2 parses the same full configuration with zero bad lines. The helper now prefers ~/.local/bin/kitty when present and retains PATH fallback elsewhere. For --scrollbar it prepends the versioned tmux binary directory to child PATH so TPM uses the same client/server version. All changes affect the disposable preview only.

Defining RED assertions independently failed for bare Kitty selection and missing versioned child PATH. Both tests now pass (python3 -B tests/test_tmux_scrollbar_preview.py, exit 0); ASCII help passes. Actual GUI launch under Xvfb with PATH=/usr/bin:/bin exited 0, showed numbered history, visible right scrollbar and exact INPUT hello, and closed only its disposable server. Screenshots inspected under /tmp/school-2-tmux-3.8-build/kitty-preview-{fixed,input}.png. Earlier GUI probe unnecessarily sent Escape at live input; removed that test-only keystroke before confirming exact hello. Expected isolated-display transparency/portal warnings remain unrelated to parsing.

Installed helper bytes match tracked source via cmp. No Kitty config edits or broad refresh were needed; no live tmux session was restarted. Full tmux suites were not repeated for this launcher-only follow-up; previous 3.8 edge-selection limitations remain. Register local-kitty-preview-inherited-path as verified_fix with runtime evidence; retain the separate unresolved edge-gesture finding.

## Commit privacy gate

The first exact candidate scan blocked a home_path reference in the new ledger alias. Public staging must use the established /home/example placeholder while the working ledger retains the physical alias for local targeted checks. The unrelated working-ledger edits remain uncommitted. Retry the privacy gate against the isolated sanitized candidate; no bypass or hook change.

Privacy retry passed for the isolated candidate after replacing only the public ledger alias with /home/example. Working physical-alias knowledge remains usable and its targeted check passes; no private alias is included in the commit.

## Commit index reconciliation failure

Commit dbc6146 (feat(tmux): add isolated native scrollbar preview) succeeded with all nine scoped files and privacy hooks passing. The follow-on shared-index reconciliation failed on the newly tracked incident file because git update-index --cacheinfo omitted --add. The commit remains intact; push was not reached. Working files and unrelated dirty changes were not discarded. Recovery: compare current staged entries against the saved pre-commit baseline and committed entries, then update only matching session entries using --add; preserve concurrent staging. Record the correction in a focused follow-up commit and push the verified series once.

Index recovery completed using --add after matching each entry to the saved baseline or already committed value. Shared index has no residual staged changes; dbc6146 is preserved. Lookup `tmux commit index reconciliation` returned local-git-index-same-filesystem-publish: its preserve-commit/concurrent-index checks apply, but its cross-device rename remedy does not apply to this missing --add argument. No additional memory finding is warranted for this standard Git invocation correction; record the actionable engineering lesson and refresh this report's existing evidence hashes.
