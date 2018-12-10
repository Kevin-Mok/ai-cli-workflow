#!/bin/bash

# Backup destination
case $1 in
	nzxt )
		backup_dest="/run/media/example-user/nzxt-backup/"
		;;
	x1 )
		backup_dest="/run/media/example-user/laptop-backup"
		;;
esac
exclude_dirs_list="/home/example/linux-config/txt/exlude-dirs-backup.txt"

# Labels for backup name
distro="arch"
datetime=$(date "+%m.%d-%H.%M")
backup_file="$backup_dest/$datetime-$distro.tar.gz"

sudo tar -czpvf "$backup_file" --exclude-from="$exclude_dirs_list" /
