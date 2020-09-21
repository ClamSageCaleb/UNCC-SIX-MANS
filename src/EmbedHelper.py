from discord import Color, Embed


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
