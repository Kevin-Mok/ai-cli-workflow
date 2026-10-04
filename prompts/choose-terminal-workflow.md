Determine whether I should configure my existing Kitty installation, update Kitty, or switch terminal emulators for the greatest practical improvement to my CLI workflow.

Research and recommend only. Use read-only inspection; do not install software, edit configuration, switch defaults, or interrupt running sessions.

My requirements:
- A sleek, minimal, interactive scrollbar at the terminal-window level. Separate scrollbars for every tmux pane are not required.
- Reliable Shift+PageUp/PageDown navigation through long output, preserving ordinary PageUp/PageDown for applications.
- Prefer a thin scrollbar that hides when unnecessary; this appearance preference is flexible.
- Any replacement must have at least 1,000 GitHub stars, verified when researching.
- Retain Ubuntu/i3/X11 compatibility. Prioritize useful customization, responsiveness, stability, and low maintenance.
- Recommend switching only when its benefits justify migration effort.

Known context, observed during prompt preparation:
- Repository: /home/example/linux-config.
- Installed terminal: Kitty 0.49.2.
- Desktop: Ubuntu 24.04, i3, X11.
- Workflow includes fish, tmux, Codex CLI, Vim/Neovim, and multiple concurrent terminal sessions.
- Kitty uses Hack Nerd Font Mono, 0.9 background opacity, pywal colors, and a remote-control socket for theme refresh.
- i3 launches Kitty directly, including a Codex shortcut and a launcher using Kitty-specific font-size arguments.
- I currently experience missing scrollbar/paging functionality. Treat this as a reported symptom, not proof that Kitty lacks those capabilities.
- Screenshot: /home/example/Pictures/screenshots/desktop/unsorted/screenshot-2026-10-04_15:29:47.png. Use it as workflow and appearance context, not proof of which component owns each split or scrolling behavior.

Investigation:
1. Follow repository instructions. Inspect the live configuration against:
   - dot_config/kitty/kitty.conf
   - dot_tmux.conf
   - dot_config/i3/config.tmpl
   - scripts/executable_apply-pywal-theme
   Consult README.md and existing terminal plans for integration history. Reconfirm versions where relevant.

2. Diagnose the existing experience before proposing migration. Check version-specific scrollbar support, default versus overridden keybindings, and whether tmux or an application intercepts paging keys. Distinguish terminal scrollback, tmux copy-mode history, and Codex’s own transcript/navigation. Explain alternate-screen limitations and which layer actually owns the history. Do not promise that a terminal scrollbar can access arbitrary application or tmux history.

3. Compare current Kitty, latest stable Kitty, and up to four credible alternatives. Start with WezTerm, Ghostty, Alacritty, and Konsole, filtering against the requirements rather than assuming eligibility. Use current official documentation, release notes, and upstream repositories. Verify Linux/X11 support, scrollbar availability and customization, paging behavior, release/maintenance status, and GitHub stars. Identify official mirrors explicitly where upstream lives elsewhere.

4. Assess practical speed: startup, input responsiveness, sustained streaming output, scrolling long histories, and resource use with several sessions. Separate measured results, upstream claims, and untested expectations. Do not rank speed from popularity, implementation language, or “GPU accelerated” marketing. Do not imply a faster terminal makes remote AI generation faster. If comparable evidence is unavailable, say so and avoid declaring a performance winner.

5. Evaluate migration costs: existing shortcuts and launch arguments, tmux/Vim keybindings, fish integration, fonts, clipboard, transparency, pywal updates, and relevant terminal protocols. Prefer capabilities I will actually use over feature counts.

Deliver:
- Lead with a clear verdict: configure Kitty, update Kitty, or switch to a named terminal. Give the decisive reasons and confidence.
- A compact comparison table covering scrollbar/paging support, workflow fit, verified popularity, performance evidence, and important drawbacks.
- Explain my current scrolling problem as far as evidence permits. Provide documented settings/keybindings for the recommended setup, distinguishing terminal history from application history.
- A minimal, reversible trial or migration plan covering launchers, theming, acceptance checks, and rollback.
- Acceptance checks for shell scrollback, Codex output, tmux navigation, Vim key compatibility, theme refresh, and responsiveness under representative output.
- Cite primary sources beside material claims and date version/star observations. Clearly separate completed checks from proposed tests.

If no candidate meets all requirements, state the unmet requirement and the best supported compromise. Do not force a replacement recommendation.
