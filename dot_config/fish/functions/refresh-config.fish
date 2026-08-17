function refresh-config
    snapshot-codex-config
    or return $status
    and echo 'Copied local Codex config into repo source.'
    chezmoi apply --force ~/.codex/config.toml
    or return $status
    and echo 'Applied snapshotted Codex config.'
    set gitconfig_source_path (chezmoi source-path ~/.gitconfig)
    or return $status
    cp ~/.gitconfig $gitconfig_source_path
    or return $status
    sed -i 's/^\([[:space:]]*helper =\)[[:space:]]*$/\1/' $gitconfig_source_path
    or return $status
    and echo 'Copied local Git config into repo source.'
    chezmoi apply --force ~/.gitconfig
    or return $status
    and echo 'Applied snapshotted Git config.'
    chezmoi apply
    and echo 'Applied chezmoi.'
    # and tmux source-file ~/.tmux.conf
    # and echo 'Sourced tmux config.'

    sync-shortcuts
    echo 'Synced shortcuts.'
    source ~/.config/fish/key_abbr.fish > /dev/null
    and echo 'Sourced shortcuts.'
    and echo 'Reloading fish.'
    and exec fish
end
