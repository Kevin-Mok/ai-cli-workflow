function git-push-new-gitea
    git remote add $argv[1] ssh:user@example.invalid:399/example-user/$argv[2].git
    and git push --set-upstream $argv[1] master
end
