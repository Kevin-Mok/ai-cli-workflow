function refresh-config-task
    set codex_source_path (chezmoi source-path ~/.codex/config.toml)
    and cp ~/.codex/config.toml $codex_source_path
    and cli-message 📋 'Copied local Codex config into repo source.'
    chezmoi apply
    and cli-message ✅ 'Applied chezmoi.'
    # and tmux source-file ~/.tmux.conf
    # and echo 'Sourced tmux config.'

    sync-shortcuts
    cli-message ✅ 'Synced shortcuts.'
    source ~/.config/fish/key_abbr.fish > /dev/null
    and cli-message ✅ 'Sourced shortcuts.'
    and cli-message 🔄 'Reloading fish.'
end
