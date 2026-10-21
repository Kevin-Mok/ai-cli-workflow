#!/usr/bin/env bash

# Human-facing decoration; keep protocol/data output unchanged.
cli_emoji() {
  [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"
}

set -euo pipefail

APT_GET_BIN="${UPDATE_CHROME_APT_GET:-apt-get}"
APT_CACHE_BIN="${UPDATE_CHROME_APT_CACHE:-apt-cache}"
DPKG_QUERY_BIN="${UPDATE_CHROME_DPKG_QUERY:-dpkg-query}"
PACKAGE_NAME="google-chrome-stable"

print_section() {
  printf '\n%s== %s ==\n' "$(cli_emoji '🔧')" "$1"
}

print_note() {
  printf '%s%s\n' "$(cli_emoji 'ℹ️')" "$1"
}

print_fail() {
  printf '%sFAIL: %s\n' "$(cli_emoji '❌')" "$1" >&2
}

usage() {
  printf '%s' "$(cli_emoji '📖')"
  cat <<'EOF'
Usage:
  ./scripts/executable_update-chrome.sh [--check]

What this does:
  - Verifies that google-chrome-stable is installed from apt
  - Shows the installed and candidate versions (--check uses cached metadata)
  - Runs apt update and upgrades google-chrome-stable when needed

Options:
  --check      Only print installed and cached candidate versions. Do not update.
  -h, --help   Show this help text.

This script re-execs itself with sudo to refresh apt metadata and update Chrome.
EOF
}

require_root() {
  if [ "${UPDATE_CHROME_ASSUME_ROOT:-0}" = "1" ]; then
    return 0
  fi

  if [ "${EUID:-$(id -u)}" -eq 0 ]; then
    return 0
  fi

  if ! command -v sudo >/dev/null 2>&1; then
    print_fail "This script must run as root and sudo is not available"
    exit 1
  fi

  exec sudo "$0" "$@"
}

get_installed_version() {
  "$DPKG_QUERY_BIN" -W -f='${Version}\n' "$PACKAGE_NAME" 2>/dev/null || true
}

get_candidate_version() {
  local candidate
  # Drain output so apt-cache cannot fail with SIGPIPE under pipefail.
  if ! candidate="$(LC_ALL=C "$APT_CACHE_BIN" policy "$PACKAGE_NAME" 2>/dev/null | awk '/Candidate:/ && !found {print $2; found=1}')"; then
    print_fail "Could not read the Chrome candidate version. Check apt-cache policy google-chrome-stable."
    return 1
  fi
  if [ -z "$candidate" ] || [ "$candidate" = "(none)" ]; then
    print_fail "No candidate version found for ${PACKAGE_NAME}. Check apt sources."
    return 1
  fi
  printf '%s\n' "$candidate"
}

check_only=0
original_args=("$@")

while [ $# -gt 0 ]; do
  case "$1" in
    --check)
      check_only=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      print_fail "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
  shift
done

print_note "Checking installed Chrome and the APT candidate version..."
installed_version="$(get_installed_version)"
if [ -z "$installed_version" ]; then
  print_fail "${PACKAGE_NAME} is not installed via dpkg on this system"
  exit 1
fi

if [ "$check_only" -eq 0 ]; then
  require_root "${original_args[@]}"
  print_section "Updating apt Metadata"
  "$APT_GET_BIN" update
fi

candidate_version="$(get_candidate_version)"

print_section "Chrome Version Status"
print_note "Installed: ${installed_version}"
print_note "Candidate: ${candidate_version}"

if [ "$check_only" -eq 1 ]; then
  exit 0
fi

if dpkg --compare-versions "$installed_version" ge "$candidate_version"; then
  print_note "Google Chrome is already up to date."
  exit 0
fi

print_section "Upgrading Google Chrome"
"$APT_GET_BIN" install -y --only-upgrade "$PACKAGE_NAME"

updated_version="$(get_installed_version)"
candidate_version="$(get_candidate_version)"
print_section "Verification"
print_note "Installed: ${updated_version}"
print_note "Candidate: ${candidate_version}"

if ! dpkg --compare-versions "$updated_version" ge "$candidate_version"; then
  print_fail "Chrome did not reach the candidate version"
  exit 1
fi

print_note "Google Chrome update complete."
