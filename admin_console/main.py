import eel
from FilePaths import queueFilePath, tokenPath, activeMatchPath, leaderboardPath
import json

eel.init("gui")


@eel.expose
def getCurrentQueue():
    fileToRead = open(queueFilePath, "r")
    curr_queue = json.load(fileToRead)
    fileToRead.close()
    return curr_queue


@eel.expose
def getActiveMatches():
    fileToRead = open(activeMatchPath, "r")
    matches = json.load(fileToRead)
    fileToRead.close()
    return matches


@eel.expose
def getLeaderboard():
    fileToRead = open(leaderboardPath, "r")
    ldrbrd = json.load(fileToRead)
    fileToRead.close()
    return ldrbrd


@eel.expose
def getConfig():
    fileToRead = open(tokenPath, "r")
    config = json.load(fileToRead)
    fileToRead.close()
    return config


eel.start("index.html", size=(1356, 900))
