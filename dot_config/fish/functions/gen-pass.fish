function gen-pass
    if count $argv > /dev/null
        set chars $argv[1]
    else
        set chars 25
    end
    set password (tr -dc '[:alnum:][:punct:]' </dev/urandom | head -c $chars)
    printf '%s' "$password" | xclip -selection clipboard
    echo $password
end
