from datetime import datetime
from os import path
import json
import random

default = {
    "started": "",
    "queue": [],
    "orangeCap": "",
    "blueCap": "",
    "orangeTeam": [],
    "blueTeam": [],
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


def queueAlreadyPopped(curr_queue: dict):
    if (not curr_queue["orangeCap"] == "" or not curr_queue["blueCap"] == ""):
        print("Captains already chosen. Captains please pick your team.")
        return True
    if (not len(curr_queue["queue"]) == 6):
        print("Queue not full")
        return True
    return False


def listTeams():
    curr_queue: dict = readQueue()

    output = "Blue Team: "
    for player in curr_queue["blueTeam"]:
        output += str(player) + " "

    output += "\nOrange Team: "
    for player in curr_queue["orangeTeam"]:
        output += str(player) + " "

    print(output)


'''
    Commands
'''


def addToQueue(player):
    curr_queue: dict = readQueue()

    if (player in curr_queue["queue"]):
        print("{0} already in queue".format(player))
    else:
        if (len(curr_queue["queue"]) == 0):
            curr_queue["started"] = datetime.now()
        curr_queue["queue"].append(player)
        writeQueue(curr_queue)
        print("{0} added to queue".format(player))


def removeFromQueue(player):
    curr_queue: dict = readQueue()

    if (player in curr_queue["queue"]):
        curr_queue["queue"].remove(player)
        writeQueue(curr_queue)
        print("{0} removed from queue".format(player))
    else:
        print("{0} not in queue".format(player))


def listQueue():
    curr_queue: dict = readQueue()

    output = ""

    for player in curr_queue["queue"]:
        output += str(player) + " "

    print(output)


def randomPop():
    curr_queue: dict = readQueue()

    if (queueAlreadyPopped(curr_queue)):
        return

    curr_queue["orangeTeam"] = random.sample(curr_queue["queue"], 3)

    for player in curr_queue["orangeTeam"]:
        curr_queue["queue"].remove(player)

    curr_queue["blueTeam"] = curr_queue["queue"][:]

    writeQueue(default)

    listTeams()


def captainsPop():
    curr_queue: dict = readQueue()

    if (queueAlreadyPopped(curr_queue)):
        return

    curr_queue["orangeCap"] = random.sample(curr_queue["queue"], 1)[0]
    curr_queue["queue"].remove(curr_queue["orangeCap"])
    curr_queue["orangeTeam"].append(curr_queue["orangeCap"])

    curr_queue["blueCap"] = random.sample(curr_queue["queue"], 1)[0]
    curr_queue["queue"].remove(curr_queue["blueCap"])
    curr_queue["blueTeam"].append(curr_queue["blueCap"])

    print("Orange captain: {0}\nBlue captain: {1}".format(
        curr_queue["orangeCap"], curr_queue["blueCap"]))

    writeQueue(curr_queue)

    print("{0} please pick one person.".format(curr_queue["orangeCap"]))
    print("Players available: ", end="")
    listQueue()


def pick(player_picking, player_picked, player_picked_2=""):
    curr_queue: dict = readQueue()

    if (curr_queue["orangeCap"] == "" or curr_queue["blueCap"] == "" or len(curr_queue["queue"]) == 0):
        print("Captains not assigned")
        return

    if (len(curr_queue["orangeTeam"]) == 1 and player_picking == curr_queue["orangeCap"]):
        if (player_picked in curr_queue["queue"]):
            curr_queue["queue"].remove(player_picked)
            curr_queue["orangeTeam"].append(player_picked)
            print("{0} please pick two people.".format(curr_queue["blueCap"]))
        else:
            print("Player not in queue")
            return

    if (len(curr_queue["orangeTeam"]) == 2 and player_picking == curr_queue["blueCap"]):
        if (player_picked in curr_queue["queue"] and player_picked_2 in curr_queue["queue"]):
            curr_queue["queue"].remove(player_picked)
            curr_queue["queue"].remove(player_picked_2)
            curr_queue["blueTeam"].append(player_picked)
            curr_queue["blueTeam"].append(player_picked_2)

            curr_queue["orangeTeam"].append(curr_queue["queue"].pop(0))
        else:
            print("Player not in queue")
            return

    writeQueue(curr_queue)

    listTeams()

    if (len(curr_queue["queue"]) == 0):
        writeQueue(default)
    else:
        print("Players still available: ", end="")
        listQueue()


def main():
    if not path.exists("queue.json"):
        with open("queue.json", "w") as queue:
            json.dump(default, queue)

    while (1):
        user_input = input("Awaiting command...\n")
        print()

        if ("!q" in user_input):
            command, player = user_input.split()
            addToQueue(player)
        elif ("!leave" in user_input):
            command, player = user_input.split()
            removeFromQueue(player)
        elif ("!list" in user_input):
            listQueue()
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
