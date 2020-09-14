from Queue import clearQueue, BallChaser
from datetime import datetime, timedelta
from FilePaths import currQueue, activeMatches
from tinydb import where
from Leaderboard import getActiveMatch


def fillQueue():
    clearQueue()
    new_queue = [
        BallChaser(
            name="Tux#9267",
            id=346838372649795595,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="Don#1424",
            id=528369347807412227,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="Durham#1999",
            id=251924205271121920,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="DaffyJr#6070",
            id=209084277223194624,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="cash#1547",
            id=347083937216200704,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="! KwLogic#1837",
            id=293413288723611649,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
    ]
    currQueue.insert_multiple([p.toJSON() for p in new_queue])


def fillWithCaptains():
    clearQueue()
    new_queue = [
        BallChaser(
            name="Tux#9267",
            id=346838372649795595,
            isCap=True,
            team="blue",
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="Don#1424",
            id=528369347807412227,
            isCap=True,
            team="orange",
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="Durham#1999",
            id=251924205271121920,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="DaffyJr#6070",
            id=209084277223194624,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="cash#1547",
            id=347083937216200704,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="! KwLogic#1837",
            id=293413288723611649,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
    ]
    currQueue.insert_multiple([p.toJSON() for p in new_queue])


def flipCaptains():
    blueCap = currQueue.get((where("team") == "blue") & (where("isCap") == True))
    orangeCap = currQueue.get((where("team") == "orange") & (where("isCap") == True))

    currQueue.update({"team": "orange"}, doc_ids=[blueCap.doc_id])
    currQueue.update({"team": "blue"}, doc_ids=[orangeCap.doc_id])


# FIXME - Convert to new active matches format
def swapReportedPlayer():
    player_tux = BallChaser(
        name="Tux#9267",
        id=346838372649795595,
    )
    player_don = BallChaser(
        name="Don#1424",
        id=528369347807412227,
    )
    match = getActiveMatch(player_tux)

    foundPlayer = next((x for x in match["players"] if x["id"] == match["reportedWinner"]["ballChaser"]["id"]))
    player_don.team = foundPlayer["team"]
    player_tux.team = "orange" if foundPlayer["team"] == "blue" else "blue"

    activeMatches.update({
        "reportedWinner": {
            "winningTeam": match["reportedWinner"]["winningTeam"],
            "ballChaser": player_don.toJSON(short=True),
        }
    }, doc_ids=[match.doc_id])
    # player_reported = active["reportedWinner"]["player"]["ballChaser"]
    # active["reportedWinner"]["player"]["ballChaser"] = active["blueTeam"][0]
    # active["blueTeam"][0] = player_reported
    # active["orangeTeam"][0] = active["reportedWinner"]["player"]["ballChaser"]

    # active["reportedWinner"]["player"]["ballChaser"] = active["reportedWinner"]["player"]["ballChaser"].toJSON()
    # for i in range(len(active["blueTeam"])):
    #     active["blueTeam"][i] = active["blueTeam"][i].toJSON()
    #     active["orangeTeam"][i] = active["orangeTeam"][i].toJSON()
