# History Auditor Missed Short Base64 Key Header

This incident records a test-discovered gap in the new full-history auditor. The detector found ordinary credentials and PII but missed a short base64-encoded private-key header because its base64 prefilter counted only unpadded characters; the defining regression remains the gate for the correction.

## Symptom

The first GREEN run of `test_detects_sensitive_data_in_historical_blob_without_echoing_values` failed because the audit report omitted the expected `private_key` category.

## Impact

- No repository history was rewritten and no sensitive value was printed.
- Relying on the initial detector would have left a coverage gap for short base64 strings that decode to private-key PEM headers.
- The independent read-only audit had already found the repository's real encoded Kubernetes key, so the confirmed repository finding was not lost.

## Evidence

- The focused test consistently returned four of five expected categories.
- Direct category-only instrumentation showed that `private_key` alone was absent.
- The fixture payload decoded successfully and matched the PEM private-key marker.
- The candidate contained 38 unpadded base64 characters plus two padding characters, while the prefilter required at least 40 unpadded characters.

## Prior-Knowledge Lookup

- Query: `history scanner missing category base64 private key detector test`.
- Result: no directly applicable detector-length finding. The nearest reviewed references concerned boundary validation and fixture contracts, not base64 candidate sizing.
- Decision: diagnose from the failing fixture and detector boundary instead of applying an unrelated prior remedy.

## Root Cause

The base64 candidate regex applied its minimum length to the non-padding character class. The fixture was 40 characters overall but only 38 before `==`, so the value was never decoded even though the decoded content was a private-key header.

## Current Status

Resolved.

## Resolution And Verification

The base64 prefilter accepts the short padded fixture while decoded PEM content
remains the confirmation boundary. All 11 focused auditor/sanitizer tests pass,
and the latest all-object scan reports zero findings across 688 commits and 5,128
unique blobs.

## Follow-Up

- Keep decoded-content confirmation as the authority; base64 length is only a performance prefilter.
- Add future private-key encodings as fixture variants before changing detector logic.
- The canonical postmortem-memory ledger is outside the user-authorized folder and remains intentionally untouched.
