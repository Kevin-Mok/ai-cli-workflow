# Planning-only Procedure

Use only for planning-only requests. Preserve the entrypoint read-only guard;
return before the execution workflow.

Inspect the repository, branch, status, all staged/unstaged/untracked diffs,
history and related files. Plan every safe, reviewable group oldest-to-newest;
preserve prerequisite chronology and explain ambiguity. Identify secrets,
credentials, caches, generated files, risky binaries and ownership questions as
exclusions. Review README impact without applying repairs. Keep companion
plans, docs, tests and postmortems with the matching implementation. Treat
ordinary validation and README findings as warnings for later execution.

Then return: working-tree summary; numbered commit groups with purpose, files,
rationale, README impact and concise Conventional Commit subjects/minimal
concrete bodies; risks and exclusions; optional manual commands in chronology;
and a final subject-only message summary. Recommend the smallest checks for
later execution and **return before the delivery workflow**.

Return to [the skill entrypoint](../SKILL.md) for the shared workflow and boundaries.
