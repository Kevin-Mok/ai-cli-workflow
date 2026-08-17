#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
function_path="${repo_root}/dot_config/fish/functions/refresh-config.fish"

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

mkdir -p "${tmpdir}/bin" "${tmpdir}/repo/dot_codex" "${tmpdir}/home/.codex" "${tmpdir}/home/.config/fish"
log_path="${tmpdir}/calls.log"
real_fish="$(command -v fish)"

cat > "${tmpdir}/bin/snapshot-codex-config" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'snapshot-codex-config:%s\n' "$*" >> "$TEST_LOG"
if [ "${TEST_SNAPSHOT_FAIL:-0}" = "1" ]; then
  exit 9
fi
/bin/cp "$TEST_CODEX_SOURCE" "$TEST_CODEX_TARGET"
EOF
chmod +x "${tmpdir}/bin/snapshot-codex-config"

cat > "${tmpdir}/bin/chezmoi" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
if [ "$1" = "source-path" ] && [ "$2" = "$HOME/.gitconfig" ]; then
  printf 'chezmoi:%s\n' "$*" >> "$TEST_LOG"
  printf '%s\n' "$TEST_GITCONFIG_TARGET"
  exit 0
fi
printf 'chezmoi:%s\n' "$*" >> "$TEST_LOG"
EOF
chmod +x "${tmpdir}/bin/chezmoi"

cat > "${tmpdir}/bin/sync-shortcuts" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'sync-shortcuts\n' >> "$TEST_LOG"
EOF
chmod +x "${tmpdir}/bin/sync-shortcuts"

cat > "${tmpdir}/bin/fish" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'fish-reload:%s\n' "$*" >> "$TEST_LOG"
EOF
chmod +x "${tmpdir}/bin/fish"

cat > "${tmpdir}/home/.codex/config.toml" <<'EOF'
model = "local"
EOF

cat > "${tmpdir}/home/.gitconfig" <<'EOF'
[user]
\tname = Local User
[credential "https://github.com"]
EOF
printf '\thelper = %s\n' '' >> "${tmpdir}/home/.gitconfig"

cat > "${tmpdir}/home/.config/fish/key_abbr.fish" <<'EOF'
printf 'sourced-shortcuts\n' >> "$TEST_LOG"
EOF

cat > "${tmpdir}/repo/dot_codex/config.toml" <<'EOF'
model = "repo"
EOF

cat > "${tmpdir}/repo/dot_gitconfig.tmpl" <<'EOF'
[user]
\tname = Repo User
EOF

success_output="$(TEST_LOG="$log_path" \
TEST_CODEX_SOURCE="${tmpdir}/home/.codex/config.toml" \
TEST_CODEX_TARGET="${tmpdir}/repo/dot_codex/config.toml" \
TEST_GITCONFIG_TARGET="${tmpdir}/repo/dot_gitconfig.tmpl" \
PATH="${tmpdir}/bin:${PATH}" \
HOME="${tmpdir}/home" \
"$real_fish" -c "source '$function_path'; refresh-config")"

if [ "$success_output" != 'REFRESH COMPLETE' ]; then
  printf 'expected one skimmable success line, got: %s\n' "$success_output" >&2
  exit 1
fi

if ! grep -Fxq 'snapshot-codex-config:' "$log_path"; then
  printf 'expected refresh-config to delegate to snapshot-codex-config\n' >&2
  cat "$log_path" >&2
  exit 1
fi

expected_force_apply="chezmoi:apply --force ${tmpdir}/home/.codex/config.toml"
if ! grep -Fxq "$expected_force_apply" "$log_path"; then
  printf 'expected refresh-config to force-apply only the config it just snapshotted\n' >&2
  cat "$log_path" >&2
  exit 1
fi

expected_gitconfig_source="chezmoi:source-path ${tmpdir}/home/.gitconfig"
if ! grep -Fxq "$expected_gitconfig_source" "$log_path"; then
  printf 'expected refresh-config to resolve the tracked Git config target\n' >&2
  cat "$log_path" >&2
  exit 1
fi

expected_gitconfig_apply="chezmoi:apply --force ${tmpdir}/home/.gitconfig"
if ! grep -Fxq "$expected_gitconfig_apply" "$log_path"; then
  printf 'expected refresh-config to force-apply only the Git config it just copied\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fq 'chezmoi:apply' "$log_path"; then
  printf 'expected refresh-config to run chezmoi apply\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if grep -Fxq "chezmoi:source-path ${tmpdir}/home/.codex/config.toml" "$log_path"; then
  printf 'expected Codex source-path resolution to stay inside snapshot-codex-config\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fxq 'sync-shortcuts' "$log_path"; then
  printf 'expected refresh-config to keep interactive shortcut regeneration\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fxq 'sourced-shortcuts' "$log_path"; then
  printf 'expected refresh-config to keep interactive shortcut sourcing\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fxq 'fish-reload:' "$log_path"; then
  printf 'expected refresh-config to keep interactive Fish reload\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fq 'model = "local"' "${tmpdir}/repo/dot_codex/config.toml"; then
  printf 'expected repo config to be overwritten by local config contents\n' >&2
  cat "${tmpdir}/repo/dot_codex/config.toml" >&2
  exit 1
fi

if ! grep -Fq 'name = Local User' "${tmpdir}/repo/dot_gitconfig.tmpl"; then
  printf 'expected tracked Git config to be overwritten by local config contents\n' >&2
  cat "${tmpdir}/repo/dot_gitconfig.tmpl" >&2
  exit 1
fi

if rg -q '[[:blank:]]+$' "${tmpdir}/repo/dot_gitconfig.tmpl"; then
  printf 'expected copied blank credential helpers to have no trailing whitespace\n' >&2
  cat "${tmpdir}/repo/dot_gitconfig.tmpl" >&2
  exit 1
fi

: > "$log_path"
if TEST_LOG="$log_path" \
  TEST_SNAPSHOT_FAIL=1 \
  TEST_CODEX_SOURCE="${tmpdir}/home/.codex/config.toml" \
  TEST_CODEX_TARGET="${tmpdir}/repo/dot_codex/config.toml" \
  PATH="${tmpdir}/bin:${PATH}" \
  HOME="${tmpdir}/home" \
  "$real_fish" -c "source '$function_path'; refresh-config"; then
  printf 'expected refresh-config to fail when snapshot helper fails\n' >&2
  exit 1
fi

if grep -Eq 'chezmoi:apply|sync-shortcuts|sourced-shortcuts|fish-reload' "$log_path"; then
  printf 'expected failed snapshot to stop before interactive refresh steps\n' >&2
  cat "$log_path" >&2
  exit 1
fi
