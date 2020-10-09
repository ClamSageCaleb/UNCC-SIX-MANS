from DataFiles import currQueue
from Types import BallChaser, Team, BallChaserKey
from datetime import datetime, timedelta
from discord import Role, Member
from math import ceil
import random
from tinydb import where
from tinydb.table import Document
from typing import Tuple, List


'''
    Utility Functions
'''


def isBotAdmin(roles: List[Role]) -> bool:
    return any(role.name == "Bot Admin" for role in roles)


def queueAlreadyPopped() -> bool:
    return currQueue.contains(where(BallChaserKey.IS_CAP) == True)


def getQueueLength() -> int:
    return currQueue.count(where(BallChaserKey.ID).exists())


def isPlayerInQueue(player: Member) -> bool:
    return currQueue.contains(where(BallChaserKey.ID) == player.id)


def clearQueue() -> None:
    currQueue.truncate()


def validateOrangePick(player: Member) -> bool:
    player = currQueue.get(doc_id=player.id)
    return (
        currQueue.count(where(BallChaserKey.TEAM) == Team.BLUE) == 2 and
        player[BallChaserKey.IS_CAP] and
        player[BallChaserKey.TEAM] == Team.ORANGE
    )


def validateBluePick(player: Member) -> bool:
    player = currQueue.get(doc_id=player.id)
    return (
        currQueue.count(where(BallChaserKey.TEAM) == Team.BLUE) == 1 and
        player[BallChaserKey.IS_CAP] and
        player[BallChaserKey.TEAM] == Team.BLUE
    )


def getTeamList() -> Tuple[List[BallChaser], List[BallChaser]]:
    orangeTeam = currQueue.search(where(BallChaserKey.TEAM) == Team.ORANGE)
    blueTeam = currQueue.search(where(BallChaserKey.TEAM) == Team.BLUE)
    return [BallChaser.fromDocument(p) for p in blueTeam], [BallChaser.fromDocument(p) for p in orangeTeam]


def getQueueTimeRemaining(player: BallChaser) -> int:
    return ceil((player.queueTime - datetime.now()).seconds / 60)


'''
    Commands
'''


def addToQueue(player: Member, mins_to_queue_for: int = 60) -> None:
    new_player = BallChaser(
        str(player),
        player.id,
        queueTime=(datetime.now() + timedelta(minutes=mins_to_queue_for))
    )
    currQueue.insert(Document(new_player.toJSON(), doc_id=new_player.id))


def removeFromQueue(player: Member) -> None:
    currQueue.remove(doc_ids=[player.id])


def resetPlayerQueueTime(player: Member, mins_to_queue_for: int = 60) -> None:
    removeFromQueue(player)
    addToQueue(player, mins_to_queue_for)


def getQueueList(mentionPlayers: bool = False, includeTimes: bool = True, separator: str = "\n") -> str:
    playerList = []

    for player in currQueue.search(where(BallChaserKey.TEAM) == None):
        player = BallChaser.fromDocument(player)
        if (mentionPlayers):
            playerList.append(player.mention)
        else:
            player_name = player.name.split("#")[0]
            if (includeTimes):
                minutes_diff = getQueueTimeRemaining(player)
                player_name += " (" + str(minutes_diff) + " mins)"
            playerList.append(player_name)

    return separator.join(playerList)


def randomPop() -> Tuple[List[BallChaser], List[BallChaser]]:
    players = [BallChaser.fromDocument(p) for p in currQueue.all()]
    orangeTeam = random.sample(players, 3)

    for player in orangeTeam:
        player.team = Team.ORANGE
        players.remove(player)

    blueTeam = players[:]
    currQueue.truncate()

    for player in blueTeam:
        player.team = Team.BLUE

    return blueTeam, orangeTeam


def captainsPop() -> Tuple[List[BallChaser], List[BallChaser]]:
    if (not queueAlreadyPopped()):
        orangeCapDoc = random.sample(currQueue.all(), 1)[0]
        orangeCap = BallChaser.fromDocument(orangeCapDoc)
        currQueue.update({BallChaserKey.IS_CAP: True, BallChaserKey.TEAM: Team.ORANGE}, doc_ids=[orangeCapDoc.doc_id])

        blueCapDoc = random.choice(currQueue.search(where(BallChaserKey.IS_CAP) == False))
        blueCap = BallChaser.fromDocument(blueCapDoc)
        currQueue.update({BallChaserKey.IS_CAP: True, BallChaserKey.TEAM: Team.BLUE}, doc_ids=[blueCapDoc.doc_id])
    else:
        orangeCap = BallChaser.fromDocument(
            currQueue.get((where(BallChaserKey.TEAM) == Team.ORANGE) & (where(BallChaserKey.IS_CAP) == True))
        )
        blueCap = BallChaser.fromDocument(
            currQueue.get((where(BallChaserKey.TEAM) == Team.BLUE) & (where(BallChaserKey.IS_CAP) == True))
        )

    return blueCap, orangeCap


# Returns a string if there is an error. Otherwise returns an empty string
def pick(player_picked: Member, player_picked_2: Member = None) -> str:
    playerPickedDoc = currQueue.get(doc_id=player_picked.id)
    secondPlayerPickedDoc = None

    if (player_picked_2 is not None):
        secondPlayerPickedDoc = currQueue.get(doc_id=player_picked_2.id)

    if (playerPickedDoc is not None):
        if (playerPickedDoc[BallChaserKey.TEAM] is not None):
            return "<@{0}> has already been picked. Pick someone else 4head.".format(playerPickedDoc[BallChaserKey.ID])
        if (secondPlayerPickedDoc is not None and secondPlayerPickedDoc[BallChaserKey.TEAM] is not None):
            return ("<@{0}> has already been picked."
                    " Pick someone else 4head. Pick reset.".format(secondPlayerPickedDoc[BallChaserKey.ID]))
        if (player_picked_2):
            currQueue.update({BallChaserKey.TEAM: Team.ORANGE}, doc_ids=[playerPickedDoc.doc_id])
        else:
            currQueue.update({BallChaserKey.TEAM: Team.BLUE}, doc_ids=[playerPickedDoc.doc_id])
    else:
        return "Player not in queue, dummy. Try again."

    if (player_picked_2 is not None):
        if (secondPlayerPickedDoc is not None):
            currQueue.update({BallChaserKey.TEAM: Team.ORANGE}, doc_ids=[secondPlayerPickedDoc.doc_id])

            currQueue.update({BallChaserKey.TEAM: Team.BLUE}, where(BallChaserKey.TEAM) == None)
        else:
            return "{0} is not in the queue. Try again.".format(player_picked_2.name)

    return ""


def checkQueueTimes() -> Tuple[List[BallChaser], List[BallChaser]]:
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
