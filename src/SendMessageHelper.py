import discord
from discord.ext import commands
from typing import List, Union

reactions = {
    "queue": [
        "✅",
        "❌"
    ],
    "popped": [
        "\U0001F1E8",
        "\U0001F1F7"
    ],
    "active": [
        "💔",
        "🔷",
        "🔶",
    ],
    "picks": [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
    ],
}


async def sendMessage(
    channel: Union[commands.context.Context, discord.TextChannel],
    content: Union[str, discord.Embed],
    add_reaction_group: Union["queue", "popped", "active", "picks", None]
) -> None:

    if (isinstance(content, discord.Embed)):
        embedMsg = await channel.send(embed=content)
        if (add_reaction_group):
            for reaction in reactions[add_reaction_group]:
                await embedMsg.add_reaction(reaction)
    else:
        txtMsg = await channel.send(content)
        await txtMsg.delete()
