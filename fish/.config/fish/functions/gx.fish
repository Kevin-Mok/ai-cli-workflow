function gx
	set key_aliases /home/example/linux-config/aliases/key_aliases
	grep $argv[1] $key_aliases 
end
