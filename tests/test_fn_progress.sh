#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
function_path="${repo_root}/dot_config/fish/functions/fn-progress.fish"
tmpdir="$(mktemp -d)"

cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

mkdir -p "${tmpdir}/bin"
cat > "${tmpdir}/bin/date" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  printf 'Thu Sep 10 10:07:46 EDT 2026\n'
elif [ "$1" = "-d" ]; then
  case "$2" in
    "2026-08-20 00:00:00") printf '0\n' ;;
    "2026-11-01 00:00:00") printf '6307200\n' ;;
    *) printf 'unexpected parsed date: %s\n' "$2" >&2; exit 2 ;;
  esac
elif [ "$1" = "+%s" ]; then
  printf '1814400\n'
else
  printf 'unexpected date arguments: %s\n' "$*" >&2
  exit 2
fi
EOF
chmod +x "${tmpdir}/bin/date"

output="$(PATH="${tmpdir}/bin:${PATH}" fish --no-config -c "source '${function_path}'; fn-progress")"
level_output="$(PATH="${tmpdir}/bin:${PATH}" fish --no-config -c "source '${function_path}'; fn-progress 75")"

if [[ "$output" != *'🚀 Season Start: 2026-08-20 00:00:00'* ]]; then
  printf 'expected August 20 C7S4 season start in output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'🛑 Season End: 2026-11-01 00:00:00'* ]]; then
  printf 'expected November 1 C7S4 season end in output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'⏱️ Days: 21 elapsed, 52 remaining'* ]]; then
  printf 'expected elapsed and remaining whole-day output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'✅ Fortnite C7S4 is 29% complete!'* ]]; then
  printf 'expected 28.8 percent to round to 29 percent\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'✅ Fortnite C7S4 is '*'% complete!'* ]]; then
  printf 'expected active C7S4 progress output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" == *'has ended'* ]]; then
  printf 'expected September 10 to remain inside the C7S4 date range\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$level_output" != *'🎮 Level 75 is 6 days ahead of level 200 pace.'* ]]; then
  printf 'expected level 75 to report six days ahead of level 200 pace\n%s\n' "$level_output" >&2
  exit 1
fi

if [[ "$level_output" != *'📈 At current pace, 35 days left to reach level 200.'* ]]; then
  printf 'expected level 75 to report projected days left at current pace\n%s\n' "$level_output" >&2
  exit 1
fi

if [[ "$level_output" != *'📊 Average pace: 3.57 levels/day.'* ]]; then
  printf 'expected level 75 to report an average of 3.57 levels per day\n%s\n' "$level_output" >&2
  exit 1
fi
