#!/usr/bin/env bash
set -euo pipefail

cli_emoji() { [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"; }

if [[ "$(uname)" != "Darwin" ]]; then
  echo "$(cli_emoji ❌)ensure_macos_permissions.sh only supports macOS" >&2
  exit 1
fi

if ! command -v swift >/dev/null 2>&1; then
  echo "$(cli_emoji ❌)swift is required to check macOS screen capture permissions" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERM_SWIFT="$SCRIPT_DIR/macos_permissions.swift"
MODULE_CACHE="${TMPDIR:-/tmp}/codex-swift-module-cache"
mkdir -p "$MODULE_CACHE"

screen_capture_status() {
  local json
  json="$(swift -module-cache-path "$MODULE_CACHE" "$PERM_SWIFT" "$@")"
  python3 -c 'import json, sys; data=json.loads(sys.argv[1]); print("1" if data.get("screenCapture") else "0")' "$json"
}

if [[ -n "${CODEX_SANDBOX:-}" ]]; then
  echo "$(cli_emoji ⚠️)Screen capture checks are blocked in the sandbox; rerun with escalated permissions." >&2
  exit 3
fi

if [[ "$(screen_capture_status)" == "1" ]]; then
  echo "$(cli_emoji ✅)Screen Recording permission already granted."
  exit 0
fi

printf '%s' "$(cli_emoji ℹ️)"
cat <<'MSG'
This workflow needs macOS Screen Recording permission to capture screenshots.
macOS will show a single system prompt for Screen Recording. Approve it, then
return here. If macOS opens System Settings instead of prompting, enable Screen
Recording for your terminal and rerun the command.
MSG

# Request permission once after explaining why it is needed.
screen_capture_status --request >/dev/null || true

if [[ "$(screen_capture_status)" != "1" ]]; then
  printf '%s' "$(cli_emoji ⚠️)"
  cat <<'MSG'
Screen Recording is still not granted.
Open System Settings > Privacy & Security > Screen Recording and enable it for
your terminal (and Codex if needed), then rerun your screenshot command.
MSG
  exit 2
fi

echo "$(cli_emoji ✅)Screen Recording permission granted."
