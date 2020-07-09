import boto3
from dotenv import load_dotenv
from os import getenv
import json
from FilePaths import leaderboardPath, tokenPath


aws_id = ""
aws_secret = ""
s3 = None

# the lack of .env file results in dev
load_dotenv()
status = getenv("status")
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
