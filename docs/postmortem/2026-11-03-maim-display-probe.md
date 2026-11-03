# Maim display probe blocked

This report records the desktop-access limitation encountered while checking an
alternative to the user's scrot screenshot shortcut.

- Symptom: `maim --hidecursor --geometry=160x100+0+0 /tmp/i3-maim-alternative-check.png`
  exited 1 with `Error: Failed to open X display: :1` in the restricted runner.
- Impact: basic capture and interactive selection have not been verified. No i3
  configuration or clipboard state changed.
- Lookup: `scrot` returned only the unrelated hidden-workspace titlebar finding;
  `Failed to open X display` returned general sandbox guidance, but no confirmed
  remedy for this desktop display. No screenshot artifact remedy was established.
- Status: verified workaround for the runner limitation. Installed maim 5.7.4 supports region selection, hiding the
  cursor, and disabling OpenGL according to its local help.
- Cause: supported restriction on desktop access in the runner: the identical
  command succeeded with approved escalation, exit 0. `file` identified a valid
  160 x 100 RGBA PNG. No desktop configuration was changed.
- Resolution: scoped approved access bypassed the runner limitation; it did not
  establish a fix for the user's original grey selection marks.
- Next step: user selection and comparison against the original grey marks remain
  manual checks before claiming a fix. Print Screen was confirmed as the user's
  shortcut and maps directly to scrot in the live config.
- Learning: no new reusable remedy; this repeats the existing scoped-access
  workaround, without proving a new X11-specific root cause or selector fix.

## Binding implementation checks

The follow-up binding change initially hit two verification limitations: the test
removed the closing escaped quote with `strip`, and restricted i3 validation
could not write its runtime error log and exited 139. The test now removes exactly
the outer quote pair. Validation will run with scoped runtime access. An earlier
helper lookup used a nonexistent `scripts/executable_refresh-config` path; the
actual helper is `dot_config/fish/functions/refresh-config.fish`.

Resolution: corrected quote extraction passed all four binding checks, including
cancellation. Scoped live candidate validation exited 0 (existing deprecated
wheel commands remain); refresh-config and i3 reload succeeded. Real focused-window
capture produced a PNG in the existing directory whose bytes exactly matched the
clipboard. Physical-key region selection and grey-mark elimination remain manual.
No new reusable learning beyond existing scoped-access and quoting guidance.

## User-reported live regression

After activation the user reports rapid screen flashing during region selection
and no pasteable screenshot. Earlier shell-stub and direct-window checks did not
exercise the physical binding through i3. Status: unresolved; inspect actual i3
command execution and compare selector rendering modes before another remedy.
The `maim` memory lookup returned no matching finding.

Follow-up resolution: removed `--noopengl` from both region bindings and live
Print binding. Picom was confirmed running. Normal direct selection returned 0
and copied identical PNG bytes. The exact i3 IPC region command then saved
`screenshot-2026-11-03_12:13:48.png` under the original desktop directory and
clipboard bytes matched. Two overlapping diagnostic selectors initially prevented
completion; only those known test PIDs were terminated before the isolated check.
This establishes selection/file/clipboard operation, not visual absence of flicker
or physical key behavior. Forced XShape/picom interaction is a supported hypothesis,
not a proven visual root cause. Refresh completed; i3 validation/reload passed.
An overescaped diagnostic IPC quoting probe failed to parse; the real binding's
quoting was retained and verified by the successful isolated capture.

## Operator rollback

User reports the command was unsuccessful and an i3 error, and asks to return to
scrot. Current live file still contains maim; i3 reports that file as loaded.
Validation exits 0 but emits existing wheel_up/down deprecations. These observations
do not reproduce or diagnose the user's error. Earlier IPC capture successes did
not establish physical shortcut acceptance. Restore original scrot bindings now;
maim integration remains unresolved and is withdrawn.

Rollback verified: tracked i3 template now has no diff from HEAD; unrelated smoke
edits remain intact. Live Print and Control+Print use original scrot commands.
i3 reload returned success true; refresh-config completed. The first restricted
refresh attempt could not apply; approved host execution succeeded. A verification
attempt assumed JSON for get_config, but i3-msg renders config as plain text by
default; reading its actual output confirmed the restored commands. Original
wheel-command deprecation warnings remain and were not changed. Grey marks remain
an unresolved original scrot issue. No physical key or receiving-app paste test
was performed during rollback.

## Rollback interpretation corrected

User clarifies that scrot still being active after rf/reload is unwanted. The
assistant had interpreted the preceding ambiguous message as a rollback request;
that interpretation was wrong. Both source and live bindings were deliberately
restored to scrot, explaining persistence without invoking an overwrite bug.
Restore maim normal rendering and check actual injected Print press/release,
selection and clipboard, then repeat rf/reload to prove persistence.

Final root cause evidence: actual injected Print press/release launched maim with
no filename from the inline binding, while IPC invocation had included it. This
reproduced the user path's missing saved file and invalidated the prior shell/IPC
acceptance checks. Removed nested shell logic from i3 config into the shared
`scripts/executable_i3-screenshot`; bindings now only launch that helper. Normal
selector rendering retained; no forced --noopengl. Both source and live bindings
updated, helper installed at ~/scripts/i3-screenshot. Target remains chezmoi-ignored,
so live deployment was explicit; refresh preserves it rather than installing it.

Final verification: refresh-config completed, reload returned success true; actual
Print press/release launched maim with the expected filename. Paced drag created
`screenshot-2026-11-03_14:34:32.png` in the original desktop directory; clipboard
PNG bytes matched. A second actual-key selection cancelled with Escape preserved
clipboard bytes. Helper tests passed for region/window, directories with spaces,
original naming, copy success and capture failure. Physical hardware interaction,
visible flashing and pasting in the user's receiving app remain unverified.

Learning validation initially rejected scalar symptoms/diagnostics; corrected both
to the required nonempty lists. Independent final helper, shell syntax and diff
checks passed. This was a ledger authoring error, not a runtime screenshot failure.

## Raw keycode 107 report

User reports keycode 107 still uses scrot. Live map has Print on both 107 and 218;
previous keysym injection did not prove raw107. Loaded config contains helper
bindings and only commented scrot lines. Inspect raw-key launch before editing.
Initial multi-command inventory returned 1 because absent hotkey daemons make
pgrep nonzero; i3/config/keymap reads themselves succeeded.

Raw107 verification: XTestFakeKeyEvent injected exactly keycode107 press/release,
not a Print keysym lookup. Process inspection showed maim --select --hidecursor
with expected output filename and no scrot process. Paced drag saved
screenshot-2026-11-03_14:39:13.png in original directory; PNG matched clipboard.
No additional live/tracked scrot binding or hotkey daemon was found. No binding
change justified by this evidence. Asked what observable output identifies scrot;
physical keyboard/device and user-observed indication remain unconfirmed.

## Shading verification

User requested dimmed surroundings. Added maim supported large translucent black
border (10000px, alpha0.4), leaving interior unfilled. Stub defining RED then GREEN.
Initial pixel comparison using maim root captures found outside ratio0.971 rather
than0.6; this does not establish whether the composited selector is visible in
maim's own root capture. Inspect compositor-visible root capture before remedy.
The visible-root and direct compositor-overlay pixel checks also found no expected
outside dimming (ratios0.971 and0.979). A basic highlight check likewise did not
show expected alpha. A diagnostic ImageMagick overlay capture could not identify
the COW window and its selector timed out; released mouse and stopped only that
probe. A later bounded direct XGetImage probe completed. Large-border approach is
not accepted as visually verified; inspect actual shader/rendering before delivery.
Two web shader-example fetches returned cache misses; source lookup remains pending.
Shader probe found a concrete installed-version contract: despite maim help saying
~/.config/maim, libslopy looks in ~/.config/slop. Probe exited134 with explicit
missing i3-dim.vert path. Move only the new owned shader files to slop config and
retry. The large-border attempt is withdrawn; normal shader framebuffer will use
an opaque desktop snapshot and selection mask.

Shading final result: minimal supported GLSL120 shader compiled and ran. Opaque
frozen desktop pass uses white selection alpha mask: outside brightness60%, inside
100%. Direct compositor samples measured inside1.0/outside0.593. After refresh and
reload, raw XTest keycode107 launched maim with --shader=i3-dim. Saved original
brightness ratio was exactly1.0 in selected sample, output path retained original
folder/name and PNG bytes matched clipboard; Escape preserved clipboard. Independent
helper regression, bash syntax and scoped diff checks passed. No shader fallback
or compositor setting added. Hardware key and receiving-app paste remain unchecked.
