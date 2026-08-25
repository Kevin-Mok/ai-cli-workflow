# FN Progress Fish Variable Expansion Failure

- Symptom: The C7S4 regression produced empty dates and arithmetic errors after the dynamic function was restored.
- Impact: `fn-progress` was temporarily invalid during the TDD GREEN step; no live refresh was run.
- Evidence: The deterministic test reported `unexpected parsed date:` and Fish reported missing numeric arguments.
- Root cause: Perl interpolated Fish variable names in the fallback replacement instead of emitting literal Fish variables.
- Resolution: Rewrite the function with escaped literal Fish variables, then rerun the same regression.
- Verification: `fish -n dot_config/fish/functions/fn-progress.fish` and `bash tests/test_fn_progress.sh` passed after the literal-variable rewrite. Live output reports C7S4 progress and days remaining; `refresh-config` emitted `REFRESH COMPLETE`.
- Follow-up: When a fallback generator emits another language, escape that language’s variable syntax explicitly.
