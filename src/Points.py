from tinydb.table import Document
from Types import Team, MatchKey


def calculateMMR(match: Document) -> int:
    blueMMR = 0
    orangeMMR = 0

    for playerId in match:
        if (playerId != MatchKey.REPORTED_WINNER):
            player = match[playerId]
            if (player[MatchKey.TEAM] == Team.BLUE):
                blueMMR += player[MatchKey.MMR]
            else:
                orangeMMR += player[MatchKey.MMR]

    avgBlueMMR = blueMMR / 3
    avgOrangeMMR = orangeMMR / 3

    # determine the new MMR on probability

    # determine the difference in MMR
    difference = ((avgOrangeMMR - avgBlueMMR) / 400)

    # take 10 to the power of our difference and make it postive by adding 1
    power = (pow(10, difference) + 1)

    # 1 divided by our positive number to determine % chance of winning
    probability = (1 / power)

    # 1 - our probability to start with a number greater than 1
    # 20 * our new number to enhance the amount of MMR
    mmr = ((1 - probability) * 20)

    mmr = min(15, mmr)
    mmr = max(5, mmr)

    return int(mmr)
