#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="${repo_root}/scripts/executable_fix-aux-speaker-audio"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

cat >"${tmp_dir}/pactl" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"${PACTL_LOG}"
case "$*" in
  info)
    printf '%s\n' 'Default Sink: aux-speakers'
    ;;
  'list short sink-inputs')
    printf '17\t3\t1\tPipeWire\tfloat32le 2ch 48000Hz\tRUNNING\n'
    ;;
esac
EOF
chmod +x "${tmp_dir}/pactl"

PACTL_LOG="${tmp_dir}/pactl.log" PATH="${tmp_dir}:${PATH}" "${script}" --fix >/dev/null

grep -Fx 'set-sink-mute @DEFAULT_SINK@ 0' "${tmp_dir}/pactl.log"
grep -Fx 'move-sink-input 17 aux-speakers' "${tmp_dir}/pactl.log"
