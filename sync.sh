#!/bin/bash
while inotifywait -r -e modify,create,delete,move /home/ubuntu/music; do
    rsync -r /home/ubuntu/music/ /home/ubuntu/ruizu_player/
done
