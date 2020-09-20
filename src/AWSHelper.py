from DataFiles import configPath
from Leaderboard import resetFromRemote
import boto3
import json

aws_id = ""
aws_secret = ""
aws_object = ""
s3 = None


def init() -> None:
    global aws_id, aws_secret, aws_object, s3

    if (
        aws_id == "" or
        aws_secret == "" or
        aws_object == ""
    ):
        with open(configPath, "r") as config:
            configData = json.load(config)
            aws_id = configData["aws_access_key_id"]
            aws_secret = configData["aws_secret_access_key"]
            aws_object = configData["aws_object_name"]

    if (
        aws_id != "" and
        aws_secret != "" and
        s3 is None
    ):
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_id,
            aws_secret_access_key=aws_secret
        )
    else:
        print("No AWS settings provided. Leaderboard remote backup feature disabled.")


def readRemoteLeaderboard() -> None:
    global aws_id, aws_secret, aws_object, s3

    if (
        aws_id != "" and
        aws_secret != "" and
        aws_object != "" and
        s3 is not None
    ):
        remote_leaderboard = s3.Object("uncc-six-mans", aws_object)
        remote_leaderboard_data = json.loads(remote_leaderboard.get()["Body"].read().decode("utf-8"))
        resetFromRemote(remote_leaderboard_data)


def writeRemoteLeaderboard(leaderboardData: str) -> None:
    global aws_id, aws_secret, aws_object, s3

    if (
        aws_id != "" and
        aws_secret != "" and
        aws_object != "" and
        s3 is not None
    ):
        leaderboard = bytes(leaderboardData, "utf-8")
        s3.Bucket("uncc-six-mans").put_object(ACL="public-read", Key=aws_object, Body=leaderboard)
