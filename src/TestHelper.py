from DataFiles import currQueue, activeMatches
from Queue import clearQueue, BallChaser
from Types import Team, MatchKey, BallChaserKey
from datetime import datetime, timedelta
from tinydb import where
from tinydb.table import Document


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
    for p in new_queue:
        currQueue.insert(Document(p.toJSON(), doc_id=p.id))


def fillWithCaptains():
    clearQueue()
    new_queue = [
        BallChaser(
            name="Tux#9267",
            id=346838372649795595,
            isCap=True,
            team=Team.BLUE,
            queueTime=(datetime.now() + timedelta(minutes=60))
        ),
        BallChaser(
            name="Don#1424",
            id=528369347807412227,
            isCap=True,
            team=Team.ORANGE,
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
    for p in new_queue:
        currQueue.insert(Document(p.toJSON(), doc_id=p.id))


def flipCaptains():
    blueCap = currQueue.get((where(BallChaserKey.TEAM) == Team.BLUE) & (where(BallChaserKey.IS_CAP) == True))
    orangeCap = currQueue.get((where(BallChaserKey.TEAM) == Team.ORANGE) & (where(BallChaserKey.IS_CAP) == True))

    currQueue.update({BallChaserKey.TEAM: Team.ORANGE}, doc_ids=[blueCap.doc_id])
    currQueue.update({BallChaserKey.TEAM: Team.BLUE}, doc_ids=[orangeCap.doc_id])


def swapReportedPlayer():
    match = activeMatches.get(where(MatchKey.REPORTED_WINNER)[MatchKey.WINNING_TEAM] != None)
    updated_match = match.copy()

    originalReporter = match[MatchKey.REPORTED_WINNER][MatchKey.REPORTER]

    otherTeam = Team.BLUE if originalReporter[MatchKey.TEAM] == Team.ORANGE else Team.ORANGE
    unlucky_id = str(next(key for key in match if match[key][MatchKey.TEAM] == otherTeam))

    updated_match[unlucky_id][MatchKey.TEAM] = originalReporter[MatchKey.TEAM]
    updated_match[str(originalReporter[str(MatchKey.ID)])][MatchKey.TEAM] = otherTeam

    updated_match[MatchKey.REPORTED_WINNER][MatchKey.REPORTER] = match[unlucky_id]

    activeMatches.update(updated_match, doc_ids=[match.doc_id])
