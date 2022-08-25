#!/bin/bash
device_file="/dev/sdc1"
if [ -e "$device_file" ]
then
    echo "Mounting device"
    sudo mount /dev/sdc1 ~/ruizu_player -o umask=000
    echo "rsyncing"
    rsync -rv /home/ubuntu/music/ /home/ubuntu/ruizu_player/
fi
