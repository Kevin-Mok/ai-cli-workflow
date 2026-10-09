function refresh-config
    set -l refresh_log "/tmp/refresh-config-"(date +%Y%m%d-%H%M%S)-$fish_pid.log
    touch $refresh_log
    cli-message 📝 "refresh-config log: $refresh_log" >&2

    cli-message 🔄 "[start] snapshot-codex-config" | tee -a $refresh_log >&2
    snapshot-codex-config >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] apply Codex config" | tee -a $refresh_log >&2
    chezmoi apply --force ~/.codex/config.toml >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] resolve Git config source path" | tee -a $refresh_log >&2
    set gitconfig_source_path (chezmoi source-path ~/.gitconfig)
    or return $status
    cli-message 🔄 "[start] copy Git config into source" | tee -a $refresh_log >&2
    cp ~/.gitconfig $gitconfig_source_path >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] normalize Git credential helper" | tee -a $refresh_log >&2
    sed -i 's/^\([[:space:]]*helper =\)[[:space:]]*$/\1/' $gitconfig_source_path >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] apply Git config" | tee -a $refresh_log >&2
    chezmoi apply --force ~/.gitconfig >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] apply remaining chezmoi targets" | tee -a $refresh_log >&2
    chezmoi apply --no-tty --keep-going </dev/null >>$refresh_log 2>&1
    set chezmoi_apply_status $status

    if test $chezmoi_apply_status -ne 0
        set conflicted_targets (rg '^[^ ]+ has changed since chezmoi last wrote it' $refresh_log | awk '{print $1}')
        for target in $conflicted_targets
            cli-message 🔄 "[start] adopt local $target" | tee -a $refresh_log >&2
            chezmoi add -- "$HOME/$target" >>$refresh_log 2>&1
            if test $status -ne 0
                cli-message ❌ "Failed to adopt local $target; see $refresh_log" >&2
                return 1
            end
        end
        if test (count $conflicted_targets) -gt 0
            cli-message 🔄 "[start] retry remaining chezmoi targets" | tee -a $refresh_log >&2
            chezmoi apply --no-tty --keep-going </dev/null >>$refresh_log 2>&1
            set chezmoi_apply_status $status
        end
    end
    cli-message 🔄 "[start] sync shortcuts" | tee -a $refresh_log >&2
    sync-shortcuts >>$refresh_log 2>&1
    or return $status
    cli-message 🔄 "[start] source shortcuts" | tee -a $refresh_log >&2
    source ~/.config/fish/key_abbr.fish >>$refresh_log 2>&1
    or return $status
    if test $chezmoi_apply_status -ne 0
        cli-message ⚠️ "Conflicts from $refresh_log:" >&2
        rg -n -i 'changed since|conflict|error|failed|could not|EOF' $refresh_log >&2
        return $chezmoi_apply_status
    end
    if isatty stdout
        set_color --bold green
    end
    cli-message ✅ "REFRESH COMPLETE"
    if isatty stdout
        set_color normal
    end
end
