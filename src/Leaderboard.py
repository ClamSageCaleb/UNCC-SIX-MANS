from FilePaths import tinyDbPath
from Queue import BallChaser
import AWSHelper as AWS
from tinydb import TinyDB, where
from json import dumps


db = TinyDB(tinyDbPath)
leaderboard = db.table("leaderboard")
activeMatches = db.table("activeMatches")

sorted_lb = None


def startMatch(blueTeam, orangeTeam):
    activeMatches.insert({
        "reportedWinner": {
            "player": {
                "ballChaser": "",
                "team": ""
            },
            "winningTeam": "",
        },
        "blueTeam": [p.toJSON() for p in blueTeam],
        "orangeTeam": [p.toJSON() for p in orangeTeam]
    })


def brokenQueue(player):
    if (activeMatches.count(where("reportedWinner").exists()) == 0):
        return "There are no currently active matches."

    player = BallChaser(player.name, player.id)
    match = getActiveMatch(player)

    if (not match):
        return "You are not in the queue; therefore you cannot report a broken queue."

    if (match["reportedWinner"]["winningTeam"] != ""):
        return "You cannot report a broken queue once someone reports the match."

    if (player.isPlayerInList(match["blueTeam"] + match["orangeTeam"]) != -1):
        activeMatches.remove(doc_ids=[match.doc_id])
        return ":white_check_mark: Previous queue removed."


def getActiveMatch(player):
    if (not isinstance(player, BallChaser)):
        player = BallChaser(player.name, player.id)

    return activeMatches.get(
        where("blueTeam").any(where("id") == player.id) |
        where("orangeTeam").any(where("id") == player.id)
    )


def reportConfirm(player: BallChaser, match, whoWon):
    reportingPlayersTeam = "blue" if (player.isPlayerInList(match["blueTeam"]) != -1) else "orange"

    # If first responder or a winning team disagreement, we update the report
    if (
        match["reportedWinner"]["winningTeam"] == "" or
        match["reportedWinner"]["winningTeam"] != whoWon
    ):

        activeMatches.update({
            "reportedWinner": {
                "winningTeam": whoWon,
                "player": {
                    "ballChaser": player.toJSON(),
                    "team": reportingPlayersTeam
                }
            }
        }, doc_ids=[match.doc_id])

        return "Match reported, awaiting confirmation from other team."

    # Make sure second reported is on the other team
    if (reportingPlayersTeam == match["reportedWinner"]["player"]["team"]):
        return (
            ":x: Your team has already reported the match."
            " One person from the other team must now confirm."
        )

    return ""


def reportMatch(player, whoWon):
    global sorted_lb
    match = getActiveMatch(player)

    if (not match):
        return ":x: Match not found"

    msg = reportConfirm(player, match, whoWon)
    if (msg != ""):
        return msg

    for teamMember in (match["blueTeam"] + match["orangeTeam"]):
        if (
            (whoWon == "blue" and teamMember in match["blueTeam"]) or
            (whoWon == "orange" and teamMember in match["orangeTeam"])
        ):
            win = 1
            loss = 0
        else:
            win = 0
            loss = 1

        player = leaderboard.get(where("id") == teamMember["id"])
        if (not player):
            leaderboard.insert({
                "id": teamMember["id"],
                "Name": teamMember["name"],
                "Wins": win,
                "Losses": loss,
                "Matches Played": 1,
                "Win Perc": float(win),
            })
        else:
            updated_player = {
                "Name": teamMember["name"],
                "Wins": player["Wins"] + win,
                "Losses": player["Losses"] + loss,
                "Matches Played": player["Matches Played"] + 1,
                "Win Perc": player["Win Perc"],
            }

            total_wins = int(updated_player["Wins"])
            total_matches = int(updated_player["Matches Played"])
            updated_player["Win Perc"] = float("{:.2f}".format(total_wins / total_matches))

            leaderboard.update(updated_player, doc_ids=[player.doc_id])

    activeMatches.remove(doc_ids=[match.doc_id])
    sorted_lb = sorted(leaderboard.all(), key=lambda x: (x["Wins"], x["Win Perc"]), reverse=True)
    AWS.writeRemoteLeaderboard(dumps(sorted_lb))

    return ":white_check_mark: Match has been reported successfully."


def makePretty(player_index, player):
    msg = "Rank: {0}\n".format(player_index + 1)
    for key in player:
        if (type(player[key]) == float):
            msg += "\t{0}: {1}%\n".format(key, int(player[key] * 100))
        elif (key != "id"):
            msg += "\t{0}: {1}\n".format(key, player[key])

    return msg


def showLeaderboard(player=None, limit=None):
    global sorted_lb
    if (not sorted_lb):
        sorted_lb = sorted(leaderboard.all(), key=lambda x: (x["Wins"], x["Win Perc"]), reverse=True)

    if (player):
        player_data = leaderboard.get(where("id") == player.id)

        if (not player_data):
            return player

        # returns the index in the sorted leaderboard where the IDs match
        player_index = next((i for i, p in enumerate(sorted_lb) if p['id'] == player_data['id']))

        return "```" + makePretty(player_index, player_data) + "\n```"

    else:
        msg = "```\n"

        for i, player_data in enumerate(sorted_lb):
            if (not limit or i < limit):
                msg += makePretty(i, player_data) + "\n"

        return msg + "\n```"


def resetFromRemote(remoteData):
    leaderboard.truncate()
    leaderboard.insert_multiple(remoteData)
