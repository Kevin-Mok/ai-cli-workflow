# Sanitizer Email Prefix Corruption

This incident records a test-discovered corruption risk in the public-tree sanitizer. The initial email expression accepted `=` inside the local part and could therefore consume an assignment key such as `email=`; the defining regression prevents the sanitizer from deleting configuration structure while redacting values.

## Symptom

The first GREEN run of the tree-sanitizer test replaced an entire `email=<value>` line with only the public placeholder, removing the `email=` key.

## Impact

- No repository history had been rewritten, and the failure occurred only in a temporary test tree.
- If used unchanged, the sanitizer could corrupt configuration and documentation fields whose key immediately preceded an address.
- No sensitive value was printed by the sanitizer.

## Evidence

- The regression preserved every other key and replacement but failed the literal `email=user@example.invalid` assertion.
- The observed sanitized fixture contained the placeholder address on a line by itself.
- The local-part character class allowed `=`, so matching began at the assignment key and extended through the address.

## Prior-Knowledge Lookup

- Query: `email redaction regex consumed assignment prefix equals local part`.
- Result: no directly applicable email-redaction finding. The nearest regex guidance concerned flag placement, not token boundaries.
- Decision: constrain the email token boundary and keep the existing behavioral regression as proof.

## Root Cause

The regex modeled the full RFC local-part punctuation set, including `=`, without distinguishing an address token from a configuration assignment. That made `email=person@host` one syntactically acceptable regex match.

## Current Status

Resolved.

## Resolution And Verification

The conservative local-part class excludes the assignment delimiter, preserving
configuration keys while replacing only the address. The defining regression
and all 11 auditor/sanitizer tests pass.

## Follow-Up

- Prefer preservation of surrounding structure over exhaustive acceptance of unusual address syntax in a destructive sanitizer.
- Add boundary fixtures before expanding token character classes.
- The canonical postmortem-memory ledger remains outside the authorized folder and is intentionally untouched.
