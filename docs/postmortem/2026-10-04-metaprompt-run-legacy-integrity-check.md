# Metaprompt & Run legacy integrity check failure

This record tracks the legacy checksum failure discovered while validating the
new runner. Compare the failing files and assertions with the committed baseline,
verify the runner separately, and preserve unrelated legacy changes.

## Symptom and impact

- `python3 tests/test_metaprompt_integration.py` ran eight tests and exited 1.
- The new three-skill discovery check passed, as did Sentry packaging/updater
  checks. One legacy integrity test failed in four reference-file subtests:
  `execution-routing.md`, `examples.md`, `model-profiles.md` and
  `compilation-rules.md`.
- Current SHA-256 digests differ from the frozen assertions. The runner task
  has not modified the legacy package or those assertions. A complete green
  integration-suite claim is not supported.

## Evidence and current status

- The initial tracked change in the suite only adds `metaprompt-run` to the
  discovery names and generalizes the module docstring.
- Current status reports no modifications under `metaprompt-alxve`.
- All four current files match their `HEAD` bytes. Executing the legacy
  integrity test from `git show HEAD:tests/test_metaprompt_integration.py`
  against those unchanged files reproduced the identical four subtest
  failures. This is a committed baseline mismatch, not runner-induced drift.
- `python3 tests/test_metaprompt_contract.py` passed all 12 behavioral tests,
  exit 0. Keep the mismatched historical hashes intact in this task.

## Root cause and disposition

- The committed integrity assertions describe different legacy reference
  bytes from the committed package. The failing comparison is reproducible
  without this session's discovery-test change.
- No legacy repair is included: this request explicitly preserves that package.
  The full integration suite remains red until a separate provenance review
  reconciles the committed package and historical hash inventory.

## Investigation and next steps

- Completed: compare current files and assertions with `HEAD` and reproduce
  the baseline failure independently. Parent behavioral regressions are green.
- Continue runner and Sentry-specific checks, and report the unresolved baseline
  integrity failure with the final verification evidence.
- A future legacy maintenance task should audit provenance before changing
  reference bytes or historical assertions.
