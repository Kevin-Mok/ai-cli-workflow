# Directory abbreviation does not expand

This report tracks interactive verification of the requested or directory shortcut.

- Symptom: user reports or does not expand; intended destination /mnt/usb-8tb/concerts/olivia-rodrigo.
- Evidence: stored generated abbreviation exists; prior syntax and enumeration checks did not exercise interactive expansion.
- Lookup: searched postmortem-memory for "fish reserved keyword abbreviation expansion"; stored-text verification finding reinforces that enumeration is insufficient but does not establish this cause.
- Status: unresolved; build an interactive Fish3.7 reproducer before changing configuration.

- PTY evidence: normal command-position rule captures literal or; anywhere rule expands but needs guard. First capture had a prompt synchronization race; replaced prompt matching with file acknowledgement.
- Broader existing test module cannot parse: pre-existing test_example-user_home_directory_normalization has a hyphenated identifier (line76). Preserve unrelated file; use a standalone stdlib interactive regression.

## Resolution and verification

- Root cause confirmed: Fish3.7 treats or as a keyword, skipping default command-position abbreviation expansion. Stored-name checks cannot prove expansion.
- Fix: generator emits an anywhere/function abbreviation guarded to a fresh buffer containing only or and whitespace. Other directory abbreviations are unchanged.
- Test evidence: standalone stdlib PTY test first failed with actual "or " versus expected cd. A preliminary Popen PTY lacked a controlling terminal; pty.fork corrected the harness. GREEN: interactive fixture test passed, bash syntax passed, live generated Fish syntax passed.
- Runtime: installed generator and full refresh completed (exit0, /tmp/refresh-config.XLuGaB02.log); live-file PTY captures prove standalone expansion, unchanged false; or and echo or. No supplied directory command executed.
- Status: verified fix. Existing open shells must source ~/.config/fish/key_abbr.fish because a subprocess cannot reload a parent shell.
- Limits: shortcut intentionally expands only on a fresh command line; not after a command separator. Existing full fish-alias suite is blocked by its pre-existing invalid identifier; that file was preserved byte-for-byte.
