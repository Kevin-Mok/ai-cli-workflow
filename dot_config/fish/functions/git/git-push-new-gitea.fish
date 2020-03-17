function git-push-new-gitea
    git remote add origin ssh:user@example.invalid:399/example-user/$argv[1].git
    and git push --set-upstream origin master
end
