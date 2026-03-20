# ExecPlan: Install Superpowers Skills

## Checklist

- [x] Add the chezmoi source-state entries that clone `obra/superpowers` into `~/.codex/superpowers` and expose its `skills/` directory at `~/.agents/skills/superpowers`.
- [x] Update the root `README.md` so the bootstrap path and AI operating surface describe the externally managed superpowers bundle.
- [x] Update `dot_agents/skills/README.md` so the local skill catalog stays truthful about which skills are repo-tracked versus externally mounted.
- [x] Verify the generated target state with chezmoi dry runs and apply the live targets.

## Assumptions

- The upstream `INSTALL.md` at `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md` is authoritative and should be followed as-is: clone the repo and symlink its `skills/` directory into `~/.agents/skills/superpowers`.
- In this repo, the right way to encode that install is a root `.chezmoiexternal.toml.tmpl` entry plus a tracked chezmoi symlink target, not vendoring the upstream skills into `dot_agents/skills/`.
- The existing `dot_agents/skills/` catalog should remain focused on repo-tracked local skills, with a short note explaining that `superpowers` is mounted externally.

## Review Notes

- Added a root [`.chezmoiexternal.toml.tmpl`](/home/example/linux-config/.chezmoiexternal.toml.tmpl) entry that manages `https://github.com/obra/superpowers.git` as a git-repo external at `~/.codex/superpowers` with `git pull --ff-only` semantics.
- Added [`dot_agents/skills/symlink_superpowers.tmpl`](/home/example/linux-config/dot_agents/skills/symlink_superpowers.tmpl), which renders `~/.agents/skills/superpowers` as a symlink to `~/.codex/superpowers/skills` so Codex sees the upstream bundle through native skill discovery.
- Refreshed [`README.md`](/home/example/linux-config/README.md) to document that the repo bootstrap flow now installs the superpowers bundle declaratively through chezmoi instead of relying on a manual bootstrap block in `~/.codex/AGENTS.md`.
- Refreshed [`dot_agents/skills/README.md`](/home/example/linux-config/dot_agents/skills/README.md) to clarify that the catalog covers only repo-tracked local skills and intentionally omits the externally mounted superpowers bundle.
- Verified the repo-managed targets with:
  - `chezmoi -S /home/example/linux-config apply -n -v /home/example/.codex/superpowers /home/example/.agents/skills/superpowers`
  - `chezmoi -S /home/example/linux-config managed /home/example/.codex/superpowers /home/example/.agents/skills/superpowers`
- Applied the live install with:
  - `chezmoi -S /home/example/linux-config apply -v /home/example/.codex/superpowers /home/example/.agents/skills/superpowers`
- Confirmed the live state after apply with:
  - `ls -ld /home/example/.codex/superpowers /home/example/.agents/skills/superpowers`
  - `readlink -f /home/example/.agents/skills/superpowers`
  - `find /home/example/.codex/superpowers/skills -maxdepth 1 -mindepth 1 -type d | sort | head -n 20`
  - `git -C /home/example/.codex/superpowers rev-parse --short HEAD`
