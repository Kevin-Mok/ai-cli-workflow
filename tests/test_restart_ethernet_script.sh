#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_restart-ethernet"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mkdir -p "${tmpdir}/bin"
export TEST_LOG="${tmpdir}/commands.log"

cat > "${tmpdir}/bin/sudo" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'sudo %s\n' "$*" >> "$TEST_LOG"
"$@"
EOF

cat > "${tmpdir}/bin/nmcli" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'nmcli %s\n' "$*" >> "$TEST_LOG"
EOF

chmod +x "${tmpdir}/bin/sudo" "${tmpdir}/bin/nmcli"
export PATH="${tmpdir}/bin:${PATH}"

"$script_path"

expected=$'sudo nmcli connection down netplan-enp42s0\nnmcli connection down netplan-enp42s0\nsudo nmcli connection up netplan-enp42s0\nnmcli connection up netplan-enp42s0'
actual="$(cat "$TEST_LOG")"

if [[ "$actual" != "$expected" ]]; then
  printf 'unexpected command sequence:\n%s\n' "$actual" >&2
  exit 1
fi

printf 'restart-ethernet script test passed\n'
