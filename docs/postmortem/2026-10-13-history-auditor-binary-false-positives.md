# History Auditor Binary False Positives

This report records false-positive text findings produced by scanning compressed
binary bytes as if they were source text.

## Symptom

On 2026-10-13, the post-rewrite audit reported three residual findings in PNG
and MP3 blobs. Two private-term byte sequences occurred deep inside compressed
payloads, and one email-shaped sequence occurred in PNG data.

## Impact

The audit failed even though the reported byte sequences were not readable file
content or metadata. One screenshot was independently found unsuitable during
visual review and must still be removed by path; the other binary findings were
scanner noise.

## Evidence

- All three blobs contained NUL bytes and were identified as PNG or MP3 data.
- Private-term matches appeared hundreds of kilobytes into compressed payloads,
  outside structured metadata headers.
- Visual review identified private work context in one screenshot independently
  of the regex finding.

## Root Cause

The auditor applied email, credential, network, and private-literal regexes to
every blob without distinguishing text from binary content. Arbitrary compressed
bytes can coincidentally contain short forbidden sequences.

## Resolution

The auditor now counts NUL-containing blobs as covered without applying text
regexes. Binary assets use a separate file-type inventory, metadata review, and
visual review. A regression fixture proves compressed binary bytes do not create
text findings.

## Verification

All 11 focused tests pass. The all-object audit counted 258 binary blobs and
reported zero findings; separate review classified all retained assets as small
generic UI/icon PNGs.

## Follow-up

Document the split between text scanning and binary review in the audit command
and task lessons. The canonical postmortem-memory ledger is outside the
user-authorized folder and must not be changed during this task.
