# Terminal selection activation checks

A read-only lookup guessed a refresh helper path that does not exist. Use the mapped Fish function for refresh instead.

- Symptom/evidence: `cat scripts/executable_refresh-config` reported no such file; no files were changed by that lookup.
- Impact: diagnostic lookup only; terminal configuration and running sessions unaffected.
- Lookup: postmortem-memory search “missing script path file mapping”; results concern other missing installed helpers, so no remedy applies to this repository path guess.
- Cause: assumed executable-script layout instead of the existing Fish function.
- Resolution: read `dot_config/fish/functions/refresh-config.fish`, which contains the apply/sync/reload implementation.
- Verification: reading that function succeeded (exit 0).
- Path lookup status: resolved; no new reusable learning beyond mapping existing helpers.
- Additional diagnostic evidence: an assumed installed typing-stub path was absent; the tagged upstream source was used instead. Kitty socket access was denied in the sandbox and `/tmp/kitty` was absent outside it. The configured basename produces per-process `/tmp/kitty-PID` sockets; an escalated query to an existing socket succeeded (exit 0).
- Deployment check: refresh-config exited 0 and Kitty files matched, but the tmux byte assertion failed. A focused comparison showed the live tmux file lacks the new Ctrl+A bindings and retains its original contact comment. A glob also included a temporary Python file; only actual socket files should be reloaded. No terminal data was lost.
- Lookup: “deployed bytes local comment difference”; returned AST-offset, cache timestamp and rendered-command findings do not apply. `chezmoi ignored` and a filtered data-membership query established `.tmux.conf` is a migration-preserved target, so successful apply intentionally skips it.
- Root cause: the deployment verifier assumed every tracked target was managed; the refresh operation succeeded within its documented exclusions.
- Resolution: merge only the requested binding block into the preserved live file, retaining every other byte, then source it. Do not remove preservation settings or overwrite local comments.
- Verification: refresh-config exited 0; Kitty configuration and adapter bytes matched; 13 actual Kitty sockets reloaded. Live tmux root/copy-mode/copy-mode-vi Ctrl+A keys each contained history-top, history-bottom and stop-selection. Live temporary Kitty tab selected exactly all 200 lines and was closed. Focused tests: 8 routing and 22 tmux tests passed; real Kitty Screen covered repeated selection, wrapping and retained-history eviction.
- Status: verified workaround for preserved-target deployment; live tmux ownership remains unchanged. Keyboard/clipboard acceptance by the user remains a manual check.
- Learning: `local-chezmoi-preserved-target-activation` records this distinction; targeted ledger check passed with no errors.

- Commit privacy verification: the gate found two `home_path` findings in the plan command and local report alias. Use a repository-relative command and a public-safe alias in the candidate ledger; preserve the real local alias only in the uncommitted working copy for lookup. The block was intentional gate enforcement; no private candidate was committed.
