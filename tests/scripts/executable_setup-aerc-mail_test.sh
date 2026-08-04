#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
script_path="${repo_root}/scripts/executable_setup-aerc-mail.sh"
fixture_root="$(mktemp -d)"
trap 'rm -rf "$fixture_root"' EXIT

fixture_home="${fixture_root}/home"
fixture_bin="${fixture_root}/bin"
fixture_config="${fixture_root}/config"
fixture_state="${fixture_root}/state"
fixture_store="${fixture_root}/pass-store"
fixture_log="${fixture_root}/log"
mkdir -p "$fixture_home" "$fixture_bin" "$fixture_config" "$fixture_state" "$fixture_store" "$fixture_log"
printf 'test@example.invalid\n' > "${fixture_store}/.gpg-id"

write_fake_command() {
  local name="$1"
  shift
  local path="${fixture_bin}/${name}"

  printf '%s\n' '#!/usr/bin/env bash' 'set -euo pipefail' "$@" > "$path"
  chmod +x "$path"
}

write_fake_command pass '
case "${1:-}" in
  show)
    key="${2:?missing pass key}"
    test -f "${FAKE_PASS_DATA}/${key}"
    cat "${FAKE_PASS_DATA}/${key}"
    ;;
  insert)
    key="${@: -1}"
    mkdir -p "$(dirname "${FAKE_PASS_DATA}/${key}")"
    cat > "${FAKE_PASS_DATA}/${key}"
    printf "insert:%s\\n" "$key" >> "${FAKE_LOG}/pass.log"
    ;;
  init)
    printf "%s\\n" "${2:?missing recipient}" > "${PASSWORD_STORE_DIR}/.gpg-id"
    ;;
  *)
    printf "unexpected pass invocation: %s\\n" "$*" >&2
    exit 64
    ;;
esac'

write_fake_command oama '
case "${1:-}" in
  template)
    cat <<"EOF"
encryption: GPG
services:
  microsoft:
    client_id: application-CLIENT-ID
EOF
    ;;
  authorize)
    printf "authorize:%s:%s:%s\\n" "${2:-}" "${3:-}" "${4:-}" >> "${FAKE_LOG}/oama.log"
    ;;
  access)
    printf "fixture-oauth-token\\n"
    ;;
  *)
    printf "unexpected oama invocation: %s\\n" "$*" >&2
    exit 64
    ;;
esac'

write_fake_command notify-send 'exit 0'

run_script() {
  HOME="$fixture_home" \
  XDG_CONFIG_HOME="$fixture_config" \
  XDG_STATE_HOME="$fixture_state" \
  PASSWORD_STORE_DIR="$fixture_store" \
  FAKE_PASS_DATA="${fixture_root}/pass-data" \
  FAKE_LOG="$fixture_log" \
  PATH="${fixture_bin}:$PATH" \
  "$script_path" "$@"
}

assert_contains() {
  local needle="$1"
  local path="$2"

  if ! grep -Fq -- "$needle" "$path"; then
    printf 'expected %s to contain: %s\n' "$path" "$needle" >&2
    exit 1
  fi
}

assert_not_contains() {
  local needle="$1"
  local path="$2"

  if grep -Fq -- "$needle" "$path"; then
    printf 'did not expect %s to contain: %s\n' "$path" "$needle" >&2
    exit 1
  fi
}

help_output="${fixture_root}/help.out"
run_script --help > "$help_output"
assert_contains '--install' "$help_output"
assert_contains '--init-pass' "$help_output"
assert_contains '--add-gmail' "$help_output"
assert_contains '--add-outlook' "$help_output"
assert_contains '--status' "$help_output"
assert_contains 'never prints credentials' "$help_output"

if run_script --status --add-gmail > "${fixture_root}/multi.out" 2>&1; then
  printf 'expected multiple actions to fail\n' >&2
  exit 1
fi
assert_contains 'exactly one action' "${fixture_root}/multi.out"

if printf 'bad label\nname@example.com\napp-password\n' | run_script --add-gmail > "${fixture_root}/invalid.out" 2>&1; then
  printf 'expected malformed Gmail label to fail\n' >&2
  exit 1
fi
assert_contains 'lowercase letters, digits, and hyphens' "${fixture_root}/invalid.out"
test ! -e "${fixture_config}/aerc/accounts.conf"

printf 'gmail-main\ngmail.main@example.com\napp-password\n' | run_script --add-gmail --dry-run > "${fixture_root}/gmail-dry-run.out"
test ! -e "${fixture_config}/aerc/accounts.conf"
test ! -e "${fixture_log}/pass.log"
assert_contains 'would add Gmail account gmail-main' "${fixture_root}/gmail-dry-run.out"

printf 'gmail-main\ngmail.main@example.com\napp-password\n' | run_script --add-gmail
accounts_file="${fixture_config}/aerc/accounts.conf"
assert_contains '# BEGIN aerc-mail-setup: gmail-main' "$accounts_file"
assert_contains 'imaps:user@example.invalid:993' "$accounts_file"
assert_contains 'smtps+plain:user@example.invalid:465' "$accounts_file"
assert_contains 'pass show email/aerc/gmail/gmail-main' "$accounts_file"
assert_contains '[hooks]' "$fixture_config/aerc/aerc.conf"
assert_contains 'mail-received =' "$fixture_config/aerc/aerc.conf"

if printf 'gmail-main\ngmail.main@example.com\nsecond-password\n' | run_script --add-gmail > "${fixture_root}/duplicate.out" 2>&1; then
  printf 'expected duplicate Gmail account to fail\n' >&2
  exit 1
fi
assert_contains 'already exists' "${fixture_root}/duplicate.out"
test "$(grep -Fc '# BEGIN aerc-mail-setup: gmail-main' "$accounts_file")" -eq 1

printf 'outlook-main\noutlook.main@example.com\nfixture-client-id\n' | run_script --add-outlook --dry-run > "${fixture_root}/outlook-dry-run.out"
test ! -e "${fixture_log}/oama.log"
assert_contains 'would add Outlook account outlook-main' "${fixture_root}/outlook-dry-run.out"

printf 'outlook-main\noutlook.main@example.com\nfixture-client-id\n' | run_script --add-outlook
assert_contains '# BEGIN aerc-mail-setup: outlook-main' "$accounts_file"
assert_contains 'imaps+xoauth2:user@example.invalid:993' "$accounts_file"
assert_contains 'smtp+xoauth2:user@example.invalid:587' "$accounts_file"
assert_contains 'oama access outlook.main@example.com' "$accounts_file"
assert_contains 'client_id_cmd: |' "${fixture_config}/oama/config.yaml"
assert_contains 'pass show email/aerc/oama/microsoft-client-id' "${fixture_config}/oama/config.yaml"
assert_contains 'authorize:microsoft:outlook.main@example.com:--device' "${fixture_log}/oama.log"

status_output="${fixture_root}/status.out"
run_script --status > "$status_output"
assert_contains 'gmail-main: gmail' "$status_output"
assert_contains 'outlook-main: outlook' "$status_output"
assert_not_contains 'app-password' "$status_output"
assert_not_contains 'fixture-client-id' "$status_output"

rm "${fixture_root}/pass-data/email/aerc/gmail/gmail-main"
if run_script --status > "${fixture_root}/missing-secret.out" 2>&1; then
  printf 'expected missing Gmail secret to fail status\n' >&2
  exit 1
fi
assert_contains 'missing credential' "${fixture_root}/missing-secret.out"

rm -f "$accounts_file"
ln -s /tmp "$accounts_file"
if printf 'gmail-link\nlink@example.com\napp-password\n' | run_script --add-gmail > "${fixture_root}/symlink.out" 2>&1; then
  printf 'expected symlink accounts target to fail\n' >&2
  exit 1
fi
assert_contains 'refusing symbolic link' "${fixture_root}/symlink.out"
