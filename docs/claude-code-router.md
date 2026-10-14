# Optional Claude Code Router

Use CCR to try provider/model routing with Claude Code or Codex without changing
their normal sessions. The repo installs a verified CLI release, seeds disabled
profiles and logging on first use, and leaves provider selection and startup
manual. Measure cost and task quality before adopting a route.

## What it runs and why add it

[CCR 3.1.3](https://github.com/musistudio/claude-code-router/releases/tag/v3.1.3)
is an MIT-licensed Node 22+ local gateway and browser management service, not an
automatic token compressor. The published CLI supports both agents and
Anthropic Messages/OpenAI Responses and other provider protocols. Its default
ports are gateway 3456, gateway core 3457 and management 3458. The npm CLI avoids
the Electron desktop app. See the [upstream CLI guide](https://ccrdesk.top/en/guides/cli/).

Ponytail v5.2.0 is already installed at this branch's baseline; it supplies
minimal-change guidance, review skills and local hooks. The locally cached
`github/feat/install-rtk` branch (`14cbb59f`) is not merged here; it declares RTK
shell-output compression for both agents. Neither routes model requests. Codex
already uses cheaper helper agents in `dot_codex/agents/`. CCR adds a distinct
capability, but cheaper routing can sacrifice quality or increase retries.

## Installation and first-run boundary

The [run-onchange installer](../run_onchange_after_install-claude-code-router.sh.tmpl)
pins npm **3.1.3** and the archive's SHA-512. It checks the installed version,
uses the private user prefix `~/.local/share/claude-code-router`, and requires
Node 22+, npm, curl and coreutils. Missing prerequisites skip with instructions;
after fixing them, rerun the same script because chezmoi may remember that
successful skip. No sudo is needed. Native `better-sqlite3` may need a compiler,
Python and Node headers. npm dependency installation runs dependency lifecycle
scripts; their caret ranges are **not** a frozen dependency graph.

The managed launcher is `~/.local/bin/ccr`; that directory must be on PATH.
It forces the bundled model catalog (disabling automatic catalog downloads)
and loopback management default, and supplies `--version` because upstream
treats that argument as a profile name. `CLI_PLAIN=1` removes wrapper/installer
decoration; `CLI_DETAILS=1` exposes failed installer diagnostics. Installer
progress appears every ten seconds during slow downloads/installations.

The [create-only private JSON seed](../dot_claude-code-router/create_private_config.json)
targets `~/.claude-code-router/config.json` with mode 0600. It disables gateway
startup, agent profiles, request/body logging, analysis, TLS/system proxy,
context archive, ToolHub/MCP, media, bots and custom plugins. It contains no
credentials or provider. The installer never starts CCR or launches an agent.
No `dot_claude/settings.json` or `dot_codex/config.toml` changes are necessary.

**Existing installs:** `create_` preserves existing JSON content. CCR loads
`config.sqlite` first; JSON is only a first-run migration, not ongoing policy.
The upstream migration archives the seed; a later apply can recreate it, but
SQLite still wins. Review existing profiles and logging in the UI before
starting the gateway. Do not overwrite live databases or assume this seed
turns off an existing install. Private file attributes may tighten permissions.

No chezmoi apply or refresh-config was run for this change, as requested.

## Explicit onboarding

After a later deliberate apply, inspect `ccr --version` and `ccr --help`.
Use `ccr serve --no-open --no-gateway` for foreground management only; stop with
Ctrl+C. Its printed URL contains an authentication token: keep it private.
`ccr ui --no-gateway` opens the browser UI. Host/port flags select management
binding; `--no-open` avoids opening a browser. Management port collisions try
the next free port; use the printed URL. `ccr stop` stops only detached services
started with `start`/`ui`, not foreground `serve`.
An existing detached service is reused: `ui --no-gateway` does not stop a
gateway that is already running. Stop it with `ccr stop` before restarting in
management-only mode. Review existing state before explicitly starting it.

Add a provider/model and client key in the UI, then enable/start the gateway
under Server. Create agent profiles with **Only opened from CCR** scope (`ccr`),
not Global; launch an enabled profile by name with `ccr "Profile Name"`.
Credentials belong in the local runtime database, never in tracked JSON.
Avoid importing subscription credentials until their terms and handling have
been reviewed. No provider, savings benchmark or model recommendation is
preselected. Profile launch can generate isolated agent config and MCP entries
when optional features are enabled.

## Security and telemetry

The gateway receives prompts, source code, tools and keys and forwards requests
to selected providers. Client keys and management tokens are separate. The
inspected release generates random credentials; a runtime check rejected a
bad management token with HTTP 401. Credentials default to plaintext local
SQLite storage with private filesystem permissions, not encryption at rest.

No telemetry collector was identified in the inspected CLI/ai-gateway bundles;
there is no verified universal telemetry-off switch. Logging/analysis/body
capture are explicitly off in the seed. Usage metadata may still be stored
locally. Upstream normally fetches `models.ccrdesk.top/models.json` at startup
and hourly; our launcher disables that fetch. UI provider/model discovery,
icons, optional plugin marketplace, credential refresh, search and bots can
make additional network calls. This is not a full browser traffic/dependency
audit. These settings do not disable Codex or Claude's own telemetry.

There are no added agent lifecycle hooks or MCP servers in this integration.
Internal router/auth/header hooks belong to the gateway. Optional plugins,
ToolHub/MCP subprocesses, browser automation and TLS interception/CA installation
expand trust; leave them disabled for this trial. Read [upstream observability
docs](https://ccrdesk.top/en/configuration/observability/) before enabling logs.

## Verification and rollback

Run `python3 -B tests/test_claude_code_router.py` for offline installer checks.
Run `python3 -B scripts/smoke_claude_code_router.py` after installation, or pass
`--package-dir PATH` for a disposable package location; `--plain` gives ASCII
output. This starts management in a temporary HOME with no providers, verifies
real seed migration/SQLite, disabled gateway/profiles/logging and 401 auth,
then stops and cleans up. It never reads live CCR/agent credentials.
See [smoke tests](smoke-tests.md#claude-code-router).

Paid requests, cost savings, real-agent profile launches, streaming/tool fidelity,
full dependency CVEs and browser network activity remain unverified. Runtime
management checks do not prove model routing quality. The exact archive was
verified; the release page references commit `3b0aebf`, but npm has no `gitHead`
and source-to-bundle reproducibility was not established.

Rollback: end opted-in sessions and stop CCR, remove its private npm package
with npm's uninstall command/prefix, and stop managing its new launcher/seed.
Keep runtime databases for recovery until deliberately removed; they may
contain secrets. Normal agent config is untouched by this integration; any
Global profile you later enable needs its own restore procedure.
