#!/usr/bin/env bash

# Human-facing decoration; keep protocol/data output unchanged.
cli_emoji() {
  [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"
}

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  printf '%sRun with sudo: sudo %s\n' "$(cli_emoji 'ℹ️')" "$0" >&2
  exit 1
fi

apt-get update
apt-get install -y numlockx
