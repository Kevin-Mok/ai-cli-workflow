#!/usr/bin/env bash

set -euo pipefail

CURL_BIN="${UPDATE_VESKTOP_CURL:-curl}"
DPKG_QUERY_BIN="${UPDATE_VESKTOP_DPKG_QUERY:-dpkg-query}"
DPKG_DEB_BIN="${UPDATE_VESKTOP_DPKG_DEB:-dpkg-deb}"
DPKG_BIN="${UPDATE_VESKTOP_DPKG:-dpkg}"
APT_GET_BIN="${UPDATE_VESKTOP_APT_GET:-apt-get}"
DOWNLOAD_URL="${UPDATE_VESKTOP_DOWNLOAD_URL:-https://vencord.dev/download/vesktop/amd64/deb}"
PACKAGE_NAME="vesktop"

print_section() {
  printf '\n== %s ==\n' "$1"
}

print_note() {
  printf '%s\n' "$1"
}

print_fail() {
  printf 'FAIL: %s\n' "$1" >&2
}

usage() {
  cat <<'EOF'
Usage:
  ./scripts/executable_update-vesktop.sh [--check]

What this does:
  - Verifies that vesktop is installed from dpkg
  - Checks Vesktop's official upstream Debian release
  - Downloads and installs the amd64 .deb when a newer version is available

Options:
  --check      Only print installed and latest upstream versions. Do not update.
  -h, --help   Show this help text.

This script re-execs itself with sudo when you are not already root and an update is needed.
EOF
}

require_root() {
  if [ "${UPDATE_VESKTOP_ASSUME_ROOT:-0}" = "1" ]; then
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

get_latest_deb_url() {
  "$CURL_BIN" -fsSIL "$DOWNLOAD_URL" |
    awk '$1 ~ /^[Ll]ocation:$/ && $2 ~ /\/vesktop_[^/]+_amd64\.deb/ {url=$2; sub(/\r$/, "", url)} END {print url}'
}

get_version_from_url() {
  local deb_name="${1##*/}"

  deb_name="${deb_name%%\?*}"
  case "$deb_name" in
    vesktop_*_amd64.deb)
      deb_name="${deb_name#vesktop_}"
      printf '%s\n' "${deb_name%_amd64.deb}"
      ;;
    *)
      return 1
      ;;
  esac
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

installed_version="$(get_installed_version)"
if [ -z "$installed_version" ]; then
  print_fail "${PACKAGE_NAME} is not installed via dpkg on this system"
  exit 1
fi

latest_deb_url="$(get_latest_deb_url)"
if [ -z "$latest_deb_url" ]; then
  print_fail "Could not determine the latest Vesktop .deb from ${DOWNLOAD_URL}"
  exit 1
fi

latest_version="$(get_version_from_url "$latest_deb_url" || true)"
if [ -z "$latest_version" ]; then
  print_fail "The Vesktop download did not resolve to an amd64 .deb"
  exit 1
fi

print_section "Vesktop Version Status"
print_note "Installed: ${installed_version}"
print_note "Latest: ${latest_version}"

if "$DPKG_BIN" --compare-versions "$installed_version" ge "$latest_version"; then
  if "$DPKG_BIN" --compare-versions "$installed_version" eq "$latest_version"; then
    print_note "Vesktop is already up to date."
  else
    print_note "Installed Vesktop is newer than the latest upstream release."
  fi
  exit 0
fi

if [ "$check_only" -eq 1 ]; then
  exit 0
fi

require_root "${original_args[@]}"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
deb_path="${tmpdir}/vesktop.deb"

print_section "Downloading Vesktop"
"$CURL_BIN" -fsSL -o "$deb_path" "$latest_deb_url"

downloaded_version="$("$DPKG_DEB_BIN" -f "$deb_path" Version 2>/dev/null || true)"
if [ -z "$downloaded_version" ] || [ "$downloaded_version" != "$latest_version" ]; then
  print_fail "Downloaded Vesktop package version does not match the release URL"
  exit 1
fi

print_section "Installing Vesktop"
"$APT_GET_BIN" install -y "$deb_path"

updated_version="$(get_installed_version)"
print_section "Verification"
print_note "Installed: ${updated_version}"
print_note "Latest: ${latest_version}"

if [ "$updated_version" != "$latest_version" ]; then
  print_fail "Vesktop did not reach the latest upstream version"
  exit 1
fi

print_note "Vesktop update complete."
