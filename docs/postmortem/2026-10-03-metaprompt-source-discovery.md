# Metaprompt source discovery corrections

- Date: 2026-10-03
- Symptom: A search-indexed jaiskills URL and GitHub contents query returned
  404. A local search including a guessed `dot_local/bin/second-brain*` path
  exited 2 because that path does not exist.
- Impact: Read-only research needed corrected paths; no implementation or
  user files were affected.
- Root cause: The indexed upstream directory moved from `skills/prompting/`
  to `skills/models/`; the local helper layout had been assumed rather than
  enumerated. The web tool also could not open the GitHub API URL.
- Resolution: Enumerated the upstream Git tree through the public API and
  inspected the actual fish refresh function and `scripts/` helpers.
- Verification: Public API returned the current tree and MIT metadata;
  `dot_config/fish/functions/refresh-config.fish` and
  `scripts/executable_snapshot-codex-config` were read successfully.
- Status: Resolved for this task. Follow-up: enumerate paths before targeted
  reads and verify search results against current upstream trees.
