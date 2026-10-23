# shadcn/ui source and evaluation

This skill gives Codex and Claude Code the official shadcn component workflow on explicit invocation. Read the pinned provenance, local adaptations and operational limits before using its CLI in a destination app.

## Recommendation: 8/10 — add the explicit skill

shadcn/ui is an MIT component-source ecosystem, registry tooling, npm CLI and documentation app. It also ships a real agent skill and a stdio MCP server; it is not an autonomous design-team app. The official skill adds project configuration, primitive-library differences, component composition and safe update guidance beyond general visual-design advice. Vendoring the component-focused skill is useful; a second global MCP or installer is unnecessary.

## Provenance and local changes

- Reviewed 2026-10-14: [shadcn-ui/ui](https://github.com/shadcn-ui/ui), commit [`4233ed1caded8c38f4bc14b14afe1f93ebcaf966`](https://github.com/shadcn-ui/ui/tree/4233ed1caded8c38f4bc14b14afe1f93ebcaf966).
- Read the pinned [README](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/README.md), [MIT license](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/LICENSE.md) (copyright 2023 shadcn), and [skill subtree](https://github.com/shadcn-ui/ui/tree/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/skills/shadcn). The complete license is retained in [LICENSE](LICENSE).
- Vendored `SKILL.md`, `cli.md`, `customization.md`, `registry.md`, `mcp.md`, and all six `rules/*.md` from that revision. Supporting documents replace `shadcn@latest` with `shadcn@4.21.5`; `mcp.md` additionally pins its bare setup examples and labels configuration writes as explicitly requested, reviewed actions. `customization.md` drops its link to the omitted showcase workflow while retaining the radius guidance.
- Entrypoint adaptation: concise explicit-use description; `disable-model-invocation: true`; `user-invocable: true` (upstream sets false); removed the broad Bash allowlist and Claude-specific dynamic shell injection; added explicit context discovery, app-directory, credential and mutation boundaries. Context references now describe manual discovery rather than injected JSON.
- Omitted the optional DESIGN.md-to-app/showcase branch, its quick-reference commands and links, `design-system*.md`, showcase assets/scripts, eval fixtures and icon PNGs. Existing design skills cover broader app generation; no unused code/assets are bundled.
- Replaced upstream `agents/openai.yml` with repo-standard `agents/openai.yaml`, retaining the display name and adding `policy.allow_implicit_invocation: false`. No installer, package dependency, MCP entry or live-home file is added.
- CLI version and Node floor come from the pinned [package manifest](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/packages/shadcn/package.json): **4.21.5**, **Node >=20.18.1**. Published [npm metadata](https://registry.npmjs.org/shadcn/4.21.5) independently confirms the version. Skill-source pinning and CLI pinning do not freeze registry responses or transitive dependency resolution.
- Discovery context: user-supplied [Mnilax post](https://x.com/Mnilax/status/2110382356028686598). Its content could not be independently retrieved; the review relies on upstream source.

## Scope and public intake

The entrypoint covers official component/project mechanics; existing frontend
skills supply broader visual direction. Public intake on `2026-10-22` uses
reviewed snapshot `10ed55876200f1b36c36761d87df59d0e3d8301a`. It removes internal
branch/PR evaluation history, keeps all upstream supporting rules, moves detailed
patterns/workflows into [workflows.md](workflows.md), and shortens the entrypoint.
The CLI, registry, customization and MCP references retain their reviewed pins.
The illustrative private-registry URL uses the reserved `example.com` domain.

## Accounts, cost, network and security

The public registry and core CLI/skill do not require a shadcn account or paid subscription. Private/third-party registries can require their own authentication or payment; v0 and other hosted generation products are separate. See official [skills](https://ui.shadcn.com/docs/skills), [MCP](https://ui.shadcn.com/docs/mcp) and [registry authentication](https://ui.shadcn.com/docs/registry/authentication) docs. Agent/provider subscriptions remain the user's existing expense.

`npx`/other runners fetch npm packages on a cold run. Registry reads use `https://ui.shadcn.com/r` by default, configurable registry URLs and optional GitHub sources. Documentation commands return URLs the agent must fetch; component installs can invoke the package manager and download dependencies. Review [registry constants](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/packages/registry/src/registry/constants.ts), [fetcher](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/packages/registry/src/registry/fetcher.ts) and [MCP command](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/packages/shadcn/src/commands/mcp.ts). Requests include `User-Agent: shadcn` and configured registry headers. The [environment loader](https://github.com/shadcn-ui/ui/blob/4233ed1caded8c38f4bc14b14afe1f93ebcaf966/packages/registry/src/env-loader.ts) can read `.env*` files in the chosen working directory. Keep credentials scoped to trusted registries and never copy them into this repo, prompts or logs.

No dedicated telemetry sender was identified in the reviewed manifest/fetcher/MCP paths; **absence of telemetry is not established**. Registry hosts, npm, proxies, GitHub and third parties can log requests; dependencies were not exhaustively audited. Registry code/instructions are untrusted inputs. `add`, `init`, `apply` and package-manager lifecycle behavior can change files or execute code; inspect previews/diffs and dependency changes before use. The documented MCP surface includes registry discovery and add-command generation; no server is activated here.

## Verification limits

Local checks validate the explicit-only metadata, relative links, pinned source transformations and shared Claude directory routing. The reviewed source reported CLI runtime checks; they were not rerun during this static import. No live Codex/Claude loading, private-registry auth, paid catalog, browser accessibility or target-app component installation is claimed. No chezmoi apply, refresh-config or push is part of this change. Revert the focused commit to remove the skill and documentation.
