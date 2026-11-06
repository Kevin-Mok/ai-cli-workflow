# Prompt attachment ZIP packaging — PASS (2026-11-06)

Explicit user request; value5, uniqueness1. Closest precedents are
existing:metaprompt (prompt authoring) and existing:feedback-memory (durable
preferences); neither requires portable attachment ZIPs with scoped ignore rules.
Merge into the existing prompt-save bullet; add no skill or trigger.
Measured rule addition: 231 UTF-8 bytes/57.75 estimated recurring tokens;
body0, weightedcost57.75, score19.047619. No savings claimed.
Baseline: `scripts/trim-benchmark --plain` reports loaded_bytes14800.
Scope/privacy: generic user-requested workflow only; archive contents remain
private and ignored. Prepared cases: attachments require packaging; no attachments
require no ZIP; direct/nested prompt ZIPs are ignored; non-ZIP prompts remain visible.
Rule remains in the existing documentation section; catalog/triggers are unchanged.
Current canonical file already exceeds the historical 9KB budget; this explicit
user-directed addition is a disclosed exception, not a claim of budget compliance.
