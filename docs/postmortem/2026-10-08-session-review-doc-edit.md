# Session review documentation replacement marker

Use the destination file's actual neighboring section when replacing documentation. A marker from the README was mistakenly used for the usage guide.

## Symptom and impact
A scoped Python edit returned `ValueError: substring not found` after writing README changes. Usage and smoke-check files were not changed by that script. CLI help and the separate incident-ledger check still succeeded.

## Lookup and diagnosis
Search `substring not found exact text replacement` matched `ext-stale-patch-context`. Current source inspection confirms the guide's next boundary is `After explicitly deciding`, while the attempted marker belonged to README. This is an editing-tool mismatch, not an application failure.

## Resolution and verification
Partial writes inspected and retained. Remaining usage and smoke edits used current exact boundaries and succeeded. Review and refresh CLI help confirms the documented options and bounds. Existing exact-context guidance covers this incident; no new reusable finding.

## Verification helper interpreter follow-up
The README gate's `--help` was mistakenly launched with Python, producing `SyntaxError: unterminated string literal` before any shell code ran. Lookup `wrong interpreter shell script Python SyntaxError` found no exact remedy. The file's shebang identifies Bash; invoke the executable directly. This is a task invocation error, not a source defect; no new reusable learning.

The executable helper subsequently reported its Bash usage successfully and the README gate returned `pass_no_change` (exit 0). No source repair was needed for the interpreter error.

A final orchestration wrapper had an unmatched parenthesis and was rejected before any nested tool or shell command ran. Existing exact-context/nested-language invocation guidance applies. The corrected wrapper started the intended read-only verification; no product files were changed by the failed wrapper.
