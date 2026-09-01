#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_update-vesktop.sh"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mockbin="${tmpdir}/mockbin"
state_file="${tmpdir}/state.txt"
log_file="${tmpdir}/commands.log"

mkdir -p "$mockbin"
printf '1.6.2\n' > "$state_file"
: > "$log_file"

cat > "${mockbin}/dpkg-query" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat "$TEST_STATE"
EOF

cat > "${mockbin}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'curl %s\n' "$*" >> "$TEST_LOG"
if [ "${1:-}" = "-fsSIL" ]; then
  cat <<HEADERS
HTTP/2 302
location: https://github.com/Vencord/Vesktop/releases/download/v1.6.8/vesktop_1.6.8_amd64.deb
HEADERS
  exit 0
fi

output_file=""
while [ $# -gt 0 ]; do
  if [ "$1" = "-o" ]; then
    shift
    output_file="$1"
  fi
  shift
done
printf 'fake deb\n' > "$output_file"
EOF

cat > "${mockbin}/dpkg-deb" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '1.6.8\n'
EOF

cat > "${mockbin}/apt-get" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'apt-get %s\n' "$*" >> "$TEST_LOG"
if [ "${1:-}" = "install" ]; then
  printf '1.6.8\n' > "$TEST_STATE"
fi
EOF

chmod +x "${mockbin}/dpkg-query" "${mockbin}/curl" "${mockbin}/dpkg-deb" "${mockbin}/apt-get"

run_script() {
  TEST_STATE="$state_file" \
  TEST_LOG="$log_file" \
  UPDATE_VESKTOP_ASSUME_ROOT=1 \
  UPDATE_VESKTOP_DPKG_QUERY="${mockbin}/dpkg-query" \
  UPDATE_VESKTOP_CURL="${mockbin}/curl" \
  UPDATE_VESKTOP_DPKG_DEB="${mockbin}/dpkg-deb" \
  UPDATE_VESKTOP_APT_GET="${mockbin}/apt-get" \
  bash "$script_path" "$@"
}

if ! help_output="$(run_script --help 2>&1)"; then
  printf 'expected help command to succeed for %s\n' "$script_path" >&2
  exit 1
fi

printf '%s\n' "$help_output" | grep -Fq "Usage:"
printf '%s\n' "$help_output" | grep -Fq "executable_update-vesktop.sh"
printf '%s\n' "$help_output" | grep -Fq -- "--check"

check_output="$(run_script --check)"
printf '%s\n' "$check_output" | grep -Fq "Installed: 1.6.2"
printf '%s\n' "$check_output" | grep -Fq "Latest: 1.6.8"
grep -Fq "curl -fsSIL" "$log_file"

run_script
grep -Fq "curl -fsSL -o" "$log_file"
grep -Fq "apt-get install -y " "$log_file"

printf '1.6.8\n' > "$state_file"
: > "$log_file"
up_to_date_output="$(run_script)"
printf '%s\n' "$up_to_date_output" | grep -Fq "Vesktop is already up to date."
! grep -Fq "curl -fsSL -o" "$log_file"
! grep -Fq "apt-get install" "$log_file"
