function refresh-config
    snapshot-codex-config
    or return $status
    and echo 'Copied local Codex config into repo source.'
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
