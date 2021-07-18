from DataFiles import currQueue
from Types import BallChaser, Team, BallChaserKey
from datetime import datetime, timedelta
from discord import Role, Member
from math import ceil
import random
from tinydb import where
from tinydb.table import Document
from typing import Tuple, List, Union
import Leaderboard


'''
    Utility Functions
'''


def isBotAdmin(roles: List[Role]) -> bool:
    return any(role.name == "Bot Admin" for role in roles)


def queueAlreadyPopped() -> bool:
    return currQueue.contains(where(BallChaserKey.IS_CAP) == True)


def getQueueLength() -> int:
    return currQueue.count(where(BallChaserKey.ID).exists())


def isPlayerInQueue(player: Union[Member, str]) -> bool:
    if (isinstance(player, Member)):
        return currQueue.contains(where(BallChaserKey.ID) == player.id)
    elif (isinstance(player, str)):
        return currQueue.contains(where(BallChaserKey.ID) == currQueue.get(doc_id=int(player))["id"])


def getPlayerFromQueue(player: str) -> Union[BallChaser, None]:
    return currQueue.get(doc_id=int(player))


def clearQueue() -> None:
    currQueue.truncate()


def validateOrangePick(player: Member) -> bool:
    player = currQueue.get(doc_id=player.id)
    if (player is not None):
        return (
            currQueue.count(where(BallChaserKey.TEAM) == Team.BLUE) == 2 and
            player[BallChaserKey.IS_CAP] and
            player[BallChaserKey.TEAM] == Team.ORANGE
        )


def validateBluePick(player: Member) -> bool:
    player = currQueue.get(doc_id=player.id)
    if (player is not None):
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
        id=player.id,
        name=str(player),
        mmr=Leaderboard.getPlayerMMR(player),
        queueTime=(datetime.now() + timedelta(minutes=mins_to_queue_for))
    )
    print(Leaderboard.getPlayerMMR(player))
    currQueue.insert(Document(new_player.toJSON(), doc_id=new_player.id))


def removeFromQueue(player: Union[Member, BallChaser, str]) -> None:
    if (isinstance(player, Member) or isinstance(player, BallChaser)):
        currQueue.remove(doc_ids=[player.id])
    elif (isinstance(player, str)):
        currQueue.remove(doc_ids=[int(player)])


def resetPlayerQueueTime(player: Member, mins_to_queue_for: int = 60) -> None:
    removeFromQueue(player)
    addToQueue(player, mins_to_queue_for)


def getCaptains() -> Union[Tuple[BallChaser, BallChaser], Tuple[None, None]]:
    if (queueAlreadyPopped()):
        orangeCap = BallChaser.fromDocument(
            currQueue.get((where(BallChaserKey.TEAM) == Team.ORANGE) & (where(BallChaserKey.IS_CAP) == True))
        )
        blueCap = BallChaser.fromDocument(
            currQueue.get((where(BallChaserKey.TEAM) == Team.BLUE) & (where(BallChaserKey.IS_CAP) == True))
        )
        return blueCap, orangeCap
    else:
        return None, None


def getQueueList(mentionPlayers: bool = False, includeTimes: bool = True, separator: str = "\n", includeLetters=False) -> str:  # noqa
    playerList = []
    letters = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
    ]
    i = 0

    for player in currQueue.search(where(BallChaserKey.TEAM) == None):
        player = BallChaser.fromDocument(player)
        if (mentionPlayers):
            playerList.append(player.mention)
        else:
            player_name = player.name.split("#")[0]
            if (includeTimes):
                minutes_diff = getQueueTimeRemaining(player)
                player_name += " (" + str(minutes_diff) + " mins)"
            if (includeLetters):
                player_name = letters[i] + " " + player_name
            playerList.append(player_name)
        i += 1

    return separator.join(playerList)


def getAvailablePicks() -> List[BallChaser]:
    availablePicks = []
    for player in currQueue.search(where(BallChaserKey.TEAM) == None):
        availablePicks.append(BallChaser.fromDocument(player))
    return availablePicks


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


def captainsPop() -> Tuple[BallChaser, BallChaser]:
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
def pick(player_picked: BallChaser) -> str:

    blueTeam, orangeTeam = getTeamList()
    if (len(blueTeam) == 1):
        currQueue.update({BallChaserKey.TEAM: Team.BLUE}, doc_ids=[player_picked.id])
    elif (len(blueTeam) == 2):
        currQueue.update({BallChaserKey.TEAM: Team.ORANGE}, doc_ids=[player_picked.id])
    if (len(orangeTeam) == 2):
        currQueue.update({BallChaserKey.TEAM: Team.BLUE}, where(BallChaserKey.TEAM) == None)
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
