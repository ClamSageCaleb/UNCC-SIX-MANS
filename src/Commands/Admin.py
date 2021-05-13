from CheckForUpdates import updateBot
from EmbedHelper import AdminEmbed, ErrorEmbed, QueueUpdateEmbed, captainsRandomHelpEmbed
from Leaderboard import brokenQueue as lbBrokenQueue
from typing import List
from bot import __version__
from discord import Role, Embed, Member
import Queue
import DataFiles


def update(roles: List[Role]) -> Embed:
    """
        Middleware function to check author's permissions before running the update script.

        Parameters:
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if(Queue.isBotAdmin(roles)):
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


def kick(mentions: str, roles: List[Role], *arg) -> Embed:
    """
        Kicks the mentioned player from the queue. Requires Bot Admin role.

        Parameters:
            mentions: List[discord.Member] - The mentions in the message.
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (not Queue.queueAlreadyPopped()):
        blueTeam, orangeTeam = Queue.getTeamList()
    else:
        blueTeam, orangeTeam = Queue.getTeamList()
        blueCap, orangeCap = Queue.captainsPop()
    if (len(arg) > 0):
        if ("<@!" in arg[0]):
            split = mentions.split("<@!")
            player_id = split[1][:-1]
            if (player_id.isdigit()):
                if (not Queue.isBotAdmin(roles)):
                    embed = ErrorEmbed(
                        title="Permission Denied",
                        desc="You do not have the leg strength to kick other players."
                    )
                    if (len(blueTeam) == 0):
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                    else:
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                    return embed

                if (Queue.queueAlreadyPopped()):
                    embed = ErrorEmbed(
                        title="Queue Already Popped",
                        desc="Can't kick players while picking teams."
                    )
                    captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                    return embed

                if (Queue.getQueueLength() == 0):
                    embed = ErrorEmbed(
                        title="Queue is Empty",
                        desc="The queue is empty, what are you doing?"
                    )
                    captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                    return embed

                member = DataFiles.leaderboard.get(doc_id=int(player_id))
                if (Queue.isPlayerInQueue(player_id)):
                    Queue.removeFromQueue(player_id)
                    embed = AdminEmbed(
                        title="Kicked Player",
                        desc="Removed {0} from the queue".format(member["Name"].split("#")[0])
                    )
                    if (len(blueTeam) == 0):
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                    else:
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                    return embed

                if (not Queue.isPlayerInQueue(player_id)):
                    embed = ErrorEmbed(
                        title="User Not in Queue",
                        desc="To see who is in current queue, type: **!list**"
                    )
                    if (len(blueTeam) == 0):
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                    else:
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                    return embed

                else:
                    embed = ErrorEmbed(
                        title="Did Not Mention a Player",
                        desc="Please mention a player in the queue to kick."
                    )
                    if (len(blueTeam) == 0):
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                    else:
                        captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                    return embed
            else:
                embed = ErrorEmbed(
                    title="Did Not Mention a Player",
                    desc="Please mention a player in the queue to kick."
                )
                if (len(blueTeam) == 0):
                    captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
                else:
                    captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
                return embed
        else:
            embed = ErrorEmbed(
                title="Did Not Mention a Player",
                desc="Please mention a player in the queue to kick."
            )
            if (len(blueTeam) == 0):
                captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
            else:
                captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
            return embed
    else:
        embed = ErrorEmbed(
            title="Did Not Mention a Player",
            desc="Please mention a player in the queue to kick."
        )
        if (len(blueTeam) == 0):
            captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, None, None)
        else:
            captainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
        return embed


def brokenQueue(player: Member, roles: List[Role]) -> Embed:
    """
        Removes the active match that the author is in.

        Parameters:
            player: dicord.Member - The author of the message.
            roles: List[discord.Role] - The roles of the author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (not Queue.isBotAdmin(roles)):
        return ErrorEmbed(
            title="Permission Denied",
            desc="You do not have permission to break the queue without a majority."
        )

    msg = lbBrokenQueue(player)
    if (":white_check_mark:" in msg):
        return QueueUpdateEmbed(
            title="Popped Queue Removed",
            desc="The popped queue has been removed from active matches. You may now re-queue."
        ).add_field(
            name="Current Queue 0/6",
            value="Queue is empty."
        )

    return ErrorEmbed(
        title="Could Not Remove Queue",
        desc=msg
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
