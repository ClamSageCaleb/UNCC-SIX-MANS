from discord import Color, Embed
from Types import BallChaser
from typing import List
import Queue


def BaseEmbed(title: str, description: str, color: Color) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=color,
    ).set_thumbnail(
        url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/norm_still.png"
    )


def ErrorEmbed(title: str, desc: str) -> Embed:
    return BaseEmbed(
        title=":x:\t{0}".format(title),
        description="{0}".format(desc),
        color=Color.red(),
    )


def QueueUpdateEmbed(title: str, desc: str) -> Embed:
    return BaseEmbed(
        title="{0}".format(title),
        description="{0}".format(desc),
        color=Color.green(),
    )


def AdminEmbed(title: str, desc: str) -> Embed:
    return BaseEmbed(
        title=":exclamation:\t{0}".format(title),
        description="{0}".format(desc),
        color=Color.dark_gold(),
    )


def InfoEmbed(title: str, desc: str) -> Embed:
    return BaseEmbed(
        title="{0}".format(title),
        description="{0}".format(desc),
        color=Color.blue(),
    )


def CaptainsPopEmbed(blueCap: BallChaser, orangeCap: BallChaser, playerList: str) -> Embed:
    embed = QueueUpdateEmbed(
        title="Captains Have Been Set",
        desc="🔷 Blue Team Captain 🔷: " + blueCap.mention +
        "\n\n🔶 Orange Team Captain 🔶: " + orangeCap.mention
    ).add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )

    blueTeam, _ = Queue.getTeamList()
    if (len(blueTeam) == 1):
        embed.add_field(
            name="It is 🔷 " + blueCap.name + "'s 🔷 turn to pick",
            value="Pick a player from the list below by reacting to the numbers.\n",
            inline=False
        )
    else:
        embed.add_field(
            name="It is 🔶 " + orangeCap.name + "'s 🔶 turn to pick",
            value="Please pick two players.\n"
            "React to the numbers to select a player.",
            inline=False
        )

    embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    ).add_field(
        name="Available picks",
        value=playerList,
        inline=False
    )

    return embed


def PlayersSetEmbed(blueTeam: List[BallChaser], orangeTeam: List[BallChaser]) -> Embed:
    return QueueUpdateEmbed(
        title="Teams are Set!",
        desc=""
    ).add_field(
        name="🔷 BLUE TEAM 🔷",
        value="\n".join([player.mention for player in blueTeam]),
        inline=False
    ).add_field(
        name="🔶 ORANGE TEAM 🔶",
        value="\n".join([player.mention for player in orangeTeam]),
        inline=False
    )


def CaptainsRandomHelpEmbed(embed: Embed, blueTeam: List[BallChaser],
                            orangeTeam: List[BallChaser], blueCap: BallChaser,
                            orangeCap: BallChaser) -> Embed:
    new_embed: Embed = embed.copy()

    if (not Queue.queueAlreadyPopped()):
        blueTeam, orangeTeam = Queue.getTeamList()
        if (len(blueTeam) >= 1):
            new_embed.add_field(
                name="Available Picks",
                value=Queue.getQueueList(includeTimes=False, includeLetters=True),
                inline=False
            )
        else:
            if (Queue.getQueueLength() == 6):
                new_embed.add_field(
                    name="Queue Popped!",
                    value="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
                    inline=False
                )
            new_embed.add_field(
                name="Current Queue",
                value=Queue.getQueueList() if Queue.getQueueLength() >= 1 else "Current Queue 0/6\n Queue is empty.\n Join the queue by reacting to the ✅", # noqa
                inline=False
            )
    else:
        blueTeam, orangeTeam = Queue.getTeamList()
        blueCap, orangeCap = Queue.captainsPop()
        if (len(blueTeam) == 1):
            new_embed.add_field(
                name="It is 🔷 " + blueCap.name + "'s 🔷 turn to pick",
                value="Pick a player from the list below by reacting to the numbers.\n",
                inline=False
            )
        elif (len(blueTeam) == 2 and len(orangeTeam) == 1):
            new_embed.add_field(
                name="It is 🔶 " + orangeCap.name + "'s 🔶 turn to pick",
                value="Please pick two players.\n"
                "React to the numbers to select a player.",
                inline=False
            )
        elif (len(orangeTeam) == 2):
            new_embed.add_field(
                name="It is 🔶 " + orangeCap.name + "'s 🔶 turn to pick",
                value="Please pick one player.\n"
                "React to the numbers to select a player.",
                inline=False
            )
    return new_embed


def HelpEmbed() -> Embed:
    return Embed(
        title="Norm Help",
        description="https://clamsagecaleb.github.io/UNCC-SIX-MANS",
        color=0x38761D
    ).add_field(
        name="✅",
        value="Adds you to the queue.",
        inline=False
    ).add_field(
        name="🤫",
        value="Adds you to the queue *quietly* 🤫",
        inline=False
    ).add_field(
        name="❌",
        value="Removes you from the queue.",
        inline=False
    ).add_field(
        name="\U0001F1F1",
        value="Lists the current queue.",
        inline=False
    ).add_field(
        name="\U0001F1F7",
        value="Randomly picks teams. (Requires 6 players in queue)",
        inline=False
    ).add_field(
        name="\U0001F1E8",
        value="Randomly selects captains. (Requires 6 players in queue)"
        "\nFirst captain picks __ONE__ player. \nSecond captain picks the next __TWO__ players.",
        inline=False
    ).add_field(
        name="1️⃣ 2️⃣ 3️⃣ 4️⃣",
        value="Picks the corresponding player to add to your team.",
        inline=False
    ).add_field(
        name="🔷 or 🔶",
        value="Reports the result of your queue. React to the color of the winning team.\n"
        "When the match is reported successfully, Norm will react to the same message with 👍",
        inline=False
    ).add_field(
        name="💔",
        value="Broken Queue's the current match (Requires 4 players as majority vote).",
        inline=False
    ).add_field(
        name="🔢",
        value="Shows the top 5 players on the leaderboard.",
        inline=False
    ).add_field(
        name="\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
        "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
        value="For all `!` commands, you must **reply** to a message sent by Norm for it to work.\n"
        "This __does not__ apply to Easter Egg commands.",
        inline=False
    ).add_field(
        name="!q <time>",
        value="Queue for a certain amount of time, 10 - 60 minutes.",
        inline=False
    ).add_field(
        name="!leaderboard me",
        value="Shows your stats in the leaderboard.",
        inline=False
    ).add_field(
        name="!leaderboard <player>",
        value="Mention a player to show that player's stats on the leaderboard.",
        inline=False
    ).add_field(
        name="!norm, !asknorm, or !8ball",
        value="Will respond to a yes/no question. Good for predictions.",
        inline=False
    ).add_field(
        name="!help or ❓",
        value="This is the help command :O",
        inline=False
    ).set_thumbnail(
        url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/49ers.png"
    ).set_footer(
        text="Developed by Twan, Clam, Tux, and h"
    )
