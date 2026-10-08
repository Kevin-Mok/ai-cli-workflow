# Fish alias validation fixtures

Two inspection/validation mistakes were corrected without changing live aliases. The fixture contract now compares the actual generated fish names.

- Symptom: an rg query failed on an unescaped template delimiter. A GREEN fixture expected file key bn to conflict with cbn.
- Impact: inspection query produced no matches; one test incorrectly failed despite correct generated-name matching. No mapped commands ran.
- Evidence: rg reported a repetition-quantifier error; fixture failure showed bn unchanged. Generator prepends n, so bn produces nbn, not cbn.
- Lookup: existing API-contracts/fixtures guidance requires checking the real generator contract; direct inspection of sync-shortcuts established the n prefix.
- Cause: invalid regex syntax and arithmetic-by-eye mistake in the initial fixture/inspection summary.
- Resolution: use separate escaped patterns; correct fixture to test an actual nbn collision and retain cbn as unrelated. Strengthen command/path and idempotence cases.
- Verification: corrected 13-test fixture suite passed (exit 0); independent real-template forward tests passed command, spaced file, idempotence and conditional conflict cases with fish syntax exit 0. Type checker initially returned exit 1 on 17 warnings; typed JSON/argparse boundaries and match iteration now pass with 0 errors/0 warnings. Independent fixture marker typo corrected by reading actual section marker.
- Status: resolved tooling/fixture mistakes. Final 15-test suite passes; basedpyright reports 0 errors/0 warnings.
- Additional review: a harmless request containing a Go-template hostname expression was accepted in preview. It reached template evaluation, violating the no-command-execution boundary for template functions. A defining guard test observed RED, then passed after rejecting request delimiters before rendering. No output-function command was executed.
- Resolution evidence: request-template guard passes, live refresh exits 0 and installed helper bytes match the guarded source.
- Learning: no reusable new learning beyond checking executable contracts and fixtures; reviewed record updated when verification completes.
