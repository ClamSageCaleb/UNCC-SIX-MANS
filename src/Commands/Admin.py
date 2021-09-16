from CheckForUpdates import updateBot
from EmbedHelper import AdminEmbed, ErrorEmbed, QueueUpdateEmbed, CaptainsRandomHelpEmbed
from Leaderboard import brokenQueue as lbBrokenQueue
from typing import List
from Types import Team
from bot import __version__
from discord import Role, Embed, Member, channel as Channel
import Queue
from Commands.Utils import updateLeaderboardChannel
from Leaderboard import reportMatch
from DataFiles import getMMRMultiplier, updateMMRMultiplier


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
            mentions: str - The content of the message.
            roles: List[discord.Role] - The roles of the author of the message.
            *arg: - The arguments in the message.

        Returns:
            discord.Embed - The embedded message to respond with.
    """
    blueTeam, orangeTeam = Queue.getTeamList()
    blueCap, orangeCap = Queue.getCaptains()

    if (len(arg) > 0 and "<@!" in arg[0]):
        split = mentions.split("<@!")
        player_id = split[1][:-1]

        if (player_id.isdigit()):
            embed = None

            if (not Queue.isBotAdmin(roles)):
                embed = ErrorEmbed(
                    title="Permission Denied",
                    desc="You do not have the leg strength to kick other players."
                )

            elif (Queue.queueAlreadyPopped()):
                embed = ErrorEmbed(
                    title="Queue Already Popped",
                    desc="Can't kick players while picking teams."
                )

            elif (Queue.getQueueLength() == 0):
                embed = ErrorEmbed(
                    title="Queue is Empty",
                    desc="The queue is empty, what are you doing?"
                )

            elif (not Queue.isPlayerInQueue(player_id)):
                embed = ErrorEmbed(
                    title="User Not in Queue",
                    desc="To see who is in current queue, type: **!list**"
                )

            else:
                member = Queue.getPlayerFromQueue(player_id)
                Queue.removeFromQueue(player_id)
                embed = AdminEmbed(
                    title="Kicked Player",
                    desc="Removed {0} from the queue".format(member["name"].split("#")[0])
                )

            edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
            return edited_embed

    embed = ErrorEmbed(
        title="Did Not Mention a Player",
        desc="Please mention a player in the queue to kick."
    )
    edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
    return edited_embed


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


async def mentionBrokenQueue(mentions: str, roles: List[Role], *arg) -> Embed:
    if (Queue.isBotAdmin(roles)):

        if (len(arg) > 0 and "<@!" in arg[0]):
            split = mentions.split("<@!")
            player_id = split[1][:-1]

            if (player_id.isdigit()):
                msg = lbBrokenQueue(player_id)
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
        return ErrorEmbed(
            title="Did Not Mention a Player",
            desc="Please mention a player in an active match to broken queue."
        )
    return ErrorEmbed(
        title="Permission Denied",
        desc="You do not have permission to break the queue without a majority."
    )


async def forceReport(mentions: str, roles: List[Role], lbChannel: Channel, *arg) -> Embed:
    if (Queue.isBotAdmin(roles)):

        if (len(arg) == 2 and "<@!" in arg[0]):
            split = mentions.split("<@!")
            if (str(arg[1]).lower() == Team.BLUE):
                player_id = split[1][:-6]
            elif(str(arg[1]).lower() == Team.ORANGE):
                player_id = split[1][:-8]
            else:
                return ErrorEmbed(
                    title="You Must Report A Valid Team",
                    desc="You did not supply a valid team to report."
                )

            if (player_id.isdigit()):
                msg = reportMatch(player_id, arg[1], True)

                if (msg):
                    try:
                        # if match was reported successfully, update leaderboard channel
                        await updateLeaderboardChannel(lbChannel)
                    except Exception as e:
                        print("! Norm does not have access to update the leaderboard.", e)

                    return AdminEmbed(
                        title="Match Force Reported Successfully",
                        desc="You may now re-queue."
                    )
            else:
                return ErrorEmbed(
                    title="Did Not Mention a Player",
                    desc="You must mention one player who is in the match you want to report."
                )
        else:
            ErrorEmbed(
                title="Did Not Mention a Player",
                desc="You must mention one player who is in the match you want to report."
            )
    else:
        return ErrorEmbed(
            title="Permission Denied",
            desc="You do not have the strength to force report matches. Ask an admin if you need to force report a match." # noqa
        )


def multiplier(roles: List[Role], *arg) -> Embed:
    if (Queue.isBotAdmin(roles)):
        try:
            value = float(arg[0])
        except ValueError:
            return ErrorEmbed(
                title="Not a Valid Number",
                desc="You must enter a positve number."
            )
        if (value > 0):
            multiplier = updateMMRMultiplier(value)
            return AdminEmbed(
                title="MMR Multiplied",
                desc="The MMR gain has been multiplied by a factor of **" + str(multiplier) + "**."
            )
        else:
            multiplier = getMMRMultiplier()
            return ErrorEmbed(
                title="MMR Multiplier is Negative",
                desc="You entered a negative number. The multiplier remains as **" + str(multiplier) + "**."
            )
    else:
        return ErrorEmbed(
            title="Permission Denied",
            desc="You do not have the strength to multiply MMR."
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
