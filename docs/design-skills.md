# Managed Public Design Skills

This repository pins Impeccable's web design skill locally and preserves the
separate Higgsfield plugin integration. Use Impeccable explicitly, preview
Higgsfield updates before refreshing them, and restart agent sessions after
activation. Existing upstream copies remain untouched.

## Included sources

| Capability | Upstream | Installed path |
| --- | --- | --- |
| Impeccable 4.5.2, pinned | [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/9d9fcf5cf7a47728959e0c92ae0ab274571b16e3) | `~/.agents/skills/impeccable` |
| Higgsfield plugin | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | `~/.codex/plugins/higgsfield` |

The shared tracked `frontend-design` and `brand-system-designer` skills remain
available. Codex and Claude use complete shared skill directories; the generic
Claude linker preserves supporting files and refuses non-symlink conflicts.

## Pinned Impeccable

Invoke `$impeccable` in Codex or `/impeccable` in Claude Code. The local skill
disables implicit invocation. It covers web interfaces, including mobile web;
four unused native platform references and four unregistered custom agent
profiles are omitted. Web playbooks, runtime assets, inline role contracts,
upstream hashes and license notices remain. The former external clone and Codex
exposure template are no longer configured; the tracked shared skill is the
canonical source.

Read its [source and runtime boundary](../dot_agents/skills/impeccable/SOURCE.md)
before launching. The launcher can download engine 0.1.14 when none is available,
or use another installed engine. Set `IMPECCABLE_NO_TELEMETRY=1` for launcher
calls; this disables optional choice reporting while catalog and update requests
still use the network. Downloads, hooks, shortcut creation and live mode require
their own requested operation. Without authorized runtime setup, read project
context and the requested playbook through the documented fallback. Live mode
can execute a project validation command and write project files.

`tests/test_design_skills_sync.py` checks the pin and invocation policy, retained
upstream hashes, internal links, launcher handoff to a disposable engine fixture,
Higgsfield-only refresh, and preservation of legacy upstream files. It does not
run a downloaded engine, prove design efficacy, or apply live configuration.

## Daily refresh

`design-skills-sync.timer` runs at 05:00 local time with `Persistent=true`,
catching up a missed run when the user manager starts. It refreshes only the
Higgsfield plugin, with fast-forward-only Git updates. Impeccable changes only
through reviewed repository updates; the timer does not update its pin.
`sync-design-skills --dry-run` previews the Higgsfield target. The legacy
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
