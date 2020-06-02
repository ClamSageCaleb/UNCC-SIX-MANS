import json
import pandas as pd
from os import path
import os

default = {
    "matches": []
}

defaultLeaderboard = {
    "data": []
}

df_columns = ["Name", "Wins", "Losses", "Matches Played"]


def readActiveMatches() -> list:
    fileToRead = open("activeMatches.json", "r")
    matches = json.load(fileToRead)
    fileToRead.close()
    return matches["matches"]


def writeActiveMatches(new_match_list):
    with open("activeMatches.json", "w") as activeMatches:
        new_match_json = {
            "matches": new_match_list
        }
        json.dump(new_match_json, activeMatches)


def readLeaderboard() -> pd.DataFrame:
    return pd.DataFrame(pd.read_csv("leaderboard.csv"))


def saveLeaderboard(new_leaderboard: pd.DataFrame):
    os.remove("leaderboard.csv")
    print(new_leaderboard)
    new_leaderboard.to_csv("leaderboard.csv", index=False, header=True)


def startMatch(blueTeam, orangeTeam):
    curr_matches = readActiveMatches()
    curr_matches.append({
        "blueTeam": blueTeam,
        "orangeTeam": orangeTeam
    })
    writeActiveMatches(curr_matches)


def reportMatch(player, whoWon):
    curr_matches = readActiveMatches()

    for match in curr_matches:
        if (player in match["blueTeam"] or player in match["orangeTeam"]):
            leaderboard = readLeaderboard()

            for teamMember in match["blueTeam"]:
                player_row = leaderboard.loc[leaderboard["Name"] == player]
                if (player_row.empty):
                    new_player = {
                        "Name": player,
                        "Wins": 1 if whoWon == "blue" else 0,
                        "Losses": 1 if whoWon == "orange" else 0,
                        "Matches Played": 1
                    }
                    print(pd.DataFrame(new_player, index=[0]))
                    leaderboard.append(
                        pd.DataFrame(new_player, index=[0]), ignore_index=True
                    )
                    print(leaderboard)
                else:
                    player_row.at["Wins"] += 1 if whoWon == "blue" else 0,
                    player_row.at["Losses"] += 1 if whoWon == "orange" else 0,
                    player_row.at["Matches Played"] += 1

            for teamMember in match["orangeTeam"]:
                player_row = leaderboard.loc[leaderboard["Name"] == player]
                if (player_row.empty):
                    new_player = {
                        "Name": player,
                        "Wins": 1 if whoWon == "orange" else 0,
                        "Losses": 1 if whoWon == "blue" else 0,
                        "Matches Played": 1
                    }
                    leaderboard.append(
                        pd.DataFrame(new_player, index=[0])
                    )
                else:
                    player_row.at["Wins"] += 1 if whoWon == "orange" else 0,
                    player_row.at["Losses"] += 1 if whoWon == "blue" else 0,
                    player_row.at["Matches Played"] += 1

            saveLeaderboard(leaderboard)
            curr_matches.remove(match)
            writeActiveMatches(curr_matches)

            return "Match reported"

    return "Match not found"


def checkActiveMatchesFile():
    if not path.exists("activeMatches.json"):
        with open("activeMatches.json", "w") as activeMatches:
            json.dump(default, activeMatches)


def checkLeaderboardFile():
    if not path.exists("leaderboard.json"):
        with open("leaderboard.json", "w") as leaderboard:
            json.dump(default, leaderboard)


def main():
    checkActiveMatchesFile()
    checkLeaderboardFile()

    print(reportMatch("Matt", "blue"))


if __name__ == "__main__":
    main()
