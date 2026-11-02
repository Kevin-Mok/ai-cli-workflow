# Documentation And Config

Read this procedure when its mandatory canonical AGENTS trigger applies. Follow
the preserved rules below before acting; active user/developer instructions govern.

- Start every how-to or procedural document with a short, plain-language
  overview directly below the title. Explain what the document helps the
  reader accomplish and summarize the main steps before detailed instructions
  or commands. Keep it direct and easy to understand.
- Treat root `README.md` as the public operating surface. When instructions,
  config, skills, plans, onboarding, or documented commands change, keep it
  accurate. Preserve its technical-deep order: recruiter hook, hero, stack
  rationale, navigation, AI proof, then setup and broader dotfiles detail.
- Before staging or finalizing any commit or push workflow, run the
  `readme-recruiter-sync` skill (or
  `./scripts/executable_readme-recruiter-sync`). The gate requires truthful
  install/bootstrap, day-to-day use, documented command options, repo-grounded
  tech-stack rationale, and recruiter value. Include safely separable README
  repairs; report remaining findings without blocking eligible commits.
- When a reusable manual check appears or changes, update
  `docs/smoke-tests.md` in the same change. Use grouped `Action` and
  `Expected` entries; update stale checks rather than duplicating them.
- When a user asks for clarification because a smoke test or documented
  procedure is unclear, update `docs/smoke-tests.md` or the relevant
  document in the same change; do not leave the clarification only in chat.
- After every tracked configuration change, run `refresh-config` before completion
  unless explicitly told not to; this applies to every change, not only environment
  behavior changes. The helper applies reviewed chezmoi files, regenerates
  shortcuts, and reloads fish. Keep live Codex/Git settings in private local
  configuration; refresh excludes scripts, externals, and removals and stops
  on conflicts; reconcile newer local files into source using the rule above
  before retrying.
