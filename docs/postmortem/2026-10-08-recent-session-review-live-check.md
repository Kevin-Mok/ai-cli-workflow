# Recent session review live recap validation

Keep successful recaps cached when an individual generated recap fails validation. Diagnose and retry only the missing recap within the explicit generation budget.

## Symptom and impact
The installed default review selected five real work sessions in global recency order and displayed four useful recaps. One selected entry reported `invalid_summary`; review exited 1. The failure was localized next to that entry, as designed. No raw inference response or private conversation text was persisted in this report.

An optional process-status diagnostic also failed because it split `/proc/PID/stat` on spaces even though the parenthesized command name can contain spaces, producing a ValueError converting the state field to an integer. That diagnostic made no changes and is not part of the CLI; do not rerun it.

## Lookup and investigation
Lookup `session digest invalid_summary schema inference` returned generic isolation/fixture guidance without a matching schema remedy. Inspect the fixed validator's shape/size contract and record only safe validation metrics if the issue recurs. Inference already rejects invalid results and preserves other recaps; no speculative implementation change is warranted.

## Diagnosis and repair
The one-call retry again failed with `invalid digest check`. Safe diagnostics showed one check; top-level keys and field sizes were valid. No private field text was logged. A new real inference-boundary fixture proves the provider schema accepts `UI Check` while the local validator rejects it. The provider schema lacked the validator's key pattern and nonempty bounded check-text contract. This contract gap is confirmed; the exact private live check value was deliberately not recorded.

Added key-pattern and check-text constraints to the provider schema and made the prompt's key-format rule explicit, preserving the existing strict validator. The defining fixture failed before the repair. Run session regressions, install only this additional verified runtime module with a rollback copy, and verify live selected missing recaps. The process diagnostic needs no product repair.

## Resolution and verification
The provider schema now constrains check keys to the existing validator's lowercase kebab-case pattern and constrains nonblank check text to 1–1000 characters. The prompt states the key format. The strict local validator remains unchanged.

The defining inference-boundary fixture failed before repair, then all 80 session tests passed. The installed runtime exactly matches the verified source. Live default review subsequently exited 0 and displayed useful recaps for all five selected sessions, including the previously failing playlist recap. This supports the schema gap as the cause; the exact earlier private invalid value was not retained. Broader verification ran 331 tests with only the pre-existing unrelated vault-inventory failure.

Follow-up: keep provider output constraints aligned with local validation, and diagnose failures with field shapes instead of logging private response text. Runtime rollback is available with the other session-review files in `/tmp/recent-session-review-rollback-1j1h03__`.
