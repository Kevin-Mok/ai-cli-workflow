# Temporary fish abbreviation cleanup trial

This records a cleanup-check timeout during a disposable local abbreviation trial and its verification.

- Symptom: temporary abbreviation expanded correctly, but a subsequently typed cleanup command did not write its completion marker within five seconds.
- Impact: the child fish session was terminated and reaped; the abbreviation was process-local. No persistent shortcut was added.
- Evidence: first trial captured cd /tmp after typing the temporary name plus Space, then timed out waiting for the removed marker.
- Lookup: searched interactive fish abbreviation cleanup keyword expansion before retrying. Existing reserved-keyword and commandline-context guidance is applicable: installed abbreviations can affect subsequently typed diagnostic shell code.
- Status: resolved through a verified harness workaround. Installed keyword expansion was a suspected cause of the typed cleanup failure, not independently confirmed; prebound cleanup bypassed interactive expansion.
- Verification: corrected local PTY trial exited 0; temporary abbreviation plus Space expanded exactly to cd /tmp, was cleared without execution, then erased; abbr --query confirmed absence in that same session. The session was terminated and reaped.
- Follow-up: no product fix or persistent shortcut change is needed. The trial became the committed reusable scripts/executable_check-fish-abbr checker in 5c818a4; it requires no /tmp runner. No new reusable guidance beyond existing PTY capture and quoting guidance.

- Diagnostic retry: automated setup-string editing introduced a Python SyntaxError before fish started; replaced the setup with a single triple-quoted string. No session or abbreviation was created by that failed attempt.
