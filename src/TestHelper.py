from JSONMethod import clearQueue, readQueue, writeQueue, BallChaser
from datetime import datetime, timedelta


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
    writeQueue({
        "queue": new_queue,
        "orangeCap": "",
        "blueCap": "",
        "orangeTeam": [],
        "blueTeam": []
    })


def fillWithCaptains():
    clearQueue()
    new_queue = [
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
    writeQueue({
        "queue": new_queue,
        "orangeCap": BallChaser(
            name="Don#1424",
            id=528369347807412227,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        "blueCap": BallChaser(
            name="Tux#9267",
            id=346838372649795595,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        "orangeTeam": [
            BallChaser(
                name="Don#1424",
                id=528369347807412227,
                queueTime=(datetime.now() + timedelta(minutes=60))
            ),
        ],
        "blueTeam": [
            BallChaser(
                name="Tux#9267",
                id=346838372649795595,
                queueTime=(datetime.now() + timedelta(minutes=60))
            )
        ]
    })


def flipCaptains():
    curr_queue = readQueue()
    prev_orange_cap = curr_queue["orangeCap"]
    prev_blue_cap = curr_queue["blueCap"]
    curr_queue["blueTeam"][0] = prev_orange_cap
    curr_queue["orangeTeam"][0] = prev_blue_cap
    curr_queue["blueCap"] = prev_orange_cap
    curr_queue["orangeCap"] = prev_blue_cap
    writeQueue(curr_queue)


# FIXME - Convert to new active matches format
def swapReportedPlayer():
    return True
    # active = readActiveMatches()[0]
    # player_reported = active["reportedWinner"]["player"]["ballChaser"]
    # active["reportedWinner"]["player"]["ballChaser"] = active["blueTeam"][0]
    # active["blueTeam"][0] = player_reported
    # active["orangeTeam"][0] = active["reportedWinner"]["player"]["ballChaser"]

    # active["reportedWinner"]["player"]["ballChaser"] = active["reportedWinner"]["player"]["ballChaser"].toJSON()
    # for i in range(len(active["blueTeam"])):
    #     active["blueTeam"][i] = active["blueTeam"][i].toJSON()
    #     active["orangeTeam"][i] = active["orangeTeam"][i].toJSON()

    # writeActiveMatches([active])
