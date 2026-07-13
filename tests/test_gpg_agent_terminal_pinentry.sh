#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
agent_config="${repo_root}/private_dot_gnupg/gpg-agent.conf"
agent_template="${repo_root}/private_dot_gnupg/gpg-agent-template.conf"
smoke_tests="${repo_root}/docs/smoke-tests.md"
fish_config="${repo_root}/dot_config/fish/config.fish.tmpl"
bash_config="${repo_root}/dot_bashrc"
zsh_config="${repo_root}/dot_zshrc"

assert_contains() {
  local needle="$1"
  local path="$2"

  if ! rg -F "$needle" "$path" >/dev/null; then
    printf 'expected %s to contain: %s\n' "$path" "$needle" >&2
    exit 1
  fi
}

assert_contains 'pinentry-program /usr/bin/pinentry-curses' "$agent_config"
assert_contains 'pinentry-program /usr/bin/pinentry-curses' "$agent_template"
assert_contains 'set -x GPG_TTY (tty)' "$fish_config"
assert_contains 'export GPG_TTY="$(tty)"' "$bash_config"
assert_contains 'export GPG_TTY=$(tty)' "$zsh_config"
assert_contains 'pass edit <non-sensitive-test-entry>' "$smoke_tests"
