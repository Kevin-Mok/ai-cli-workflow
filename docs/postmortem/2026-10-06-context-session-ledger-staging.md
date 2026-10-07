# Context session ledger staging assertion

Preserve mixed incident-ledger edits while staging only the current context session. This report records the stopped formatting assumption and its safe index-only repair.

## Symptom and impact

The staging script asserted that sorted-key JSON serialization matched HEAD. Existing report objects retain varied key order, so the assertion failed. Only reviewed README, smoke-test and lesson hunks were staged; the ledger and all worktree bytes were unchanged.

## Lookup and evidence

Lookup: postmortem-memory search "session staging ledger serialization key order". No exact serialization match; existing source-ownership guidance applies to separating baseline-dirty records. HEAD contains mixed report key orders. Expected report count was four.

## Resolution and verification

Preserve HEAD text exactly and insert only this session's five reviewed report objects at the reports-array boundary. Assert the parsed staged ledger equals HEAD plus those objects. Inspect the staged diff and run the targeted ledger check. Status: verified index-only repair; no private payloads or unrelated records staged.

## Follow-up

Avoid assuming canonical formatting when reconstructing a mixed-file index blob. Use structural equality plus minimal textual insertion.
