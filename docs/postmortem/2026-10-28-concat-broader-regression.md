# Concat broader regression failures

The focused concat suite passes, while the broader repository unittest run has reported failures. Keep their exact identities and attribution separate from the media checks.

- Symptom: `python3 -m unittest discover -s tests` exited 1 after 1,382 tests in 267.504s: 52 failures, 105 errors and one skip.
- Evidence: full output `/tmp/concat-full-tests.log`. The tests agent reviewed failure clusters: personal-context (including 20 store failures and three loader imports), Second Brain doctor (14 errors/nine failures), tmux scrolling (22 errors), metaprompt runtime (29 errors), screensaver runtime, vault, backup, Codex and memory integration tests. No focused concat tests failed.
- Representative causes: `test_exact_sanitized_tree_exists_without_unapproved_files` expected 35 vault files but found only README; `test_frontmatter_schema_is_consistent` lacks `00 Context/About Me.md`. `test_actual_ledger_reference_status_and_coverage` checks absent `/home/example/coding` and `/home/example/linux-config` roots and historical aliases. Runtime tests also need unavailable display/tmux/private-store dependencies.
- Impact/status: broad regression remains red; these environment/fixture gaps are outside the changed concat module. No clean-baseline rerun was performed, so do not claim every failure is proven pre-existing. The focused concat suite subsequently passed all 14 tests.
- Decision/next steps: no broad-suite remediation or repeated full run during the media change. Keep the log and disclose the incomplete broad check; use focused and real-source acceptance checks for this workflow. This report adds no new general guidance beyond the existing requirement to disclose missing fixtures/environment dependencies.
