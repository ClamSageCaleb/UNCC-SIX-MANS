import json
from os import path
from pathlib import Path
from tinydb import TinyDB


basePath = path.join(Path.home(), "SixMans")
tokenPath = path.join(basePath, "config.json")
tinyDbPath = path.join(basePath, "TinyDb.json")

db = TinyDB(tinyDbPath, indent=2)
currQueue = db.table("queue")
activeMatches = db.table("activeMatches")
leaderboard = db.table("leaderboard")


def getDiscordToken() -> str:
    with open(tokenPath, "r") as config:
        token = json.load(config)["token"]

    return token


def updateDiscordToken(newToken: str) -> str:
    with open(tokenPath, "w") as config:
        configFile = {
            "token": newToken
        }
        json.dump(configFile, config)

    return newToken
