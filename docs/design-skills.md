# Managed Public Design Skills

This repository keeps Impeccable as its external design skill and preserves the
separate Higgsfield plugin integration. Preview retained-source updates before
refreshing them, then restart agent sessions. The approved skill cull removes
unused installers and discovery links without deleting installed upstream files.

## Included sources

| Capability | Upstream | Installed path |
| --- | --- | --- |
| Impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `~/.codex/skills/impeccable` |
| Higgsfield plugin | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | `~/.codex/plugins/higgsfield` |

The shared tracked `frontend-design` and `brand-system-designer` skills remain
available. Codex and Claude use complete shared skill directories; the generic
Claude linker preserves supporting files and refuses non-symlink conflicts.

## Daily refresh

`design-skills-sync.timer` runs at 05:00 local time with `Persistent=true`,
catching up a missed run when the user manager starts. It refreshes only the
Impeccable source and Higgsfield plugin, with fast-forward-only Git updates.
`sync-design-skills --dry-run` previews these exact targets. The legacy
`--bootstrap` option remains a no-op; the obsolete one-time bootstrap hook is
removed. No npm installer runs.

Use `setup-design-skills-timer --check`, `--enable`, or `--disable` to manage
this retained timer. These commands require no sudo. Restart agent sessions
after a refresh to load updated skill definitions. Higgsfield authentication,
CLI installation and generation remain separate user operations.

## Retired integrations and existing hosts

The approved cull removes repo installation and exposure of `21st-ai`,
`21st-cli-use`, `21st-design-sync`, `21st-registry`, `review-animations`,
`scroll-world`, and the entire Superpowers bundle. UI/UX Pro Max is no longer
vendored or bootstrapped. The upstream repositories and existing home-directory
copies are untouched by this change.

Superpowers service/timer sources are removed. `sync-superpowers-release`,
including `--dry-run`, is now a compatibility no-op. Its setup command's
`--enable` is refused, while `--check` reports only the disabled repo integration
and does not inspect live timers. `--disable` remains an explicit cleanup action
for an already-installed `superpowers-release-sync.timer`; it needs no source
checkout or chezmoi and reports systemd failures without raw private diagnostics.

Deployment is intentionally not performed in the trimming worktree. Existing
installed helpers, exposure links, timers and plugin-managed copies can therefore
remain active. Review them manually before future activation: stop a legacy
Superpowers timer with the retained setup command's `--disable`, review stale
skill discovery links, and restart agents after approved cleanup. Do not delete
upstream repositories as part of this cull. Plugin-managed skills without a repo
installer require a separate manual enablement review.
