# Commit picker validation baseline failures

The numbered skill-title change passed its focused checks. A broader workflow suite exposed unrelated instruction-policy contract failures; this report records their scope so the picker change does not silently broaden into policy rewrites.

## Symptom and impact

`python3 tests/test_ai_workflow_contract.py -v`: 9 passed, 3 failed. Failures: delivery preference missing the exact expected entry; commit-dirty missing expected push-policy wording; root routing instructions 2036 bytes versus the 1200-byte limit. None of those files was modified by this task. Picker-focused contract: 4 passed. Scoped diff whitespace check passed.

## Lookup and applicability

Query: `push policy compact routing feedback preference`. Reviewed `references/artifact-verification.md#local-push-policy-baseline-contract`: unresolved exact push-policy assertion on unrelated work. Applicable to the push-policy failure; it does not establish remedies for the other two assertions. No remedial retries or policy changes made.

## Status, evidence, and next steps

Unresolved baseline contracts, outside the requested presentation change. Keep policy/test alignment as separate work. The metadata deployment completed via a process-local scoped refresh-config apply; all four installed files byte-match source and show numbered labels. No live picker interaction was performed. No new reusable learning: existing guidance already requires keeping unrelated baseline failures out of a scoped change.

## Delivery privacy check

The pre-commit privacy gate rejected the new ledger alias as `home_path`. Replaced the identifying home prefix with the ledger's existing `/home/example` public convention. The targeted check passed with the real local alias before sanitization; a sanitized alias is not a resolvable local source path. The repaired candidate passed the privacy gate. The final targeted ledger check reports only `unregistered_aliases` for the real local path; the reviewed report hash remains registered through its public alias. No policy bypass is authorized.
