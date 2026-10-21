#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_update-chrome.sh"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mockbin="${tmpdir}/mockbin"
state_file="${tmpdir}/state.txt"
log_file="${tmpdir}/commands.log"
candidate_file="${tmpdir}/candidate.txt"

mkdir -p "$mockbin"
printf '144.0.7559.96-1\n' > "$state_file"
printf '146.0.7680.177-1\n' > "$candidate_file"
: > "$log_file"

cat > "${mockbin}/dpkg-query" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat "$TEST_STATE"
EOF

cat > "${mockbin}/apt-cache" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat <<POLICY
google-chrome-stable:
  Installed: $(cat "$TEST_STATE")
  Candidate: $(cat "$TEST_CANDIDATE")
  Version table:
     146.0.7680.177-1 500
POLICY
if [ "${TEST_LARGE_POLICY:-0}" = 1 ]; then
  for ((i=0; i<10000; i++)); do
    printf '     140.0.7000.1-1 500 https://example.invalid/chrome stable/main amd64 Packages\n'
  done
fi
if [ "${TEST_POLICY_FAIL:-0}" = 1 ]; then
  exit 42
fi
EOF

cat > "${mockbin}/apt-get" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'apt-get %s\n' "$*" >> "$TEST_LOG"
if [ "${1:-}" = "update" ] && [ -n "${TEST_REFRESH_CANDIDATE:-}" ]; then
  printf '%s\n' "$TEST_REFRESH_CANDIDATE" > "$TEST_CANDIDATE"
fi
if [ "${1:-}" = "install" ]; then
  printf '%s\n' "${TEST_INSTALL_VERSION:-$(cat "$TEST_CANDIDATE")}" > "$TEST_STATE"
fi
EOF

chmod +x "${mockbin}/dpkg-query" "${mockbin}/apt-cache" "${mockbin}/apt-get"

run_script() {
  TEST_STATE="$state_file" \
  TEST_LOG="$log_file" \
  TEST_CANDIDATE="$candidate_file" \
  UPDATE_CHROME_ASSUME_ROOT=1 \
  UPDATE_CHROME_DPKG_QUERY="${mockbin}/dpkg-query" \
  UPDATE_CHROME_APT_CACHE="${mockbin}/apt-cache" \
  UPDATE_CHROME_APT_GET="${mockbin}/apt-get" \
  bash "$script_path" "$@"
}

assert_contains() {
  local needle="$1"
  local haystack_file="$2"
  if ! rg -F "$needle" "$haystack_file" >/dev/null; then
    printf 'expected to find %s in %s\n' "$needle" "$haystack_file" >&2
    return 1
  fi
}

if ! help_output="$(run_script --help 2>&1)"; then
  printf 'expected help command to succeed for %s\n' "$script_path" >&2
  exit 1
fi

printf '%s\n' "$help_output" | grep -Fq "Usage:"
printf '%s\n' "$help_output" | grep -Fq "executable_update-chrome.sh"
printf '%s\n' "$help_output" | grep -Fq -- "--check"

check_output="$(run_script --check)"
printf '%s\n' "$check_output" | grep -Fq "Installed: 144.0.7559.96-1"
printf '%s\n' "$check_output" | grep -Fq "Candidate: 146.0.7680.177-1"

run_script
assert_contains "apt-get update" "$log_file"
assert_contains "apt-get install -y --only-upgrade google-chrome-stable" "$log_file"

printf '146.0.7680.177-1\n' > "$state_file"
: > "$log_file"
up_to_date_output="$(run_script)"
printf '%s\n' "$up_to_date_output" | grep -Fq "Google Chrome is already up to date."

large_output="$(TEST_LARGE_POLICY=1 run_script --check)"
printf '%s\n' "$large_output" | grep -Fq 'Candidate: 146.0.7680.177-1'

if failed_output="$(TEST_POLICY_FAIL=1 run_script --check 2>&1)"; then
  printf 'expected failed apt-cache query to fail\n' >&2
  exit 1
fi
printf '%s\n' "$failed_output" | grep -Fq 'Could not read the Chrome candidate version'

# A metadata refresh must replace the cached candidate before verification.
printf '144.0.7559.96-1\n' > "$state_file"
refresh_output="$(TEST_REFRESH_CANDIDATE=156.0.8078.47-1 run_script)"
printf '%s\n' "$refresh_output" | grep -Fq 'Candidate: 156.0.8078.47-1'
printf '%s\n' "$refresh_output" | grep -Fq 'Google Chrome update complete.'

# An installed newer version must never cause an upgrade or false failure.
printf '155.0.8059.84-1\n' > "$candidate_file"
: > "$log_file"
newer_output="$(run_script)"
printf '%s\n' "$newer_output" | grep -Fq 'Google Chrome is already up to date.'
assert_contains 'apt-get update' "$log_file"
if rg -F 'apt-get install' "$log_file" >/dev/null; then
  printf 'expected newer installed version to skip installation\n' >&2
  exit 1
fi

# Equal cached versions cannot skip refreshing the repository metadata.
printf '155.0.8059.84-1\n' > "$state_file"
fresh_output="$(TEST_REFRESH_CANDIDATE=156.0.8078.47-1 run_script)"
printf '%s\n' "$fresh_output" | grep -Fq 'Google Chrome update complete.'
printf '155.0.8059.84-1\n' > "$candidate_file"

# Accept a newer installed version, but still reject an incomplete upgrade.
printf '144.0.7559.96-1\n' > "$state_file"
TEST_INSTALL_VERSION=156.0.8078.47-1 run_script
printf '144.0.7559.96-1\n' > "$state_file"
if older_output="$(TEST_INSTALL_VERSION=154.0.8000.1-1 run_script 2>&1)"; then
  printf 'expected incomplete upgrade to fail\n' >&2
  exit 1
fi
printf '%s\n' "$older_output" | grep -Fq 'Chrome did not reach the candidate version'
