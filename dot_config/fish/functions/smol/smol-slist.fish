function smol-slist
    curl -u (pass show technology/linux/liteshort) \
        -d 'format=json' \
        -d 'api=listshort' \
        https://shortener.example.com | jq .
end
