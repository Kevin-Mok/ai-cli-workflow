# Requested file shortcut name was changed

This report tracks why `btw` failed after the shortcut was installed, and the regression and activation checks required to repair it.

- Symptom: user requested `btw ~/coding/btw.md`; previous delivery installed and verified `nbtw` instead. The user reports `btw` did not work.
- Impact: requested interactive name was unavailable despite a passing check for a different name. Notes content was not touched.
- Cause: skill treated the first token as a legacy file source key; helper and generator added `n`. Verification accepted that derived name instead of the requested name.
- Lookup: searched `file shortcut effective fish name n prefix`; existing `local-shortcut-stored-text-verification` covers exact stored text but not preserving the requested name. Source inspection confirms helper fish_name and legacy generator both prefix file rows.
- Decision: new file requests become existing command-catalog editor mappings, preserving the exact requested abbreviation. Keep legacy file catalog/generator behavior unchanged.
- Status: defining regression observed RED (1 test: actual nbtw, expected btw); minimum helper now stores new file requests as literal-name editor commands. GREEN:22 shortcut tests and7 admission tests pass. Installed skill/helper and literal mapping deployed; scoped refresh and actual interactive btw + Space passed without editor execution.
- Resolution: three helper lines route new file requests to editor commands under the requested name; skill and verification require that exact name. Existing file-row prefixes are preserved.
- Verification: 22 shortcut tests and7 admission tests pass; scoped refresh exits0; checker reports `btw + Space -> $EDITOR ~/coding/btw.md; never executed`. Frozen routing46/51 and inventory241/0 pass. Pre-existing broad trim budget failures remain unchanged.
- Follow-up: reload abbreviations in existing shells. Opening the editor is intentionally untested. Deliver one focused commit/push with normal privacy hooks.
- Inspection limitation: optional legacy skill/PROGRESS lookup paths were absent; use discovered tracked paths rather than retry guessed locations.

- Regression setup: first RED run collected zero tests because an inherited function name contained `example-user`, an invalid Python identifier. Renamed that test identifier to `example_home` without changing its assertions; rerun is required for meaningful RED evidence.

- GREEN-check diagnostics: first generated readback assertion used a partial regex, returning only the name prefix and capture rather than the command. Corrected it to match the full definition. The admission ledger exceeded its 20KB guard after a redundant prose entry; removed that entry while retaining the dated scored JSON PASS. A sanitization-era other-home fixture also named the canonical home; changed it to a distinct other user.
- Broader trim budget: failures for canonical AGENTS bytes/lines and aggregate loaded bytes already appear in the saved pre-edit report; no instruction source change belongs to this fix.

- Validation cleanup: admission cost initially counted an extra leading newline; corrected to the benchmark parser’s7085 body bytes. Final seven-test admission run passes. No configured Python type-check command exists.
