# Fish-alias regression suite cannot import

This records a pre-existing test syntax error encountered while validating the reusable local abbreviation checker.

- Symptom: unittest cannot import tests/test_fish_alias.py, line 74, because test_example-user_home_directory_normalization contains a hyphen in a Python function identifier.
- Impact: the existing broader mapping-helper suite could not run. The new checker suite (4 tests), reserved-keyword PTY regression (1), skill-admission suite (7) and catalog inventory all passed.
- Evidence: git show HEAD:tests/test_fish_alias.py contains the same invalid definition, proving it predates this task. The file is unchanged by this task.
- Lookup: searched sanitized test function identifier hyphen SyntaxError; no applicable reviewed finding was returned. Direct HEAD inspection established the baseline cause.
- Status: unresolved baseline issue, outside this checker change. No claim is made that the broader suite passes.
- Resolution scope: proceed with independently passing focused tests and actual local CLI runs; do not weaken tests or bundle unrelated repairs.
- Follow-up: repair the malformed test identifier separately and rerun the mapping-helper suite.
- Learning: no new reusable guidance; Python identifier syntax and baseline-versus-session attribution already explain this failure.
