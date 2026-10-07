# Personal context with committed project knowledge

Implement and verify automatic relevant personal-context use and private project knowledge, following the active plan and preserving unrelated work. Use small briefs first, keep evidence available through explicit detail retrieval, and keep all real personal data outside this repository.

```prompt
Read dot_codex/AGENTS.md, plans/enable-personal-context-for-dev-choices.md, and the personal-context skill, storage contract, helper modules and synthetic tests.

Preserve v1 context.json, Markdown sources, correction precedence and forgotten-key protection. Keep real records, summaries, indexes, caches and payloads exclusively in /home/example/coding/personal-context. Do not capture private retrieval or discussions into this repo, feedback, Second Brain, Graphiti or other services.

Index only example-user Mok's committed contributions under /home/example/coding. Require the exact Git author name example-user Mok (case-insensitive) on each source's latest modifying commit, tracked HEAD membership and exact working-copy/committed-blob equality. Resolve nested projects to their actual Git owner. Exclude uncommitted, untracked, unqualified, sensitive, dependency/generated and symlink-escaping sources. Record author/commit/blob-hash evidence and inspection dates. Attribution is not exclusive ownership or capability.

Use topics/projects/brief first, at most eight records and 6,000 serialized characters by default; detail retains full evidence. Cache projections deterministically from validated stores. Preserve invalid authoritative files, provide bounded direct projections if cache writes fail, lock updates, write atomically, enforce private modes and remove forgotten information from every managed projection with rebuild suppression. Mark missing qualified projects historical/unavailable and exclude them from current recurring findings.

Verify defining synthetic RED/GREEN coverage with python3 -B -m unittest discover -s tests -p 'test_personal_context*.py' -v; regression with python3 -B -m unittest discover -s tests -p 'test_second_brain_skill.py' -v; typed helper with basedpyright dot_agents/skills/personal-context/scripts/context_store.py; README with ./scripts/executable_readme-recruiter-sync. Keep grouped docs/smoke-tests.md checks current.

Inspect real project sources read-only; initial foundation uses bounded batches and later refreshes only relevant projects. Report only safe coverage/count metadata here. Run refresh-config after tracked configuration changes, accounting for its live-to-tracked Codex snapshot. Verify installed files/implicit metadata and fresh automatic, explicit and mechanical-work sessions. Do not commit or push unless separately requested.
```
