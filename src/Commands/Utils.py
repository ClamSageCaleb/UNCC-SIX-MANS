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


def blueTeamPick(pickedPlayer: BallChaser, blueCap: BallChaser, orangeCap: BallChaser) -> Embed:
    """
        Helper function for the !pick command when blue team is picking.

        Parameters:
            mentions: List[discord.Member] - The mentions in the sent message.

        Returns:
            discord.Embed - An embedded message to send.

    """

    errorMsg = Queue.pick(pickedPlayer)

    if (errorMsg == ""):
        playerList = Queue.getQueueList(includeTimes=False)

        return QueueUpdateEmbed(
            title="Player Added to Team",
            desc="🔷 " + blueCap.name + " 🔷 picked " + pickedPlayer.mention
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="🔶 " + orangeCap.name + " 🔶 please pick 2️⃣ players.",
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


def orangeTeamPick(pickedPlayer: BallChaser, orangeTeam: List[BallChaser], blueCap: BallChaser, orangeCap: BallChaser) -> Embed: # noqa
    """
        Helper function for the !pick command when orange team is picking.

        Parameters:
            mentions: List[discord.Member] - The mentions in the sent message.

        Returns:
            List[discord.Embed] - A list of embedded messages to send.

    """
    Queue.pick(pickedPlayer)
    if (len(orangeTeam) == 1):
        return QueueUpdateEmbed(
            title="Player Added to Team",
            desc="🔶 " + orangeCap.name + " 🔶 picked " + pickedPlayer.mention
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="🔶 " + orangeCap.name + " 🔶 please pick 1️⃣ player.",
            value="React to the number of the player that you'd like to pick.",
            inline=False
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="Available Picks",
            value=Queue.getQueueList(includeTimes=False),
            inline=False
        ).add_field(
            name="Orange Captain Picked",
            value=pickedPlayer.name.split('#')[0],
            inline=False
        )

    else:
        blueTeam, orangeTeam = Queue.getTeamList()

        embed = PlayersSetEmbed(blueTeam, orangeTeam)

        Leaderboard.startMatch(blueTeam, orangeTeam)
        Queue.clearQueue()

        return embed
