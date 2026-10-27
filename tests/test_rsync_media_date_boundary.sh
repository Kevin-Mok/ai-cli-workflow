#!/usr/bin/env bash

set -euo pipefail
export TZ=America/Toronto

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/executable_rsync-media-date"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

source_root="${tmpdir}/ipad"
destination="${tmpdir}/destination"
mkdir -p "${source_root}/DCIM/100APPLE"

printf 'july 28\n' > "${source_root}/DCIM/100APPLE/IMG_JULY_28.MOV"
printf 'july 29\n' > "${source_root}/DCIM/100APPLE/IMG_JULY_29.MP4"
touch -d '2026-07-28 23:59:59' "${source_root}/DCIM/100APPLE/IMG_JULY_28.MOV"
touch -d '2026-07-29 00:00:00' "${source_root}/DCIM/100APPLE/IMG_JULY_29.MP4"

bash "$script_path" 2026-07-28 "$source_root" "$destination" >/dev/null

test -f "${destination}/IMG_JULY_28.MOV"
test ! -e "${destination}/IMG_JULY_29.MP4"

# UTC midnight is still the preceding evening in Toronto.
printf 'concert\n' > "${source_root}/DCIM/100APPLE/PXL_20260928_004333491.mp4"
printf 'next day\n' > "${source_root}/DCIM/100APPLE/PXL_20260928_040000000.mp4"
touch -d '2026-09-28 00:43:33 UTC' "${source_root}/DCIM/100APPLE/PXL_20260928_004333491.mp4"
touch -d '2026-09-28 04:00:00 UTC' "${source_root}/DCIM/100APPLE/PXL_20260928_040000000.mp4"
TZ=UTC bash "$script_path" 2026-09-27 "$source_root" "${tmpdir}/toronto" >/dev/null
test -f "${tmpdir}/toronto/PXL_20260928_004333491.mp4"
test ! -e "${tmpdir}/toronto/PXL_20260928_040000000.mp4"
