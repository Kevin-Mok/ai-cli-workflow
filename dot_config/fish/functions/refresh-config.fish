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
    set -l apply_status 0
    set -l previous_failure ''
    while true
        cli-message 🔄 'Preserving modified local managed files in source' >&2
        set -l local_changes (chezmoi status --exclude scripts,externals,remove --no-tty 2>>$refresh_log)
        set apply_status $status
        if test $apply_status -ne 0
            break
        end
        for entry in $local_changes
            if string match -rq '^[MA]' -- "$entry"
                set -l target (string sub -s 4 -- "$entry")
                chezmoi re-add --no-tty -- "$HOME/$target" >>$refresh_log 2>&1
                set apply_status $status
                if test $apply_status -ne 0
                    break
                end
            end
        end
        if test $apply_status -ne 0
            break
        end
        set -l attempt_log (mktemp /tmp/refresh-config-attempt.XXXXXXXX.log)
        chezmoi apply --exclude scripts,externals,remove --no-tty </dev/null >$attempt_log 2>&1
        set apply_status $status
        cat $attempt_log >>$refresh_log
        set -l failure (cat $attempt_log)
        rm -f $attempt_log
        if test $apply_status -eq 0
            break
        end
        if not string match -q '*has changed since chezmoi last wrote it*' -- "$failure"
            break
        end
        if test "$failure" = "$previous_failure"
            break
        end
        set previous_failure "$failure"
        cli-message 🔄 'Local drift detected; preserving and retrying' >&2
    end
    kill $progress_pid 2>/dev/null
    wait $progress_pid 2>/dev/null
    if test $apply_status -ne 0
        cli-message ❌ "Apply stopped; review local differences privately with chezmoi diff. Eligible local changes were preserved. Private log: $refresh_log" >&2
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
