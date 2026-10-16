function refresh-config
    set -l refresh_log (mktemp /tmp/refresh-config.XXXXXXXX.log)
    or return $status
    cli-message 📝 "refresh-config private log: $refresh_log" >&2
    cli-message 🔄 '[start] apply reviewed chezmoi files (scripts, externals, and removals excluded)' >&2
    set -l progress_label (cli-message 🔄 'Apply still running;')
    command python3 -c 'import os, sys, time
parent = os.getppid()
start = time.monotonic()
while True:
    time.sleep(10)
    if os.getppid() != parent:
        break
    print(f"{sys.argv[1]} elapsed {int(time.monotonic() - start)}s", flush=True)
' "$progress_label" >&2 &
    set -l progress_pid $last_pid
    chezmoi apply --exclude scripts,externals,remove --no-tty </dev/null >>$refresh_log 2>&1
    set -l apply_status $status
    kill $progress_pid 2>/dev/null
    wait $progress_pid 2>/dev/null
    if test $apply_status -ne 0
        cli-message ❌ "Apply stopped; review local differences privately with chezmoi diff. No files were adopted. Private log: $refresh_log" >&2
        return $apply_status
    end
    cli-message 🔄 '[start] sync shortcuts' >&2
    sync-shortcuts >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 '[start] source shortcuts' >&2
    source ~/.config/fish/key_abbr.fish >>$refresh_log 2>&1
    or return $status
    cli-message ✅ 'REFRESH COMPLETE'
end
