# Postmortem Learning

Use on report creation or material updates. Preserve immediate incident recording
and tracked-source ownership; fallback retrieval does not authorize installed edits.

## Learning: on creation and material updates

1. Update the original living report immediately; retain the symptom, impact,
   evidence, current status and next steps. At resolution add cause, remedy,
   verification and remaining limits.
2. Directly edit the **tracked linux-config** ledger and relevant topic guidance
   during the same task. Read the full report, use `scan` for its SHA-256 and
   aliases, and link it to findings or a specific no-new-learning decision.
   On a changed report, move its alias to the reviewed new hash, preserving
   still-valid copied aliases. Reconcile affected finding/source links and
   reference text; retire evidence that no longer supports a claim.
3. Distinguish `verified_fix`, `verified_workaround`, `unresolved` and
   `activation_pending`. A suggested remedy is unresolved. A passing code check
   cannot establish live activation. Root-cause confidence is a separate field.
4. Run the targeted read-only check:

   ```bash
   python3 /home/example/linux-config/dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /absolute/path/to/report.md
   ```

5. **Required learning record:** report/hash, finding IDs or no-new-learning
   reason, status/evidence scope, tracked edits and targeted-check result.
   If permissions block a tracked write, report the exact path and outstanding
   update; obtain the normal workspace approval. Never edit installed copies
   as the source of truth. Fallback lookup does not satisfy a blocked update.

Return to [the skill entrypoint](../SKILL.md) for the shared workflow and boundaries.
