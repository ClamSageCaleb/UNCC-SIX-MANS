from CheckForUpdates import updateBot
from EmbedHelper import AdminEmbed, ErrorEmbed
from typing import List
from bot import __version__
from discord import Role, Embed, Member
import Queue


def update(roles: List[Role]) -> Embed:
    """
        Middleware function to check author's permissions before running the update script.

        Parameters:
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if(Queue.isBotAdmin(roles)):
        return AdminEmbed(
            title="Checking For Updates",
            desc="Please hang tight."
        )
        updateBot()
        return AdminEmbed(
            title="Already Up to Date",
            desc="Current version: v{0}".format(__version__)
        )

    return AdminEmbed(
        title="Permission Denied",
        desc="You do not have permission to check for updates."
    )


def clear(roles: List[Role]) -> Embed:
    """
        Clears the current queue if the author has the Bot Admin role.

        Parameters:
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if(Queue.isBotAdmin(roles)):
        Queue.clearQueue()
        return AdminEmbed(
            title="Queue Cleared",
            desc="The queue has been cleared by an admin.  <:UNCCfeelsgood:538182514091491338>"
        )

    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to clear the queue."
    )


def kick(mentions: List[Member], roles: List[Role]) -> Embed:
    """
        Kicks the mentioned player from the queue. Requires Bot Admin role.

        Parameters:
            mentions: List[discord.Member] - The mentions in the message.
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (not Queue.isBotAdmin(roles)):
        return ErrorEmbed(
            title="Permission Denied",
            desc="You do not have the leg strength to kick other players."
        )

    if (len(mentions) != 1):
        return ErrorEmbed(
            title="Did Not Mention a Player",
            desc="Please mention a player in the queue to kick."
        )

    if (Queue.queueAlreadyPopped()):
        return ErrorEmbed(
            title="Queue Already Popped",
            desc="Can't kick players while picking teams."
        )

    if (Queue.getQueueLength() == 0):
        return ErrorEmbed(
            title="Queue is Empty",
            desc="The queue is empty, what are you doing?"
        )

    player = mentions[0]
    if (Queue.isPlayerInQueue(player)):
        Queue.removeFromQueue(player)
        return AdminEmbed(
            title="Kicked Player",
            desc="Removed " + player.display_name + " from the queue"
        )

    return ErrorEmbed(
        title="User Not in Queue",
        desc="To see who is in current queue, type: **!list**"
    )


# Disabling command as it does not work with the new executable.
# TODO: Find a new way to restart Norm since he is now an executable
def restart():
    return AdminEmbed(
        title="Command Diasbled",
        desc="This command is temporarily disabled."
    )

    # if(Queue.isBotAdmin(ctx.message.author.roles)):
    #     await ctx.send("Bot restarting...hopefully this fixes everything <:UNCCfeelsgood:538182514091491338>")
    #     os.remove("./data/queue.json")
    #     print("Restarting...")
    #     subprocess.call(["python", ".\\src\\bot.py"])
    #     sys.exit()
    # else:
    #     await ctx.send("You do not have permission to restart me.")
