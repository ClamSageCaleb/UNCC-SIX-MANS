import AWSHelper as AWS
from DataFiles import leaderboard, activeMatches
from Types import BallChaser, Team, MatchKey, LbKey
from discord import Member
from json import dumps
from tinydb import where
from tinydb.table import Document
from typing import List
import concurrent.futures


sorted_lb = None


def startMatch(blueTeam: List[BallChaser], orangeTeam: List[BallChaser]) -> None:
    allPlayers = blueTeam + orangeTeam
    newActiveMatch = {p.id: p.toJSON(short=True) for p in allPlayers}

    newActiveMatch[MatchKey.REPORTED_WINNER] = {
        MatchKey.REPORTER: None,
        MatchKey.WINNING_TEAM: None,
    }
    activeMatches.insert(newActiveMatch)


def brokenQueue(player: Member) -> str:
    if (activeMatches.count(where(MatchKey.REPORTED_WINNER).exists()) == 0):
        return "There are no currently active matches."

    match = getActiveMatch(player)

    if (not match):
        return "You are not in the queue; therefore you cannot report a broken queue."

    if (match[MatchKey.REPORTED_WINNER][MatchKey.WINNING_TEAM] is not None):
        return "You cannot report a broken queue once someone reports the match."

    activeMatches.remove(doc_ids=[match.doc_id])
    return ":white_check_mark: Previous queue removed."


def getActiveMatch(player: Member) -> Document or None:
    return activeMatches.get(where(str(player.id)).exists())


def reportConfirm(player: BallChaser, match: Document, whoWon: Team) -> str:
    # If first responder or a winning team disagreement, we update the report
    if (
        match[MatchKey.REPORTED_WINNER][MatchKey.WINNING_TEAM] is None or
        match[MatchKey.REPORTED_WINNER][MatchKey.WINNING_TEAM] != whoWon
    ):

        activeMatches.update({
            MatchKey.REPORTED_WINNER: {
                MatchKey.WINNING_TEAM: whoWon,
                MatchKey.REPORTER: player.toJSON(short=True)
            }
        }, doc_ids=[match.doc_id])

        return "Match reported, awaiting confirmation from other team."

    # Make sure second reported is on the other team
    if (player.team == match[MatchKey.REPORTED_WINNER][MatchKey.REPORTER][MatchKey.TEAM]):
        return (
            ":x: Your team has already reported the match."
            " One person from the other team must now confirm."
        )

    return ""


def reportMatch(player: Member, whoWon: Team) -> str:
    global sorted_lb
    match = getActiveMatch(player)

    if (not match):
        return ":x: Match not found"

    foundPlayer = match[str(player.id)]
    player = BallChaser(
        name=foundPlayer[MatchKey.NAME],
        id=foundPlayer[MatchKey.ID],
        team=foundPlayer[MatchKey.TEAM]
    )
    msg = reportConfirm(player, match, whoWon)
    if (msg != ""):
        return msg

    for key in match:
        if (key != MatchKey.REPORTED_WINNER):
            teamMember = match[key]
            if (
                (whoWon == Team.BLUE and teamMember["team"] == Team.BLUE) or
                (whoWon == Team.ORANGE and teamMember["team"] == Team.ORANGE)
            ):
                win = 1
                loss = 0
            else:
                win = 0
                loss = 1

            player = leaderboard.get(doc_id=teamMember[MatchKey.ID])
            if (not player):
                leaderboard.insert(Document({
                    LbKey.ID: teamMember[MatchKey.ID],
                    LbKey.NAME: teamMember[MatchKey.NAME],
                    LbKey.WINS: win,
                    LbKey.LOSSES: loss,
                    LbKey.MATCHES: 1,
                    LbKey.WIN_PERC: float(win),
                }, doc_id=teamMember[MatchKey.ID]))
            else:
                updated_player = {
                    LbKey.NAME: teamMember[MatchKey.NAME],
                    LbKey.WINS: player[LbKey.WINS] + win,
                    LbKey.LOSSES: player[LbKey.LOSSES] + loss,
                    LbKey.MATCHES: player[LbKey.MATCHES] + 1,
                    LbKey.WIN_PERC: player[LbKey.WIN_PERC],
                }

                total_wins = int(updated_player[LbKey.WINS])
                total_matches = int(updated_player[LbKey.MATCHES])
                updated_player[LbKey.WIN_PERC] = float("{:.2f}".format(total_wins / total_matches))

                leaderboard.update(updated_player, doc_ids=[player.doc_id])

    activeMatches.remove(doc_ids=[match.doc_id])
    sorted_lb = sorted(leaderboard.all(), key=lambda x: (x[LbKey.WINS], x[LbKey.WIN_PERC]), reverse=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(AWS.writeRemoteLeaderboard, dumps(sorted_lb))

    return ":white_check_mark: Match has been reported successfully."


def makePretty(player_index: int, player: BallChaser) -> str:
    msg = "Rank: {0}\n".format(player_index + 1)
    for key in player:
        if (type(player[key]) == float):
            msg += "\t{0}: {1}%\n".format(key, int(player[key] * 100))
        elif (key != LbKey.ID):
            msg += "\t{0}: {1}\n".format(key, player[key])

    return msg


def showLeaderboard(player: Member = None, limit: int = None) -> str or List[str]:
    global sorted_lb
    if (not sorted_lb):
        sorted_lb = sorted(leaderboard.all(), key=lambda x: (x[LbKey.WINS], x[LbKey.WIN_PERC]), reverse=True)

    if (player):
        player_data = leaderboard.get(doc_id=player.id)

        if (not player_data):
            return player

        # returns the index in the sorted leaderboard where the IDs match
        player_index = next((i for i, p in enumerate(sorted_lb) if p[LbKey.ID] == player_data[LbKey.ID]))

        return "```" + makePretty(player_index, player_data) + "\n```"

    else:
        max_players_per_msg = 10
        msgs = []

        if (limit is None):
            limit = len(sorted_lb)

        # start first message
        msg = "```\n"

        for i in range(limit):

            # if we reach our player limit, end and start a new message
            if (i % max_players_per_msg == 0 and i != 0):
                msgs.append(msg + "\n```")
                msg = "```\n"

            msg += makePretty(i, sorted_lb[i]) + "\n"

        # add the last message that didn't hit the if check
        msgs.append(msg + "\n```")

        # return list of messages or just the one string if msgs only has one message
        return msgs if len(msgs) > 1 else msgs[0]


def resetFromRemote(remoteData: dict) -> None:
    leaderboard.truncate()
    for p in remoteData:
        leaderboard.insert(Document(p, doc_id=p["id"]))
