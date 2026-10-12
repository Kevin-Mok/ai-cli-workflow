# Add installed agent skills

Import the installed last30days and find-skills packages into chezmoi source, document their provenance, and refresh the live configuration so future sessions use managed copies.

## Context and scope

Sources are ~/.agents/skills/last30days (157 files, version 3.28.0) and ~/.agents/skills/find-skills (one SKILL.md). Neither is currently tracked. Import installed bytes without upstream rewrites, retaining all assets and executable permissions through chezmoi naming. A subsequent commit-session request authorizes committing and pushing this session only.

## Decisions and risks

Use dot_agents/skills as the canonical source. Record local-source provenance and do not invent upstream commit IDs. The 4,014,063-byte dog-original.jpeg requires a matching Git LFS attribute. Refresh is authorized, including normal Codex/Git snapshots and chezmoi apply. Preserve initial dirty docs/smoke-tests.md, feedback.log, postmortem-memory references/artifact-verification.md and references/paths-ownership.md and sources.json, dot_config/mimeapps.list, and dot_config/vesktop/settings/settings.json. Append only scoped additions to shared dirty files.

## Implementation

- [x] Capture status, inspect installed packages and local policy.
- [x] Import both packages, record SOURCE.md, and configure the large asset for LFS.
- [x] Update root README, skill catalog, and installed-skill smoke checks.
- [x] Run refresh-config and verify package bytes and executable permissions.

## Verification

Compare every installed package file with its chezmoi-rendered counterpart and its original SHA-256 inventory; no research requests or credential setup are required. Run python3 -B ~/.agents/skills/last30days/scripts/last30days.py --help from the installed tree to validate relative imports offline. Check both managed source paths and large-asset LFS attributes. Run git diff --check for touched text and the incident targeted ledger check. Re-read final diff. Manual handoff: inspect managed source paths, render the skill definitions, and run offline help.

## Progress and review

The initial sandbox runner failed before execution; approved scoped execution works. The living report and targeted postmortem-memory registration record this known workaround. No new behavior is being designed; this is a package import, so defining RED tests do not apply. Rollback is removal of this task's new skill directories and scoped documentation/attribute additions; preserve all prior user changes. No worktree. All 158 original files match their chezmoi-rendered SHA-256. Large image has filter/diff/merge=lfs. git diff --check passed. Installed offline help exited 0. Direct source-tree help failed because chezmoi escapes private_files.py as literal_private_files.py; use installed entrypoints, as recorded in the second incident. fish -c refresh-config exited 0 with REFRESH COMPLETE; log: /tmp/refresh-config-20261012-162756-3091419.log. Post-refresh installed hashes match all 158 originals, both SOURCE.md files match rendered source, and installed help exited 0. Both targeted postmortem-memory checks passed with no errors. Refresh introduced no additional dirty tracked paths. README-sync outcome: update_in_same_change, with grounded research/discovery links added and existing recruiter-first hierarchy preserved. No external research or credential health checks were run. No remaining import blockers. Suggested future commit subject: chore(skills): add last30days and find-skills.


## Delivery milestone: chore(skills): add last30days and find-skills

Ready for the session-scoped commit on main, followed by one push to origin/main. Session ID: 01a131c8-da73-7172-90e5-79c913e6bf3c. Scope helper reported no successful repo-writing actions; directly observed imports and edits establish scope. Stage only our installed-skill smoke additions and the two skill-import report records in sources.json, leaving all pre-existing hunks untouched. Include the new packages, LFS rule, README/catalog, incidents and this plan together. README gate reports pass_no_change; fresh package integrity verification passed. No implementation changes were made during delivery, so the completed refresh remains applicable. Commit hash and push result will be reported in the final handoff. Remaining pre-existing work includes feedback, memory references/ledger, desktop configs and unrelated smoke checks.

Final staged check warning: eight upstream trailing-whitespace lines in providers.py/watchlist.py; preserved byte-for-byte by design. Recorded in the matching whitespace incident. This warning does not block the authorized scoped commit. Exact staged smoke/ledger hunks were reviewed; no pre-existing changes are staged. LFS staging produced a valid pointer for the 4 MB asset.
