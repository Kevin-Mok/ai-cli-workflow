#!/usr/bin/env bash

set -euo pipefail

print_fail() {
  printf 'FAIL: %s\n' "$1" >&2
}

usage() {
  cat <<'EOF'
Usage:
  ./scripts/executable_setup-termux-mosh.sh --host HOST --user USER --ssh-port PORT [options]

Installs mosh, OpenSSH, and rsync in Termux, then creates a named SSH host and
helper commands for connecting to a public Linux host.

Required options:
  --host HOST       Public hostname or IP address of the Linux host.
  --user USER       Existing key-based SSH login user on the Linux host.
  --ssh-port PORT   Existing public SSH TCP port on the Linux host.

Optional options:
  --alias NAME      SSH host alias and helper target. Defaults to pc-remote.
  --bin-dir PATH    Helper-command directory. Defaults to ~/.local/bin.
  -h, --help        Show this help text.

The PC must already allow and forward UDP 60000:61000 for mosh. This script
does not create an Android SSH server or alter router configuration.
EOF
}

require_command() {
  local name="$1"

  if command -v "$name" >/dev/null 2>&1; then
    return 0
  fi

  print_fail "Required command is unavailable: $name"
  exit 1
}

is_valid_port() {
  local value="$1"

  [[ "$value" =~ ^[0-9]+$ ]] || return 1
  [ "$value" -ge 1 ] && [ "$value" -le 65535 ]
}

is_valid_name() {
  local value="$1"

  [[ "$value" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]
}

write_ssh_config() {
  local config_path="$1"
  local temp_path

  temp_path="$(mktemp)"
  if [ -f "$config_path" ]; then
    awk '
      $0 == "# BEGIN linux-config Termux Mosh" { skipping = 1; next }
      $0 == "# END linux-config Termux Mosh" { skipping = 0; next }
      !skipping { print }
    ' "$config_path" > "$temp_path"
  fi

  cat >> "$temp_path" <<EOF
# BEGIN linux-config Termux Mosh
Host ${ssh_alias}
  HostName ${host}
  User ${ssh_user}
  Port ${ssh_port}
# END linux-config Termux Mosh
EOF

  install -m 600 "$temp_path" "$config_path"
  rm -f "$temp_path"
}

write_helper() {
  local destination="$1"
  local temp_path

  temp_path="$(mktemp)"
  cat > "$temp_path"
  install -m 755 "$temp_path" "$destination"
  rm -f "$temp_path"
}

host=""
ssh_user=""
ssh_port=""
ssh_alias="pc-remote"
bin_dir="${HOME}/.local/bin"

while [ $# -gt 0 ]; do
  case "$1" in
    --host)
      shift
      host="${1:-}"
      ;;
    --user)
      shift
      ssh_user="${1:-}"
      ;;
    --ssh-port)
      shift
      ssh_port="${1:-}"
      ;;
    --alias)
      shift
      ssh_alias="${1:-}"
      ;;
    --bin-dir)
      shift
      bin_dir="${1:-}"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      print_fail "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
  shift
done

if [ -z "$host" ] || [[ "$host" =~ [[:space:]] ]] || [[ "$host" == -* ]]; then
  print_fail '--host must be a hostname or IP address without whitespace'
  exit 1
fi

if [ -z "$ssh_user" ] || [[ "$ssh_user" =~ [[:space:]] ]] || [[ "$ssh_user" == -* ]]; then
  print_fail '--user must be an SSH user name without whitespace'
  exit 1
fi

if ! is_valid_port "$ssh_port"; then
  print_fail '--ssh-port must be a number from 1 to 65535'
  exit 1
fi

if ! is_valid_name "$ssh_alias"; then
  print_fail '--alias must start with a letter or number and use only letters, numbers, ., _, or -'
  exit 1
fi

if [ -z "$bin_dir" ] || [[ "$bin_dir" != /* ]]; then
  print_fail '--bin-dir must be an absolute path'
  exit 1
fi

require_command pkg
require_command awk
require_command install
require_command mktemp

printf 'Installing Termux packages: mosh, openssh, rsync\n'
pkg install -y mosh openssh rsync

ssh_dir="${HOME}/.ssh"
ssh_config="${ssh_dir}/config"
mkdir -p -m 700 "$ssh_dir" "$bin_dir"
write_ssh_config "$ssh_config"

write_helper "${bin_dir}/pc-mosh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec mosh ${ssh_alias@Q} "\$@"
EOF

write_helper "${bin_dir}/pc-push" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [ "\$#" -ne 2 ]; then
  printf 'Usage: pc-push LOCAL_PATH REMOTE_PATH\\n' >&2
  exit 1
fi
exec scp -r -- "\$1" ${ssh_alias@Q}:"\$2"
EOF

write_helper "${bin_dir}/pc-pull" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [ "\$#" -ne 2 ]; then
  printf 'Usage: pc-pull REMOTE_PATH LOCAL_PATH\\n' >&2
  exit 1
fi
exec scp -r -- ${ssh_alias@Q}:"\$1" "\$2"
EOF

write_helper "${bin_dir}/pc-sync-to-pc" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [ "\$#" -ne 2 ]; then
  printf 'Usage: pc-sync-to-pc LOCAL_DIR REMOTE_DIR\\n' >&2
  exit 1
fi
exec rsync -a --info=progress2 --human-readable --protect-args -e ssh -- "\${1%/}/" ${ssh_alias@Q}:"\${2%/}/"
EOF

write_helper "${bin_dir}/pc-sync-from-pc" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [ "\$#" -ne 2 ]; then
  printf 'Usage: pc-sync-from-pc REMOTE_DIR LOCAL_DIR\\n' >&2
  exit 1
fi
exec rsync -a --info=progress2 --human-readable --protect-args -e ssh -- ${ssh_alias@Q}:"\${1%/}/" "\${2%/}/"
EOF

printf '\nConfigured SSH host: %s\n' "$ssh_alias"
printf 'Installed helpers in: %s\n' "$bin_dir"
printf '\nRun these checks from Termux:\n'
printf '  ssh %s true\n' "$ssh_alias"
printf '  pc-mosh\n'
printf '\nFile helpers:\n'
printf '  pc-push LOCAL_PATH REMOTE_PATH\n'
printf '  pc-pull REMOTE_PATH LOCAL_PATH\n'
printf '  pc-sync-to-pc LOCAL_DIR REMOTE_DIR\n'
printf '  pc-sync-from-pc REMOTE_DIR LOCAL_DIR\n'
printf '\nIf your shell cannot find pc-mosh, add this for the current session:\n'
printf '  export PATH="%s:$PATH"\n' "$bin_dir"
