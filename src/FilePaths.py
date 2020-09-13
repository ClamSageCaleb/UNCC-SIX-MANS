import json
from os import path, mkdir
from pathlib import Path


basePath = path.join(Path.home(), "SixMans")
dataBasePath = path.join(basePath, "data")

programFilesPath = path.join(basePath)
tokenPath = path.join(basePath, "config.json")
queueFilePath = path.join(dataBasePath, "queue.json")
activeMatchPath = path.join(dataBasePath, "activeMatches.json")
leaderboardPath = path.join(dataBasePath, "Leaderboard.json")
tinyDbPath = path.join(dataBasePath, "TinyDb.json")


def checkProgramFiles():
    if (not path.exists(programFilesPath)):
        mkdir(programFilesPath)

    if (not path.exists(dataBasePath)):
        mkdir(dataBasePath)

    if (not path.exists(tokenPath)):
        with open(tokenPath, "w") as config:
            blankConfigFile = {
                "aws_access_key_id": "",
                "aws_secret_access_key": "",
                "aws_object_name": "",
                "token": ""
            }
            json.dump(blankConfigFile, config)

    if not path.exists(queueFilePath):
        default = {
            "queue": [],
            "orangeCap": "",
            "blueCap": "",
            "orangeTeam": [],
            "blueTeam": []
        }
        with open(queueFilePath, "w") as queueFile:
            json.dump(default, queueFile)

    if not path.exists(activeMatchPath):
        with open(activeMatchPath, "w") as activeMatches:
            json.dump([], activeMatches)

    if not path.exists(leaderboardPath):
        with open(leaderboardPath, "w") as leaderboard:
            json.dump([], leaderboard)
