# Session review module missing from installer manifest

Keep the Second Brain installer's explicit Python module inventory aligned when extracting runtime code. The new review module must be installed with the CLI that imports it.

## Symptom and impact
The first full session regression ran 72 tests with four failures in timer installation. The enable fixtures returned exit 2 with `chezmoi runtime package source is incomplete`. No live timer or installation was changed.

## Lookup and evidence
The lookup `runtime package source incomplete module manifest` returned generic path/reinstall guidance with no exact remedy. Inspection of `_runtime_modules` showed an exact inventory comparison against `RUNTIME_MODULE_NAMES` in `scripts/executable_setup-second-brain-timer`. The new `session_review.py` was absent from this list. The four existing enable/check tests are executable reproducers.

## Resolution and verification
Added `session_review.py` to `RUNTIME_MODULE_NAMES`. The same 72-test session suite now passes (exit 0), including all four prior failures. This verifies source/package installation in fixtures; live activation remains a separate delivery check.

## Learning and follow-up
When extracting a Second Brain Python module, update the timer installer's explicit module inventory in the same change. Run the session/timer regressions before installing any CLI files. This maintains the strict source inventory check instead of weakening it.
