from FilePaths import activeMatchPath, leaderboardPath
from JSONMethod import BallChaser
import json
import AWSHelper as AWS
from math import ceil


def readActiveMatches() -> list:
    fileToRead = open(activeMatchPath, "r")
    curr_matches = matches = json.load(fileToRead)
    fileToRead.close()

    for i, match in enumerate(matches):
        blue = []
        orange = []

        for player in match["blueTeam"]:
            blue.append(BallChaser(player["name"], player["id"]))
        for player in match["orangeTeam"]:
            orange.append(BallChaser(player["name"], player["id"]))

        curr_matches[i]["blueTeam"] = blue
        curr_matches[i]["orangeTeam"] = orange

        reported_player = curr_matches[i]["reportedWinner"]["player"]["ballChaser"]
        if (reported_player != ""):
            curr_matches[i]["reportedWinner"]["player"]["ballChaser"] = BallChaser(
                reported_player["name"], reported_player["id"]
            )

    return curr_matches


def writeActiveMatches(new_match_list):
    with open(activeMatchPath, "w") as activeMatches:
        json.dump(new_match_list, activeMatches)


def readLeaderboard():
    fileToRead = open(leaderboardPath, "r")
    ldrbrd = json.load(fileToRead)
    fileToRead.close()
    return ldrbrd


def saveLeaderboard(new_leaderboard):
    sorted_ldrbrd = sorted(new_leaderboard, key=lambda x: (x["Wins"], x["Win Perc"]), reverse=True)
    with open(leaderboardPath, "w") as ldrbrd:
        json.dump(sorted_ldrbrd, ldrbrd)
    AWS.writeRemoteLeaderboard()


def startMatch(blueTeam, orangeTeam):
    curr_matches = readActiveMatches()
    blue = []
    orange = []

    for i in range(len(blueTeam)):
        blue.append(blueTeam[i].toJSON())
        orange.append(orangeTeam[i].toJSON())

    curr_matches.append({
        "reportedWinner": {
            "player": {
                "ballChaser": "",
                "team": ""
            },
            "winningTeam": "",
        },
        "blueTeam": blue,
        "orangeTeam": orange
    })
    writeActiveMatches(curr_matches)


def brokenQueue(player):
    curr_matches = readActiveMatches()

    if (len(curr_matches) == 0):
        return "There are no currently active matches."

    match = curr_matches.pop()

    if (match["reportedWinner"]["winningTeam"] != ""):
        return "You cannot report a broken queue once someone reports the match."

    player = BallChaser(player.name, player.id)
    if (player.isPlayerInList(match["blueTeam"] + match["orangeTeam"]) != -1):
        writeActiveMatches(curr_matches)
        return ":white_check_mark: Previous queue removed."

    return "You are not in the queue; therefore you cannot report a broken queue."


def isPlayerInActiveMatch(player):
    curr_matches = readActiveMatches()
    player = BallChaser(player.name, player.id)

    for match in curr_matches:
        if (player.isPlayerInList(match["blueTeam"] + match["orangeTeam"]) != -1):
            return True

    return False


def getPlayerIndex(player):
    curr_ldrbrd = readLeaderboard()

    for i, row in enumerate(curr_ldrbrd):
        if (row["id"] == player.id):
            return i

    return -1


def reportConfirm(player, match, curr_matches, match_index, whoWon):
    # If first responder or a winning team disagreement, we update the report
    if (
        match["reportedWinner"]["winningTeam"] == "" or
        match["reportedWinner"]["winningTeam"] != whoWon
    ):
        match["reportedWinner"]["winningTeam"] = whoWon
        match["reportedWinner"]["player"]["ballChaser"] = player.toJSON()

        if (player.isPlayerInList(match["blueTeam"]) != -1):
            match["reportedWinner"]["player"]["team"] = "blue"
        else:
            match["reportedWinner"]["player"]["team"] = "orange"

        blue = []
        orange = []
        for i in range(3):
            blue.append(match["blueTeam"][i].toJSON())
            orange.append(match["orangeTeam"][i].toJSON())
        match["blueTeam"] = blue
        match["orangeTeam"] = orange

        curr_matches[match_index] = match
        writeActiveMatches(curr_matches)
        return "Match reported, awaiting confirmation from other team."

    # Make sure second reported is on the other team
    reportingPlayersTeam = "blue" if player.isPlayerInList(match["blueTeam"]) != -1 else "orange"
    if (reportingPlayersTeam == match["reportedWinner"]["player"]["team"]):
        return (
            ":x: Your team has already reported the match."
            " One person from the other team must now confirm."
        )

    return ""


def reportMatch(player, whoWon):
    curr_matches = readActiveMatches()

    for i, match in enumerate(curr_matches):
        if (player.isPlayerInList(match["blueTeam"] + match["orangeTeam"]) != -1):

            msg = reportConfirm(player, match, curr_matches, i, whoWon)
            if (msg != ""):
                return msg

            leaderboard = readLeaderboard()

            for teamMember in match["blueTeam"]:

                if (whoWon == "blue"):
                    win = 1
                    loss = 0
                else:
                    win = 0
                    loss = 1

                player_index = getPlayerIndex(teamMember)
                if (player_index == -1):
                    new_player = {
                        "id": teamMember.id,
                        "Name": teamMember.name,
                        "Wins": win,
                        "Losses": loss,
                        "Matches Played": 1,
                        "Win Perc": float(win),
                    }
                    leaderboard.append(new_player)
                else:
                    if (leaderboard[player_index]["Name"] != teamMember.name):
                        leaderboard[player_index]["Name"] = teamMember.name

                    leaderboard[player_index]["Wins"] += win
                    leaderboard[player_index]["Losses"] += loss
                    leaderboard[player_index]["Matches Played"] += 1

                    total_wins = int(leaderboard[player_index]["Wins"])
                    total_matches = int(leaderboard[player_index]["Matches Played"])
                    leaderboard[player_index]["Win Perc"] = float("{:.2f}".format(total_wins / total_matches))

            for teamMember in match["orangeTeam"]:

                if (whoWon == "orange"):
                    win = 1
                    loss = 0
                else:
                    win = 0
                    loss = 1

                player_index = getPlayerIndex(teamMember)
                if (player_index == -1):
                    new_player = {
                        "id": teamMember.id,
                        "Name": teamMember.name,
                        "Wins": win,
                        "Losses": loss,
                        "Matches Played": 1,
                        "Win Perc": float(win),
                    }
                    leaderboard.append(new_player)
                else:
                    if (leaderboard[player_index]["Name"] != teamMember.name):
                        leaderboard[player_index]["Name"] = teamMember.name

                    leaderboard[player_index]["Wins"] += win
                    leaderboard[player_index]["Losses"] += loss
                    leaderboard[player_index]["Matches Played"] += 1

                    total_wins = int(leaderboard[player_index]["Wins"])
                    total_matches = int(leaderboard[player_index]["Matches Played"])
                    leaderboard[player_index]["Win Perc"] = float("{:.2f}".format(total_wins / total_matches))

            saveLeaderboard(leaderboard)
            curr_matches.remove(match)
            writeActiveMatches(curr_matches)

            return ":white_check_mark: Match has been reported successfully."

    return ":x: Match not found"


def makePretty(player_index, player):
    msg = "Rank: {0}\n".format(player_index + 1)
    for key in player:
        if (type(player[key]) == float):
            msg += "\t{0}: {1}%\n".format(key, int(player[key] * 100))
        elif (key != "id"):
            msg += "\t{0}: {1}\n".format(key, player[key])

    return msg


def showLeaderboard(player=None, limit=None):
    curr_leaderboard = readLeaderboard()

    if (player):
        player_index = getPlayerIndex(player)
        player_data = curr_leaderboard[player_index]

        if (player_index == -1):
            return player

        return "```" + makePretty(player_index, player_data) + "\n```"

    else:
        players_per_msg = 10
        num_of_msgs = ceil(len(curr_leaderboard) / players_per_msg) if limit is None else ceil(limit / players_per_msg)
        msgs = []

        # start at 0, count by 10, up to the number of messages needed * 10
        for n in range(0, num_of_msgs * players_per_msg, players_per_msg):

            msg = "```\n"

            # starting at n, get the next 10 players
            i = n
            while (i < (n + players_per_msg) and i < len(curr_leaderboard)):
                msg += makePretty(i, curr_leaderboard[i]) + "\n"
                i += 1

                #  if there is a limit and we've reached it, stop looping
                if (limit is not None and i >= limit):
                    break

            # add new msg to msg list
            msgs.append(msg + "\n```")

        # return list of messages or just the one string if msgs only has one message
        return msgs if len(msgs) > 1 else msgs[0]
