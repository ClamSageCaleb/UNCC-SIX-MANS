from FilePaths import tokenPath, currQueue
import json
import random
from datetime import datetime, timedelta
from math import ceil
from tinydb import where


class BallChaser:
    def __init__(self, name: str, id: int, isCap: bool = False, team=None, queueTime=datetime.now()):
        self.name = name
        self.id = id
        self.mention = "<@{0}>".format(self.id)
        self.isCap = isCap
        self.team = team
        self.queueTime = queueTime

    @classmethod
    def fromDocument(cls, document):
        return cls(
            id=document["id"],
            name=document["name"],
            isCap=document["isCap"],
            team=document["team"],
            queueTime=datetime.strptime(document["queueTime"], "%Y-%m-%dT%H:%M:%S.%f")
        )

    def toJSON(self, short: bool = False):
        return {
            "id": self.id,
            "name": self.name,
            "isCap": self.isCap,
            "team": self.team,
            "queueTime": self.queueTime.isoformat(),
        } if not short else {
            "id": self.id,
            "name": self.name,
            "team": self.team
        }

    def isPlayerInList(self, listOfBallChasers: list) -> bool:
        return any(self.id == chaser["id"] for chaser in listOfBallChasers)


'''
    Utility Functions
'''


def isBotAdmin(roles):
    return any(role.name == "Bot Admin" for role in roles)


def queueAlreadyPopped():
    return currQueue.contains(where("isCap").one_of([True]))


def getQueueLength():
    return currQueue.count(where("id").exists())


def isPlayerInQueue(player):
    return currQueue.contains(where("id") == player.id)


def clearQueue():
    currQueue.truncate()


def getDiscordToken():
    with open(tokenPath, "r") as config:
        token = json.load(config)["token"]

    return token


def updateDiscordToken(newToken):
    with open(tokenPath, "w") as config:
        configFile = {
            "token": newToken
        }
        json.dump(configFile, config)

    return newToken


def validateOrangePick(player: BallChaser):
    player = currQueue.get(where("id") == player.id)
    return (
        currQueue.count(where("team") == "blue") == 2 and
        player["isCap"] and
        player["team"] == "orange"
    )


def validateBluePick(player):
    player = currQueue.get(where("id") == player.id)
    return (
        currQueue.count(where("team") == "blue") == 1 and
        player["isCap"] and
        player["team"] == "blue"
    )


def getTeamList():
    orangeTeam = currQueue.search(where("team") == "orange")
    blueTeam = currQueue.search(where("team") == "blue")
    return [BallChaser.fromDocument(p) for p in blueTeam], [BallChaser.fromDocument(p) for p in orangeTeam]


def getQueueTimeRemaining(player: BallChaser) -> int:
    return ceil((player.queueTime - datetime.now()).seconds / 60)


'''
    Commands
'''


def addToQueue(player, mins_to_queue_for=60):
    new_player = BallChaser(
        str(player),
        player.id,
        queueTime=(datetime.now() + timedelta(minutes=mins_to_queue_for))
    )
    currQueue.insert(new_player.toJSON())


def removeFromQueue(player):
    currQueue.remove(where("id") == player.id)


def resetPlayerQueueTime(player, mins_to_queue_for=60):
    removeFromQueue(player)
    addToQueue(player, mins_to_queue_for)


def getQueueList(mentionPlayers: bool = False, includeTimes: bool = True):
    playerList = []

    for player in currQueue.search(where("team").one_of([None])):
        player = BallChaser.fromDocument(player)
        if (mentionPlayers):
            playerList.append(player.mention)
        else:
            player_name = player.name.split("#")[0]
            if (includeTimes):
                minutes_diff = getQueueTimeRemaining(player)
                player_name += " (" + str(minutes_diff) + " mins)"
            playerList.append(player_name)

    return ", ".join(playerList)


def randomPop():
    players = [BallChaser.fromDocument(p) for p in currQueue.all()]
    orangeTeam = random.sample(players, 3)

    for player in orangeTeam:
        player.team = "orange"
        players.remove(player)

    blueTeam = players[:]
    currQueue.truncate()

    for player in blueTeam:
        player.team = "blue"

    return blueTeam, orangeTeam


def captainsPop():
    if (not queueAlreadyPopped()):
        orangeCapDoc = random.sample(currQueue.all(), 1)[0]
        orangeCap = BallChaser.fromDocument(orangeCapDoc)
        currQueue.update({"isCap": True, "team": "orange"}, doc_ids=[orangeCapDoc.doc_id])

        blueCapDoc = random.sample(currQueue.search(where("isCap").one_of([False])), 1)[0]
        blueCap = BallChaser.fromDocument(blueCapDoc)
        currQueue.update({"isCap": True, "team": "blue"}, doc_ids=[blueCapDoc.doc_id])
    else:
        orangeCap = BallChaser.fromDocument(
            currQueue.get((where("team") == "orange") & (where("isCap").one_of([True])))
        )
        blueCap = BallChaser.fromDocument(
            currQueue.get((where("team") == "blue") & (where("isCap").one_of([True])))
        )

    return blueCap, orangeCap


# Returns a string if there is an error. Otherwise returns an empty string
def pick(player_picked, player_picked_2=None):
    player_picked = currQueue.get(where("id") == player_picked.id)

    if (player_picked is not None):
        if (player_picked_2):
            currQueue.update({"team": "orange"}, doc_ids=[player_picked.doc_id])
        else:
            currQueue.update({"team": "blue"}, doc_ids=[player_picked.doc_id])
    else:
        return "Player not in queue, dummy. Try again."

    if (player_picked_2 is not None):
        player_picked_2 = currQueue.get(where("id") == player_picked_2.id)

        if (player_picked_2):
            currQueue.update({"team": "orange"}, doc_ids=[player_picked_2.doc_id])

            currQueue.update({"team": "blue"}, where("team").one_of([None]))
        else:
            return "{0} is not in the queue. Try again.".format(player_picked_2.name)

    return ""


def checkQueueTimes():
    warn_players = []
    remove_players = []

    for player in currQueue.all():
        player = BallChaser.fromDocument(player)
        minutes_diff = getQueueTimeRemaining(player)
        if (minutes_diff == 5):  # 5 minute warning
            warn_players.append(player)
        elif (minutes_diff > 60):  # There is no negative time, it just overflows to like 1430
            removeFromQueue(player)
            remove_players.append(player)

    return warn_players, remove_players
