from discord import Color, Embed
from Types import BallChaser, Team
from typing import List


def BaseEmbed(title: str, description: str, color: Color) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=color,
    ).set_thumbnail(
        url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/norm_masked.png"
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


def CaptainsAlreadySetEmbed(blueCap: BallChaser, orangeCap: BallChaser, teamToPick: Team, playerList: str) -> Embed:
    embed = InfoEmbed(
        title="Captains Already Set",
        desc="🔷 Blue Team Captain 🔷: " + blueCap.mention +
        "\n\n🔶 Orange Team Captain 🔶: " + orangeCap.mention
    ).add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )

    if (teamToPick == Team.BLUE):
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


def CaptainsPopEmbed(blueCap: BallChaser, orangeCap: BallChaser, playerList: str) -> Embed:
    return QueueUpdateEmbed(
        title="Captains",
        desc="🔷 BLUE Team Captain 🔷: " + blueCap.mention +
        "\n\n🔶 ORANGE Team Captain 🔶: " + orangeCap.mention
    ).add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    ).add_field(
        name="🔷 " + blueCap.mention + " 🔷 picks first",
        value="Pick a player from the list below by reacting to the numbers.\n",
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


def HelpEmbed() -> Embed:
    return Embed(
        title="Norm Commands",
        description="https://clamsagecaleb.github.io/UNCC-SIX-MANS",
        color=0x38761D
    ).add_field(
        name="✅",
        value="Adds you to the queue",
        inline=False
    ).add_field(
        name="🤫",
        value="Adds you to the queue *quietly* 🤫",
        inline=False
    ).add_field(
        name="❌",
        value="Removes you from the queue",
        inline=False
    ).add_field(
        name="\U0001F1F1",
        value="Lists the current queue",
        inline=False
    ).add_field(
        name="\U0001F1F7",
        value="Randomly picks teams (Requires 6 players in queue)",
        inline=False
    ).add_field(
        name="\U0001F1E8",
        value="Randomly selects captains (Requires 6 players in queue)."
        "\nFirst captain picks 1 \nSecond captain picks the next two",
        inline=False
    ).add_field(
        name="🔷 or 🔶",
        value="Reports the result of your queue. React to the color of the winning team.",
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
        "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
        value="For all `!` commands, you must **reply** to a message sent by Norm for it to work.\n"
        "This does not apply to Easter Egg commands.",
        inline=False
    ).add_field(
        name="!leaderboard me",
        value="Shows your rank on the leaderboard.",
        inline=False
    ).add_field(
        name='!norm, !asknorm, or !8ball',
        value='Will respond to a yes/no question. Good for predictions',
        inline=False
    ).add_field(
        name="❓",
        value="This is the help command :O",
        inline=False
    ).set_thumbnail(
        url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/49ers.png"
    ).set_footer(
        text="Developed by Twan, Clam, Tux, and h"
    )
