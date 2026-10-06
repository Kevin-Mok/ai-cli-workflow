# Codex search hidden picker UI

A real fzf smoke check exposed a display problem missed by argument stubs. Keep fzf stderr attached to the terminal, then verify visible selection and cancellation on synthetic history.

## Symptom and impact

The first real fzf invocation displayed search output but no picker. fzf stayed running awaiting selection. No conversation was resumed or prompt submitted. Only disposable synthetic data and a temporary extracted Ubuntu fzf binary were used.

## Lookup and evidence

Read the tracked incident and systematic debugging skills; search `fzf stderr tty picker` found no directly applicable fix. The search command uses subprocess capture_output, which captures stderr where fzf renders its UI. Existing tests stubbed row selection and did not assert terminal presentation. A synthetic stderr-display defining test will reproduce the boundary.

## Root cause and status

Verified runtime fix: pick() previously captures both stdout (the selected row) and stderr (the interactive UI), so the user's terminal never sees the picker. Preserve stdout capture for validated selection, inherit stderr for display, and record generic failure status after fzf's own error output.

## Next steps

Run the stderr-display regression RED, change the subprocess stream wiring, rerun the entire suite, and repeat live Escape/Enter checks. No private sessions or system package installation are needed.

## Runtime fixture correction

After visible real fzf selection, installed Codex 0.160.1 resumed the synthetic UUID and /status showed its recorded directory and 0 token usage. Exiting exposed a smoke-helper assertion that wrongly required the actual Codex process to leave its own synthetic log byte-identical. Real resume records lifecycle data; only search/indexing promises read-only source behavior. Fix the helper to assert immutability immediately after search and only in the stub picker path. Add mirrored event records to the synthetic fixture so the interactive history projection is also exercised. No real session files were used.

## Resolution and final evidence

Capture only fzf stdout and inherit stderr. The defining stderr-display test observed RED, then the full 22-test suite passed. Real Ubuntu fzf 0.44.1 displayed the row/header; Esc exited 0 without launch, and Enter forwarded exactly resume/-C/synthetic-directory/UUID. The corrected real-resume fixture displayed both saved user and assistant messages in Codex 0.160.1. /status confirmed the UUID, thread title, recorded directory with spaces and zero tokens; no inference prompt was submitted. Exit returned 0. The temp-home helper warning is an upstream CLI limitation, not a search failure. No private conversation files were copied.

Follow-up: keep subprocess UI stream verification separate from argument stubs. Search immutability is checked before real Codex startup; resumed Codex may append lifecycle records. fzf was downloaded/extracted only in /tmp, so the normal PATH still requires the optional dependency for --pick.
