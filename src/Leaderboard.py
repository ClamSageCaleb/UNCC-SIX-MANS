import json
from os import path
import os

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
    blue = []; orange = []

    for i in range(len(blueTeam)):
        blue.append(blueTeam[i].name)
        orange.append(orangeTeam[i].name)

    curr_matches.append({
        "blueTeam": blue,
        "orangeTeam": orange
    })
    writeActiveMatches(curr_matches)


def brokenQueue(player):
    curr_matches = readActiveMatches()

    if (len(curr_matches) == 0):
        return ":x: There are no active matches."

    match = curr_matches.pop()

    if player in (match["blueTeam"] + match["orangeTeam"]):
        writeActiveMatches(curr_matches)
        return "Previous queue removed."

    return "Player is not in queue, therefore cannot report broken queue."


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

def reportMatch(player, whoWon):
    curr_matches = readActiveMatches()

    for match in curr_matches:
        if (player in (match["blueTeam"] + match["orangeTeam"])):
            leaderboard = readLeaderboard()

            for teamMember in match["blueTeam"]:

                if (whoWon == "blue"): win = 1; loss = 0
                else: win = 0; loss = 1

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
                    leaderboard[player_index]["Win Perc"] = float("{:.2f}".format(int(leaderboard[player_index]["Wins"]) / int(leaderboard[player_index]["Matches Played"])))

            for teamMember in match["orangeTeam"]:

                if (whoWon == "orange"): win = 1; loss = 0
                else: win = 0; loss = 1

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
                    leaderboard[player_index]["Win Perc"] = float("{:.2f}".format(int(leaderboard[player_index]["Wins"]) / int(leaderboard[player_index]["Matches Played"])))

            saveLeaderboard(leaderboard)
            curr_matches.remove(match)
            writeActiveMatches(curr_matches)

            return ":white_check_mark: Match reported"

    return ":x: Match not found"

def makePretty(player_index, player):
    msg = "Rank: {0}\n".format(player_index + 1)
    for key in player:
        if (type(player[key]) == float):
            msg += "\t{0}: {1}%\n".format(key, int(player[key] * 100))
        else:
            msg += "\t{0}: {1}\n".format(key, player[key])
    
    return msg

def showLeaderboard(player = None, limit = None):
    curr_leaderboard = readLeaderboard()

    if (player):
        player_index = getPlayerIndex(player)
        player_data = curr_leaderboard[player_index]

        return "```\nUNCC 6 Mans | {0}\n\n".format(player) + makePretty(player_index, player_data) + "\n```"

    else:
        msg = "```\n"

        if (limit):
            msg += "UNCC 6 Mans | Top {0}\n\n".format(limit)
        else:
            msg += "UNCC 6 Mans | Full Leaderboard\n\n"

        for i, player in enumerate(curr_leaderboard):
            if (not limit or i < limit):
                msg += makePretty(i, player) + "\n"
        
        return msg + "\n```"

def checkActiveMatchesFile():
    if not path.exists(activeMatchPath):
        with open(activeMatchPath, "w") as activeMatches:
            json.dump(default, activeMatches)


def checkLeaderboardFile():
    if not path.exists(leaderboardPath):
        with open(leaderboardPath, "w") as leaderboard:
            json.dump(default, leaderboard)


def main():
    checkActiveMatchesFile()
    checkLeaderboardFile()

    print(reportMatch("Tux#9267", "orange"))


if __name__ == "__main__":
    main()
