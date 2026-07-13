#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
script_path="${repo_root}/scripts/executable_setup-termux-mosh.sh"
tmp_dir="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

mkdir -p "$tmp_dir/fake-bin" "$tmp_dir/home"
printf '%s\n' '#!/usr/bin/env bash' 'exit 0' > "$tmp_dir/fake-bin/pkg"
chmod 755 "$tmp_dir/fake-bin/pkg"

output="$(HOME="$tmp_dir/home" PATH="$tmp_dir/fake-bin:$PATH" "$script_path" \
  --host example.net \
  --user example-user \
  --ssh-port 22229 \
  --bin-dir "$tmp_dir/helpers")"

printf '%s\n' "$output" | grep -Fq "export PATH=\"$tmp_dir/helpers:\$PATH\""
