# Local Context Mode retrieval

Context Mode keeps indexed text in a local SQLite database and returns selected excerpts. This guide explains the preserved local integration, the pinned portable installer, and disposable retrieval checks.

## Runtime and installation

The portable installer `run_onchange_after_install-context-mode.sh` pins Context Mode 1.0.169, verifies its tarball checksum, and installs under `~/.local/share/context-mode/1.0.169`. It requires Node 22.5 or newer, npm, curl and sha256sum. General npm lifecycle scripts are disabled; only better-sqlite3 is rebuilt when the SQLite FTS5 probe requires it. The wrapper at `~/.local/bin/context-mode` starts the CLI bundle directly, avoiding upstream bootstrap configuration edits.

The migration does not add client declarations or run installers. Existing local Codex configuration, Claude settings, `~/.claude.json` and optional MCP declarations must remain privately preserved. Source templates remain in the private recovery archive. Confirm server/tool availability in the client's MCP view before relying on retrieval. Keep ordinary approval requirements; upstream arbitrary execution tools are not a filesystem sandbox.

## Disposable checks

From the checkout root, no sudo, after the pinned package is installed:

```sh
python3 scripts/executable_context-mode-demo --case index --plain
python3 scripts/executable_context-mode-demo --case search --plain
python3 scripts/executable_context-mode-demo --case empty --plain
```

Each check starts a real MCP server with disposable HOME/state, indexes a synthetic marker, and checks index/stats, matching search, or no-result behavior. `--package PATH` selects a separate package installation. These checks do not exercise the client's UI or approval flow and do not measure token savings.

## Boundaries

Indexed text persists on disk. The package checks npm for updates at startup and periodically; it can access the network within its process permissions. Transitive dependencies remain an installation risk despite the top-level artifact checksum. Keep hooks, self-upgrades and hosted Insight excluded from this retrieval pilot. Preserve local indexed databases separately from Git.
