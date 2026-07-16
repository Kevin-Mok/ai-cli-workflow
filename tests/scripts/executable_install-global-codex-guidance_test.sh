#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
installer="$repo_root/scripts/executable_install-global-codex-guidance"
test_root="$(mktemp -d)"
trap 'rm -rf "$test_root"' EXIT

test_home="$test_root/home"
mkdir -p "$test_home"

HOME="$test_home" "$installer" --dry-run >/dev/null
[[ ! -e "$test_home/.codex/AGENTS.md" ]]

HOME="$test_home" "$installer" >/dev/null
HOME="$test_home" "$installer" >/dev/null

[[ "$(readlink -f "$test_home/.codex/AGENTS.md")" == "$repo_root/dot_codex/AGENTS.md" ]]
[[ "$(readlink -f "$test_home/.agents/system-design")" == "$repo_root/dot_agents/system-design" ]]

expected_skill_count="$(find "$repo_root/dot_agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)"
installed_skill_count="$(find "$test_home/.codex/skills" -mindepth 1 -maxdepth 1 -type l | wc -l)"
[[ "$installed_skill_count" == "$expected_skill_count" ]]

conflict_home="$test_root/conflict-home"
mkdir -p "$conflict_home/.codex"
touch "$conflict_home/.codex/AGENTS.md"
if HOME="$conflict_home" "$installer" >/dev/null 2>&1; then
  echo 'Expected installer to refuse a user-managed AGENTS.md path.' >&2
  exit 1
fi

printf 'executable_install-global-codex-guidance tests passed.\n'
