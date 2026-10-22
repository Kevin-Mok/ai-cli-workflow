# UBS i3 keyboard repeat

Make i3's `ubuntu-start` apply the existing fast keyboard repeat defaults without requiring a Fish environment. Reproduce the missing-variable case, add independent defaults, then check startup behavior and the live X11 result.

## Scope and decisions

- `ubs` is Fish's abbreviation for `ubuntu-start`; i3 launches that script directly.
- Fish supplies `XSET_DELAY=200` and `XSET_RATE=90`, but the startup script currently skips `xset` when either variable is absent. Preserve nonempty environment overrides and default absent/empty values independently.
- Scope: startup script, its existing shell regression fixture, README startup note, smoke checklist, and this incident's reviewed memory. No new dependencies or changes to desktop services.
- Current live `xset q` already shows 200/90; this does not establish the values at login. Restricted execution cannot access X11; approved host execution can.
- Initial dirty state includes unrelated postmortems, three memory reference files and `sources.json`, two plans, and five prompts. Preserve them; only append this report's memory record to the already-dirty ledger.

## Checklist

- [x] Inspect startup chain and relevant incident knowledge; capture initial Git status.
- [x] Add and observe a failing startup reproducer with missing variables.
- [x] Default missing/empty values independently while preserving overrides.
- [x] Run startup regressions, update README/manual checks, refresh configuration and verify live repeat settings.
- [x] Review final diff and record incident learning and remaining limitations.

## Risks and rollback

Run the startup regression with temporary HOME and stubbed external desktop commands to avoid mounts/services/theme changes. Do not restart the desktop to test this fix. Preserve newer live managed-file changes before applying. Rollback is restoring the previous startup rate guard; overrides continue working. Fresh login and physical typing remain manual acceptance checks.

## Verification

- RED/GREEN: run the actual Bash startup script under the existing external-command fixture with neither, one, empty, and both repeat variables; observe emitted `xset` arguments.
- Broader checks: existing ubuntu-start, keyboard-remap and i3 startup tests; Bash syntax and diff whitespace checks.
- Runtime: `refresh-config`, then exercise the startup script's repeat operation on X11 without inherited `XSET_*`, and query `xset q`.
- Manual: at the next fresh i3 login, before a Fish terminal can initialize exports, verify fast key repetition and 200/90 through `xset q`. No sudo is required for repeat settings.

## Progress and review

Lookup `ubuntu-start` found the previous wallpaper mount finding; that remedy does not address missing repeat variables. A live `xset q` failed only inside the sandbox and succeeded via permitted host execution.

The defining test exited 1 before implementation: `expected startup repeat command "r rate 200 90", got ""`. The fix replaces the two-variable guard with independent Bash defaults. The live script is older than source (October 9 versus October 20), so no newer live source adoption is needed. This host's non-GUI chezmoi configuration ignores desktop scripts; deployment must preserve unrelated differences in the existing live script. A `pgrep -x i3` inspection found no current i3 process, so fresh-i3-login activation cannot be established here.

### Verification evidence

- `bash tests/test_ubuntu_start.sh`: RED exit 1 above; GREEN exit 0 for missing, empty, partial and full overrides plus unavailable optional xset.
- `bash tests/test_shell_keyboard_remaps.sh`, `bash tests/test_i3_speechnotes_dictation_binding.sh`, `bash tests/test_apply_pywal_theme.sh`: all exit 0.
- `bash -n scripts/executable_ubuntu-start tests/test_ubuntu_start.sh`: exit 0. The delegated runner first guessed a nonexistent startup path; corrected to these actual files.
- `python3 /tmp/apply-ubs-repeat.py`: exit 0; invoked the actual `refresh-config` with a temporary source containing only the live script plus this correction. `REFRESH COMPLETE`; installed bytes matched the intended merge exactly. Unrelated managed targets were not applied.
- `python3 /tmp/probe-ubs-repeat.py`: final exit 0; real installed startup script against real X11 with unrelated commands absent from PATH. Missing/empty => 200/90; delay-only => 300/90; rate-only => 200/50; both => 300/50; restored 200/90. An initial probe wrongly expected a requested 60 to be reported exactly (server reports 62); corrected the temporary probe to use 50, without changing production or the argument regression at 60.
- README documents defaults/overrides; smoke checklist includes fresh login before Fish and manual missing-variable startup. No desktop restart or physical typing test performed.
- `python3 dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/example/linux-config/docs/postmortem/2026-10-21-ubs-key-repeat.md`: exit 0, no errors or missing/changed sources. Reviewed SHA-256 `a7bc73007b5411bbf81844f5d0cc130bca4584625d0a24305f712e112657b561`, finding `local-ubs-repeat-without-shell-exports`; appended guidance and a local lesson while preserving pre-existing dirty ledger/reference content.
- Final implementation/test/README/smoke diff reviewed; `git diff --check` exit 0. Live installation preserves the older script's unrelated differences; general chezmoi status remains outside this task's deployment scope.

### Delivery notes

Atomic implementation: reproduce absent exports, independently default the existing xset call, deploy the correction, and verify arguments plus live server state. Rollback changes only the two repeat-setting lines. No commit or push requested.

Suggested commit: `fix(i3): apply repeat defaults without fish exports` (include this plan, regression, README/smoke changes and reviewed incident learning together).

Paste-ready Cursor review prompt:

```text
Review the UBS repeat fix in scripts/executable_ubuntu-start and tests/test_ubuntu_start.sh against plans/ubs-key-repeat.md. Confirm missing/empty values use 200/90 independently, nonempty overrides survive, optional xset remains optional, and no unrelated dirty changes are included. Run the four documented shell regressions and Bash syntax check. Review README and smoke instructions. Do not restart i3 or commit unrelated work. Fresh-login acceptance requires the actual i3 host.
```

### Authorized delivery milestone

Included in fix(i3): apply repeat defaults without fish exports under the user-requested full-worktree series. Fresh startup, keyboard-remap, dictation-binding and pywal regressions plus Bash syntax pass; targeted memory check passes. README gate passes. Related documentation and evidence ship together; fresh-login acceptance remains manual. See plans/discord-volume-delivery.md for series/push status.
