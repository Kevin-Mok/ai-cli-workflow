# Postmortems

Read this procedure when its mandatory canonical AGENTS trigger applies. Follow
the preserved rules below before acting; active user/developer instructions govern.

- For a reported bug or unexpected task failure, read
  `/home/example/linux-config/dot_agents/skills/postmortem-memory/SKILL.md`
  (installed `$postmortem-memory` as read-only fallback) and search relevant
  symptoms before retries or remedial actions. Record applicability and evidence;
  preserve immediate living-postmortem recording. Intentional RED tests and
  deliberately exercised failure paths retain their existing exemptions.
- Whenever a postmortem is created or materially updated, update its reviewed
  hash/aliases and findings (or explicit no-new-learning decision) directly in
  `/home/example/linux-config/dot_agents/skills/postmortem-memory/`, including
  relevant guidance, during the same task. Run its helper `check --postmortem
  /absolute/path/to/report.md`. Preserve unrelated dirty work and workspace
  permissions; report exact blocked writes and outstanding learning updates.
  Never make installed copies the source of truth.
- For every unexpected task failure—an unplanned unsuccessful command, test, deployment, or workflow outcome—immediately create a dated, descriptive postmortem under `docs/postmortem/`. Record the symptom, impact, evidence, current status, and next steps; keep that same document current throughout investigation. When the issue is fixed, update it with root cause, resolution, verification, and follow-up, and keep the completed postmortem in the same commit as the related fix. Deliberately failing TDD RED tests and intentionally exercised failure paths do not trigger a postmortem.
