function smol-add
    if test (count $argv) -eq 2
        curl -d 'format=json' \
            -d "long=$argv[1]" \
            -d "short=$argv[2]" \
            https://shortener.example.com | jq .
    else
        curl -d 'format=json' -d "long=$argv[1]" https://shortener.example.com | jq .
    end
end
