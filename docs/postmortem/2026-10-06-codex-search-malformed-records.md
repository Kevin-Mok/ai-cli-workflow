# Codex search malformed record validation

This report tracks malformed synthetic records that interrupted a valid session search during independent review. Reproduce each case, validate at the decoding boundary, and rerun the complete focused suite.

## Symptom and impact

Reviewer probes confirmed that response payload type arrays raise TypeError in tool-type set membership, while JSON-legal unpaired Unicode surrogates raise UnicodeEncodeError during message digesting/cache writes. Valid neighboring messages were not returned because the entire process exited with a traceback. Only synthetic fixtures were used.

## Lookup and evidence

Read systematic-debugging and the tracked postmortem-memory skill. Query `malformed json schema unicode` returned local-ledger-invalid-link-diagnostic and unrelated adapter/migration findings. Existing guidance concerns shape validation but does not establish a fix for this extractor. The reviewer isolated each case against a passing baseline; defining local regression tests will independently verify the same failures before any fix.

## Root cause and status

Verified implementation fix (code scope): syntax-valid JSON is not guaranteed to have string discriminants or UTF-8-encodable text. The extraction loop assumed both after decoding. No production sessions were changed.

## Next steps and verification

Add discriminant and surrogate cases to synthetic tests, observe RED, then skip malformed records with stderr counts while preserving good messages. Check the complete suite and add verified boundary guidance after GREEN.

## Resolution and verification

Validate string discriminants before tool-type set membership and skip per-record Unicode encoding errors with counts. Reject non-printable cwd for resume; retain escaped directory display. Move BrokenPipeError before OSError and flush stdout inside its guard so early-closing consumers exit 0 quietly. Each malformed-discriminant, surrogate, raw-control cwd and pipe regression observed RED before its corresponding fix. The complete focused suite now passes 22 tests; no test expectation was weakened. Independent review verified cache locking/publication/privacy and safe picker argument arrays. Tests prove synthetic code behavior, not completeness of every historical schema.

## Follow-up

Keep malformed shape/Unicode fixtures and terminal pipe regressions. Never assume JSON syntax validation establishes UTF-8 or field shape. Search skips bad records while preserving valid neighbors; original logs remain read-only to the search process.
