# Managed Public Design Skills

This repository installs the requested public design stack reproducibly through
chezmoi rather than committing moving upstream copies. A normal
`chezmoi apply` clones the public sources and creates the visible Codex skill
links; the one-time post-apply bootstrap installs UI/UX Pro Max's official
global bundle.

## Included sources

| Capability | Upstream | Installed path |
| --- | --- | --- |
| Impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `~/.codex/skills/impeccable` |
| 21st CLI, AI, design sync, registry | [21st-dev/skill](https://github.com/21st-dev/skill) | `~/.codex/skills/21st-*` |
| Review Animations | [emilkowalski/skills](https://github.com/emilkowalski/skills) | `~/.codex/skills/review-animations` |
| Scroll World | [oso95/scroll-world](https://github.com/oso95/scroll-world) | `~/.codex/skills/scroll-world` |
| UI/UX Pro Max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `~/.agents/skills/` |
| Higgsfield plugin | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | `~/.codex/plugins/higgsfield` |

## Daily refresh

`design-skills-sync.timer` runs at 05:00 local time with
`Persistent=true`; a missed run is caught up when the user manager starts.
Its service refreshes only the managed upstream repositories fast-forward and
runs UI/UX Pro Max's official updater. It does not authenticate 21st or
Higgsfield, create media, spend credits, or upgrade the Higgsfield CLI.

Use `sync-design-skills --dry-run` to preview the source refresh. Use
`setup-design-skills-timer --check`, `--enable`, or `--disable` to manage
the user timer. Both commands require no sudo.

After a refresh, restart Codex to load the updated skill definitions. For
Higgsfield, install its CLI separately if needed, then run
`higgsfield auth login` yourself before requesting any generation.
