from datetime import datetime
from os import path
import json
import random

default = {
    "timeReset": "",
    "queue": [],
    "orangeCap": "",
    "blueCap": "",
    "orangeTeam": [],
    "blueTeam": []
}

'''
    File IO Helpers
'''


def readQueue():
    fileToRead = open("queue.json", "r")
    curr_queue = json.load(fileToRead)
    fileToRead.close()
    return curr_queue


def writeQueue(new_queue):
    with open("queue.json", "w") as queue:
        json.dump(new_queue, queue)


'''
    Utility Functions
'''


def queueAlreadyPopped():
    curr_queue: dict = readQueue()
    return (not curr_queue["orangeCap"] == "" or not curr_queue["blueCap"] == "")


def getQueueLength():
    curr_queue = readQueue()
    return len(curr_queue["queue"])


def isPlayerInQueue(player):
    curr_queue: dict = readQueue()
    return str(player) in curr_queue["queue"]


def getQueueTime():
    curr_queue: dict = readQueue()
    return curr_queue["timeReset"]


def incrementTimer():
    curr_queue: dict = readQueue()
    curr_queue["timeReset"] += 1
    writeQueue(curr_queue)


def clearQueue():
    writeQueue(default)


def checkQueueFile():
    if not path.exists("queue.json"):
        with open("queue.json", "w") as queue:
            json.dump(default, queue)


'''
    Commands
'''


def addToQueue(player):
    curr_queue: dict = readQueue()
    curr_queue["timeReset"] = 0
    curr_queue["queue"].append(str(player))
    writeQueue(curr_queue)


def removeFromQueue(player):
    curr_queue: dict = readQueue()
    curr_queue["queue"].remove(str(player))
    writeQueue(curr_queue)


def getQueueList():
    curr_queue: dict = readQueue()

    playerList = []

    for player in curr_queue["queue"]:
        playerList.append(str(player).split("#")[0])

    return playerList


def randomPop():
    curr_queue: dict = readQueue()

    curr_queue["orangeTeam"] = random.sample(curr_queue["queue"], 3)

    for player in curr_queue["orangeTeam"]:
        curr_queue["queue"].remove(player)

    curr_queue["blueTeam"] = curr_queue["queue"][:]

    writeQueue(default)

    return curr_queue["blueTeam"], curr_queue["orangeTeam"]


def captainsPop():
    curr_queue: dict = readQueue()

    if (not queueAlreadyPopped()):
        curr_queue["orangeCap"] = random.sample(curr_queue["queue"], 1)[0]
        curr_queue["queue"].remove(curr_queue["orangeCap"])
        curr_queue["orangeTeam"].append(curr_queue["orangeCap"])

        curr_queue["blueCap"] = random.sample(curr_queue["queue"], 1)[0]
        curr_queue["queue"].remove(curr_queue["blueCap"])
        curr_queue["blueTeam"].append(curr_queue["blueCap"])

        writeQueue(curr_queue)

    return curr_queue["blueCap"], curr_queue["orangeCap"]


def pick(player_picking: str, player_picked: str, player_picked_2: str = ""):  # Not used in bot
    curr_queue: dict = readQueue()

    if (len(curr_queue["orangeTeam"]) == 1 and player_picking == curr_queue["orangeCap"]):
        curr_queue["queue"].remove(player_picked)
        curr_queue["orangeTeam"].append(player_picked)

    if (len(curr_queue["orangeTeam"]) == 2 and player_picking == curr_queue["blueCap"]):
        curr_queue["queue"].remove(player_picked)
        curr_queue["queue"].remove(player_picked_2)
        curr_queue["blueTeam"].append(player_picked)
        curr_queue["blueTeam"].append(player_picked_2)

        curr_queue["orangeTeam"].append(curr_queue["queue"].pop(0))

    writeQueue(curr_queue)


'''
    Main function for testing
'''


def main():

    while (1):
        user_input = input("Awaiting command...\n")
        print()

        if ("!q" in user_input):
            command, player = user_input.split()
            addToQueue(player)
        elif ("!leave" in user_input):
            command, player = user_input.split()
            removeFromQueue(player)
        elif ("!captains" in user_input):
            captainsPop()
        elif ("!random" in user_input):
            randomPop()
        elif ("!pick" in user_input):
            options = user_input.split()
            options.pop(0)

            curr_queue: dict = readQueue()  # take me out

            if (len(options) == 1):
                pick(curr_queue["orangeCap"], options[0])
            elif (len(options) == 2):
                pick(curr_queue["blueCap"], options[0], options[1])
            else:
                print("Incorrect number of mentions")
        else:
            print("Not a command")


if __name__ == "__main__":
    main()
