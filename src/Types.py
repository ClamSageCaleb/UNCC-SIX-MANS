from datetime import datetime
from tinydb.table import Document


class Team():
    ORANGE = "orange"
    BLUE = "blue"


class MatchKey():
    ID = "id"
    NAME = "name"
    TEAM = "team"
    REPORTED_WINNER = "reportedWinner"
    REPORTER = "reporter"
    WINNING_TEAM = "winningTeam"


class LbKey():
    ID = "id"
    NAME = "Name"
    WINS = "Wins"
    LOSSES = "Losses"
    MATCHES = "Matches Played"
    WIN_PERC = "Win Perc"


class BallChaserKey():
    ID = "id"
    NAME = "name"
    IS_CAP = "isCap"
    TEAM = "team"
    QUEUE_TIME = "queueTime"


class BallChaser:
    def __init__(
        self,
        name: str,
        id: int,
        isCap: bool = False,
        team: Team = None,
        queueTime: datetime = datetime.now()
    ):
        self.name = name
        self.id = id
        self.mention = "<@{0}>".format(self.id)
        self.isCap = isCap
        self.team = team
        self.queueTime = queueTime

    @classmethod
    def fromDocument(cls, document: Document):
        return cls(
            id=document["id"],
            name=document["name"],
            isCap=document["isCap"],
            team=document["team"],
            queueTime=datetime.strptime(document["queueTime"], "%Y-%m-%dT%H:%M:%S.%f")
        )

    def toJSON(self, short: bool = False) -> dict:
        return {
            BallChaserKey.ID: self.id,
            BallChaserKey.NAME: self.name,
            BallChaserKey.IS_CAP: self.isCap,
            BallChaserKey.TEAM: self.team,
            BallChaserKey.QUEUE_TIME: self.queueTime.isoformat(),
        } if not short else {
            # this short version is used only for active match objects
            MatchKey.ID: self.id,
            MatchKey.NAME: self.name,
            MatchKey.TEAM: self.team
        }

    def isPlayerInList(self, listOfBallChasers: list) -> bool:
        return any(self.id == chaser["id"] for chaser in listOfBallChasers)
