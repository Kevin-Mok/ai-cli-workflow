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

cat > "${tmpdir}/home/.config/fish/key_abbr.fish" <<'EOF'
printf 'sourced-shortcuts\n' >> "$TEST_LOG"
EOF

cat > "${tmpdir}/repo/dot_codex/config.toml" <<'EOF'
model = "repo"
EOF

TEST_LOG="$log_path" \
TEST_CODEX_SOURCE="${tmpdir}/home/.codex/config.toml" \
TEST_CODEX_TARGET="${tmpdir}/repo/dot_codex/config.toml" \
PATH="${tmpdir}/bin:${PATH}" \
HOME="${tmpdir}/home" \
"$real_fish" -c "source '$function_path'; refresh-config"

if ! grep -Fxq 'snapshot-codex-config:' "$log_path"; then
  printf 'expected refresh-config to delegate to snapshot-codex-config\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if ! grep -Fq 'chezmoi:apply' "$log_path"; then
  printf 'expected refresh-config to run chezmoi apply\n' >&2
  cat "$log_path" >&2
  exit 1
fi

if grep -Fq 'chezmoi:source-path' "$log_path"; then
  printf 'expected source-path resolution to stay inside snapshot-codex-config\n' >&2
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
