from datetime import datetime
from os import path
import json
import random

default = {
    "timeReset": 0,
    "queue": [],
    "orangeCap": "",
    "blueCap": "",
    "orangeTeam": [],
    "blueTeam": []
}

queueFilePath = "./data/queue.json"


class BallChaser:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.mention = "<@{0}>".format(self.id)

    def toJSON(self):
        return {
            "name": self.name,
            "id": self.id
        }


'''
    File IO Helpers
'''


def readQueue():
    fileToRead = open(queueFilePath, "r")
    curr_queue = json.load(fileToRead)
    fileToRead.close()

    for key in curr_queue:

        if (type(curr_queue[key]) == list):
            tempChasers = []
            for player in curr_queue[key]:
                tempChasers.append(BallChaser(player["name"], player["id"]))

        elif (type(curr_queue[key]) == dict):
            tempChasers = BallChaser(curr_queue[key]["name"], curr_queue[key]["id"])

        else:
            tempChasers = curr_queue[key]

        curr_queue[key] = tempChasers

    return curr_queue


def writeQueue(new_queue):

    for key in new_queue:

        if (type(new_queue[key]) == list):
            tempChasers = []
            for player in new_queue[key]:
                tempChasers.append(player.toJSON())

        elif (type(new_queue[key]) == BallChaser):
            tempChasers = new_queue[key].toJSON()

        else:
            tempChasers = new_queue[key]

        new_queue[key] = tempChasers

    with open(queueFilePath, "w") as queue:
        json.dump(new_queue, queue)


'''
    Utility Functions
'''


def indexOfPlayer(player, curr_queue = None):
    if (not curr_queue):
        curr_queue = readQueue()

    for i, ballchaser in enumerate(curr_queue["queue"]):
        if (ballchaser.id == player.id):
            return i
    
    return -1


def queueAlreadyPopped():
    curr_queue = readQueue()
    return (not curr_queue["orangeCap"] == "" or not curr_queue["blueCap"] == "")


def getQueueLength():
    curr_queue = readQueue()
    return len(curr_queue["queue"])


def isPlayerInQueue(player):
    return indexOfPlayer(player) != -1


def getQueueTime():
    curr_queue = readQueue()
    return curr_queue["timeReset"]


def incrementTimer():
    curr_queue = readQueue()
    curr_queue["timeReset"] += 1
    writeQueue(curr_queue)


def clearQueue():
    writeQueue(default)


def checkQueueFile():
    if not path.exists(queueFilePath):
        with open(queueFilePath, "w") as queue:
            json.dump(default, queue)


def validateOrangePick(player):
    curr_queue = readQueue()
    return (len(curr_queue["orangeTeam"]) == 1 and player.id == curr_queue["orangeCap"].id)


def validateBluePick(player):
    curr_queue = readQueue()
    return (len(curr_queue["orangeTeam"]) == 2 and player.id == curr_queue["blueCap"].id)


def getTeamList():
    curr_queue = readQueue()
    return curr_queue["blueTeam"], curr_queue["orangeTeam"]


'''
    Commands
'''


def addToQueue(player):
    curr_queue = readQueue()
    curr_queue["timeReset"] = 0
    new_player = BallChaser(str(player), player.id)
    curr_queue["queue"].append(new_player)
    writeQueue(curr_queue)


def removeFromQueue(player):
    curr_queue = readQueue()
    index = indexOfPlayer(player)

    if (index != -1):
        curr_queue["queue"].pop(index)
        writeQueue(curr_queue)


def getQueueList():
    curr_queue = readQueue()
    playerList = []

    for player in curr_queue["queue"]:
        playerList.append(player.name.split("#")[0])

    return ", ".join(playerList)


def randomPop():
    curr_queue = readQueue()

    curr_queue["orangeTeam"] = random.sample(curr_queue["queue"], 3)

    for player in curr_queue["orangeTeam"]:
        curr_queue["queue"].remove(player)

    curr_queue["blueTeam"] = curr_queue["queue"][:]

    writeQueue(default)

    return curr_queue["blueTeam"], curr_queue["orangeTeam"]


def captainsPop():
    curr_queue = readQueue()

    if (not queueAlreadyPopped()):
        orangeCap = curr_queue["orangeCap"] = random.sample(curr_queue["queue"], 1)[0]
        curr_queue["queue"].remove(curr_queue["orangeCap"])
        curr_queue["orangeTeam"].append(curr_queue["orangeCap"])

        blueCap = curr_queue["blueCap"] = random.sample(curr_queue["queue"], 1)[0]
        curr_queue["queue"].remove(curr_queue["blueCap"])
        curr_queue["blueTeam"].append(curr_queue["blueCap"])

        writeQueue(curr_queue)
    else:
        orangeCap = curr_queue["orangeCap"]
        blueCap = curr_queue["blueCap"]

    return blueCap, orangeCap

# Returns a string if there is an error. Otherwise returns an empty string
def pick(player_picked, player_picked_2 = None):
    curr_queue = readQueue()

    player_picked = BallChaser(str(player_picked), player_picked.id)

    if (isPlayerInQueue(player_picked)):
        curr_queue["queue"].pop(indexOfPlayer(player_picked))
        curr_queue["orangeTeam"].append(player_picked)
    else:
        return "Player not in queue, dummy. Try again."

    if (player_picked_2):

        player_picked_2 = BallChaser(str(player_picked_2), player_picked_2.id)

        if (isPlayerInQueue(player_picked_2)):
            curr_queue["queue"].pop(indexOfPlayer(player_picked_2, curr_queue))
            curr_queue["blueTeam"].append(player_picked_2)

            curr_queue["orangeTeam"].append(curr_queue["queue"].pop(0))
        else:
            return "{0} is not in the queue. Try again".format(player_picked_2.name)

    writeQueue(curr_queue)
    return ""


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

            curr_queue = readQueue()  # take me out

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
