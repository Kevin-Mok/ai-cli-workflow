#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
fixture_root=$(mktemp -d)
trap 'rm -rf "$fixture_root"' EXIT

home_dir="$fixture_root/home"
agents_dir="$home_dir/.agents/skills"
claude_dir="$home_dir/.claude/skills"
mkdir -p "$agents_dir/alpha/references" "$agents_dir/superpowers" "$claude_dir"

printf '%s\n' '---' 'name: alpha' 'description: test skill' '---' > "$agents_dir/alpha/SKILL.md"
printf '%s\n' '# Detail' > "$agents_dir/alpha/references/detail.md"
printf '%s\n' '# Catalog' > "$agents_dir/README.md"
ln -s "$agents_dir/alpha/SKILL.md" "$claude_dir/alpha.md"

rendered="$fixture_root/install-claude-skills.sh"
sed "s#{{ .chezmoi.homeDir }}#$home_dir#g" \
  "$repo_root/run_after_install-claude-skills.sh.tmpl" > "$rendered"

bash "$rendered"

test -L "$claude_dir/alpha"
test "$(readlink "$claude_dir/alpha")" = "$agents_dir/alpha"
test -f "$claude_dir/alpha/SKILL.md"
test -f "$claude_dir/alpha/references/detail.md"
test ! -e "$claude_dir/alpha.md"
test ! -e "$claude_dir/superpowers"
test ! -e "$claude_dir/README.md"

bash "$rendered"
test "$(readlink "$claude_dir/alpha")" = "$agents_dir/alpha"

mkdir -p "$agents_dir/bravo" "$claude_dir/bravo"
printf '%s\n' '---' 'name: bravo' 'description: test skill' '---' > "$agents_dir/bravo/SKILL.md"
printf '%s\n' 'preserve me' > "$claude_dir/bravo/marker"

if bash "$rendered" > "$fixture_root/conflict.out" 2>&1; then
  echo "expected a non-symlink destination conflict" >&2
  exit 1
fi
grep -q 'Refusing to replace non-symlink Claude skill path' "$fixture_root/conflict.out"
test -f "$claude_dir/bravo/marker"
