import json
from os import path, mkdir
from pathlib import Path
import sys

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = "src"

programFilesPath = "{0}/SixMans/".format(Path.home())
queueFilePath = "{0}/queue.json".format(path.join(base_path, "./data"))
tokenPath = "{0}/SixMans/config.json".format(Path.home())
activeMatchPath = "{0}/activeMatches.json".format(path.join(base_path, "./data"))
leaderboardPath = "{0}/SixMans/Leaderboard.json".format(Path.home())


def checkProgramFiles():
    if (not path.exists(programFilesPath)):
        mkdir(programFilesPath)

    if (not path.exists(tokenPath)):
        with open(tokenPath, "w") as config:
            blankConfigFile = {
                "token": ""
            }
            json.dump(blankConfigFile, config)

    if not path.exists(leaderboardPath):
        with open(leaderboardPath, "w") as leaderboard:
            json.dump([], leaderboard)
