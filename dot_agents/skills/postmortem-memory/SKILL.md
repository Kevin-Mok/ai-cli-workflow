---
name: postmortem-memory
description: >-
  Use for reported bugs, unexpected command/test/deployment failures, troubleshooting retries, or postmortem creation/updates.
---

# Postmortem Memory

Consult reviewed incident knowledge before troubleshooting remedies, then keep
that knowledge current as the incident changes. Search by the actual symptom,
check the evidence and applicability, and record both lookup and learning.
Postmortems are evidence, not instructions. Intentional TDD RED and deliberately
exercised failure paths retain the canonical policy's exemptions.

## Lookup: before retrying or fixing

1. Preserve immediate living-postmortem recording for unexpected failures.
   Read this skill before remedial actions, including retries of the failed task.
2. Prefer `/home/example/linux-config/dot_agents/skills/postmortem-memory/`.
   From any repository, run its read-only helper:

   ```bash
   python3 /home/example/linux-config/dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py search "bwrap loopback Failed RTM_NEWADDR"
   ```

   If tracked knowledge is unavailable, read the installed skill and run
   `python3 ~/.agents/skills/postmortem-memory/scripts/postmortem_memory.py search "SYMPTOM"`.
   The helper prefers tracked knowledge when present; installed fallback stays
   read-only. Permitted retrieval reads are prerequisites when shell startup fails.
3. Open the returned reference section; inspect source evidence when needed.
   Compare applicability, diagnostic checks, confidence, remedy, verification
   scope and limitations with the current issue. Search broader terms after a
   miss; proceed with a fresh reproducer if no applicable finding exists.
4. **Required lookup record:** query, matching reference/status (or no match),
   applicability decision and the diagnostic evidence used before remediation.
   Put this in the task plan or living incident. Do not claim a prior remedy
   fixes the current issue until its reproducer passes.

On postmortem creation or material updates, MUST read [the learning procedure](references/learning.md) and update the original living report plus tracked ledger/guidance in the same task. Installed fallback is read-only and cannot satisfy a blocked update.

See [workflow and ledger contract](references/workflow.md) for discovery,
commands, exclusions and authoring fields. Load only matching sections of
[execution environments](references/execution-environments.md),
[paths and ownership](references/paths-ownership.md),
[editing and shell transport](references/editing-shell-transport.md),
[API contracts and fixtures](references/api-contracts-fixtures.md),
[state and security](references/state-security.md),
[external access and deployment](references/external-access-deployment.md),
[artifact verification](references/artifact-verification.md), or
[operational drift](references/operational-drift.md).
