# Trim intake history-audit findings

The required privacy preflight found historical candidates before any private
PR source was imported. Review these candidates separately from the safe current
index and inspect every selected incoming file before it can enter a commit.

## Symptom, Impact And Evidence
Both `audit-public-history --scope all` and `--scope reachable` exited 1 after
checking 1,463 commits and 5,935 unique blobs. Each reported 1,604 candidates:
13 credential, 1,462 email, 4 home-path, 4 provider-token and 121 runtime-ID.
Only these aggregate counts are published; no matched value or source payload.
The exact current index privacy gate exited 0, `Privacy gate PASS`.

## Current Status
Unresolved historical candidates. The current index is unchanged baseline
content; its PASS does not cover the prepared cull, untracked files or private
intake. No private remote was added or fetched and no PR source was imported.
No history rewrite, push, live configuration apply or permission bypass occurred.
The metadata read-only boundary also still prevents staging and local commits.

## Interpretation And Next Steps
An audit match is a candidate, not a verified secret disclosure. Metadata,
reviewed synthetic fixtures and actual sensitive values require different
adjudication; no conclusion about individual matches is claimed. Keep detailed
safe diagnostics in `/tmp/trim-intake-*-audit.log`. Do not publish raw values.
After the cull, review only the approved private paths, drop private/personal
content, and run the exact-candidate gate on every imported file. Resolve or
explicitly account for historical candidates before any public delivery; no
history cleanup is authorized by this task.

## Learning
No remedy or clean-history claim established. Existing source-scope and
privacy-boundary guidance applies. Canonical postmortem hash/alias registration
at `/home/kevin/linux-config/dot_agents/skills/postmortem-memory/` remains outside
permitted writes, alongside the earlier task incidents. No installed copy changed.
