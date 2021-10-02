#!/usr/bin/env bash

echo url="https://www.duckdns.org/update?domains=supermaestro-uk&token=REDACTED&ip=" | curl -k -K -
echo "Updated the dns"

./myhttpserver.py >>myhttpserver_history.log 2>&1 &
echo "My http server started"

sudo ufw disable & sudo ufw status
echo "Firewall disabled"

love ~/Downloads/UPDeck_2-1-19.love &
echo "Updeck running"
