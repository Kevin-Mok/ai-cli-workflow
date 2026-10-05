Implement a shared Codex troubleshooting skill named postmortem-memory
in /home/example/linux-config.

Create the tracked skill at dot_agents/skills/postmortem-memory/.
Keep SKILL.md compact, with trigger metadata, a lookup workflow, an update
workflow, and links to supporting references. Add agents/openai.yaml
using existing conventions.

Build the initial knowledge from all eligible postmortems and incident
reports under /home/example/coding and this repo. Include ignored and
historical repository copies, but prune dependencies, build output, .git,
and private personal-context material before reading. Exclude templates
and unrelated narrative content. Deduplicate exact content while retaining
all source aliases.

Review every unique report. Distill reusable patterns into topic references
covering execution environments, paths and ownership, editing and shell
transport, API contracts and fixtures, state and security boundaries,
external access and deployment, artifact verification and measurement,
and operational drift or resource limits.

Each finding must include searchable symptoms, applicability, diagnostic
checks, root cause confidence, remedy, verification evidence, limitations,
and source links. Distinguish verified fixes, verified workarounds,
unresolved diagnoses, and activation pending. Record reviewed reports
without reusable findings rather than inventing guidance. Avoid copying
raw reports or sensitive details into the skill.

Package a Python standard-library helper, postmortem_memory.py:
- scan: report discovered documents, hashes, duplicate aliases, and new
  or changed sources; accept repeatable --root overrides.
- search QUERY: search symptom signatures and distilled guidance, returning
  matching reference locations, status, applicability, and sources.
- check: validate references and source coverage; support --postmortem PATH
  for checking one report during a task.

These commands are read-only. Maintain a tracked sources.json ledger
linking reviewed content hashes to findings or explicit no-new-learning
decisions. Report unreadable sources and incomplete coverage clearly.

Prefer the tracked linux-config knowledge when available; use the installed
skill as a read-only fallback. Never update installed copies as the source
of truth.

Update dot_codex/AGENTS.md with a mandatory rule: for a reported bug or
unexpected task failure, read postmortem-memory and search before remedial
actions. Preserve immediate living-postmortem recording. On creation and
material updates, update the shared ledger and relevant guidance directly
in linux-config, then run the targeted coverage check. Respect workspace
permissions and preserve unrelated dirty work. Intentional RED tests and
deliberately exercised failure paths retain their existing exemptions.

Update the skill catalog, README, smoke tests, and an ExecPlan together.
Add tests before implementation and record RED/GREEN evidence. Run
refresh-config after the configuration changes with the established
ownership preflight. Do not commit or push without separate authorization.
