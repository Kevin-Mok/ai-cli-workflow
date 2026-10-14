# Auditor Test Fixture Self-Match

This postmortem records why the audit tool's own regression tests initially
triggered its generic credential detector.

## Symptom

On 2026-10-14, a direct self-scan of the new auditor, sanitizer, and their tests
reported the `credential` category for both test modules. All 10 behavioral
tests themselves passed.

## Impact

Copying those tests into the sanitized repository would have made the final
all-object audit fail on the audit fixtures. No commit or push occurred.

## Evidence

- The auditor and sanitizer source files had no findings.
- Each test module had exactly the generic credential category.
- The fixtures intentionally constructed sensitive-looking assignments inside
  Python source, so the detector correctly treated the source blob as content.

## Root Cause

The runtime fixtures correctly needed credential-shaped configuration lines,
but those same complete assignments were contiguous in the Python source. The
auditor therefore could not distinguish the test source blob from a real
configuration blob.

## Resolution

The fixture keys and sensitive-looking values are assembled from separate
source tokens. At runtime they remain identical, so the tests still exercise
the full credential, email, address, home-path, and encoded-key detectors.

## Verification

- All 10 auditor and sanitizer tests passed.
- A direct scan of both tools and both test modules with the complete private
  rules returned no categories for any file.

## Current Status

Resolved.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
