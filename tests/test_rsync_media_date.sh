#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_rsync-media-date"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mockbin="${tmpdir}/mockbin"
source_root="${tmpdir}/ipad"
destination="${tmpdir}/jcole"
rsync_log="${tmpdir}/rsync-args.bin"
rsync_calls="${tmpdir}/rsync-calls"

mkdir -p "${mockbin}" "${source_root}/DCIM/100APPLE" \
  "${source_root}/DCIM/101APPLE" "${source_root}/PhotoData"

touch -d '2026-07-27 23:59:00' "${source_root}/DCIM/100APPLE/IMG_OLD.MOV"
touch -d '2026-07-28 12:00:00' "${source_root}/DCIM/101APPLE/IMG_JULY_28.MOV"
touch -d '2026-07-28 13:00:00' "${source_root}/DCIM/101APPLE/IMG_JULY_28.MP4"
touch -d '2026-07-29 00:00:00' "${source_root}/DCIM/101APPLE/IMG_JULY_29.M4V"
touch -d '2026-07-28 14:00:00' "${source_root}/PhotoData/ignored.MOV"

cat > "${mockbin}/rsync" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\0' "$@" > "$TEST_RSYNC_LOG"
printf 'called\n' >> "$TEST_RSYNC_CALLS"
EOF
chmod +x "${mockbin}/rsync"

run_script() {
  TEST_RSYNC_LOG="$rsync_log" \
  TEST_RSYNC_CALLS="$rsync_calls" \
  PATH="${mockbin}:${PATH}" \
  bash "$script_path" "$@"
}

assert_contains_nul() {
  local expected="$1"
  if ! tr '\0' '\n' < "$rsync_log" | rg -Fqx -- "$expected"; then
    printf 'expected rsync argument: %s\n' "$expected" >&2
    exit 1
  fi
}

assert_not_contains_nul() {
  local unexpected="$1"
  if tr '\0' '\n' < "$rsync_log" | rg -Fqx -- "$unexpected"; then
    printf 'unexpected rsync argument: %s\n' "$unexpected" >&2
    exit 1
  fi
}

test -x "$script_path"
bash -n "$script_path"

run_script 2026-07-28 "$source_root" "$destination"

test -d "$destination"
test -s "$rsync_calls"
assert_contains_nul '--archive'
assert_contains_nul '--info=progress2'
assert_contains_nul '--human-readable'
assert_contains_nul '--no-relative'
assert_contains_nul "${source_root}/DCIM/101APPLE/IMG_JULY_28.MOV"
assert_contains_nul "${source_root}/DCIM/101APPLE/IMG_JULY_28.MP4"
assert_contains_nul "${destination}/"
assert_not_contains_nul '--ignore-existing'
assert_not_contains_nul '--update'
assert_not_contains_nul "${source_root}/DCIM/100APPLE/IMG_OLD.MOV"
assert_not_contains_nul "${source_root}/DCIM/101APPLE/IMG_JULY_29.M4V"
assert_not_contains_nul "${source_root}/PhotoData/ignored.MOV"

rm -f "$rsync_calls"
if run_script 2026-7-28 "$source_root" "$destination" >"${tmpdir}/invalid.out" 2>&1; then
  printf 'expected malformed date to fail\n' >&2
  exit 1
fi
rg -Fq 'YYYY-MM-DD' "${tmpdir}/invalid.out"
test ! -e "$rsync_calls"
