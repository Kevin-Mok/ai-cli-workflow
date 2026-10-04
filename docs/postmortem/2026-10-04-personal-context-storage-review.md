# Private context storage review findings

This record tracks two storage edge cases found by independent synthetic
review. Add defining regressions, correct the update-order and file-creation
behavior, then rerun the complete focused suite before installation.

## Symptom, Impact, And Evidence

The initial 19 personal-context checks passed, but review reproduced two gaps
using invented data in temporary directories:

- A distinct-ID user statement with an older `recorded_at` could supersede a
  newer active statement for the same concept key. Existing retry coverage
  protected identical IDs, and concurrency coverage used different keys.
- Under umask `0277`, a newly created atomic temporary file had mode `0400`.
  The helper required `0600` before its subsequent chmod could run, so both
  first writes and retries failed without creating the store.

No real personal data was used or lost by these review probes. They were
deliberately exercised failure paths, and are recorded here to keep the related
fixes and verification together.

## Root Cause And Current Status

Correction merging checked evidence basis but not recording order. Temporary
file opening checked final permissions before initialization had finished.
Both findings were reproduced by focused failing tests and are now resolved.

## Resolution And Verification

The helper rejects a backdated user correction without modifying existing memory;
evidence-source dates remain separate from recording order. Exclusive new
temporary files receive ownership/type/link safety checks and then mode 0600
before writing. Strict permission checks remain for existing files.

The two defining tests failed for the expected reasons before the fixes, then
passed. Parent verification of `python3 -B -m unittest discover -s tests -p
'test_personal_context*.py' -v` passed 22/22, including both regressions. The
helper's basedpyright check returned zero errors, warnings, or notes. Both
commands exited 0.

## Follow-up

Keep these regressions when changing storage. Do not claim locking alone
establishes semantic update order; source dates and user recording dates serve
different purposes.
