#!/usr/bin/env bash

set -euo pipefail

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
