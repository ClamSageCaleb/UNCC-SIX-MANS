from Types import Team, MatchKey


def calculateMMR(match) -> int:
    blueMMR = 0
    orangeMMR = 0

    for playerId in match:
        player = match[playerId]
        if (player[MatchKey.Team] == Team.BLUE):
            blueMMR += player[MatchKey.MMR]
        else:
            orangeMMR += player[MatchKey.MMR]

    avgBlueMMR = blueMMR / 3
    avgOrangeMMR = orangeMMR / 3

    # determine the new MMR on probability

    # determine the difference in MMR
    difference = (avgOrangeMMR - avgBlueMMR) / 400

    # take 10 to the power of our difference and make it postive by adding 1
    power = 1 + pow(10, difference)

    # 1 divided by our positive number to determine % chance of winning
    probability = 1 / power

    # 1 - our probability to start with a number greater than 1
    # 20 * our new number to enhance the amount of MMR
    mmr = 20(1 - probability)

    mmr = min(15, mmr)
    mmr = max(5, mmr)

    return int(mmr)
