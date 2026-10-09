function git-log-short
    set -l cue '📝 '
    if set -q CLI_PLAIN; and test "$CLI_PLAIN" = 1
        set cue ''
    end
    git log --pretty="$cue%C(Yellow)%h  %C(reset)%ad (%C(Green)%cr%C(reset))%x09 %C(Cyan)%an: %C(reset)%s"
end
