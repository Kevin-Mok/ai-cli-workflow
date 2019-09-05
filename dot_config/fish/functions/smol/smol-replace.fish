function smol-replace
    curl -u (pass show technology/linux/liteshort) \
        -d 'format=json' \
        -d 'api=delete' \
        -d "long=$argv[1]" \
        https://shortener.example.com | jq .
    and curl -d 'format=json' \
        -d "long=$argv[1]" \
        -d "short=$argv[2]" \
        https://shortener.example.com | jq .
end
