function cli-message --description 'Print a human-facing message with an optional emoji cue'
    # Keep raw data and command output outside this presentation helper.
    set -l message (string join ' ' -- $argv[2..])
    if set -q CLI_PLAIN; and test "$CLI_PLAIN" = 1
        printf '%s\n' "$message"
    else
        printf '%s %s\n' "$argv[1]" "$message"
    end
end
