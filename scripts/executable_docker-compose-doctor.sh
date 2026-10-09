#!/usr/bin/env bash

# Human-facing decoration; keep protocol/data output unchanged.
cli_emoji() {
  [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"
}

set -u

print_section() {
  printf '\n%s== %s ==\n' "$(cli_emoji '🔧')" "$1"
}

print_ok() {
  printf '%sOK: %s\n' "$(cli_emoji '✅')" "$1"
}

print_warn() {
  printf '%sWARN: %s\n' "$(cli_emoji '⚠️')" "$1"
}

print_fail() {
  printf '%sFAIL: %s\n' "$(cli_emoji '❌')" "$1"
}

print_section "Docker Compose Doctor"
printf '%sTime: %s\n' "$(cli_emoji 'ℹ️')" "$(date -Is 2>/dev/null || date)"

if [ -r /etc/os-release ]; then
  . /etc/os-release
  printf '%sOS: %s\n' "$(cli_emoji 'ℹ️')" "${PRETTY_NAME:-unknown}"
fi

docker_path="$(command -v docker 2>/dev/null || true)"
legacy_compose_path="$(command -v docker-compose 2>/dev/null || true)"

print_section "CLI Detection"
if [ -z "$docker_path" ]; then
  print_fail "docker is not installed or not on PATH."
  printf '%sNext step: install Docker first, then rerun this doctor.\n' "$(cli_emoji 'ℹ️')"
  exit 1
fi

print_ok "docker found at $docker_path"

docker_version_output="$(docker --version 2>&1)"
docker_version_status=$?
if [ "$docker_version_status" -eq 0 ]; then
  printf '%s\n' "$docker_version_output"
else
  print_warn "docker exists but docker --version failed:"
  printf '%s\n' "$docker_version_output"
fi

compose_v2_output="$(docker compose version 2>&1)"
compose_v2_status=$?
compose_v2_missing=0
if printf '%s' "$compose_v2_output" | grep -Fq "is not a docker command"; then
  compose_v2_missing=1
fi

if [ "$compose_v2_status" -eq 0 ] && [ "$compose_v2_missing" -eq 0 ]; then
  print_ok "docker compose is already available."
  printf '%s\n' "$compose_v2_output"
  exit 0
fi

print_fail "docker compose is not usable on this machine."
printf '%s\n' "$compose_v2_output"

legacy_compose_output=""
if [ -n "$legacy_compose_path" ]; then
  legacy_compose_output="$(docker-compose --version 2>&1)"
  legacy_compose_status=$?
  if [ "$legacy_compose_status" -eq 0 ]; then
    print_ok "legacy docker-compose binary found at $legacy_compose_path"
    printf '%s\n' "$legacy_compose_output"
  else
    print_warn "legacy docker-compose binary exists but failed to run:"
    printf '%s\n' "$legacy_compose_output"
  fi
else
  print_warn "legacy docker-compose binary was not found on PATH."
fi

print_section "Docker Client Plugins"
client_info_output="$(docker info --format '{{json .ClientInfo}}' 2>/dev/null || true)"
if [ -n "$client_info_output" ]; then
  printf '%s\n' "$client_info_output"
else
  print_warn "Could not read docker client plugin metadata."
fi

print_section "Plugin Search Paths"
plugin_found=0
for plugin_dir in \
  /usr/libexec/docker/cli-plugins \
  /usr/lib/docker/cli-plugins \
  /usr/local/lib/docker/cli-plugins \
  "${HOME}/.docker/cli-plugins"
do
  if [ -d "$plugin_dir" ]; then
    printf '%s\n' "$plugin_dir"
    ls -1 "$plugin_dir" 2>/dev/null || true
    if [ -e "$plugin_dir/docker-compose" ]; then
      plugin_found=1
    fi
  fi
done

print_section "Diagnosis"
if [ "$compose_v2_missing" -eq 1 ]; then
  print_fail "Docker Compose v2 plugin is missing from the Docker CLI."
  if [ -n "$legacy_compose_path" ]; then
    print_warn "You only have legacy docker-compose v1 installed."
  fi
  if [ "$plugin_found" -eq 0 ]; then
    print_warn "No docker-compose plugin binary was found in standard plugin directories."
  fi
  printf '%sRecommended fix: run bash scripts/executable_install-docker-compose-v2.sh\n' "$(cli_emoji 'ℹ️')"
  exit 1
fi

print_warn "The failure is not the usual missing-plugin message."
printf '%sInvestigate the error above before installing anything.\n' "$(cli_emoji 'ℹ️')"
exit 1
