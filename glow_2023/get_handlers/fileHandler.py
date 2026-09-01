#!/usr/bin/env python3

def getFile(reqHandler, path):
    from get_handlers import sendData
    maindir = '/home/andrea/Dropbox/gallery'
    if path == "/":
        sendData.sendFile(reqHandler, "./update.html")
        return 1
    if path == "/brb":
        sendData.sendFile(reqHandler, "./gallery.html")
        return 1
    if path.startswith("/chat"):
        sendData.sendFile(reqHandler, "./chat.html")
        return 1
    if path.startswith("/countdown"):
        sendData.sendFile(reqHandler, "./show_countdown.html")
        return 1
    if path.startswith("/youtube"):
        sendData.sendFile(reqHandler, "./youtube_player.html")
        return 1
    if path == "/list":
        import os
        sendData.sendString(reqHandler, os.listdir(maindir))
        return 1
    if path == "/quotes":
        sendData.sendFile(reqHandler, "./show_quotes.html")
        return 1
    if path == "/start":
        sendData.sendFile(reqHandler, "./update_start.html", "r")
        return 1
    if path == "/start/how":
        sendData.sendFile(reqHandler, "./show_marathon.html", "r")
        return 1
    if path == "/status/display":
        sendData.sendFile(reqHandler, "./show_status.html", "r")
        return 1
    if path == "/updeck":
        sendData.sendFile(reqHandler, "./kill_updeck.log", "r")
        return 1
    return 0