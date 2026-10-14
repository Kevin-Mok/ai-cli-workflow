# Account Identifier Audit Scope Failure

This postmortem records why the final full-history audit reported hundreds of
findings after the last hostname rewrite, and how the audit rule was narrowed
without weakening file-content coverage.

## Symptom

On 2026-10-14, the all-object public-history audit exited with status 1 after
checking 688 commits and 5,129 unique blobs. It reported 687 findings in the
`account_identifier` category.

## Impact

The sanitized history could not be declared clean or moved into the requested
repository. No history was published or pushed.

## Evidence

- The rewrite completed with 688 commits, 18 neutral local heads, and zero
  unreachable objects.
- The failing audit count closely matched the number of commits attributed to
  the retained primary author.
- The follow-up rule had been added as a generic forbidden literal, so the
  scanner applied it to both blob content and commit metadata.

## Root Cause

The historical calendar account identifier overlaps with intentionally retained
public author attribution. Literal rules previously had no location scope, so a
value meant to be forbidden in file content was also forbidden in commit
objects.

## Resolution

The auditor now accepts an optional `locations` list for each private literal
rule. The calendar account rule is restricted to blob content, while every other
literal continues to scan both blobs and commits by default. A regression test
first reproduced the failure and then passed with the scoped implementation.

## Verification

- `python3 -m unittest tests.test_audit_public_history tests.test_sanitize_public_tree`
  passed all 10 tests.
- The all-object audit passed after checking 688 commits and 5,129 unique blobs
  with zero findings.

## Current Status

Resolved. The content remains forbidden throughout history without treating
the retained author name in commit metadata as sensitive.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
