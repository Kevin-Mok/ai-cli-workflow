function git-push-new-gitea
    git remote add gitea user@example.invalid:example-user/$argv[1].git
    and git push --set-upstream gitea master
end
