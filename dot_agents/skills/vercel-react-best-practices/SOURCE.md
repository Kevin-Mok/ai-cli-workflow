# Source and evaluation

This pins Vercel's React performance skill for optional use in Codex CLI and
Claude Code. It supplies technical review examples alongside the existing
visual-design skills, without installing the rest of the collection.

- Upstream repo: https://github.com/vercel-labs/agent-skills
- Upstream commit: `063bee94c3f4df8453406c830b0a7df0f2860278`
- Original source path: `skills/react-best-practices/`
- Adapted on: `2026-10-14`
- Reviewed import snapshot: `bef1bc61c33450cddc8fd34e645e915b7866ec92`.
- Public intake on `2026-10-22`: removed internal evaluation-history references;
  preserved the upstream guide, entrypoint, license and client metadata.
- Adaptation basis: vendored upstream `SKILL.md` and compiled `AGENTS.md`.
- Local adaptation: explicit-only frontmatter and Codex policy, concise
  description, version/measurement cautions, compiled-only reference routing;
  rename compiled guide to `references/react-best-practices.md` so it is not
  a directory instruction file. Repair its three relative rule links to anchors
  within that document. No rule bodies changed; omit duplicate individual rules,
  build scripts, packages, archives and unrelated skills.
- Upstream compiled guide SHA-256:
  `fc93e7421177bbf869cce892bc60a6c83a4517d974bc3bf65c4e2c1e58a6ccf6`.
- Licence: [README declaration](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/README.md#license)
  and [React skill](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md)
  declare MIT. The reviewed tree contains no standalone LICENSE/COPYING file.
  Local LICENSE supplies standard MIT terms with Vercel attribution based on
  those declarations; it is not an upstream licence-file copy. No upstream
  copyright year was supplied. Preserve this caveat when updating the import.
- Discovery: https://x.com/Mnilax/status/2110382356028686598; tweet contents
  were not retrievable and are not evidence for repository capabilities.

## Product and security boundaries

The repository ships nine Agent Skills directories, supporting scripts, ZIPs,
and build packages. It is not an MCP server, design app, or UI component library.
README labels differ from disk for deployment and React Native, and omit the
token-based CLI skill. Review the tree rather than installing every advertised
capability with `npx skills add`.

The vendored subset is static Markdown/YAML: no account, API key, paid tier,
executable helper, active telemetry, or required network call. Optional source
links need ordinary public HTTPS. Existing agent-provider costs still apply.
No installer CLI runs here, so its telemetry is outside this integration.

Excluded upstream surfaces:

- Web/writing guidelines fetch mutable `main/command.md` from separate GitHub
  repositories each review, creating a network dependency and changing policy.
- Deployment helpers upload project tarballs to
  `claude-skills-deploy.vercel.com/api/deploy` or
  `codex-deploy-skills.vercel.sh/api/deploy`. Exclusion lists are not comprehensive
  secret protection. Deployment guidance also proposes broad Git writes/pushes.
- Token-based CLI guidance prints environment tokens and greps `.env` files.
  Do not import these instructions into this skill.
- Vercel Optimize requires authenticated Vercel CLI, a linked project and API
  calls; route metrics depend on Observability Plus, with possible service costs.
  Billing/team/project data enters local audit artifacts. Provider retention,
  pricing, and CLI telemetry were not verified by live execution.

## Recommendation and overlap

**8/10: add only this explicit-only React subset.** the retired `optimize` skill historically discussed
React memoization and profiling, and design/audit skills cover general UI quality.
This adds deeper request-waterfall, RSC serialization/cache isolation, server
action authentication, bundle-import, hydration, and rerender examples.
It does not replace brand direction, component discovery or visual QA.

Use the existing `dot_agents/skills` deployment and
`run_after_install-claude-skills.sh.tmpl` directory linker. No Codex MCP or Claude
MCP configuration is needed. After separately authorized deployment, invoke
`$vercel-react-best-practices` or `/vercel-react-best-practices` explicitly.
This evaluation does not apply configuration or modify installed skills.

## Unverified items

Live discovery and explicit-only behavior in both clients, real-project speed
gains, framework-version compatibility of every example, upstream release
maintenance, deployment endpoint retention, and paid-service runtime behavior
remain unverified. The compiled reference is about 108 KB and can consume a
large context window if read in full; load only relevant sections. Updates are
manual, with revision and adaptation review, rather than an automatic updater.
