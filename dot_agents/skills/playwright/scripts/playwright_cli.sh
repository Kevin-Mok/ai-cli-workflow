#!/usr/bin/env bash
set -euo pipefail

cli_emoji() { [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"; }

if ! command -v npx >/dev/null 2>&1; then
  echo "$(cli_emoji ❌)Error: npx is required but not found on PATH." >&2
  exit 1
fi

has_session_flag="false"
for arg in "$@"; do
  case "$arg" in
    --session|--session=*)
      has_session_flag="true"
      break
      ;;
  esac
done

cmd=(npx --yes --package @playwright/cli playwright-cli)
if [[ "${has_session_flag}" != "true" && -n "${PLAYWRIGHT_CLI_SESSION:-}" ]]; then
  cmd+=(--session "${PLAYWRIGHT_CLI_SESSION}")
fi
cmd+=("$@")

exec "${cmd[@]}"
