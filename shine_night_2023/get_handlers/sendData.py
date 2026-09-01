#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler

def sendFile(reqHandler, path, contentType="text/html", isUtf8=True):
    print("Sending %s" % path)
    reqHandler.send_response(200)
    reqHandler.send_header("Content-type", contentType)
    reqHandler.end_headers()
    f = open(path, "r")
    if isUtf8:
        reqHandler.wfile.write(bytes(f.read(), "utf-8"))
    else:
        reqHandler.wfile.write(bytes(f.read()))
    return

def sendString(reqHandler, data):
    reqHandler.send_response(200)
    reqHandler.send_header("Content-type", "application/json")
    reqHandler.end_headers()
    import json
    import os
    jsonData = json.dumps(data) 
    reqHandler.wfile.write(bytes(jsonData, "utf-8"))