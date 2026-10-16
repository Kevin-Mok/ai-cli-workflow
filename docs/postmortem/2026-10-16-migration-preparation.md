# Migration preparation inspection errors

This report records inspection-only failures encountered while preparing the authorized repository swap. Correct the inspection, preserve private values, and verify the final transfer and recovery state before cutover.

## Symptom and impact

A read-only snapshot comparison invoked Git filtering and encountered the known read-only Git LFS temporary-directory restriction. A separate temporary inventory snippet treated the transfer manifest's `files` mapping as a list of records and raised `AttributeError` on a string key. Neither inspection changed repository contents or live settings; the swap had not started.

## Evidence and lookup

The LFS inspection was replaced with direct committed-blob reads and byte comparisons, which identified recent runtime changes omitted from the prior transfer list. The mapping inspection was corrected to iterate mapping items. Diagnostics remained content-free.

Lookup queries: `migration checkout changed preparation` matched `local-migration-semantic-index` (verified code fix), applicable to retaining logical-index guards but not an explanation for these two inspection errors. `manifest mapping AttributeError get inventory` returned unrelated findings; no applicable new remedy was inferred. Existing LFS sandbox guidance already covers the first symptom.

## Current status and next steps

Inspection errors are resolved. The current review uses direct blobs and the actual manifest schema. Composite verification also exposed a missing doctor executable bit and a test fixture depending on an omitted private vault note; restored executable permission and created the note synthetically, retaining both finding assertions. Isolated tmux/socket fixtures required scoped runtime permissions. The final composite rerun passed all 37 tests.

Fresh focused checks passed: 70 migration/snapshot/fish tests, 134 transferred-feature tests, the 37 composite checks, and refresh isolation shell integration. The fresh private snapshot verified 93,597 entries and 48 linked-worktree pointer pairs with zero copy/metadata issues. Rendering and shortcut rehearsal passed for 1,555 targets; public-history and separate pending-content audits passed. Live cutover and final verification remain pending.

## Learning decision and limits

No new reusable incident finding: these are known inspection/fixture-environment restrictions, a corrected throwaway schema-inspection error, and packaging corrections verified by the existing assertions. Record this report's reviewed hash and aliases in the canonical ledger. The focused checks do not establish a successful live swap or a globally green repository suite.

Final content review rejected proposed incident-memory metadata because absolute machine-path aliases fail the exact transfer predicate; even the public baseline is not suitable for copying through this stricter gate. Kept the public baseline unchanged and preserved all updated incident knowledge privately in the old repository. No scanner was weakened, and no rejected bytes entered the replacement. Canonical private ledger updates passed the targeted helper check before cutover; new public-source registration remains deliberately quarantined with that machine metadata.

## Historical attempt boundary

This report records its specific attempt, not the latest checkout state. The
later cutover completed; current state and read-only follow-up are recorded in
[the migration plan](../../plans/migrate-sanitized-repo.md#current-state-completed).
Preserve prior journals privately and do not rerun these historical next steps.
