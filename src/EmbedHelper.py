from discord import Color, Embed
from Types import BallChaser, Team
from Typing import List


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
        desc="🔷 BLUE Team Captain 🔷: " + blueCap.mention +
        "\n\n🔶 ORANGE Team Captain 🔶: " + orangeCap.mention
    ).add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )

    if (teamToPick == Team.BLUE):
        embed.add_field(
            name="It is 🔷 BLUE Team's 🔷 turn to pick",
            value="Type **!pick** and mention a player from the queue below.",
            inline=False
        )
    else:
        embed.add_field(
            name="It is 🔶 ORANGE Team's 🔶 turn to pick",
            value="Please pick two players.\nEx: `!pick @Twan @Tux`",
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
        name="🔷 BLUE Team 🔷 picks first",
        value="Type **!pick** and mention a player from the queue below.",
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


def PlayersSetEmbed(blueTeam: List[BallChaser], orangeTeam: List[BallChaser]):
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
