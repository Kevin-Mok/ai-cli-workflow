# mpv counter state verification blocked by sandbox

The initial normal-state CLI check could not create its database in the read-only
home directory. Repeat the check with approved filesystem access; keep automated
playback fixtures inside temporary directories.

## Symptom, impact and evidence

`python3 scripts/executable_mpv-count --plain --count /tmp/mpv-count-unplayed-example.mp4`
printed `[Errno 30] Read-only file system: '/home/kevin/.local/state/mpv-count'`
and returned 1. No counts were lost. Temporary-state headless playback tests had
already passed.

## Lookup and applicability

Read tracked postmortem-memory instructions and searched `read-only sandbox home
directory`. Sandbox write boundaries apply; an application change is unnecessary.
The read-only filesystem error identifies the denied directory directly.

## Root cause and resolution

Workspace-only filesystem permissions exclude the normal XDG state directory.
Repeating the exact CLI check with approved elevated access returned `Plays: 0`
and exit 0. Status: verified workaround, CLI runtime scope. No production change
was needed. GUI video output remains outside this verification.

## Learning and next steps

No new learning: this is the existing filesystem-boundary limitation; use a
writable temporary XDG_STATE_HOME for isolated tests and approved access for the
normal persistence check. Record this report in the tracked reviewed ledger.

## Final regression sandbox boundary

A fresh focused test later returned 1 with `[Errno 1] Operation not permitted`
while opening local mpv IPC. Earlier passes used the same real playback test.
Lookup `Operation not permitted socket sandbox` confirmed applicability of local
socket permission boundaries. The exact focused unittest rerun with approved
access exited 0 and passed real loop counting, persistence and path handling.
Status: verified workaround, headless runtime scope; no implementation change.

## Shortcut delivery verification boundaries

A default-sandbox Fish invocation triggered startup attempts to write fnm
multishell links and universal variables, which the read-only home boundary
rejected. Avoid normal startup for syntax checks; inspect only the target
abbreviation in an approved fresh shell. Also, this installed Fish prints every
abbreviation for `abbr --show cgc`; filter the output rather than exposing the
full mapping list. Refresh-config itself succeeded with approved access.

The broader `python3 -m unittest discover -s tests -p test_fish_alias.py -v`
failed before collecting tests: SyntaxError at line 74, in the pre-existing
`test_example-user_home_directory_normalization` identifier. The focused mpv
suite passed both tests. Leave the unrelated alias-test source unchanged;
report the broader check as blocked rather than claiming it passed.

## Migration-preserved alias activation

Refresh succeeded but cgc was absent from the generated file and fresh-shell
inspection exited 1. `chezmoi ignored` includes aliases/key_aliases; exact-target
status reports it is not managed. Existing operational-drift guidance at
migration-preserved targets applies: merge only the authorized new mapping into
the preserved live file, keeping other contents, then refresh and verify.
Targeted insertion and a second approved refresh succeeded. Generated Fish
syntax passed; fresh interactive inspection returned the exact cgc expansion
and exit 0. Status: verified workaround at installed-shell runtime scope.
No broad alias-file replacement and no playback launched during alias checks.
