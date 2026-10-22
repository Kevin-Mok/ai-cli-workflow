# Kitty shortcut inspection path

This report records a read-only inspection mistake while adding Kitty font
shortcuts. Use the discovered Fish function rather than guessing a script path.

- Symptom/evidence: `sed` could not read `scripts/executable_refresh-config`;
  that path does not exist. No configuration was changed by the failed read.
- Impact: one unnecessary diagnostic; shortcut work can continue.
- Lookup: query `guessed source path missing` matched
  `local-discover-paths-before-reads`, which explicitly identifies refresh as a
  Fish function. Applicable: the search agent had already located that function.
- Cause/resolution: an unnecessary guessed path was included beside valid reads.
  Read `dot_config/fish/functions/refresh-config.fish` successfully instead.
- Status: resolved inspection error; no runtime fix required.
- Follow-up/learning: no new learning beyond the existing path-discovery finding;
  use the returned inventory and keep this report reviewed in the source ledger.

## Fish inspection sandbox

- `fish -c 'functions refresh-config'` printed the function and exited0, but
  startup attempted writes to fnm, universal variables and generated aliases
  outside the writable roots. Those writes were denied; no successful refresh
  was implied. Use an approved host-side refresh for the required deployment.
- This is the known sandbox/write-boundary limitation already recorded by the
  monitor-font task. No shell-startup configuration change is warranted here.

## Required refresh

Host-side `fish -c refresh-config` exited1 on an existing local change to
`.config/kitty/monitor_font.py`; the private log is
`/tmp/refresh-config.axW3FVOV.log`. The recorded monitor-font incident explains
why scoped deployment is appropriate, although its earlier conflict target was
audio-mute. Preserve the current helper and deploy only reviewed shortcut targets.

## Disposable verification inspection

The verification agent reported two harmless inspection failures: piping `find`
to `head` produced a broken pipe, and Kitty0.49.2 rejected `--debug-config`.
Neither changed tracked/live configuration. Use the already confirmed
`kitty +runpy`/`load_config(..., accumulate_bad_lines=...)` API and bounded
inventory output. No new learning beyond path/API discovery and pipe-consumer
guidance already present in the knowledge base.

## Socket discovery

The inherited `KITTY_LISTEN_ON` value named `/tmp/kitty-18018`, which no longer
existed. i3 validation succeeded (existing wheel-command deprecation warnings)
and reload returned success before Kitty reload failed. Discover owned live
Kitty sockets rather than treating inherited environment as proof of existence.
The verification fixture also initially waited for an exact listen-on name;
Kitty appends a PID. Existing monitor-font smoke discovers by unique prefix,
and the relevant lesson already records that requirement. Correct the fixture
before retry; no existing desktop windows were changed by its failed startup.

The isolated fixture also initially used `windowactivate` without an Xvfb window
manager; direct `windowfocus` is appropriate. Its temporary no-UI query then
treated `boss.list_os_windows()` dictionaries as integer IDs. Pass each `w['id']`
to `os_window_font_size` as the already working monitor adapter does. These are
fixture mistakes; retain explicit API-shape checks and do not alter product code.

A later refresh attempt used `fish --no-config` to avoid unrelated startup, but
that also removed the CLI helper from PATH (`cli-message: command not found`).
Use the normal host Fish environment for this repository's refresh entrypoint.
The ordinary host refresh had already reached its legitimate conflict guard.

## Outcome

Scoped Kitty deployment succeeded; i3's user-approved one-line gaps relocation
validated and reloaded successfully. All16 owned live Kitty instances reloaded,
with each OS window's existing font size preserved. The final disposable real
keypress check passed all five requested/native aliases with a second OS window
unchanged and `bad_lines=[]`; both Kitty and Xvfb were cleaned up. Full refresh
remains limited by the existing monitor helper conflict; no unrelated adoption.

The final live i3 probe initially parsed human-facing `i3-msg -t get_config` as
JSON; that command prints the config text. Use `-r` for the IPC JSON response.
This read-only verifier error did not affect the successful configuration reload.
Normal refresh was repeated after both config changes and again stopped safely
on the same monitor helper conflict (`/tmp/refresh-config.wrOgtkKi.log`).

## Gaps key runtime check

The first real `ctrl+super+shift+plus` injection left all i3 workspace gaps at
zero, despite a validated/reloaded binding. The reproducer failed its expected
nonzero-gap assertion; its finally block successfully restored/confirmed zero
gaps. Investigate actual modifier/symbol delivery and active binding mode before
changing the binding. Kitty's isolated font-key verification remains green.

Resolution: active mode was default and X modifiers were normal. A raw IPC
subscription acknowledged readiness and observed both Ctrl+Super+Shift+Plus and
Ctrl+Super+Shift+= emit `symbol=plus`, modifiers shift/ctrl/Mod4 and the unchanged
command `gaps inner all set 20;gaps outer all set 0`. No binding change was needed;
the workspace-only gap-value assertion was an inadequate behavior probe. The
original zero-gap state was restored. Modifier routing is verified; physical gap
geometry was not accepted by that assertion. Lookup `i3 shifted plus key binding`
matched `local-i3-probe-ipc-unicode`; its raw acknowledged subscription guidance
was applicable and enabled direct evidence. No new reusable finding is needed.

## Session commit privacy review

The isolated candidate's privacy check blocked one `home_path` finding in this
report's source-ledger alias. The public candidate uses the repository's existing
`/home/example/linux-config` alias convention. Keep the actual local alias outside
the commit; the helper compares literal paths, so its local targeted check and
the public alias have different environments. No scanner rule or hook is bypassed.
This repeats existing public-history sanitization guidance; no new finding is
needed. Re-run the exact candidate gate before committing.
