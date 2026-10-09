#!/usr/bin/env bash

# Human-facing decoration; keep protocol/data output unchanged.
cli_emoji() {
  [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"
}

set -euo pipefail

usage() {
  printf '%s' "$(cli_emoji '📖')"
  cat <<'USAGE'
Usage:
  scripts/executable_install-tmux-tpm.sh

What this script does:
  - Clones or updates ~/.tmux/plugins/tpm
  - Ensures ~/.tmux/plugins/tpm/tpm is executable
  - Fixes the default quoted TPM launch line in ~/.tmux.conf (if present)
  - Reloads ~/.tmux.conf in an active tmux server, when possible

After running:
  1) Start/restart tmux.
  2) Run tmux-prefix + I to install plugins.
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

tpm_root="${HOME}/.tmux/plugins"
tpm_dir="${tpm_root}/tpm"
tmux_conf="${HOME}/.tmux.conf"
tpm_remote="https://github.com/tmux-plugins/tpm.git"

if ! command -v git >/dev/null 2>&1; then
  echo "$(cli_emoji '❌')ERROR: git is required." >&2
  exit 1
fi

mkdir -p "$tpm_root"

if [ -d "$tpm_dir/.git" ]; then
  echo "$(cli_emoji 'ℹ️')Updating TPM in $tpm_dir..."
  git -C "$tpm_dir" pull --ff-only
else
  echo "$(cli_emoji 'ℹ️')Installing TPM to $tpm_dir..."
  git clone --depth 1 "$tpm_remote" "$tpm_dir"
fi

chmod +x "$tpm_dir/tpm"

if [ -f "$tmux_conf" ] && grep -Fq "run -b '~/.tmux/plugins/tpm/tpm'" "$tmux_conf"; then
  echo "$(cli_emoji 'ℹ️')Fixing tmux quoted TPM bootstrap path in $tmux_conf..."
  sed -i "s#run -b '~/.tmux/plugins/tpm/tpm'#run -b ~/.tmux/plugins/tpm/tpm#g" "$tmux_conf"
fi

if command -v tmux >/dev/null 2>&1 && tmux list-sessions >/dev/null 2>&1; then
  echo "$(cli_emoji 'ℹ️')Reloading tmux config..."
  tmux source-file "$tmux_conf"
  echo "$(cli_emoji 'ℹ️')TPM bootstrap line is now loaded in active tmux session."
else
  echo "$(cli_emoji 'ℹ️')TMUX is not running or unreachable."
  echo "$(cli_emoji 'ℹ️')Start tmux and run the prefix + I to install plugins after this."
fi

echo "$(cli_emoji '✅')Done. TPM bootstrap installed at: $tpm_dir"
