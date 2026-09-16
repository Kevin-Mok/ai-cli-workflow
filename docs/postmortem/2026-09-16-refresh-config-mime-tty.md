# Refresh Config MIME TTY Failure

- Symptom: The broad `chezmoi apply` inside `refresh-config` waited on a locally modified `.config/mimeapps.list` and appeared stuck because helper output was suppressed.
- Impact: `rf`/`refresh-config` blocked the invoking terminal and held the chezmoi persistent-state lock.
- Evidence: PID 359502 (`chezmoi apply`) held `~/.config/chezmoi/chezmoistate.boltdb`; `wchan` was `futex_wait_queue`; other chezmoi commands reported a persistent state-lock timeout.
- Root cause: The broad apply attempted an interactive overwrite decision for MIME drift; the hidden prompt made the wait look like a deadlock.
- Resolution: `refresh-config` now uses `chezmoi apply --no-tty --keep-going`, continues shortcut refresh, and reports `REFRESH PARTIAL` with a nonzero status when conflicts remain.
- Verification: The fixed live helper completed within the 20-second timeout, printed the MIME conflict and `REFRESH PARTIAL`, and left no chezmoi process running. The focused regression and Fish syntax checks pass.
- Follow-up: Resolve the MIME association interactively if a fully successful `REFRESH COMPLETE` is required.
