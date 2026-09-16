# Refresh Config Logging Edit Failure

- Symptom: A fallback Perl substitution corrupted the new conflict-reporting lines with a literal `$1` and removed the log variable.
- Impact: The helper would have failed to print the intended conflict details.
- Evidence: The file showed `$1    echo` and `rg ... >&2` without `$refresh_log`.
- Root cause: Perl replacement interpolation expanded shell-style variables in the replacement text.
- Resolution: Replaced the two lines explicitly with a line-based edit.
- Verification: Fish syntax, the focused regression, diff checks, and a live timed refresh all pass; the live run prints the MIME conflict details.
- Follow-up: Prefer encoded or line-based edits for shell code containing `$` and backreferences.
