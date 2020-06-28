
import discord


def ErrorEmbed(title, desc):
    return discord.Embed(
        title=":x:\t{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.red(),
    )


def QueueUpdateEmbed(title, desc):
    return discord.Embed(
        title="{0}".format(title),
        description="{0}".format(desc),
        color=discord.Color.green(),
    )
