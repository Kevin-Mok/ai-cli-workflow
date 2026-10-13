# tmux scroll and copy gesture mismatch

Make the user's familiar gestures work across Kitty and tmux: Shift+wheel browses pane history, mouse release preserves the highlight, and Ctrl+Shift+C copies it without holding the mouse button.

## Symptoms and impact

User tried Shift+wheel without a held button and Ctrl+Shift+C on a blue highlight; neither worked as expected. Earlier configuration only added Alt+wheel and preserved tmux's default drag-release copy/cancel behavior. Ctrl+Shift+C normally belongs to Kitty's terminal selection, which is separate from tmux's rendered selection. No UX behavior edits yet.

## Lookup and evidence

Query `tmux selection Ctrl Shift clipboard` matched local-tmux-history-mouse-ownership: applies to event/history ownership but does not implement these desired gestures. Effective mouse on, set-clipboard external, extended-keys off. MouseDragEnd1Pane is copy-pipe-and-cancel in both stock mode tables. Kitty clipboard_control permits write-clipboard. Installed Kitty encoding confirms Shift wheel forwards SGR68/69 while mouse tracking is active; raw Kitty keeps native scrolling. F13 encoding is a Kitty extended code rather than portable legacy F13, so use an explicit tmux user-key byte sequence rather than guessing function-key translation.

## Status and next steps

Active diagnosis; create defining RED checks, change persistent selection and copy gesture, preserve raw Kitty copy and ordinary application mouse behavior, verify actual X11 clipboard contents on an isolated display, deploy and document clear usage.

## Environment and read-only probe limits

Native title update failed again with the known local MCP HTTP transport error; keep the prior native title and do not claim service repair. Agent's default exec hit known bwrap loopback error, approved scoped reads work. Installed frozen Kitty modules do not expose source to inspect.getsource; source/disassembly needed. A guessed /tmp/kitty socket and guessed GLFW_KEY_F13 symbol were absent; use process-specific socket and supported symbols. No production mutation from these diagnostic misses.

## Defining RED and initial implementation

Twelve PTY checks returned1: the six new failures were the expected Shift-wheel, release persistence and explicit OSC52 copy gaps in emacs/vi; the six existing checks passed. Actual Kitty/XTest Shift-wheel also failed before implementation. Implemented Shift bindings, stop-selection on release, dedicated User0 explicit copy-selection-no-clear, Escape cancel and a compact on-screen hint. Kitty no-UI adapter prefers native selection, otherwise detects foreground tmux process groups even beneath fish and forwards only the dedicated copy key; raw shell copy stays native. Existing Alt/y mappings preserved. Full GUI/clipboard and deployment evidence pending.

## Actual clipboard check failed

After twelve PTY tests passed, required refresh completed and twelve active owned Kitty processes reloaded successfully. Installed/source artifacts matched. The first actual Kitty/XTest check reached Shift-wheel history and a released highlight, but Ctrl+Shift+C did not put HISTORY text in the X11 clipboard before the deadline. Do not claim the complete copy flow works based on PTY OSC52 evidence. Inspect Kitty logs/mapping dispatch and the foreground adapter before changing or retrying.

Refresh used its documented live-to-source capture: only source model_reasoning_effort followed the already-live value; live Codex bytes preserved. Local .bashrc/.zshrc conflicts were adopted by the helper's existing recovery. Exact backup /tmp/tmux-copy-protected-hy8yam20, log /tmp/refresh-config-20261013-125032-648427.log.

Further diagnostics: native raw Kitty copying also timed out with the new adapter, and direct remote `action kitten tmux_copy.py` did not create a tmux buffer. Copy mode/selection remained1/1 and clipboard retained the seed. This narrows the runtime fault to adapter invocation or detection rather than OSC52/selection commands; inspect a no-UI debug handler before another production change.

No-UI diagnostic handler executed (targetwindow1 exists), native selection empty, but foreground_processes was empty even though child argv was tmux attach. Sending the dedicated key directly in that handler copied successfully, proving the runtime failure is process detection. Inspect supported foreground_cmdline/fallback before changing detection. Direct-action success must not be mislabeled as a keyboard mapping failure.

Confirmed detector cause: terminal fd14 and foreground group matched the tmux client pid, foreground_cmdline showed tmux attach, but cached foreground_processes stayed empty. Query the terminal's foreground group directly and resolve its command; retain supported foreground_cmdline fallback only on tty query errors. This handles fish-launched job control without relying on Kitty's empty process list.

Native-copy isolation: direct no-UI handler saw RAW COPY SAMPLE and copied it correctly; thus native selection/copy APIs work. Installed default Ctrl+Shift+C definition includes shifted/ASCII fallback, while the replacement omitted it. Match the existing shortcut's fallback flags for shifted key delivery, then rerun actual keyboard tests to confirm rather than assuming parser acceptance proves dispatch.

## Strengthened repeat-copy failure

With direct foreground-group detection and the default shifted/ASCII key fallback restored, actual raw Kitty, fish-launched tmux and shell/app copy sequences passed. A stronger check then replaced the X11 clipboard with a different seed before pressing copy again. Repeat copy did not restore the selected text; the same strengthened PTY check saw no second OSC52 write. Do not claim repeat copy based only on an unchanged clipboard value. Investigate whether the transient display-message feedback consumes the next key; if confirmed, move feedback into the nonblocking status line.

Repeat diagnosis: both second keyboard copy and a direct copy-mode command added new tmux buffers, but clipboard remained the replacement seed. Therefore keyboard dispatch was not consumed; clipboard output was suppressed while transient message feedback was active. Move Copied feedback to a pane-local status value and refresh the status line, avoiding a message overlay. Mouse release clears that feedback and freezes the highlight; the copy-status value only displays while a selection exists. Preserve normal status text including the larger-window offset indicator. Verify second OSC52 and clipboard restoration before claiming resolution.

## Resolution and verified outcome

Verified fix, runtime scope: Shift-wheel bindings, drag-release stop-selection, Ctrl+Shift+C adapter/user-key explicit copy-selection-no-clear and one-step Escape. Native Kitty selection takes priority. Foreground detection uses direct terminal group resolution; preserve shifted/ASCII key fallback. Copy feedback uses pane-local status text, not a transient overlay. Existing normal app gestures, Alt-wheel, vi y/xclip and raw Kitty copy are preserved.

Final fourteen PTY tests pass (exit0), including repeated OSC52 and no-selection input. Actual Kitty/XTest on isolated Xvfb passes shell/app workflows with exact X11 clipboard text HISTORY002966|t, persistent released highlight/viewport, clipboard reseeding followed by successful repeated copying, and Escape/live INPUT hello. Native raw fish Kitty copies RAW COPY SAMPLE; fish-launched tmux copies history selection correctly. Images inspected and result files saved in /tmp/tmux-copy-gui-results.json and /tmp/kitty-copy-compat-results.json. Three terminal regressions, syntax parsing and independent correction review pass. Final deployment refresh/reload and reviewed knowledge reconciliation are recorded below.

Limits: native tmux3.4 scrollbar remains absent; this fixes gestures and copying. Existing history limits cannot recover discarded lines. Isolated actual graphical verification is distinct from physical shared-desktop/imwheel acceptance. No upgrade, session/history destruction, commit or push.

## Final activation and learning

Final refresh exit0: /tmp/refresh-config-20261013-130824-696318.log. Scoped source-file installs the final full binding bodies; twelve active owned Kitty instances reload successfully. Source/deployed tmux, Kitty config, adapter and fixture match. Native parser and final whitespace checks pass. Reviewed learning local-tmux-released-selection-copy-ux records the runtime fix and its physical-desktop boundary; targeted hash/alias/schema validation passes. No outstanding task writes, package changes, commit or push.
