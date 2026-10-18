# Managed Public Design Skills

This repository manages external design skills through chezmoi and vendors
UI/UX Pro Max at a reviewed immutable revision. Normal deployment clones the
external sources, exposes their Codex links, and deploys shared tracked skills
for Codex CLI and Claude Code. See the evaluation below before choosing a skill.

## Included sources

| Capability | Upstream | Installed path |
| --- | --- | --- |
| Impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `~/.codex/skills/impeccable` |
| 21st CLI, AI, design sync, registry | [21st-dev/skill](https://github.com/21st-dev/skill) | `~/.codex/skills/21st-*` |
| Review Animations | [emilkowalski/skills](https://github.com/emilkowalski/skills) | `~/.codex/skills/review-animations` |
| Scroll World | [oso95/scroll-world](https://github.com/oso95/scroll-world) | `~/.codex/skills/scroll-world` |
| UI/UX Pro Max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `~/.agents/skills/ui-ux-pro-max/` with a Claude directory link |
| Higgsfield plugin | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | `~/.codex/plugins/higgsfield` |

## Daily refresh

`design-skills-sync.timer` runs at 05:00 local time with
`Persistent=true`; a missed run is caught up when the user manager starts.
Its service refreshes only the managed upstream repositories fast-forward and
leaves the vendored UI/UX Pro Max skill pinned. `--bootstrap` is retained as a
compatibility no-op for the old one-time hook; no npm installer runs. It does
not authenticate 21st or Higgsfield, create media, spend credits, or upgrade the Higgsfield CLI.

Use `sync-design-skills --dry-run` to preview the source refresh. Use
`setup-design-skills-timer --check`, `--enable`, or `--disable` to manage
the user timer. Both commands require no sudo.

After a refresh, restart Codex to load the updated skill definitions. For
Higgsfield, install its CLI separately if needed, then run
`higgsfield auth login` yourself before requesting any generation.

## UI/UX Pro Max evaluation (2026-10-14)

**Recommendation: 8/10 — retain it as an explicit-only, pinned shared skill.**
The repo previously advertised a global Codex install using an unpinned npm
CLI. This change replaces that route with reviewed local Python runtime/CSV
files, [MIT licence and source provenance](../dot_agents/skills/ui-ux-pro-max/SOURCE.md),
and both agent invocation gates. No MCP entries or accounts are required.

It is an upstream agent skill with an optional Node installer and Claude plugin
packaging, not an MCP server or UI component library. Despite the README's
“AI-powered” language, the bundled generator uses deterministic BM25 retrieval
and rules; the calling agent supplies interpretation and implementation.
Invoke `$ui-ux-pro-max` in Codex or `/ui-ux-pro-max` in Claude Code after the
normal shared-skill deployment and session restart. The skill's `--help`
documents domains, stacks, JSON output, design-system generation and optional
persistence. Existing MASTER files are preserved unless explicitly forced.

### Overlap with existing skills

| Existing capability | Overlap and distinct role |
| --- | --- |
| `frontend-design`, `design-taste-frontend`, `high-end-visual-design`, `redesign-existing-projects`, `minimalist-ui` | Strong overlap in visual direction; those prompts lack this bundled searchable CSV engine. |
| 21st CLI/registry skills | Component sourcing; UI/UX Pro Max supplies guidance rather than installed components. |
| Impeccable, `critique`, `audit`, `polish`, `animate` | Use these for craft and rendered verification; retrieved suggestions are not proof of quality or accessibility. |

### Pros, cons and tradeoffs

Pros: offline Python standard-library runtime, concrete domain/stack search,
structured output, candidate design-system synthesis and optional persistence;
shared complete directory works with both CLI agents. Vendoring removes npm
execution, API credentials and automatic policy drift from this route.

Cons: broad advice duplicates many existing skills, retrieval is heuristic,
and its approximately 3 MB dataset requires manual reviewed updates. Static
framework guidance can age. It is not a renderer or accessibility validator.
Explicit invocation trades automatic discovery for deliberate use and avoids
another broad default design trigger. Previously generated companion skills on
an existing host are not removed or retroactively gated by this change.

Security/licence: MIT copyright 2024 Next Level Builder is retained. Search
runtime has no network, account, paid tier or telemetry requirement. Source
inspection found no runtime/CLI telemetry client; installer paths use npm and
GitHub (optional PAT for rate limits), which this integration does not execute.
Generated Google Fonts imports can cause network requests when adopted in an
app; individual font/package licences still apply. Only text/catalog metadata,
not font binaries, is bundled. Agent-provider billing remains separate.

Unverified: live Codex/Claude discovery after deployment, full visual quality,
and third-party dependency/site privacy policies.
