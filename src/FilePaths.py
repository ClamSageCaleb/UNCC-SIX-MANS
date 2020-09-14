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
