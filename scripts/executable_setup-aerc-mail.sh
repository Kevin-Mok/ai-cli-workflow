#!/usr/bin/env bash

set -euo pipefail

readonly script_name="$(basename "$0")"
readonly config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
readonly aerc_dir="${config_home}/aerc"
readonly aerc_config="${aerc_dir}/aerc.conf"
readonly accounts_config="${aerc_dir}/accounts.conf"
readonly oama_dir="${config_home}/oama"
readonly oama_config="${oama_dir}/config.yaml"
readonly pass_prefix="email/aerc"

action=""
dry_run=false
pass_recipient=""

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

note() {
  printf '%s\n' "$*"
}

usage() {
  cat <<EOF
Usage: ${script_name} ACTION [--dry-run]

Actions (exactly one is required):
  --install                 Install shared aerc mail prerequisites; may require sudo.
  --init-pass GPG_KEY_ID    Initialize an empty pass store for this GPG recipient.
  --add-gmail               Interactively add one Gmail account and app password.
  --add-outlook             Interactively add one Outlook.com OAuth2 account.
  --status                  Check configured accounts without printing credentials.
  -h, --help                Show this help text.

Options:
  --dry-run                 Print sanitized add/install operations without writing files,
                            inserting credentials, or starting OAuth.

Each add action manages one account. Gmail needs a Google app password. Outlook
needs IMAP enabled plus a Microsoft app client ID for device-code OAuth2. This
script stores secrets outside Git and never prints credentials.
EOF
}

require_one_action() {
  if [ -z "$action" ]; then
    fail 'exactly one action is required; run --help for usage'
  fi
}

set_action() {
  if [ -n "$action" ]; then
    fail 'exactly one action is allowed'
  fi
  action="$1"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --install|--add-gmail|--add-outlook|--status)
      set_action "$1"
      ;;
    --init-pass)
      set_action "$1"
      shift
      pass_recipient="${1:-}"
      [ -n "$pass_recipient" ] || fail '--init-pass requires a GPG_KEY_ID'
      ;;
    --dry-run)
      dry_run=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
  shift
done

require_one_action

need_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command is unavailable: $1"
}

password_store_dir() {
  printf '%s\n' "${PASSWORD_STORE_DIR:-$HOME/.password-store}"
}

require_pass_store() {
  local store
  store="$(password_store_dir)"
  [ -f "${store}/.gpg-id" ] || fail "pass is not initialized; run ${script_name} --init-pass GPG_KEY_ID first"
}

validate_label() {
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail 'account labels must use lowercase letters, digits, and hyphens'
}

validate_email() {
  [[ "$1" =~ ^[A-Za-z0-9.!#$%\&\'*+/=?^_\`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]] || fail 'email address is not valid'
}

url_encode_email() {
  printf '%s\n' "${1//@/%40}"
}

ensure_private_dir() {
  local path="$1"

  [ ! -L "$path" ] || fail "refusing symbolic link directory: $path"
  if [ ! -e "$path" ]; then
    if "$dry_run"; then
      note "would create private directory: $path"
      return
    fi
    mkdir -p "$path"
    chmod 700 "$path"
  fi
  [ -d "$path" ] || fail "expected directory: $path"
}

ensure_private_file() {
  local path="$1"

  [ ! -L "$path" ] || fail "refusing symbolic link target: $path"
  if [ ! -e "$path" ]; then
    if "$dry_run"; then
      note "would create private file: $path"
      return
    fi
    : > "$path"
    chmod 600 "$path"
  fi
  [ -f "$path" ] || fail "expected regular file: $path"
}

backup_if_needed() {
  local path="$1"
  local backup="${path}.aerc-mail-setup.bak"

  [ -e "$path" ] || return
  [ -e "$backup" ] && return
  "$dry_run" && return
  cp -- "$path" "$backup"
  chmod 600 "$backup"
  note "Backup retained at: $backup"
}

append_atomically() {
  local path="$1"
  local snippet="$2"
  local temp

  temp="$(mktemp "${path}.tmp.XXXXXX")"
  trap 'rm -f "$temp"' RETURN
  cat "$path" > "$temp"
  printf '\n%s\n' "$snippet" >> "$temp"
  chmod 600 "$temp"
  mv -- "$temp" "$path"
  trap - RETURN
}

account_exists() {
  local label="$1"
  [ -f "$accounts_config" ] && grep -Fq "# BEGIN aerc-mail-setup: ${label}" "$accounts_config"
}

remove_account_block() {
  local label="$1"
  local temp

  temp="$(mktemp "${accounts_config}.tmp.XXXXXX")"
  awk -v begin="# BEGIN aerc-mail-setup: ${label}" -v end="# END aerc-mail-setup: ${label}" '
    $0 == begin { skip = 1; next }
    $0 == end { skip = 0; next }
    !skip { print }
  ' "$accounts_config" > "$temp"
  chmod 600 "$temp"
  mv -- "$temp" "$accounts_config"
}

ensure_mail_hook() {
  ensure_private_dir "$aerc_dir"
  ensure_private_file "$aerc_config"

  if grep -Eq '^[[:space:]]*mail-received[[:space:]]*=' "$aerc_config"; then
    note 'aerc mail-received hook already exists; leaving it unchanged.'
    return
  fi

  backup_if_needed "$aerc_config"
  if "$dry_run"; then
    note "would add aerc mail-received hook: $aerc_config"
    return
  fi

  cat >> "$aerc_config" <<'EOF'

[hooks]
mail-received = notify-send -a aerc -i mail-unread "[$AERC_ACCOUNT] $AERC_FROM_NAME" "$AERC_SUBJECT"
EOF
}

prepare_accounts_file() {
  ensure_private_dir "$aerc_dir"
  ensure_private_file "$accounts_config"
  backup_if_needed "$accounts_config"
}

prompt_value() {
  local prompt="$1"
  local value
  read -r -p "$prompt" value
  printf '%s' "$value"
}

prompt_secret() {
  local prompt="$1"
  local value
  read -r -s -p "$prompt" value
  printf '\n' >&2
  printf '%s' "$value"
}

store_pass_secret() {
  local key="$1"
  local secret="$2"

  if "$dry_run"; then
    note "would store credential in pass: $key"
    return
  fi
  if pass show "$key" >/dev/null 2>&1; then
    fail "pass entry already exists: $key"
  fi
  printf '%s\n' "$secret" | pass insert --multiline "$key" >/dev/null
}

ensure_oama_client_id_command() {
  local command_value="pass show ${pass_prefix}/oama/microsoft-client-id"
  local temp

  ensure_private_dir "$oama_dir"
  [ ! -L "$oama_config" ] || fail "refusing symbolic link target: $oama_config"
  if [ ! -e "$oama_config" ]; then
    if "$dry_run"; then
      note "would create oama config: $oama_config"
      return
    fi
    oama template > "$oama_config"
    chmod 600 "$oama_config"
  fi
  [ -f "$oama_config" ] || fail "expected regular file: $oama_config"

  if grep -Fq "$command_value" "$oama_config"; then
    return
  fi
  grep -Eq '^  microsoft:[[:space:]]*$' "$oama_config" || fail "oama config has no microsoft service block: $oama_config"
  if grep -Eq '^    client_id_cmd:' "$oama_config"; then
    fail "oama config already has a different Microsoft client_id_cmd; update it manually: $oama_config"
  fi
  grep -Eq '^    client_id:' "$oama_config" || fail "oama config has no replaceable Microsoft client_id field: $oama_config"

  backup_if_needed "$oama_config"
  if "$dry_run"; then
    note "would configure oama Microsoft client ID lookup: $oama_config"
    return
  fi

  temp="$(mktemp "${oama_config}.tmp.XXXXXX")"
  awk -v cmd="$command_value" '
    /^  microsoft:[[:space:]]*$/ { in_microsoft = 1; print; next }
    in_microsoft && /^  [[:alnum:]_-]+:[[:space:]]*$/ { in_microsoft = 0 }
    in_microsoft && /^    client_id:[[:space:]]*/ {
      print "    client_id_cmd: |"
      print "      " cmd
      replaced = 1
      next
    }
    { print }
    END { if (!replaced) exit 1 }
  ' "$oama_config" > "$temp" || fail "could not configure Microsoft client ID lookup in $oama_config"
  chmod 600 "$temp"
  mv -- "$temp" "$oama_config"
}

add_gmail() {
  local label email password encoded_email pass_key block

  need_command pass
  require_pass_store
  label="$(prompt_value 'Gmail account label: ')"
  validate_label "$label"
  email="$(prompt_value 'Gmail address: ')"
  validate_email "$email"
  password="<redacted> 'Google app password: ')"
  [ -n "$password" ] || fail 'Google app password cannot be empty'
  encoded_email="$(url_encode_email "$email")"
  pass_key="${pass_prefix}/gmail/${label}"

  prepare_accounts_file
  account_exists "$label" && fail "account label already exists: $label"
  if "$dry_run"; then
    note "would add Gmail account $label"
    return
  fi
  store_pass_secret "$pass_key" "$password"
  block="# BEGIN aerc-mail-setup: ${label}
[${label}]
source = imaps:user@example.invalid:993
source-cred-cmd = pass show ${pass_key}
outgoing = smtps+plain:user@example.invalid:465
outgoing-cred-cmd = pass show ${pass_key}
default = INBOX
check-mail = 5m
copy-to = [Gmail]/Sent Mail
# END aerc-mail-setup: ${label}"
  append_atomically "$accounts_config" "$block"
  ensure_mail_hook
  note "Added Gmail account: $label"
}

add_outlook() {
  local label email client_id encoded_email pass_key block

  need_command pass
  need_command oama
  require_pass_store
  label="$(prompt_value 'Outlook account label: ')"
  validate_label "$label"
  email="$(prompt_value 'Outlook address: ')"
  validate_email "$email"
  client_id="$(prompt_secret 'Microsoft application client ID: ')"
  [ -n "$client_id" ] || fail 'Microsoft application client ID cannot be empty'
  encoded_email="$(url_encode_email "$email")"
  pass_key="${pass_prefix}/oama/microsoft-client-id"

  prepare_accounts_file
  account_exists "$label" && fail "account label already exists: $label"
  if "$dry_run"; then
    note "would add Outlook account $label"
    return
  fi
  store_pass_secret "$pass_key" "$client_id"
  ensure_oama_client_id_command
  block="# BEGIN aerc-mail-setup: ${label}
[${label}]
source = imaps+xoauth2:user@example.invalid:993
source-cred-cmd = oama access ${email}
outgoing = smtp+xoauth2:user@example.invalid:587
outgoing-cred-cmd = oama access ${email}
default = INBOX
check-mail = 5m
copy-to = Sent Items
# END aerc-mail-setup: ${label}"
  append_atomically "$accounts_config" "$block"
  ensure_mail_hook
  if ! oama authorize microsoft "$email" --device; then
    remove_account_block "$label"
    fail "Outlook authorization did not complete; removed account block for $label"
  fi
  note "Added Outlook account: $label"
}

status() {
  local label block provider pass_key failed=0

  need_command pass
  [ -f "$accounts_config" ] || fail "no aerc accounts configuration exists: $accounts_config"
  while IFS= read -r label; do
    block="$(awk -v begin="# BEGIN aerc-mail-setup: ${label}" -v end="# END aerc-mail-setup: ${label}" '
      $0 == begin { emit = 1 }
      emit { print }
      $0 == end { exit }
    ' "$accounts_config")"
    if grep -Fq 'imap.gmail.com' <<< "$block"; then
      provider='gmail'
      pass_key="${pass_prefix}/gmail/${label}"
    elif grep -Fq 'outlook.office365.com' <<< "$block"; then
      provider='outlook'
      pass_key="${pass_prefix}/oama/microsoft-client-id"
      need_command oama
    else
      note "$label: unknown provider"
      failed=1
      continue
    fi
    if pass show "$pass_key" >/dev/null 2>&1; then
      note "$label: $provider"
    else
      printf '%s: %s (missing credential)\n' "$label" "$provider" >&2
      failed=1
    fi
  done < <(sed -n 's/^# BEGIN aerc-mail-setup: \(.*\)$/\1/p' "$accounts_config")
  [ "$failed" -eq 0 ] || exit 1
}

detect_package_manager() {
  if command -v apt-get >/dev/null 2>&1; then printf 'apt\n'; return; fi
  if command -v dnf >/dev/null 2>&1; then printf 'dnf\n'; return; fi
  if command -v pacman >/dev/null 2>&1; then printf 'pacman\n'; return; fi
  if command -v zypper >/dev/null 2>&1; then printf 'zypper\n'; return; fi
  fail 'supported package manager not found (apt-get, dnf, pacman, zypper)'
}

run_privileged() {
  if [ "${EUID:-$(id -u)}" -eq 0 ]; then
    "$@"
  else
    need_command sudo
    sudo "$@"
  fi
}

install_packages() {
  local manager
  manager="$(detect_package_manager)"
  "$dry_run" && { note "would install aerc, pass, GnuPG, libnotify, and dunst using $manager"; return; }
  case "$manager" in
    apt)
      run_privileged apt-get update
      run_privileged apt-get install -y aerc pass gnupg libnotify-bin dunst
      if apt-cache show oama >/dev/null 2>&1; then run_privileged apt-get install -y oama; else note 'Install oama manually from https://github.com/pdobsan/oama/releases.'; fi
      ;;
    dnf)
      run_privileged dnf install -y aerc pass gnupg2 libnotify dunst
      if dnf info -q oama >/dev/null 2>&1; then run_privileged dnf install -y oama; else note 'Install oama manually from https://github.com/pdobsan/oama/releases.'; fi
      ;;
    pacman)
      run_privileged pacman -Sy --needed --noconfirm aerc pass gnupg libnotify dunst
      if pacman -Si oama >/dev/null 2>&1; then run_privileged pacman -S --needed --noconfirm oama; else note 'Install oama manually from https://github.com/pdobsan/oama/releases.'; fi
      ;;
    zypper)
      run_privileged zypper --non-interactive install aerc pass gpg2 libnotify-tools dunst
      if zypper --non-interactive search --match-exact oama | grep -q oama; then run_privileged zypper --non-interactive install oama; else note 'Install oama manually from https://github.com/pdobsan/oama/releases.'; fi
      ;;
  esac
}

case "$action" in
  --install) install_packages ;;
  --init-pass)
    need_command pass
    "$dry_run" && { note "would initialize pass for: $pass_recipient"; exit 0; }
    pass init "$pass_recipient"
    ;;
  --add-gmail) add_gmail ;;
  --add-outlook) add_outlook ;;
  --status) status ;;
esac
