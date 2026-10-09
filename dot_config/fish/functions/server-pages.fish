function server-pages
    set sites example-user-mok.com git.example-user-mok.com calendar.example.invalid mnpd.gq/kbg pste.gq shortener.example.com twem.tk
    set titles "example-user Mok" "example-user Mok's Gitea" "BaÃ¯kal server" "kbg" "hastebin" "example-user's URL Shortener" "Twitch Emote Links"
    # set sites twem.tk
    # set titles "Twitch Emote Links"

    for i in (seq (count $sites))
        set title (wget -qO- "$sites[$i]" | perl -l -0777 -ne 'print $1 if /<title.*?>\s*(.*?)\s*<\/title/si' | recode html)
        if test $title = $titles[$i]
            set symbol "✅"
            set label OK
        else
            set symbol "❌"
            set label FAIL
        end
        cli-message "$symbol" "[$label] $sites[$i]"
    end
end

