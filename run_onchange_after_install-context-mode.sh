#!/usr/bin/env bash
# Context Mode retrieval pilot: pinned npm artifact, isolated user prefix.
# No host config edits or upstream postinstall/bootstrap self-healing.
set -euo pipefail
version=1.0.169
sha256=09c41e4cf77b21566c76b8ea2fdbd7f3d823055fee2f02c2166fd5bb575daf2c
plain=${CLI_PLAIN:-0}
details=0
for arg in "$@"; do
    case "$arg" in
        --plain) plain=1 ;;
        --details) details=1 ;;
        *) printf 'Unknown option: %s\n' "$arg" >&2; exit 2 ;;
    esac
done
say() {
    local glyph=$1; shift
    if [ "$plain" = 1 ]; then printf '%s\n' "$*" >&2
    else printf '%s %s\n' "$glyph" "$*" >&2; fi
}
for dependency in node npm curl sha256sum; do
    if ! command -v "$dependency" >/dev/null; then
        say '❌' "Context Mode needs $dependency; install it, then rerun this installer."
        exit 1
    fi
done
if ! node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>22 || (a===22 && b>=5) ? 0 : 1)'; then
    say '❌' 'Context Mode needs Node.js >=22.5.'
    exit 1
fi
parent="$HOME/.local/share/context-mode"
destination="$parent/$version"
database_probe() {
    node --input-type=module - "$1" <<'JS'
import {pathToFileURL} from 'node:url';
const {loadDatabase} = await import(pathToFileURL(process.argv[2] + '/build/db-base.js'));
const Database = loadDatabase();
const db = new Database(':memory:');
db.exec('CREATE VIRTUAL TABLE probe USING fts5(content)');
db.close();
JS
}
package="$destination/node_modules/context-mode"
if [ -f "$package/package.json" ] && [ -f "$package/cli.bundle.mjs" ] &&
   [ "$(node -p 'require(process.argv[1]).version' "$package/package.json")" = "$version" ] &&
   database_probe "$package" >/dev/null 2>&1; then
    say '✅' "Context Mode $version already installed; no network needed."
    exit 0
fi
if [ -e "$destination" ]; then
    say '❌' "Existing $destination is incomplete or incompatible; preserve it and move it aside before retrying."
    exit 1
fi
mkdir -p "$parent"
staging=$(mktemp -d "$parent/.install-XXXXXX")
trap 'rm -rf "$staging"' EXIT
log="$staging/install.log"
run_step() {
    local label=$1; shift
    say '⏳' "$label"
    "$@" >"$log" 2>&1 &
    local pid=$! elapsed=0 status=0
    while kill -0 "$pid" 2>/dev/null; do
        sleep 1
        elapsed=$((elapsed + 1))
        if (( elapsed % 10 == 0 )); then say '⏳' "$label - active for ${elapsed}s"; fi
    done
    wait "$pid" || status=$?
    if [ "$status" != 0 ]; then
        say '❌' "$label failed (exit $status); rerun with --details for diagnostics."
        if [ "$details" = 1 ]; then cat "$log" >&2; fi
        return "$status"
    fi
}
artifact="$staging/context-mode.tgz"
run_step 'Downloading pinned Context Mode 1.0.169' curl --fail --silent --show-error --location --connect-timeout 15 --max-time 120 "https://registry.npmjs.org/context-mode/-/context-mode-$version.tgz" -o "$artifact"
if ! printf '%s  %s\n' "$sha256" "$artifact" | sha256sum -c --quiet -; then
    say '❌' 'Context Mode checksum mismatch; nothing installed.'
    exit 1
fi
run_step 'Installing with lifecycle scripts disabled' npm install --prefix "$staging/runtime" --ignore-scripts --omit=dev --no-audit --no-fund "$artifact"
package="$staging/runtime/node_modules/context-mode"
if ! database_probe "$package" >"$log" 2>&1; then
    # Only this dependency's install script runs (prebuild-install || node-gyp rebuild).
    # The Context Mode postinstall remains disabled.
    run_step 'Preparing native SQLite FTS5 fallback' npm --prefix "$staging/runtime" rebuild better-sqlite3 --ignore-scripts=false --no-audit --no-fund
    if ! database_probe "$package" >"$log" 2>&1; then
        say '❌' 'SQLite FTS5 remains unavailable; install native build prerequisites and retry with --details.'
        if [ "$details" = 1 ]; then cat "$log" >&2; fi
        exit 1
    fi
fi
# Linux mv -T rejects a competing nonempty destination rather than nesting runtime.
run_step 'Publishing verified installation' mv -T "$staging/runtime" "$destination"
say '✅' "Installed Context Mode $version for Codex and Claude retrieval."
