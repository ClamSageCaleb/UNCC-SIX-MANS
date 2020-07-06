import boto3
import json
from FilePaths import leaderboardPath, tokenPath


aws_id = ""
aws_secret = ""
s3 = None


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


def readLeaderboard():
    leaderboard = s3.Object("uncc-six-mans", "Leaderboard.json")
    leaderboard = json.loads(leaderboard.get()["Body"].read().decode("utf-8"))
    with open(leaderboardPath, "w") as ldrbrd:
        json.dump(leaderboard, ldrbrd)


def writeLeaderboard():
    with open(leaderboardPath, "rb") as leaderboard:
        s3.Bucket("uncc-six-mans").put_object(ACL="public-read", Key="Leaderboard.json", Body=leaderboard)