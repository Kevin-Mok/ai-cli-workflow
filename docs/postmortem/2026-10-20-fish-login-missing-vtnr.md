# Fish login startup missing VT number

This report tracks the startup diagnostic from an unset virtual-terminal number,
the smallest guard repair, and checks that preserve automatic X startup.

- Status: resolved; source and installed guard verified.
- Symptom: new login terminals print `test: Missing argument at index 6` from
  `if test -z "$DISPLAY" -a $XDG_VTNR = 1`.
- Impact: terminal startup emits an error; the X startup guard cannot evaluate
  normally when the virtual-terminal number is absent.
- Evidence: tracked template and installed configuration contain the same guard.
  The installed file is older than the tracked template. Rendering the public
  template produces 132 diff lines and omits the host-specific X login block;
  applying it wholesale would change unrelated local configuration.
- Lookup: `postmortem_memory.py search 'XDG_VTNR'` returned no matches.
  Broader `fish startup` results concern SSH transport/newline handling, not
  missing arguments in this local condition; no prior remedy is applicable.
- Root cause: an unquoted unset Fish variable expands to zero arguments,
  leaving the binary comparison without its left operand.
- Next steps: execute the actual guard with unset/empty VT values; quote its
  scalar comparison operand; verify display/VT/login branches; safely activate
  the one-line change without replacing unrelated local settings.
- Investigation note: an optional documentation lookup used a nonexistent
  `docs/config-sync.md` path and returned exit 2. No file changed; subsequent
  lookup uses inventoried files. This is separate from the startup defect.

## Resolution and verification

Defining RED: `python3 -B tests/test_fish_startup.py` exited 1 with two failures,
both login shells with VT unset (DISPLAY set or absent), reporting the exact
missing-argument diagnostic. Six other scenarios passed. The source repair adds
quotes around `$XDG_VTNR`.

The defining regression now passes all eight scenarios (one table-driven test,
exit 0), and `bash tests/test_refresh_config_function.sh` passes (exit 0).
The installed guard was patched with an exact single byte-string replacement;
the reverse replacement reproduces every byte of the original. A private
rollback copy is in the temporary directory. Broad refresh is intentionally
withheld because its rendered target drops the host's X block and changes 132
diff lines; deploying those unrelated public placeholders is unsafe.

## Pre-existing regression blockers

- `python3 -B tests/test_fish_alias.py`: exit 1 before collection, SyntaxError
  at line 74 from a hyphen in `test_example-user_home_directory_normalization`.
- `bash tests/test_gpg_agent_terminal_pinentry.sh`: exit 1 because the expected
  `private_dot_gnupg/gpg-agent.conf` file is absent.

Neither test nor the GPG configuration was changed by this task. No retry or
unrelated repair was attempted; these checks do not establish regression
coverage. They remain follow-up work separate from the Fish guard defect.

## Runtime verification boundary

The first installed-shell probe reached its success marker with exit 0 and no
missing-argument diagnostic, but the verification wrapper exited 1 because the
workspace sandbox blocked normal startup writes: fnm multishell symlinks under
the runtime directory, Fish universal variables, and generated shortcut caches
outside the checkout. This is an execution-permission failure, not evidence of
a guard regression. Inspect reviewed sandbox guidance before repeating the
same installed-shell probes with permission for normal local startup writes.

The memory search `Read-only file system fnm universal variable` found no
applicable remedy; the observed denied paths directly established the sandbox
boundary. Repeating with approved normal local startup writes passed all three
installed login cases: DISPLAY set/VT missing, both absent, DISPLAY set/VT 1.
Each returned exit 0, reached its success marker, and produced zero stderr
bytes. The original missing-argument error is gone on the actual installed path.

## Limits and follow-up

No real X server was launched; the source regression verifies exact
`startx -- -keeptty` arguments using a harmless executable. A full refresh was
skipped to preserve unrelated local configuration. No commit or push requested.
The existing alias-test syntax error and missing GPG fixture remain unresolved.
Root-cause confidence is confirmed; the guard fix is verified at runtime.

## Follow-up scope correction

The subsequent refresh investigation checked actual managed targets and found
the local Fish config is intentionally unmanaged. Raw template differences did
not establish the real apply scope. After reconciling an unrelated launcher
permission conflict, normal refresh completed successfully. See
[refresh recovery](2026-10-20-refresh-screensaver-mode-conflict.md). The earlier
wholesale-template warning records an initial assumption, corrected here.
