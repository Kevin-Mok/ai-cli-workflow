function git-replace-origin-gitea
    git remote remove origin
    and git remote add origin ssh:user@example.invalid:399/example-user/$argv[1].git
    and git branch --set-upstream-to=origin/master master
    and git push
end
