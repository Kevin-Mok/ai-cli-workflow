# Session review extracted-tree verification

Record limits of testing the scoped Git index in a temporary directory, then verify the normal checkout before delivery.

- Symptom: the extracted-tree broader suite ran 320 tests with 27 failures and one error. Timer fixtures reported unsafe setup state paths; Git LFS attribute checks lacked a Git repository. The known vault inventory failure also remained.
- Impact: this optional additional check does not establish broader success for the extracted artifact. Its 69 session tests, runtime fixture smoke and README gate passed.
- Evidence: `/tmp/recent-review-commit-jptbkzcf/tree` is a checkout-index extraction under `/tmp`, not a Git working tree. Tests depend on repository metadata and protected source locations. No product changes are indicated by these fixture-environment failures.
- Lookup: searched `timer setup state path unsafe temporary extracted tree`; review relevant safe-path and fixture-contract knowledge. Existing artifact-versus-workspace distinction applies; no new reusable finding.
- Status: verification limitation; preserve strict checks and rerun broader tests in the supported repository location. No workaround or production safety relaxation is applied.
- Next steps: record normal-checkout verification and ship eligible scoped changes, retaining the known unrelated vault failure.

Verification: the normal repository suite ran 331 tests, with 330 passing and only the pre-existing Daily Note inventory failure. Installed runtime fixture smoke passed, README gate returned pass_no_change, and all six staged/source/installed module bytes matched. The extracted-tree failures are environment-specific; no product remedy was required.
