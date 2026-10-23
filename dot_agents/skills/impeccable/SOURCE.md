# Impeccable source record

This pinned web skill provides the upstream design playbooks to Codex and Claude Code on explicit invocation. Read the retained scope and runtime limits before using its launcher.

- Upstream: https://github.com/pbakaus/impeccable
- Reviewed and downloaded: 2026-10-14; commit `9d9fcf5cf7a47728959e0c92ae0ab274571b16e3`, skill 4.5.2, engine version file 0.1.14.
- Source subtree: [.agents/skills/impeccable](https://github.com/pbakaus/impeccable/tree/9d9fcf5cf7a47728959e0c92ae0ab274571b16e3/.agents/skills/impeccable).
- Included: web playbooks, launcher, browser/live-mode scripts, font data, inline fallback contracts, upstream root LICENSE (Apache-2.0) and NOTICE.md. Additional MIT texts for platform-design-skills and modern-screenshot remain in `licenses/`, obtained from their upstream GitHub licence endpoints. Preserve these notices on redistribution, including attribution for omitted platform material.
- Local modifications: concise explicit-only description, `disable-model-invocation: true`, the local integration boundary, and `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. `scripts/impeccable` is stored as `scripts/executable_impeccable` so chezmoi installs an executable at the upstream path. `UPSTREAM_SHA256.json` preserves original hashes, including original SKILL.md and omitted files; it is an upstream inventory, not a manifest of installed files.
- Omitted: `reference/ios.md`, `reference/android.md`, `reference/adapt.native.md`, `reference/audit.native.md`, and four unregistered `agents/impeccable_*.toml` profiles. Native-only links were removed from SKILL.md and `reference/{adapt,animate,audit,doctor,init,layout,new-work,typeset}.md`. All web runtime assets and `reference/degraded/` role contracts remain; the local boundary uses those contracts with an available agent or inline. Other retained upstream bytes are unchanged.
- Installation: normal shared-skill deployment installs `~/.agents/skills/impeccable`; Codex discovers that shared skill, and the existing Claude directory-link helper exposes `~/.claude/skills/impeccable`. The former upstream clone and Codex exposure template are no longer managed. No dedicated installer, custom Codex agent registration, or MCP registration is added. Existing upstream/plugin copies remain until separately reviewed; avoid duplicate exposure when activating this source.

## Runtime and security limits

This is a real skill with companion scripts, not a pure prompt or an MCP server. The upstream product also includes a CLI/detector, native hooks, browser extension and editor tooling; those installers/hooks/extensions are not activated here.

The launcher first accepts IMPECCABLE_BIN, sibling binaries, an unversioned home binary, the versioned cache, or PATH; it can therefore run an engine other than 0.1.14. With none available it downloads engine 0.1.14 from GitHub Releases into `~/.impeccable/bin/`, verifies a checksum sidecar from the same release channel, then executes it. That checksum is not an independently pinned trust root. No native engine is bundled or executed during this evaluation. Use the skill's direct-context fallback when downloads are not authorized.

No skill/detector account, key or paid subscription is documented; agent usage retains the provider's normal costs. Optional Impeccable image generation uses an OpenAI key and paid API calls. No credentials are stored here. Optional choice telemetry can be disabled with IMPECCABLE_NO_TELEMETRY=1 or DO_NOT_TRACK=1; catalog rolls, previews and update checks still use the network. The privacy policy says catalog requests omit prompts, briefs, project names and paths; this is a policy/source review, not a packet capture.

Live mode uses a local server, writes project artifacts and can execute `package.json`'s `impeccable:manual-edit-validate` shell command. Review it before use. The skill can write PRODUCT.md, DESIGN.md and .impeccable project state; invocation is not a filesystem sandbox. Hooks and standalone shortcut creation remain separate explicit operations.

See [local integration and verification](../../../docs/design-skills.md), [pinned README](https://github.com/pbakaus/impeccable/blob/9d9fcf5cf7a47728959e0c92ae0ab274571b16e3/README.md), and [privacy policy](https://impeccable.style/privacy/). Local checks cover the retained files, links and a fixture engine handoff; they do not establish design efficacy or validate the downloaded engine. Shared installation has not been applied or tested in live agent sessions in this task.
