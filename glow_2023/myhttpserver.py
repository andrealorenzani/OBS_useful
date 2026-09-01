#!/usr/bin/env python3
# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime

# datetime object containing current date and time

hostName = "0.0.0.0"
serverPort = 8998
current_status = '{ "status": "!!! Nessuno status, ancora... !!!", "eng": "!!! No status, by now...!!!", "time": "'+datetime.now().isoformat()+'" }'
start = '{"time":"2023-10-07T16:00:00.000+01:00"}'
longitude = "-0.1345728"
latitude = "51.6155497"
maindir = '/home/andrea/Dropbox/gallery'

class MyServer(BaseHTTPRequestHandler):

    lastSNWTweetId=None
    lastAndreaTweetId=None
    
    def do_GET(self):
        print(self.path)
        from get_handlers import fileHandler
        if fileHandler.getFile(self, self.path) == 1:
            return
        if self.path == "/quotes/img":
            self.send_response(200)
            self.send_header("Content-type", 'image/png')
            self.end_headers()
            f = open("./TwitterQuote.png", "rb")
            self.wfile.write(bytes(f.read()))
            return
        if self.path == "/quotes/retrieve":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            import json
            import os
            quoteList = json.dumps({ 'quotes': self.getQuotes() }) 
            self.wfile.write(bytes(quoteList, "utf-8"))
            return
        if self.path == "/start/when":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            global start
            self.wfile.write(bytes(start, "utf-8"))
            return
        if self.path == "/status/display":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./show_status.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path == "/updeck":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./kill_updeck.log", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        else:
            if self.path == "/favicon.ico":
                self.send_response(200)
                self.send_header("Content-type", 'la nerchia')
                self.end_headers()
                return
            from urllib.parse import unquote
            self.send_response(200)
            self.send_header("Content-type", 'image/jpg')
            self.end_headers()
            import json
            import os
            print("retrieving ({})".format(maindir + unquote(self.path)))
            f = open(maindir + unquote(self.path), 'rb') 
            self.wfile.write(f.read())
    def getQuotes(self):
        # It uses a trick: find the SearchTimeline?variables={...} and copy the curl
        from get_handlers import twitter
        tweet = twitter.getTweetSNW() + twitter.getTweetSNW2023() + twitter.getTweetAndrea()
        import json
        print(json.dumps(tweet))
        return tweet 



    def do_POST(self):
        global current_status, start, longitude, latitude
        import json
        print("POST "+self.path)
        if self.path == "/":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            data = json.loads(post_data.decode('utf-8'))
            longitude = data['longitude']
            latitude = data['latitude']
            current_status = post_data.decode('utf-8')
            print("New status: {}".format(post_data.decode('utf-8')))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({}), "utf-8"))
        if self.path == "/start":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            data = json.loads(post_data.decode('utf-8'))
            start = post_data.decode('utf-8')
            longitude = data['longitude']
            latitude = data['latitude']
            print("New start: {}".format(json.dumps(data)))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({}), "utf-8"))
        if self.path == "/webhook":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            data = json.loads(post_data.decode('utf-8'))
            print("Data received from strava")
            print(data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({}), "utf-8"))

if __name__ == "__main__": 
    import ssl
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    print("Server available at http://supermaestro-uk.duckdns.org:%s" % (serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")