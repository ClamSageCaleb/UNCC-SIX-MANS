import boto3
import json
from os import path
from sys import argv
from FilePaths import leaderboardPath, tokenPath


s3 = None
leaderboardFile = ""
aws_id = ""
aws_secret = ""

# Set prod/dev status based on file extension
_, file_extension = path.splitext(argv[0])
status = "prod" if file_extension == ".exe" else "dev"
leaderboardFile = "Leaderboard.json" if status == "prod" else "Test_Leaderboard.json"

if (aws_id == "" or aws_secret == ""):
    with open(tokenPath, "r") as config:
        configData = json.load(config)
        aws_id = configData["aws_access_key_id"]
        aws_secret = configData["aws_secret_access_key"]

if (s3 is None):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret
    )


def readRemoteLeaderboard():
    leaderboard = s3.Object("uncc-six-mans", leaderboardFile)
    leaderboard = json.loads(leaderboard.get()["Body"].read().decode("utf-8"))
    with open(leaderboardPath, "w") as ldrbrd:
        json.dump(leaderboard, ldrbrd)


def writeRemoteLeaderboard():
    with open(leaderboardPath, "rb") as leaderboard:
        s3.Bucket("uncc-six-mans").put_object(ACL="public-read", Key=leaderboardFile, Body=leaderboard)
