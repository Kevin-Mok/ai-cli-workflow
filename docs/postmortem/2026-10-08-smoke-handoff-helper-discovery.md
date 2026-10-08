# Smoke handoff helper discovery

Locate the actual configuration refresh function before verifying the new post-commit handoff rule.

- Symptom: a read-only rg query named scripts/executable_refresh-config, which does not exist, and exited 2.
- Impact: no writes or user files were affected; helper inspection was briefly incomplete.
- Evidence/root cause: rg --files identified dot_config/fish/functions/refresh-config.fish. The command is a fish function, not a scripts executable.
- Lookup: searched missing guessed documentation helper path. Existing path discovery and fixture-contract guidance applies; no new reusable learning.
- Resolution/verification: read the discovered refresh-config.fish and refresh-config-task.fish successfully. Use fish -c refresh-config for the required invocation.
- Status: discovery error resolved; refresh outcome is verified separately. No product fix required.
