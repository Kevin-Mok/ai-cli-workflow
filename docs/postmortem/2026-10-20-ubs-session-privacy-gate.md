# UBS session privacy gate

Keep public incident records useful without publishing machine-local home paths. Review the exact isolated commit candidate, sanitize its aliases, and rerun the required privacy check before committing.

- Symptom and impact: the isolated UBS candidate was blocked by one `home_path` category finding before any commit or push.
- Evidence: the required privacy gate exited 1; staged incident ledger aliases used the live home root.
- Lookup and applicability: existing privacy and local-path boundaries apply. The ledger needs live aliases for local targeted checks, while published aliases use the existing public example root.
- Resolution: sanitize only session-owned aliases in the isolated public candidate, preserving live local aliases and unrelated ledger edits in the working tree. Do not relax scanner rules or hooks.
- Status: resolved for the public candidate; local live aliases remain uncommitted.
- Verification: repaired isolated candidate privacy scan exited 0 with PASS. Repeat the gate immediately before committing the final documentation revision. No privacy rules or hooks were bypassed.
- Learning: no new reusable finding; existing public privacy boundary applies. Local checks and public candidate checks have different path roots and must both be reported honestly.

- Final review evidence: all three local targeted ledger checks passed, and staged report SHA-256 values match staged ledger records. A reviewer initially selected the wrong JSON key for the hash check, corrected it to `reports`, then verified all three; no production files were affected.
