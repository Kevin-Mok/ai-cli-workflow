# Commit-series inspection failures

This report records read-only inspection failures during commit planning and delivery. Approved scoped reads and schema-aware inspection enabled the review; no host sandbox repair was attempted.

## Symptom, impact and evidence

- Two initial planning reads exited 1 before shell startup with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Approved scoped status and source reads succeeded, exit 0.
- Temporary ledger inspections assumed `sources` instead of `reports`, then treated the reports list as a mapping. They raised KeyError/AttributeError and changed no files. Corrected inspection enumerated list records keyed by sha256 and findings keyed by id, exit 0.
- An optional AGENTS inventory returned no matches (rg exit 1), ending a chained read early. Explicit path discovery found no nested additions; upstream and feedback reads succeeded afterwards, exit 0.

## Lookup, cause and resolution

Read the tracked postmortem-memory skill. Query `bwrap loopback Failed RTM_NEWADDR` returned ext-sandbox-loopback and local-sandbox-loopback-approved-route; their runner-startup scope applies to the identical pre-execution error. Scoped approved execution verifies only the workaround. The default sandbox remains unresolved. Ledger errors were disposable inspection assumptions; inspecting its top-level value types established the correct list schema.

## Learning and next steps

No new reusable learning: existing sandbox and discovery guidance covers these boundaries. Register this report with an explicit no-new-learning decision and verify its current hash. Keep repository changes and Git writes limited to the authorized reviewed commit series.
