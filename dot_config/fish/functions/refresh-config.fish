function refresh-config
    snapshot-codex-config >/dev/null
    or return $status
    chezmoi apply --force ~/.codex/config.toml >/dev/null
    or return $status
    set gitconfig_source_path (chezmoi source-path ~/.gitconfig)
    or return $status
    cp ~/.gitconfig $gitconfig_source_path
    or return $status
    sed -i 's/^\([[:space:]]*helper =\)[[:space:]]*$/\1/' $gitconfig_source_path
    or return $status
    chezmoi apply --force ~/.gitconfig >/dev/null
    or return $status
    chezmoi apply >/dev/null
    or return $status
    # and tmux source-file ~/.tmux.conf

    sync-shortcuts >/dev/null
    or return $status
    source ~/.config/fish/key_abbr.fish >/dev/null
    or return $status
    if isatty stdout
        set_color --bold green
    end
    echo 'REFRESH COMPLETE'
    if isatty stdout
        set_color normal
    end
    exec fish
end
