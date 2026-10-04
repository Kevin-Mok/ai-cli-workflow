# Personal-context helper type-check failure

The first type-check pass found an incorrect return annotation on the safe
argument-parser error handler. This note records the check and repair without
including private context.

- **Symptom:** `basedpyright` reported one incompatible override error and
  warnings in the new storage helper.
- **Impact:** Synthetic runtime tests passed, but static verification was not
  yet complete. No real personal-context files were read or written.
- **Evidence:** `ArgumentParser.error` never returns, while the override was
  annotated as returning `None`.
- **Root cause:** The custom safe-diagnostic override used the wrong return
  annotation; standard-library dynamic JSON and CLI boundaries also needed
  explicit local types.
- **Resolution:** Annotated the override as `NoReturn`, marked it as an
  override, and gave JSON collections and CLI arguments explicit local types.
- **Verification:** `basedpyright` reports 0 errors, 0 warnings, and 0 notes;
  `python3 -B tests/test_personal_context_store.py` passes all 16 tests.
- **Status:** Resolved.
- **Follow-up:** Include the installed type checker in this helper's routine
  verification alongside the synthetic storage tests.
