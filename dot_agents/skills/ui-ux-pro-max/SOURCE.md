# UI/UX Pro Max source record

This package vendors the offline retrieval runtime and design data of the upstream skill. Review this record before updating the fixed source revision or changing invocation policy.

- Reviewed: 2026-10-14; upstream version metadata: 2.15.0.
- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Fixed commit: [56ea9cf174ed86786187daa9de0e6247cb0747e4](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/56ea9cf174ed86786187daa9de0e6247cb0747e4).
- Reviewed [README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/56ea9cf174ed86786187daa9de0e6247cb0747e4/README.md), upstream `.claude/skills/ui-ux-pro-max/SKILL.md`, `skill.json`, Python runtime, CLI manifest and init/update/GitHub helpers.
- Byte-identical files: complete `src/ui-ux-pro-max/data/` directory and `src/ui-ux-pro-max/scripts/{core,search,design_system,reasoning_contract}.py`.
- [MIT licence](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/56ea9cf174ed86786187daa9de0e6247cb0747e4/LICENSE): copyright 2024 Next Level Builder; bundled verbatim as LICENSE. Font licence metadata and provenance snapshots remain in data; no fonts are bundled. Check individual font/package licences when using suggestions.
- Local changes: short rewritten SKILL.md with relocatable paths, explicit invocation and persistence guidance; added `agents/openai.yaml`. No upstream templates, plugin manifest, installer, catalog refresh tools, tests or preview app are installed. Runtime/data are unmodified.

The upstream ships an agent skill, Python BM25/CSV retrieval and rule-based design-system generation, a Node installer (`ui-ux-pro-max-cli` / `uipro`), and Claude plugin packaging. It is not an MCP service. Vendored runtime imports only Python's standard library and has no network/auth/telemetry calls. No account, API key, paid tier or subscription is needed for these files. Agent-provider costs remain separate. Generated Google Fonts URLs/imports can cause browser network requests if adopted. Installer/update paths use npm and GitHub; optional PATs (`--token`, `UI_PRO_MAX_GITHUB_TOKEN`, `GITHUB_TOKEN`) raise GitHub rate limits. No telemetry client was found in the reviewed runtime/CLI; this is source inspection, not a full dependency audit or hosted-site privacy review.

Update by selecting a new immutable commit, reviewing the diff/licence, copying the same runtime/data paths, updating this record, and rerunning packaging, upstream and smoke checks. Do not run `uipro update`: its force-refresh can replace local invocation policy. Existing generated companion skills are not removed by this change.
