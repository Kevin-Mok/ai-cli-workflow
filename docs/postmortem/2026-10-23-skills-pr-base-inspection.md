# Skills PR base inspection

This report records inspection failures while preparing an isolated skills review. Use exact commit IDs rather than a stale local branch name, then request normal Git metadata access for integration.

- Symptom: `git merge-tree --write-tree main HEAD` refused unrelated histories; exact-base merge-tree later failed writing temporary Git objects on the read-only shared metadata filesystem.
- Impact: read-only inspection stopped; no tracked content was lost.
- Evidence: local `main` resolves to 20723484; requested linux-config main and GitHub main both resolve to 410feaa. `git merge-base 410feaa d615688f` returns 3e898a0f.
- Lookup: canonical postmortem-memory search for unrelated histories / sanitized repository returned general environment and ownership guidance, without an exact history finding. The exact-ref comparison establishes applicability rather than the stale-name failure.
- Root cause: stale local branch ref and sandbox-protected shared Git metadata.
- Resolution: user chose exact 410feaa; authorized ordinary Git integration on new review/skills-efficiency-20261023 branch succeeded without conflicts and retained main additions.
- Verification: merge --no-commit exited 0; staged AGENTS diff retains main repository-origin rule.
- Status: inspection and isolated fixture setup resolved. Corrected candidate run: 240 tests and 391 subtests passed; publication is tracked in the PR plan.
- Learning: no new general finding; register this report with an explicit no-new-learning decision in canonical and proposal ledgers while preserving pre-existing entries.

- Harness correction: the intentional RED test correctly measured 9,271 core bytes; a redundant wrapper assertion guessed 9,252 and failed. The complete pytest log was retained; no implementation conclusion relied on the guessed number.

- Isolated-harness setup: initial archives omitted Git objects required by historical `git show` assertions, and original/main snapshots lack the newly introduced benchmark budget files. These setup failures are not product regressions. Rebuild disposable fixtures with independent Git metadata and read-only source object access; measure baseline with the same collector directly. Retain initial logs separately from final runs.

- Auxiliary inspection: a read-only ledger query incorrectly assumed a sources array and raised IndexError; schema inspection identified reports as the correct field. No ledger write occurred before correction. An optional absent .gitattributes and absent core.hooksPath query were inspection-only, with no changes needed.

- Visual review startup: Lavish returned SERVER_ERROR in the restricted execution context. Existing environment-boundary lookup applies to local listen/process constraints; retry ordinary server startup with authorized access, without changing the artifact or publishing externally. Resolution: authorized ordinary startup succeeded; local review opened at http://127.0.0.1:4387/session/99fd1d8934c25383. This establishes an environment-boundary workaround, not a diagnosed server defect.
