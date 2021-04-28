import discord
from discord.ext import commands
from typing import List, Union
import Queue

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
