#!/usr/bin/env bash

./myhttpserver.py >>myhttpserver_history.log 2>&1 &
echo "My http server started"

sudo ufw disable & sudo ufw status
echo "Firewall disabled"

love ~/Downloads/UPDeck_2-1-19.love &
echo "Updeck running"
