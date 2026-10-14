# Rule Generator Identity Separator Bug

This incident records a pre-rewrite safety check that prevented an overbroad identity replacement. Newlines emitted between `git log` records were treated as one-character names, which would have replaced every newline in history; identity fields are now normalized before rules are generated.

## Symptom

The redacted rule summary showed a `personal_name` literal with length one and the full-history audit attributed thousands of findings to that category.

## Impact

- The generated rules were unsafe to use because one replacement would have rewritten line breaks throughout text history.
- No history rewrite had started, so no commit, tree, ref, or working file was affected.
- Raw identity values remained private; only labels, categories, and lengths were printed.

## Evidence

- The one-character rule's stable label matched the digest pattern for a record separator rather than a human name.
- The generator used a NUL-delimited format but did not remove the newline Git writes after each formatted log record.
- The independent metadata audit found only three real identity names, inconsistent with the generator's extra rule count.

## Prior-Knowledge Lookup

- Query: `git log NUL fields newline separator parsed as one-character identity`.
- Result: no direct separator-parsing finding. Related reviewed guidance emphasizes realistic fixture boundaries and preserving explicit record structure.
- Decision: normalize each parsed field with whitespace trimming and discard empty fields before classification.

## Root Cause

The parser split only on NUL bytes. Newline record separators remained attached to the following field or became their own field, so they were mistaken for author/committer names.

## Current Status

Resolved before history mutation.

## Resolution And Verification

The regenerated rule set contained no empty or one-character identity rule,
matched the independent inventory of three identity names and six emails, and
retained mode `0600`. The completed 698-input rewrite used that corrected set.

## Follow-Up

- Validate minimum lengths and expected cardinality before allowing destructive rewrite rules.
- Keep redacted summaries of labels/categories/lengths as a preflight gate.
- The shared postmortem-memory ledger remains outside the authorized folder and is intentionally untouched.
