#!/usr/bin/env bash
set -euo pipefail

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
work_dir=$(mktemp -d)
core_pid=
pulse_pid=
trap '[[ -z $pulse_pid ]] || kill "$pulse_pid" 2>/dev/null || true; [[ -z $core_pid ]] || kill "$core_pid" 2>/dev/null || true; wait; rm -rf -- "$work_dir"' EXIT

export XDG_CONFIG_HOME="$work_dir/config"
export XDG_RUNTIME_DIR="$work_dir/run"
export PIPEWIRE_RUNTIME_DIR="$XDG_RUNTIME_DIR"
export PIPEWIRE_REMOTE=pipewire-0
export PULSE_SERVER="unix:$XDG_RUNTIME_DIR/pulse/native"
drop_in=pipewire/pipewire-pulse.conf.d/50-spotify-virtual-mic.conf
mkdir -p "$XDG_RUNTIME_DIR" "$XDG_CONFIG_HOME/$(dirname "$drop_in")"
if [[ -f "$repo_dir/dot_config/$drop_in" ]]; then
    cp "$repo_dir/dot_config/$drop_in" "$XDG_CONFIG_HOME/$drop_in"
fi
pipewire >"$work_dir/pipewire.log" 2>&1 &
core_pid=$!

for attempt in {1..50}; do
    [[ ! -S "$XDG_RUNTIME_DIR/pipewire-0" ]] || break
    sleep 0.1
done
for boot in 1 2; do
    pipewire-pulse >"$work_dir/pulse.log" 2>&1 &
    pulse_pid=$!
    for attempt in {1..50}; do
        if pactl --format=json list sinks >"$work_dir/sinks.json" 2>/dev/null &&
            pactl --format=json list sources >"$work_dir/sources.json" 2>/dev/null &&
            python3 - "$work_dir" 2>"$work_dir/probe.log" <<'PY'
import json
from pathlib import Path
import sys

work_dir = Path(sys.argv[1])
sinks = json.loads((work_dir / "sinks.json").read_text())
sources = json.loads((work_dir / "sources.json").read_text())
assert [(s["name"], s["description"]) for s in sinks if "spotify" in s["name"]] == [
    ("spotify_cable", "Spotify Cable"),
]
assert sorted((s["name"], s["description"]) for s in sources if "spotify" in s["name"]) == [
    ("spotify_cable.monitor", "Monitor of Spotify Cable"),
    ("spotify_virtual_mic", "Spotify Virtual Mic"),
]
PY
        then
            break
        fi
        if [[ $attempt == 50 ]]; then
            echo "❌ Spotify audio devices missing or duplicated on Pulse start $boot" >&2
            cat "$work_dir/probe.log" "$work_dir/pipewire.log" "$work_dir/pulse.log" >&2
            exit 1
        fi
        sleep 0.1
    done
    kill "$pulse_pid"
    wait "$pulse_pid" || true
    pulse_pid=
done
echo "✅ Spotify Cable and Spotify Virtual Mic appeared on both Pulse starts"
