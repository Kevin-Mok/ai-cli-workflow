# RF Fix Edit Failure

- Symptom: The fallback multi-file edit command failed with `Substitution replacement not terminated at -e line 1`.
- Impact: The two Fish helper files were edited, but the regression test was not updated by that command.
- Evidence: The command exited nonzero during its third substitution; the first two substitutions completed before it.
- Root cause: A complex Perl replacement embedded shell quoting and delimiter characters incorrectly.
- Resolution: Applied the remaining function-name and regression-test edits as separate narrow substitutions.
- Verification: `bash tests/test_refresh_config_function.sh`, the rf completion assertion, both `fish --no-config -n` checks, and `git diff --check` all exited 0.
- Follow-up: Prefer small independent edits when the patch helper is unavailable; verify the resulting diff before running tests.
