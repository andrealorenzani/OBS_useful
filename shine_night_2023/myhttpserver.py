#!/usr/bin/env python3
# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime

# datetime object containing current date and time

hostName = "0.0.0.0"
serverPort = 8998
current_status = '{ "status": "!!! Nessuno status, ancora... !!!", "eng": "!!! No status, by now...!!!", "time": "'+datetime.now().isoformat()+'" }'
start = '{"time":"2022-09-24T20:00:00.000+01:00"}'
longitude = "-0.1345728"
latitude = "51.6155497"

maindir = '/home/andrea/Dropbox/gallery'

class MyServer(BaseHTTPRequestHandler):

    lastSNWTweetId=None
    lastAndreaTweetId=None
    
    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./update.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path == "/brb":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./gallery.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path.startswith("/chat"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./chat.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path.startswith("/countdown"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./show_countdown.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path.startswith("/youtube"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./youtube_player.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
            return
        if self.path == "/list":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            import json
            import os
            fileList = json.dumps(os.listdir(maindir)) 
            self.wfile.write(bytes(fileList, "utf-8"))
            return
        if self.path == "/quotes":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("./show_quotes.html", "r")
            self.wfile.write(bytes(f.read(), "utf-8"))
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
        if self.path == "/quotes/img":
            self.send_response(200)
            self.send_header("Content-type", 'image/png')
            self.end_headers()
            f = open("./TwitterQuote.png", "rb")
            self.wfile.write(bytes(f.read()))
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
    def getQuotes(self):
        def retrieveTweet(api, query, value):
            if(value):
                print("Retrieve since " + str(value))
                return api.search_tweets(query, result_type="recent", since_id=value, count=100)
            else:
                print("Retrieve everything")
                return api.search_tweets(query, result_type="recent")

        def getTweetById(api, ids, name=None):
            result = []
            if(len(ids) > 0):
                print("Lookup "+",".join(ids))
                for twid in ids:
                    tweet = api.get_status(twid, tweet_mode="extended")
                    result.append( {'quote':extract_text(tweet), 'author':(name if name else tweet.user.screen_name)} )
                #for tweet in api.lookup_statuses(ids):
                #    print(tweet)
                #    result.append( {'quote':extract_text(tweet), 'author':(name if name else tweet.user.screen_name)} )
            import json
            print(json.dumps(result))
            return result;

        def extract_text(status):
            try:
                return status.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                return status.full_text


        API_KEY="TCMd0uvTHErAvtghuhC4VExee"
        API_SECRET_KEY="0HNK6Kjit8fTgRIcj4HpmyeHU3QJh4e9UFBS1fIBgmRTIzlqM2"

        ACCESS_TOKEN="1237879421618606080-UxkSeEBAesucdcQ00Wlh1xw9QBKZ5v"
        ACCESS_TOKEN_SECRET="1CpkWeuVbPagW3MNE24KZ1s1Q6NoYkOS67nswOmfIAA6N"
        import tweepy
        import json
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        if api.verify_credentials():
            print("Authentication OK")
        else:
            print("Error during authentication")
            return []
        result = []
        truncated = []
        for tweet in retrieveTweet(api, "#AndreaSNW2022", MyServer.lastAndreaTweetId):
            #params = {'id': tweet.id, 'text': , 'user_id': tweet.user.id, 'user': tweet.user.screen_name, 'user_name': tweet.user.name, 'followers': tweet.user.followers_count}
            MyServer.lastAndreaTweetId = MyServer.lastAndreaTweetId if MyServer.lastAndreaTweetId and MyServer.lastAndreaTweetId > tweet.id else tweet.id
            truncated.append(str(tweet.id))
        result = getTweetById(api, truncated)
        truncated = []
        for tweet in retrieveTweet(api, "#shinenightwalk OR #shinewalk", MyServer.lastSNWTweetId):
            MyServer.lastSNWTweetId = MyServer.lastSNWTweetId if MyServer.lastSNWTweetId and MyServer.lastSNWTweetId > tweet.id else tweet.id
            truncated.append(str(tweet.id))
        return result + getTweetById(api, truncated, "Anonymous")

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