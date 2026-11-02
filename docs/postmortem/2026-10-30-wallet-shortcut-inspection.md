# Wallet shortcut inspection hit restricted startup writes

This report records a failed inspection while adding the wl directory abbreviation and the scoped activation checks.

- Symptom and evidence: configured `fish -c` inspection attempted fnm links, universal variables and `/home/kevin/aliases/.key_aliases` writes on read-only paths. Guessed sync-shortcuts/config source filenames also did not exist; the real generator is `scripts/executable_sync-shortcuts`.
- Impact: noisy inspection; no intended shortcut command executed. Initial repository status was clean.
- Lookup: searched `fish startup read-only sandbox`; inspected the 2026-10-23 agent-policy Fish inspection report. It matches the configured-shell side effects; use no-config Fish and discovered source paths.
- Cause: configured Fish loads startup side effects even for function inspection; source paths were guessed rather than discovered.
- Refresh evidence: isolated `refresh-config` exited 1 at the pre-existing `.config/mimeapps.list` conflict (private log `/tmp/refresh-config.eBLTriTE.log`). The guard stopped rather than adopting local drift.
- Resolution: changed only the live wl command line to a comment and added the requested directory line; retained every other live catalog byte, including private local differences from sanitized source. Ran the existing sync-shortcuts generator.
- Verification: generator and `fish -n ~/.config/fish/key_abbr.fish` exited 0. Isolated Fish inspection returned exactly `abbr -a -- wl 'cd ~/coding/wallet-gas-cost'`. The supplied expansion was never executed.
- Status: shortcut deployed through a verified scoped workaround; full refresh remains blocked by unrelated mimeapps drift. Existing interactive shells must source the generated file or open a new shell.
- Learning: no new reusable finding; the reviewed Fish inspection incident already covers no-config inspection, and scoped deployment preserves unrelated local differences. No sandbox repair or full refresh success is claimed.

## Commit verification follow-up

- Symptom: `python3 -B tests/test_fish_alias.py` exited 1 before running tests because line 74 defines `test_example-user_home_directory_normalization`, an invalid Python identifier.
- Evidence and scope: the test file is unchanged from HEAD and outside this session's edits. No tests ran and no retry or test repair was attempted.
- Lookup: searched `SyntaxError hyphen identifier Python`; returned AST-edit and literal-emission findings do not establish a remedy for this existing test artifact. Direct source inspection confirms the parse blocker.
- Status: unresolved suite blocker, recorded as a best-effort validation warning. Installed abbreviation, generated syntax, repeated-request no-op and README gate remain independently verified.
- Learning: no new reusable finding from this pre-existing source parse error. Keep it distinct from successful shortcut activation and do not claim suite coverage.
