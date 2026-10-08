# Fish alias completion checks

This report records the independent helper review and a test-launch issue while completing the skill. Isolated regressions verify changes without executing supplied commands.

- Review symptoms: absolute executable plus arguments routed as a path; stored fish backticks acquired backslashes.
- Evidence: defining RED tests failed for `/bin/echo notes.md`, `/bin/echo hello`, `~/bin/tool notes.md`, and stored `echo ` + backtick text; minimum routing/quoting corrections passed the focused suite.
- Resolution: multiword nonexistent path strings route as commands; retain unescaped backticks in fish double-quoted mapping values. Keep pre-existing template-delimiter rejection before rendering.
- Unexpected check failure: direct `python3 -B tests/test_second_brain_config_snapshot.py` failed with `ModuleNotFoundError: No module named scripts.second_brain`; no production or deployment command ran in that test.
- Impact: snapshot regressions not yet verified by this launch; current-template generator and fish syntax already passed independently.
- Lookup: `ModuleNotFoundError scripts.second_brain test PYTHONPATH`; reviewed local-second-brain-runtime-module-inventory. Inapplicable because this is a direct runner import failure, not a missing installed module; the module exists in the repository.
- Snapshot resolution: `PYTHONPATH=. python3 -B tests/test_second_brain_config_snapshot.py` passed all 22 tests, exit 0. No application change needed.
- Verification: all 19 shortcut tests pass, basedpyright reports no errors/warnings, skill validator and refresh/link checks pass; installed skill/helper/generator match source and generated fish syntax passes. `refresh-config` returned REFRESH COMPLETE, exit 0; protected entry-time Codex source and alias bytes preserved.
- Status: helper fixes verified in code and installed; snapshot runner workaround verified.
- Follow-up: use repository import paths for direct test scripts; compare stored abbreviation text when validating quoting, without executing commands.
- Learning: record local-shortcut-stored-text-verification; test-launch issue introduces no new reusable remedy beyond explicit repository import paths.
