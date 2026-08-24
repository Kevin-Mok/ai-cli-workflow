# Refresh-Config Regression Test Permission Failure

- Symptom: Direct execution of `tests/test_refresh_config_function.sh` failed with `Permission denied`.
- Impact: The regression body did not run on the first final-verification attempt.
- Evidence: `/usr/bin/bash: line 1: tests/test_refresh_config_function.sh: Permission denied`.
- Root cause: The tracked shell test does not have its executable mode set.
- Status: Resolved.
- Resolution: The repository convention is to invoke non-executable shell tests with `bash`; the focused and existing refresh-config tests both passed that way. No file-mode change is needed.
- Verification: `git ls-files --stage` reports mode `100644` for the existing test, while nearby tests use the same mode, and both test bodies passed via `bash`.
- Follow-up: Invoke repository shell tests through `bash` unless their tracked mode is intentionally executable.
