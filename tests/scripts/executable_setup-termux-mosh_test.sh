#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
script_path="${repo_root}/scripts/executable_setup-termux-mosh.sh"

test -f "$script_path"
bash -n "$script_path"

if ! output="$("$script_path" --help 2>&1)"; then
  printf 'expected help command to succeed for %s\n' "$script_path" >&2
  exit 1
fi

printf '%s\n' "$output" | grep -Fq 'Usage:'
printf '%s\n' "$output" | grep -Fq 'executable_setup-termux-mosh.sh'
printf '%s\n' "$output" | grep -Fq -- '--host HOST'
printf '%s\n' "$output" | grep -Fq -- '--user USER'
printf '%s\n' "$output" | grep -Fq -- '--ssh-port PORT'
printf '%s\n' "$output" | grep -Fq 'mosh, OpenSSH, and rsync'
