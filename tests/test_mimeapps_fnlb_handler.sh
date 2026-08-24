#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mimeapps_path="${repo_root}/dot_config/mimeapps.list"

expected='x-scheme-handler/fnlb=fnlb.desktop'
actual="$(rg '^x-scheme-handler/fnlb=' "${mimeapps_path}")"

if [ "${actual}" != "${expected}" ]; then
    printf 'expected %s, got %s\n' "${expected}" "${actual}" >&2
    exit 1
fi
