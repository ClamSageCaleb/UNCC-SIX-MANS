import discord
from discord.ext import commands
from typing import Union, Literal
import Queue

reactions = {
    "queue": [
        "✅",
        "🤫",
        "❌",
        "\U0001F1F1",
        "🔢",
        "❓",
    ],
    "popped": [
        "\U0001F1E8",
        "\U0001F1F7",
        "✅",
        "❌",
        "\U0001F1F1",
        "🔢",
        "❓",
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
        "❓",
    ],
}

REACTION_GROUPS = Literal["queue", "popped", "active", "picks"]


async def sendMessage(
    channel: Union[commands.context.Context, discord.TextChannel],
    content: Union[str, discord.Embed],
    add_reaction_group: Union[REACTION_GROUPS, None]
) -> None:

    blueTeam, orangeTeam = Queue.getTeamList()

    if (isinstance(content, discord.Embed)):
        embedMsg = await channel.send(embed=content)
        if (add_reaction_group):
            if (len(blueTeam) == 2):
                for reaction in reactions[add_reaction_group]:
                    if (reaction == "4️⃣"):
                        break
                    if (len(orangeTeam) == 2):
                        if (reaction == "3️⃣"):
                            break
                    await embedMsg.add_reaction(reaction)
            else:
                for reaction in reactions[add_reaction_group]:
                    await embedMsg.add_reaction(reaction)
    else:
        txtMsg = await channel.send(content)
        await txtMsg.delete()
