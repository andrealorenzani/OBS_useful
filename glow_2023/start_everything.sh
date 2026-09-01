#!/usr/bin/env bash

echo url="https://www.duckdns.org/update?domains=supermaestro-uk&token=882edcb4-9028-4a81-9170-20d7a0939941&ip=" | curl -k -K -
echo "Updated the dns"
echo "https://supermaestro-uk.duckdns.org:8998"
echo "Reverse proxy setting at cat /etc/nginx/sites-enabled/reverse-proxy.conf"
echo "Reverse proxy log at cat /var/log/nginx"

./myhttpserver.py >>myhttpserver_history.log 2>&1 &
SERVER_PID=$(echo $!)
echo "My http server started ($SERVER_PID) at $SERVER_PID"

sudo ufw disable & sudo ufw status
echo "Firewall disabled"

curl -X POST \
  https://www.strava.com/api/v3/push_subscriptions \
  -F client_id=113946 \
  -F client_secret=78aefe25da3026396d2e4691055905c00ae26730 \
  -F callback_url=https://supermaestro-uk.ddns.net/webhook \
  -F verify_token=andrea_the_best
echo "Subscription to strava webhook"

while true; do
    if ps -p $SERVER_PID > /dev/null
	then
	   echo "My http server still running at $SERVER_PID"
	else
		kill -9 $SERVER_PID
		./myhttpserver.py >>myhttpserver_history.log 2>&1 &
		SERVER_PID=$(echo $!)
		echo "My http server restarted ($SERVER_PID) at $(date)"
	fi
    echo "Starting updeck"
	love ~/Downloads/UPDeck_2-1-19.love &
	PROCESS=$(echo $!)
	echo "Killing updeck at $PROCESS at $(date -d '+30 minutes')" > kill_updeck.log
	cat kill_updeck.log
	sleep 30m
	kill -9 $PROCESS
	echo "Updeck killed at $(date)"
done