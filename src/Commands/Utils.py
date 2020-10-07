from discord import Embed, Member, channel as Channel
from EmbedHelper import ErrorEmbed, QueueUpdateEmbed, InfoEmbed, PlayersSetEmbed
import Queue
import Leaderboard
from Types import BallChaser
from typing import List


async def updateLeaderboardChannel(lbChannel: Channel) -> None:
    """
        Deletes the old leaderboard and posts the updated one.

        Parameters:
            lbChannel: discord.Channel

        Returns:
            None
    """
    if (lbChannel is None):
        print("Leaderboard channel not set in config.")
        return

    await lbChannel.purge()
    lb = Leaderboard.showLeaderboard()
    if (isinstance(lb, list)):
        for i, msg in enumerate(lb):
            await lbChannel.send(embed=InfoEmbed(
                title="UNCC 6 Mans | Full Leaderboard ({0}/{1})".format(i + 1, len(lb)),
                desc=msg,
            ))
    else:
        await lbChannel.send(embed=InfoEmbed(
            title="UNCC 6 Mans | Full Leaderboard",
            desc=lb,
        ))


def blueTeamPick(mentions: List[Member], blueCap: BallChaser, orangeCap: BallChaser) -> Embed:
    """
        Helper function for the !pick command when blue team is picking.

        Parameters:
            mentions: List[discord.Member] - The mentions in the sent message.

        Returns:
            discord.Embed - An embedded message to send.

    """
    if len(mentions) == 0:
        return ErrorEmbed(
            title="No Mentioned Player",
            desc="No one was mentioned, please pick an available player."
        )

    if len(mentions) != 1:
        return ErrorEmbed(
            title="Too Many Mentioned Players",
            desc="More than one player mentioned, please pick just one player."
        )

    errorMsg = Queue.pick(mentions[0])

    if (errorMsg == ""):
        playerList = Queue.getQueueList(includeTimes=False)

        return QueueUpdateEmbed(
            title="Player Added to Team",
            desc="🔷 " + blueCap.name + " 🔷 picked " + mentions[0].mention
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="🔶 " + orangeCap.name + " 🔶 please pick TWO players.",
            value="Ex: `!pick @Twan @Tux`",
            inline=False
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="Available picks",
            value=playerList,
            inline=False
        )

    return ErrorEmbed(
        title="Player Not in Queue",
        desc=errorMsg
    )


def orangeTeamPick(mentions: List[Member], blueCap: BallChaser, orangeCap: BallChaser) -> List[Embed]:
    """
        Helper function for the !pick command when orange team is picking.

        Parameters:
            mentions: List[discord.Member] - The mentions in the sent message.

        Returns:
            List[discord.Embed] - A list of embedded messages to send.

    """
    if len(mentions) == 0:
        return [ErrorEmbed(
            title="No Mentioned Player",
            desc="No one was mentioned, please pick an available player."
        )]

    if len(mentions) != 2:
        return [ErrorEmbed(
            title="Incorrect Format",
            desc="Use format: `!pick @player1 @player2`"
        )]

    errorMsg = Queue.pick(mentions[0], mentions[1])

    if (errorMsg == ""):
        [player1, player2] = mentions
        blueTeam, orangeTeam = Queue.getTeamList()

        embed1 = QueueUpdateEmbed(
            title="Final Players Added",
            desc="🔶 " + orangeCap.name + " 🔶 picked " + player1.mention + " & " + player2.mention +
            "\n\nLast player added to 🔷 Blue Team 🔷"
        )

        embed2 = PlayersSetEmbed(blueTeam, orangeTeam)

        Leaderboard.startMatch(blueTeam, orangeTeam)
        Queue.clearQueue()

        return [embed1, embed2]

    return [ErrorEmbed(
        title="Player(s) Not Found",
        desc="Either one or both of the players you mentioned is not in the queue. Try again."
    )]
