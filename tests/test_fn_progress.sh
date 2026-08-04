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
  printf 'Tue Aug  4 10:07:46 EDT 2026\n'
elif [ "$1" = "-d" ]; then
  case "$2" in
    "2026-06-06 00:00:00") printf '100\n' ;;
    "2026-06-10 00:00:00") printf '100\n' ;;
    "2026-08-10 00:00:00") printf '140\n' ;;
    "2026-08-19 00:00:00") printf '200\n' ;;
    *) printf 'unexpected parsed date: %s\n' "$2" >&2; exit 2 ;;
  esac
elif [ "$1" = "+%s" ]; then
  printf '150\n'
else
  printf 'unexpected date arguments: %s\n' "$*" >&2
  exit 2
fi
EOF
chmod +x "${tmpdir}/bin/date"

output="$(PATH="${tmpdir}/bin:${PATH}" fish --no-config -c "source '${function_path}'; fn-progress")"

if [[ "$output" != *'🚀 Season Start: 2026-06-06 00:00:00'* ]]; then
  printf 'expected June 6 C7S3 season start in output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'🛑 Season End: 2026-08-19 00:00:00'* ]]; then
  printf 'expected August 19 C7S3 season end in output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" != *'✅ Fortnite C7S3 is **'*' complete!'* ]]; then
  printf 'expected active C7S3 progress output\n%s\n' "$output" >&2
  exit 1
fi

if [[ "$output" == *'has ended'* ]]; then
  printf 'expected August 4 to remain inside the C7S3 date range\n%s\n' "$output" >&2
  exit 1
fi
