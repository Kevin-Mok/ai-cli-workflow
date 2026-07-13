# ExecPlan: Terminal GPG Pinentry Default

- [x] Add a regression test that requires the tracked GPG Agent config and its template to select `/usr/bin/pinentry-curses`.
- [x] Run `bash tests/test_gpg_agent_terminal_pinentry.sh` and confirm it fails because the terminal pinentry setting is absent.
- [x] Add `pinentry-program /usr/bin/pinentry-curses` to `private_dot_gnupg/gpg-agent.conf` and `private_dot_gnupg/gpg-agent-template.conf`, and export `GPG_TTY` from the tracked Fish, Bash, and Zsh interactive-shell configs.
- [x] Add a Terminal smoke test for `pass edit <non-sensitive-test-entry>` after `gpgconf --kill gpg-agent`.
- [x] Run the focused regression test, the existing config-refresh test, and the README consistency gate.
- [x] Apply the GPG and shell targets with ChezMoi and restart GPG Agent.
- [ ] Manually verify the terminal prompt with `pass edit <non-sensitive-test-entry>`.

## Review

- Automated verification passed. `refresh-config` could not finish non-interactively because its unrelated private Codex entry requires `/dev/tty`, so the verified GPG and shell targets were applied directly with `chezmoi apply --no-tty` instead. GPG Agent was restarted; interactive `pass edit` verification remains pending because it requires a real password-store prompt.
