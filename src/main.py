import eel
from bot.FilePaths import queueFilePath, tokenPath, activeMatchPath, leaderboardPath, reservesPath
import json
from multiprocessing import Process
from bot.bot import main


NormProcess = None
eel.init("./src/gui")


@eel.expose
def getCurrentQueue():
    fileToRead = open(queueFilePath, "r")
    curr_queue = json.load(fileToRead)
    fileToRead.close()
    return curr_queue


@eel.expose
def setCurrentQueue(newQueue):
    try:
        with open(queueFilePath, "w") as queueFile:
            json.dump(newQueue, queueFile)
    except Exception as e:
        return e

    return "Queue updated."


@eel.expose
def getReserves():
    fileToRead = open(reservesPath, "r")
    reserves = json.load(fileToRead)
    fileToRead.close()
    return reserves


@eel.expose
def setReserves(newReserves):
    try:
        with open(reservesPath, "w") as reservesFile:
            json.dump(newReserves, reservesFile)
    except Exception as e:
        return e

    return "Reserves updated."


@eel.expose
def getActiveMatches():
    fileToRead = open(activeMatchPath, "r")
    matches = json.load(fileToRead)
    fileToRead.close()
    return matches


@eel.expose
def setActiveMatches(newActiveMatches):
    with open(activeMatchPath, "w") as activeMatchFile:
        json.dump(newActiveMatches, activeMatchFile)


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


@eel.expose
def setConfig(newConfig):
    try:
        with open(tokenPath, "w") as config:
            json.dump(newConfig, config)
    except Exception as e:
        return e

    return "Config successfully updated."


@eel.expose
def putNormToSleep():
    global NormProcess

    if (NormProcess and NormProcess.is_alive()):
        NormProcess.kill()

        while (NormProcess.is_alive()):
            pass

        NormProcess.close()
        NormProcess = None


@eel.expose
def startNorm():
    global NormProcess

    putNormToSleep()
    NormProcess = Process(target=main)
    NormProcess.start()


@eel.expose
def checkNormStatus():
    global NormProcess

    if (NormProcess):
        return NormProcess.is_alive()
    else:
        return False


eel.start("index.html", size=(1356, 900))
