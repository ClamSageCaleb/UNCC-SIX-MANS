import math
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

    # determine MMR here

    return 
