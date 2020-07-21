import discord


def BaseEmbed(title, description, color):
    return discord.Embed(
        title=title,
        description=description,
        color=color,
    ).set_thumbnail(
        url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/norm_masked.png"
    )


def ErrorEmbed(title, desc):
    return BaseEmbed(
        title=":x:\t{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.red(),
    )


def QueueUpdateEmbed(title, desc):
    return BaseEmbed(
        title="{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.green(),
    )


def AdminEmbed(title, desc):
    return BaseEmbed(
        title=":exclamation:\t{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.dark_gold(),
    )


def InfoEmbed(title, desc):
    return BaseEmbed(
        title="{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.blue(),
    )
