# Redshift test discovery correction

Read this report to understand a read-only inspection failure and its correction: inventory test paths before opening them.

## Symptom and impact
A combined read attempted nonexistent `tests/test_i3bar_4k.py` and exited 1. No product files were changed by that read; implementation continued after discovering the actual tests.

## Evidence, lookup and cause
The missing-file diagnostic identified a guessed test filename. Postmortem-memory query `missing test file inspection` matched `local-discover-paths-before-reads` in paths-ownership.md. Its inventory-first guidance applies directly; the search agent located `test_i3blocks_4k_status.py` and `test_i3blocks_4k_overflow.py`.

## Resolution and verification
Both actual test files were read successfully and delegated layout checks ran against them. Status: resolved inspection error, no product defect. Next step: continue regression and activation checks in `plans/redshift-i3block.md`.

## Learning
No new learning: existing inventory-before-read guidance fully covers this incident. No retry of the guessed filename or product workaround was needed.
