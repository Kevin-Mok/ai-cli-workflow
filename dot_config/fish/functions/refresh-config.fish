function refresh-config
    set -l refresh_log (mktemp /tmp/refresh-config.XXXXXXXX.log)
    or return $status
    cli-message 📝 "refresh-config private log: $refresh_log" >&2
    cli-message 🔄 '[start] copy local managed updates into the repo before apply' >&2
    # Both names map to .config/mimeapps.list; retain the private attribute.
    set -l source_dir (chezmoi source-path 2>>$refresh_log)
    or return $status
    if test (count $source_dir) -ne 1; or not string match -q -- '/*' "$source_dir"; or not test -d "$source_dir"
        cli-message ❌ 'Cannot determine one absolute chezmoi source directory; refresh stopped' >&2
        return 1
    end
    set -l state_home "$HOME/.local/state"
    if set -q XDG_STATE_HOME; and test -n "$XDG_STATE_HOME"
        set state_home "$XDG_STATE_HOME"
    end
    set -l backup_root "$state_home/refresh-config/backups"
    if not command python3 -c 'from pathlib import Path; import sys; sys.exit(Path(sys.argv[1]).resolve().is_relative_to(Path(sys.argv[2]).resolve()))' "$backup_root" "$source_dir" 2>>$refresh_log
        cli-message ❌ 'Refresh backup must be outside the chezmoi source directory; choose another XDG_STATE_HOME' >&2
        return 1
    end
    set -l ordinary_mime "$source_dir/dot_config/mimeapps.list"
    set -l private_mime "$source_dir/dot_config/private_mimeapps.list"
    if test -e "$ordinary_mime"; or test -L "$ordinary_mime"
        if test -e "$private_mime"; or test -L "$private_mime"
            if test -L "$ordinary_mime"; or test -L "$private_mime"; or not test -f "$ordinary_mime"; or not test -f "$private_mime"
                cli-message ❌ "Duplicate MIME sources are not regular files; preserve both and review: $ordinary_mime and $private_mime" >&2
                return 1
            end
            if not cmp -s -- "$ordinary_mime" "$private_mime"
                cli-message ❌ "Duplicate MIME sources differ; preserve both and merge into $private_mime before retrying" >&2
                return 1
            end
            mkdir -p -m 700 -- "$backup_root" 2>>$refresh_log
            or return $status
            set -l backup_dir (mktemp -d "$backup_root/mimeapps.XXXXXXXX" 2>>$refresh_log)
            or return $status
            mv -- "$ordinary_mime" "$backup_dir/mimeapps.list" 2>>$refresh_log
            or return $status
            cli-message 📦 "Identical duplicate MIME source backed up to $backup_dir/mimeapps.list; keeping private source" >&2
        end
    end
    set -l progress_label (cli-message 🔄 'Refresh still running;')
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
                set -l local_source (chezmoi source-path -- "$HOME/$target" 2>>$refresh_log)
                set apply_status $status
                if test $apply_status -ne 0
                    break
                end
                if test (count $local_source) -ne 1; or not test -e "$local_source"
                    cli-message ❌ "Cannot locate the repo source for $target; local file preserved" >&2
                    set apply_status 1
                    break
                end
                if string match -q -- '*.tmpl' "$local_source"
                    cli-message ❌ "Local template changed: $target; merge changes into $local_source before retrying (chezmoi merge)" >&2
                    set apply_status 1
                    break
                end
                if test -f "$local_source"; or test -L "$local_source"
                    mkdir -p -m 700 -- "$backup_root" 2>>$refresh_log
                    and set -l import_backup (mktemp -d "$backup_root/local.XXXXXXXX" 2>>$refresh_log)
                    and cp -a -- "$local_source" "$import_backup/source" 2>>$refresh_log
                    set apply_status $status
                    if test $apply_status -ne 0
                        break
                    end
                    cli-message 📥 "Repo copy saved to $import_backup/source; importing local $target" >&2
                end
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
        cli-message 🔄 '[start] apply reviewed files (run scripts, externals, and removals excluded)' >&2
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
