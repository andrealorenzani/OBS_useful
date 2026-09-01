#!/usr/bin/env python3
# https://developers.strava.com/docs/webhookexample/

def checkToken(reqHandler, req):
	if req.startswith("/webhook"):
	    verify_token = "andrea_the_best"
	    print(req)
	    print(urlparse.urlparse(req).query)
	    queryParam = urlparse.parse_qs(urlparse.urlparse(req).query)
	    print(queryParam)
	    mode = queryParam.get('hub.mode', None)
	    token = queryParam.get('hub.verify_token', None)
	    challenge = queryParam.get('hub.challenge', None)
	    print("Mode: %s - Token: %s - Challenge: %s" % (mode, token, challenge))
	    if mode and token:
	        if mode == 'subscribe' and token == verify_token:
	            from get_handlers import sendData
	            sendData.sendString(reqHandler, "{\"hub.challenge\": \"%s\"}" % challenge)
	            print("Token verified!!!")
	        else: 
	            reqHandler.send_response(403)
	            reqHandler.end_headers()
	            print("Token rejected!!!")
	    return 1
	return 0