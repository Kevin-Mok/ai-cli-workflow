function certbot-ssl
	set domain_args ""
	for domain in $argv
		set -a domain_args "-d" $domain
	end
	echo sudo certbot certonly --manual --preferred-challenges=dns \
	--email user@example.invalid --server https://service.example.com/directory \
	--agree-tos $domain_args
end
