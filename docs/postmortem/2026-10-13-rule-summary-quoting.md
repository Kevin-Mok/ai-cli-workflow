# Rule Summary Diagnostic Quoting Failure

This incident records a harmless but avoidable diagnostic failure. A nested Python f-string was embedded inside a shell-quoted `python -c` command, and the escaping produced invalid Python; the replacement uses a saved temporary helper so language boundaries remain explicit.

## Symptom

The private-rule summary command exited with a Python `SyntaxError` before reading or printing the JSON rule file.

## Impact

- No repository or temporary rule file changed.
- No sensitive value was printed.
- The requested label/category/length summary was delayed until a safer helper could be used.

## Evidence

- The error pointed at escaped quotes inside the nested f-string expression.
- The command combined shell single quotes, Python double quotes, and f-string dictionary access in one physical argument.

## Prior-Knowledge Lookup

- Query: `Python -c nested f-string quote SyntaxError shell diagnostic`.
- Match: reviewed nested-language literal-emission guidance applies directly; it recommends a saved helper or reviewed explicit code instead of layered inline quoting.
- Decision: do not retry the inline command. Use an `apply_patch`-created temporary helper with ordinary Python syntax.

## Root Cause

The diagnostic compressed two language parsers into one quoted shell argument. Backslash-escaped quotes inside the f-string expression were invalid in that context.

## Current Status

Resolved.

## Resolution And Verification

An `apply_patch`-created helper printed only labels, categories, and lengths,
exited zero, and omitted every rule value. Both private rule files retained mode
`0600` through all later updates.

## Follow-Up

- Use saved helpers for non-trivial structured-data diagnostics.
- Keep private values out of diagnostic output even when transport is corrected.
- The shared postmortem-memory ledger is outside this task's authorized folder and remains untouched.
