function backup-phone-pics
    rsync -rave 'ssh -p 8022' 192.0.2.10:/data/data/com.termux/files/home/storage/dcim/Camera /mnt/linux-files/Pictures/pixel
    and rsync -rave 'ssh -p 8022' 192.0.2.10:/data/data/com.termux/files/home/storage/pictures/ /mnt/linux-files/Pictures/pixel/pictures
end
