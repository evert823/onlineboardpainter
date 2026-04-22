#!/bin/bash
echo "clean_useroutput.sh run at $(date)" >> /home/administrator/onlineboardpainter/useroutput/clean_useroutput.log

#clean /home/administrator/onlineboardpainter/useroutput/json
find /home/administrator/onlineboardpainter/useroutput/json -maxdepth 1 -type f -name 'usr_pos_*.json' -mtime +7 -exec rm {} \;
#clean /home/administrator/onlineboardpainter/useroutput/boardimages
find /home/administrator/onlineboardpainter/useroutput/boardimages -maxdepth 1 -type f -name 'usr_pos_*.png' -mtime +7 -exec rm {} \;
