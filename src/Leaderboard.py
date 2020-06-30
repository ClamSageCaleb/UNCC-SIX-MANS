import json
from os import path

default = []

activeMatchPath = "./data/activeMatches.json"
leaderboardPath = "./data/leaderboard.json"


def readActiveMatches() -> list:
    checkActiveMatchesFile()
    fileToRead = open(activeMatchPath, "r")
    matches = json.load(fileToRead)
    fileToRead.close()
    return matches


def writeActiveMatches(new_match_list):
    with open(activeMatchPath, "w") as activeMatches:
        json.dump(new_match_list, activeMatches)


def readLeaderboard():
    checkLeaderboardFile()
    fileToRead = open(leaderboardPath, "r")
    ldrbrd = json.load(fileToRead)
    fileToRead.close()
    return ldrbrd


def saveLeaderboard(new_leaderboard):
    sorted_ldrbrd = sorted(new_leaderboard, key=lambda x: (x["Win Perc"], x["Wins"]), reverse=True)
    with open(leaderboardPath, "w") as ldrbrd:
        json.dump(sorted_ldrbrd, ldrbrd)


def startMatch(blueTeam, orangeTeam):
    curr_matches = readActiveMatches()
    blue = []
    orange = []

    for i in range(len(blueTeam)):
        blue.append(blueTeam[i].name)
        orange.append(orangeTeam[i].name)

    curr_matches.append({
        "reportedWinner": {
            "player": {
                "name": "",
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

    if (player in (match["blueTeam"] + match["orangeTeam"])):
        writeActiveMatches(curr_matches)
        return ":white_check_mark: Previous queue removed."

    return "You are not in the queue; therefore you cannot report a broken queue."


def isPlayerInActiveMatch(player):
    curr_matches = readActiveMatches()

    for match in curr_matches:
        if player in (match["blueTeam"] + match["orangeTeam"]):
            return True

    return False


def getPlayerIndex(player):
    curr_ldrbrd = readLeaderboard()

    for i, row in enumerate(curr_ldrbrd):
        if (row["Name"] == player):
            return i

    return -1


def reportConfirm(player, match, curr_matches, match_index, whoWon):
    # If first responder or a winning team disagreement, we update the report
    if (
        match["reportedWinner"]["winningTeam"] == "" or
        match["reportedWinner"]["winningTeam"] != whoWon
    ):
        match["reportedWinner"]["winningTeam"] = whoWon
        match["reportedWinner"]["player"]["name"] = player

        if (player in match["blueTeam"]):
            match["reportedWinner"]["player"]["team"] = "blue"
        else:
            match["reportedWinner"]["player"]["team"] = "orange"

        curr_matches[match_index] = match
        writeActiveMatches(curr_matches)
        return "Match reported, awaiting confirmation from other team."

    # Make sure second reported is on the other team
    reportingPlayersTeam = "blue" if player in match["blueTeam"] else "orange"
    if (reportingPlayersTeam == match["reportedWinner"]["player"]["team"]):
        return (
            ":x: Your team has already reported the match."
            " One person from the other team must now confirm."
        )

    return ""


def reportMatch(player, whoWon):
    curr_matches = readActiveMatches()

    for i, match in enumerate(curr_matches):
        if (player in (match["blueTeam"] + match["orangeTeam"])):

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
                        "Name": teamMember,
                        "Wins": win,
                        "Losses": loss,
                        "Matches Played": 1,
                        "Win Perc": float(win),
                    }
                    leaderboard.append(new_player)
                else:
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
                        "Name": teamMember,
                        "Wins": win,
                        "Losses": loss,
                        "Matches Played": 1,
                        "Win Perc": float(win),
                    }
                    leaderboard.append(new_player)
                else:
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
        else:
            msg += "\t{0}: {1}\n".format(key, player[key])

    return msg


def showLeaderboard(player=None, limit=None):
    curr_leaderboard = readLeaderboard()

    if (player):
        player_index = getPlayerIndex(player)
        player_data = curr_leaderboard[player_index]

        if (player_data["Matches Played"] <= 5):
            return (player_data["Name"], player_data["Matches Played"])

        index = 0
        for i, p in enumerate(curr_leaderboard):
            if (i == player_index):
                break
            elif (p["Matches Played"] >= 5):
                index += 1

        return "```" + makePretty(index, player_data) + "\n```"

    else:
        msg = "```\n"

        index = 0
        for player_data in curr_leaderboard:
            if ((not limit or index < limit) and player_data["Matches Played"] >= 5):
                msg += makePretty(index, player_data) + "\n"
                index += 1

        return msg + "\n```"


def checkActiveMatchesFile():
    if not path.exists(activeMatchPath):
        with open(activeMatchPath, "w") as activeMatches:
            json.dump(default, activeMatches)


def checkLeaderboardFile():
    if not path.exists(leaderboardPath):
        with open(leaderboardPath, "w") as leaderboard:
            json.dump(default, leaderboard)
