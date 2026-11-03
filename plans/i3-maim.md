# Use maim for i3 screenshots

Replace the i3 region and window screenshot commands with maim while preserving
the original saved filename, directory and PNG clipboard behavior. Dim the
surroundings during region selection without darkening the saved image.

## Scope and decisions

- Four source bindings use `~/scripts/i3-screenshot`; desktop Print/Ctrl+Print
  retain `~/Pictures/screenshots/desktop/unsorted/`, laptop shortcuts retain ~/tmp.
- The shared Bash helper keeps shell variables/quoting out of i3's parser.
- Region selection uses a white filled mask and GLSL120 shader in ~/.config/slop:
  frozen desktop at60% brightness outside,100% inside. Window capture has no shader.
- Preserve `screenshot-YYYY-MM-DD_HH:MM:SS.png`; copy only after capture succeeds.
- Keep the full-monitor scrot helper unchanged. No dependencies added; requires
  installed maim/libslopy, xclip, xdotool and an OpenGL-capable selector.
- Live i3 config is chezmoi-ignored. Updated only its screenshot bindings and
  explicitly deployed helper/shaders. rf preserves that live state.

## Completed work

- [x] Capture initial dirty status and inspect tracked/live config.
- [x] Define RED before implementation: scrot bindings and absent helper fail.
- [x] Add helper, four source bindings, two shaders and focused regression check.
- [x] Update README, existing manual smoke check, engineering lesson and postmortem.
- [x] Deploy live helper/shaders and screenshot bindings, preserving local settings.
- [x] Verify runtime selection, file, clipboard, shading, cancellation and rf/reload.
- [x] Review session-only commit scope and README gate.

## Verification evidence

- `python3 tests/test_i3_screenshots.py`: PASS; region/window, directories with
  spaces, original naming, clipboard, failure retention, region-only shader args.
- `bash -n scripts/executable_i3-screenshot`: PASS.
- i3 candidate validation exits0 with pre-existing wheel-command deprecations.
  Refresh completed and reload returned success true.
- Actual injected raw X11 keycode107, after rf/reload, launched helper/maim and
  saved screenshot-2026-11-03_14:49:27.png in the original desktop directory.
- Saved PNG matched clipboard byte-for-byte. Saved brightness ratio1.0 compared
  with the underlying selected area; Escape preserved previous clipboard bytes.
- Direct compositor-overlay samples: selection brightness1.0, surroundings0.593.
- README gate: pass_no_change before final dependency clarification; rerun at commit.
- Focused postmortem-memory check passes. Independent tests agent repeated helper,
  shell syntax and whitespace checks successfully.

## Risks, rollback and review

Physical hardware keypresses, visible flicker and receiving-app paste remain manual
checks in docs/smoke-tests.md. Preview is frozen while selecting; OpenGL is required.
Original grey artifacts were reported in scrot, not independently reproduced.
Restore only original screenshot bindings to roll back; helper can remain unused.
Live backup: /tmp/i3-config-before-maim.conf. No unrelated live settings changed.

Earlier inline quoting passed IPC but actual key invocation dropped the filename;
only actual-key tests established acceptance. Forced --noopengl and huge translucent
border experiments were withdrawn. Runtime shader loader uses ~/.config/slop even
though installed maim help says ~/.config/maim. Incident evidence remains in
[the postmortem](../docs/postmortem/2026-11-03-maim-display-probe.md).

## Delivery milestone

Commit subject: `feat(i3): use maim for shaded screenshot selection`.
Scope uses direct observed writes for thread01a1a252-99e4-7253-8e9d-304f4dd1b259:
the scope helper cannot recognize this session's functions-tool writes. Only
session hunks in initially dirty smoke/memory files are eligible. Preserve unrelated
Fish, Vesktop, tests, SSH report and historical memory edits. Commit and push this
single verified change to origin/main; report resulting hash and push outcome.
