#!/usr/bin/env python3
# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime

# datetime object containing current date and time

hostName = "0.0.0.0"
serverPort = 8998
current_status = '{ "status": "!!! Nessuno status, ancora... !!!", "eng": "!!! No status, by now...!!!", "time": "'+datetime.now().isoformat()+'" }'
start = '{"time":"2021-09-25T22:05:00.000+01:00"}'
longitude = "-0.1345728"
latitude = "51.6155497"

maindir = '/home/andrea/Dropbox/gallery'

class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./update.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path == "/start":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./update_start.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path == "/start/how":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./show_marathon.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
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
        if self.path == "/status/update":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            global current_status
            self.wfile.write(bytes(current_status, "utf-8"))
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

if __name__ == "__main__": 
    import ssl
    webServer = HTTPServer((hostName, serverPort), MyServer)
    #webServer.socket = ssl.wrap_socket (webServer.socket, certfile='./server.pem', server_side=True)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")