# tmux history scrolling diagnosis

Identify the owner of each mouse gesture, test pane history in a disposable server, and preserve application mouse handling while providing an explicit history override.

## Symptom and impact

User reports dragging in tmux highlights blue without moving the viewport like raw Kitty's scrollbar. Installed tmux 3.4 has mouse enabled but only 2,000 history rows. Supported configuration improvement is deployed; exact scrollbar parity remains unavailable on tmux 3.4.

## Lookup and evidence

Postmortem query `tmux mouse scrollbar selection` returned no applicable tmux mouse fix; matches concern unrelated products. Source/live config match. Effective root MouseDrag1Pane starts copy mode selection or forwards application events; WheelUpPane enters copy-mode -e or forwards to mouse-aware applications. tmux 3.6 upstream CHANGES introduces native pane-scrollbars; 3.4 installed manual has none. Kitty's thumb cannot browse tmux-owned pane history.

## Reproducer setup correction

Initial isolated test loaded the complete config before any pane existed. Existing `set-option -gp allow-passthrough on` produced `no current pane`, and tmux displayed the error overlay, invalidating two gesture assertions. This is a harness setup issue, not scrolling RED evidence. Start the test server with /dev/null, create a placeholder pane, source the real config, then create the history fixture so configured history depth applies. Do not change the unrelated passthrough setting in this task. The original 3,000-line fixture did show the oldest retained line was 1,001, confirming the 2,000-row limit.

## Status and next steps

Verified workaround for pane history access: Alt+wheel bypasses application mouse ownership; 50,000-row retention applies to new panes. Native draggable scrollbar remains unavailable on installed tmux 3.4. Preserve normal selection, clipboard and mouse-aware applications; do not install/upgrade tmux or terminate production sessions.

## RED and GREEN progress

Corrected RED: three real-PTY tests returned 1 with exactly two expected failures (Alt+wheel app override absent and history record 000001 discarded); default wheel, selection and typing passed. After adding 50,000-row history and Alt+wheel bindings, three tests passed (exit 0). Strengthening selection-release coverage initially selected only digits at column 10, then incorrectly expected the HISTORY prefix; use column 1 to select the full record. This was a test-coordinate expectation error, not a production failure. Subsequent deployment and isolated desktop checks are recorded below.

Additional read-only probe mistakes: guessed ~/.local/share/chezmoi was absent, and guessed snapshot-codex-config.fish/dot_gitconfig paths were absent. `rg --files` and `chezmoi source-path ~/.gitconfig` resolved the actual executable and dot_gitconfig.tmpl. Source/live Codex and actual Git config bytes match before refresh. These diagnostic misses changed no behavior. Use resolver output rather than guessed paths.

## Live command transport correction

A shell-escaped `\;` argument in the first direct binding reload was interpreted by tmux as a separator between client commands instead of part of the binding body. The observed root binding contained only select-pane; subsequent copy-mode/scroll commands ran on the current pane. Use source-file with an extracted configuration block to install multi-command bindings without the CLI separator ambiguity. Restore the copy mode entered by this reload, then verify complete binding bodies. No sessions were killed and no history cleared.

## Desktop verification isolation

Shared-display checks could not establish mouse delivery: focus/pointer changed to other windows between events and screenshots. They are not passing GUI evidence. Moved graphical verification to a disposable Xvfb display using the same installed Kitty config, avoiding shared pointer/focus races. First Xvfb attempt found the mapped Kitty window before its remote-control socket existed, then failed `Failed to connect ... no such file or directory`. Wait for socket existence before remote queries; this is a startup race in the verification harness. Source/live deployment remains valid.

The next isolated GUI check reached earlier history and returned from copy mode, but typing verification timed out. Inspection of its retained pane showed `INPUT> hellokeyReturn`: xdotool's `type` consumes remaining arguments as text, so `key Return` was typed rather than executed. Split typing and Return into separate subprocess calls. Two failed disposable servers were retained after helper termination; explicitly close only those known task-created sockets. The harness now cleans its own socket on failure.

The following GUI run passed shell wheel, typing, text drag and edge drag but timed out closing the helper. Its harness sent Escape unconditionally after edge dragging; when the edge gesture had not entered copy mode, Escape went into the live canonical input line. Ctrl+D then flushed pending input rather than signaling EOF. Send Escape only while copy mode is active; close with Ctrl+D at empty live input as the manual procedure specifies. This harness error does not change the scrolling implementation.

## Resolution and final verification

Root cause confirmed: the gesture was selection, while desired draggable pane history requires a native feature absent from tmux3.4. Mouse was already on. A second route limitation is mouse-aware applications receiving ordinary wheel input; tmux pane history was only 2,000 rows. Preserve normal app mouse behavior and selection, add five Alt+wheel bindings and 50,000-row history for new panes, then apply and safely reload only that block.

Six real-PTY tests pass in emacs and vi modes (exit0); all three existing terminal regression scripts pass. Independent review found no important issue and checked multiple-pane targeting. refresh-config completed (log /tmp/refresh-config-20261013-121903-574319.log); protected settings unchanged and deployed config/helper match source. Live full binding bodies and history-limit50000 verified.

Actual Kitty/XTest checks on isolated Xvfb passed (python3 /tmp/tmux-gui-verify.py, exit0): ordinary wheel changed first visible shell history record2952 to2937; application Alt+wheel changed2952 to2940 while ordinary app wheel/click was forwarded. Both downward scrolls returned mode0 and allowed INPUT hello. Text drag and right-edge drag selected with copy scroll position0; no history scrollbar motion. Both helper lifecycles exited0. Images inspected; results /tmp/tmux-gui-results.json. This proves graphical event handling using installed Kitty and live config; shared physical desktop/imwheel acceptance remains separate because concurrent focus/pointer movement invalidated those attempts.

Limitations: no draggable pane scrollbar in3.4 (introduced3.6), existing panes retain prior limits, discarded history is unrecoverable, app document-private history is separate, external xclip delivery unchanged/not retested. No session/history destruction, package upgrade, commit or push. Follow-up: user physical gesture acceptance via documented helper; an upgrade for native scrollbar is separate scope.

## Final concurrent-work snapshot check

Final six tests passed (exit0), but a broad protected-file hash assertion then failed on README.md. Inspection against the recorded snapshot showed only an unrelated Dunst paragraph changed concurrently (notification width/height guidance); the tmux paragraph was intact. Preserve that other work rather than restoring the stale snapshot. Independent checks confirm live/tracked Codex, live/source Git, other protected config, and deployed tmux/helper still match. This diagnostic assertion failure exposed concurrent documentation activity, not refresh corruption. Final diff whitespace check returned0.
