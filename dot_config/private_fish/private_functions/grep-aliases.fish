function grep-aliases
	set key_aliases /home/example/linux-config/aliases/key_aliases
	rg $argv[1] $key_aliases
	# rg "^$argv[1]" $key_aliases
end
