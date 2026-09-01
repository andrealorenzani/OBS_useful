#!/usr/bin/python3
import os, sys, json
headers={}
def extractData():
    import sys, json
    try:
        return json.load(sys.stdin)
    except:
        return None
rawPostData=extractData()
def setHeaders(status=200):
    global headers
    global rawPostData
    print('Status: {}'.format(status))
    print("x-raw-header-qs: {}".format(os.environ.get("QUERY_STRING")))
    if rawPostData:
        print("x-raw-header-data: {}".format(json.dumps(rawPostData)))
    for k, v in headers.items():
        print("x-raw-header-{}: {}".format(k, v))
    print('Content-Type: application/json\n')
def respond(response, status=200):
    import json 
    setHeaders(status)
    print(response)
def sendData(data):
    try:
        import requests
        api_url = "https://supermaestro-uk.duckdns.org:8998/webhook"
        response = requests.post(api_url, json=data)
    except Exception as error:
        print("x-request-status: fail ", error)
    respond(data) 
if os.environ.get("QUERY_STRING", None):
    query_string = os.environ.get("QUERY_STRING")
    queryParamRaw = [i.split('=') for i in query_string.split('&')]
    queryParam = {}
    for key, value in queryParamRaw:
        queryParam[key] = value
        headers[key] = value
    mode = queryParam.get('hub.mode', None)
    token = queryParam.get('hub.verify_token', None)
    challenge = queryParam.get('hub.challenge', None)
    if mode and token:
        if mode == 'subscribe' and token == "REDACTED":
            sendData("{\"hub.challenge\": \"%s\"}\n\n" % challenge)
        else: 
            respond(None, 403)
else:
    respond(None, 204)