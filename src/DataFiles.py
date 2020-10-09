import json
from os import path, mkdir
from pathlib import Path
from tinydb import TinyDB


basePath = path.join(Path.home(), "SixMans")
configPath = path.join(basePath, "config.json")
dataPath = path.join(basePath, "data.json")

if (not path.exists(basePath)):
    mkdir(basePath)

if (not path.exists(configPath)):
    with open(configPath, "w") as config:
        blankConfigFile = {
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "aws_object_name": "",
            "token": "",
            "queue_channels": [],
            "report_channels": [],
            "leaderboard_channel": -1
        }
        json.dump(blankConfigFile, config)

db = TinyDB(dataPath, indent=2)
currQueue = db.table("queue")
activeMatches = db.table("activeMatches")
leaderboard = db.table("leaderboard")


def getDiscordToken() -> str:
    with open(configPath, "r") as config:
        token = json.load(config)["token"]

    return token


def updateDiscordToken(newToken: str) -> str:
    with open(configPath, "r") as configFile:
        config = json.load(configFile)
        config["token"] = newToken
    with open(configPath, "w") as configFile:
        json.dump(config, configFile, indent=2)

    return newToken


def getChannelIds() -> dict:
    with open(configPath, "r") as configFile:
        config = json.load(configFile)
        return {
            "queue_channels": config["queue_channels"],  # list of int
            "report_channels": config["report_channels"],  # list of int
            "leaderboard_channel": config["leaderboard_channel"],  # int
        }
