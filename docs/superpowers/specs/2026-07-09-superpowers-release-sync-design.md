# Superpowers Release Sync Design

## Goal

Keep the externally managed `obra/superpowers` skill bundle updated on a
manual release basis while letting chezmoi own the installed files.

## Design

`~/.codex/superpowers` is managed as a chezmoi external archive sourced
from the latest GitHub release tarball for `obra/superpowers`. This
avoids tracking upstream `main` while preserving a reproducible
home-directory target. The existing symlink at
`~/.agents/skills/superpowers` continues to point at
`~/.codex/superpowers/skills`, so Codex discovers the release-managed
skills through the same path as before.

Updates are intentionally manual. The operator runs
`sync-superpowers-release`, which calls `chezmoi apply
--refresh-externals` for only the Superpowers checkout and its skill
symlink. A `--dry-run` mode previews the same refresh without writing
files.

## Risks

Moving from `git-repo` to `archive` removes the local `.git` checkout
under `~/.codex/superpowers`. That is intentional: release sync should
consume upstream release artifacts, not act as a development clone.
Rollback means reverting this repo's external definition or temporarily
checking out a specific archive URL in `.chezmoiexternal.toml.tmpl`.

## Verification

- `chezmoi execute-template '{{ (gitHubLatestRelease "obra/superpowers").TarballURL }}'`
- `bash -n scripts/executable_sync-superpowers-release`
- `./scripts/executable_sync-superpowers-release --help`
- `./scripts/executable_sync-superpowers-release --dry-run`
