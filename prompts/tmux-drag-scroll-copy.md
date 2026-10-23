Fix tmux selection scrolling and clipboard copying in /home/kevin/linux-config.

Observed problem:
The blue-highlighted selection lets me access older tmux output, but
Ctrl+Shift+C does not copy it. The white/native terminal selection copies,
but does not let me select older tmux output.

Required interaction:
1. Start selecting text with the left mouse button.
2. Keep holding the button and drag to the top edge of the pane.
3. While the pointer stays at that edge, continue scrolling into older
   output and extending the same selection across multiple screens.
4. Release the mouse, then press Ctrl+Shift+C.
5. Paste the entire selected text into another application.

“Full screen” means selecting as much text as needed, including across
multiple screens. Copy the selection; no separate copy-all shortcut is needed.

Inspect before changing:
- Follow the repository’s AGENTS.md.
- Read dot_tmux.conf, dot_config/kitty/kitty.conf, and
  dot_config/kitty/tmux_copy.py.
- Read tests/test_tmux_scrolling.py and the tmux section of
  docs/smoke-tests.md.
- Consult docs/postmortem/2026-10-13-tmux-scroll-copy-ux.md and its
  reviewed postmortem-memory finding.

The existing copy bridge already forwards Ctrl+Shift+C to tmux when no
native Kitty selection exists. Investigate activation, shortcut delivery,
selection ownership, and clipboard transport before adding another mechanism.
Establish the actual terminal/tmux/SSH nesting and effective configuration;
tracked settings and the screenshot hostname alone cannot establish it.

Implementation and verification:
- Capture git status and preserve unrelated work and existing sessions.
- Reproduce both reported failures before editing, using the existing
  disposable numbered-history fixture where possible.
- Add the smallest regression coverage, observe the expected failure,
  and implement the minimum supported correction.
- Acceptance requires drag-to-edge scrolling itself. Wheel-only checks
  do not establish this requirement.
- Verify copying after mouse release using actual system clipboard text,
  not only a tmux buffer or a visible highlight.
- Cover a selection exceeding one viewport, wrapped lines, and repeated
  copying after replacing clipboard contents with a different value.
- Preserve native terminal copying, ordinary application mouse handling,
  Escape back to live input, and the existing emacs/vi copy-mode behavior.
- Reuse existing configuration, adapter, fixtures, and tests.
- Keep production sessions and retained history intact.

Run relevant automated checks and actual terminal/clipboard verification.
After configuration changes, follow the required refresh-config workflow
and verify activation. Update the existing smoke instructions and relevant
documentation with the exact final gestures.

Report the demonstrated cause, minimal changes, test results, activation
requirements, and remaining limits. Distinguish isolated GUI evidence from
verification on the user’s physical desktop. If physical interaction cannot
be verified, provide the disposable reproducer and mark that acceptance pending.
