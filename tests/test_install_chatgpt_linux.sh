#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_install-chatgpt-linux"

if [ ! -x "$script_path" ]; then
  printf 'installer is missing or not executable: %s\n' "$script_path" >&2
  exit 1
fi

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mockbin="${tmpdir}/mockbin"
log_file="${tmpdir}/commands.log"
mkdir -p "$mockbin"
: > "$log_file"

cat > "${mockbin}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

output=""
url=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --output)
      output="$2"
      shift 2
      ;;
    *)
      url="$1"
      shift
      ;;
  esac
done

printf 'curl url=%s output=%s\n' "$url" "$output" >> "$TEST_LOG"
printf 'package\n' > "$output"
EOF

cat > "${mockbin}/sudo" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

printf 'sudo %s\n' "$*" >> "$TEST_LOG"
exec "$@"
EOF

cat > "${mockbin}/apt" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

package_path="${!#}"
package_directory="$(dirname "$package_path")"
if [ "$(stat -c '%a' "$package_directory")" != "711" ]; then
  printf 'apt cannot traverse the temporary package directory: %s\n' "$package_directory" >&2
  exit 1
fi
if [ "$(stat -c '%a' "$package_path")" != "644" ]; then
  printf 'apt cannot read the temporary package: %s\n' "$package_path" >&2
  exit 1
fi

printf 'apt %s\n' "$*" >> "$TEST_LOG"
EOF

cat > "${mockbin}/dnf" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

package_path="${!#}"
package_directory="$(dirname "$package_path")"
if [ "$(stat -c '%a' "$package_directory")" != "711" ]; then
  printf 'dnf cannot traverse the temporary package directory: %s\n' "$package_directory" >&2
  exit 1
fi
if [ "$(stat -c '%a' "$package_path")" != "644" ]; then
  printf 'dnf cannot read the temporary package: %s\n' "$package_path" >&2
  exit 1
fi

printf 'dnf %s\n' "$*" >> "$TEST_LOG"
EOF

chmod +x "${mockbin}/curl" "${mockbin}/sudo" "${mockbin}/apt" "${mockbin}/dnf"

assert_contains() {
  local needle="$1"
  local file="$2"

  if ! rg -F "$needle" "$file" >/dev/null; then
    printf 'expected to find %s in %s\n' "$needle" "$file" >&2
    return 1
  fi
}

write_os_release() {
  local id="$1"
  local version="$2"

  cat > "${tmpdir}/os-release" <<EOF
ID=${id}
VERSION_ID=${version}
EOF
}

run_installer() {
  local architecture="$1"

  PATH="${mockbin}:$PATH" \
  TEST_LOG="$log_file" \
  CHATGPT_INSTALL_OS_RELEASE_FILE="${tmpdir}/os-release" \
  CHATGPT_INSTALL_ARCHITECTURE="$architecture" \
  bash "$script_path"
}

: > "$log_file"
write_os_release ubuntu 24.04
run_installer x86_64
assert_contains 'curl url=https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_amd64.deb' "$log_file"
assert_contains 'sudo apt install ' "$log_file"
assert_contains 'apt install ' "$log_file"

: > "$log_file"
write_os_release debian 13
run_installer arm64
assert_contains 'curl url=https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_arm64.deb' "$log_file"
assert_contains 'apt install ' "$log_file"

: > "$log_file"
write_os_release fedora 43
run_installer x86_64
assert_contains 'curl url=https://persistent.oaistatic.com/codex-app-prod/linux/rpm/latest/chatgpt.x86_64.rpm' "$log_file"
assert_contains 'dnf install ' "$log_file"

: > "$log_file"
write_os_release arch 2026.09
if run_installer x86_64; then
  printf 'expected unsupported distribution to fail\n' >&2
  exit 1
fi
if [ -s "$log_file" ]; then
  printf 'unsupported distribution must not download or invoke sudo\n' >&2
  exit 1
fi

: > "$log_file"
write_os_release ubuntu 24.04
if run_installer i686; then
  printf 'expected unsupported architecture to fail\n' >&2
  exit 1
fi
if [ -s "$log_file" ]; then
  printf 'unsupported architecture must not download or invoke sudo\n' >&2
  exit 1
fi

: > "$log_file"
write_os_release ubuntu 22.04
if run_installer x86_64; then
  printf 'expected unsupported distribution version to fail\n' >&2
  exit 1
fi
if [ -s "$log_file" ]; then
  printf 'unsupported distribution version must not download or invoke sudo\n' >&2
  exit 1
fi
