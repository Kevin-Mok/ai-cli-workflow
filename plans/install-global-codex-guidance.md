# Install Global Codex Guidance

## Goal

Make the repository's canonical Codex guidance and reusable skills available
to every local Codex session through live symlinks.

## Plan

- [x] Link `~/.codex/AGENTS.md` to `dot_codex/AGENTS.md`.
- [x] Link every `dot_agents/skills/<skill>` directory into
  `~/.codex/skills/<skill>` without modifying bundled `.system` skills.
- [x] Link `dot_agents/system-design` to `~/.agents/system-design`.
- [x] Verify every link resolves to this checkout and source/target skill
  names match.
- [x] Add an idempotent installer that reproduces the links and refuses to
  overwrite user-managed paths.
- [x] Add automated coverage for dry-run, idempotent install, link targets,
  skill count, and collision protection.
- [x] Document the manual installer smoke test in `docs/smoke-tests.md`.

## Review

Completed on 2026-07-16. The global AGENTS link and system-design support-pack
link resolve to this checkout; all 43 skill links resolve to readable
`SKILL.md` files. Codex's bundled `~/.codex/skills/.system` directory remains
present, and no dangling symlinks were found.

The repository now provides `scripts/executable_install-global-codex-guidance`
for repeatable setup. Its test uses a temporary home directory and covers both
the successful idempotent path and user-managed-path collision protection.
