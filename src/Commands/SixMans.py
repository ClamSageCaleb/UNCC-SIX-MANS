from discord.ext.commands import context as Context
from discord import Embed, Member, Role
import Queue
import Leaderboard
from typing import List
from Types import Team
from math import ceil
from EmbedHelper import \
    ErrorEmbed,\
    QueueUpdateEmbed,\
    AdminEmbed,\
    InfoEmbed,\
    CaptainsAlreadySetEmbed,\
    CaptainsPopEmbed,\
    PlayersSetEmbed
from bot import REPORT_CH_IDS


def playerQueue(ctx: Context, *arg, quiet: bool = False) -> Embed:
    """
        Adds the author to the Queue for the specified amount of time.

        Parameters:
            ctx: discord.ext.commands.context - The context object passed into the client function.
            *arg: tuple - The args passed into the client function.
            quiet: bool (optional, default is False) - Specifies whether to include @here ping in channel.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    queue_length = Queue.getQueueLength()
    player = ctx.message.author

    try:
        queueTime = int(arg[0]) if len(arg) > 0 else 60
    except ValueError:  # if someone doesn't input a number we default to 60 minutes
        queueTime = 60

    # this converts the input to the next highest value of 10
    # ex: 14 -> 20, 9 -> 10, -5 -> 10, 3 -> 10
    queueTime = int(ceil(queueTime / 10)) * 10

    # minimum queue time of 10 minutes and maximum of 60 minutes
    if (queueTime < 10):
        queueTime = 10
    elif (queueTime > 60):
        queueTime = 60

    if (Queue.queueAlreadyPopped()):
        return ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Please wait until current lobby has been set.",
        )

    if (Queue.isPlayerInQueue(player)):
        Queue.resetPlayerQueueTime(player, queueTime)
        return QueueUpdateEmbed(
            title="Already in Queue, Queue Time Reset",
            desc="You're already in the queue, but your queue time has been reset to {0} minutes.".format(queueTime),
        )

    if (Leaderboard.getActiveMatch(player) is not None):
        return ErrorEmbed(
            title="Match Still Active",
            desc="Your previous match has not been reported yet."
            " Report your match in <#{0}> and try again.".format(REPORT_CH_IDS[0]),
        )

    if(queue_length == 0):
        Queue.addToQueue(player, queueTime)

        if (quiet):
            return QueueUpdateEmbed(
                title="Queue has Started :shushing_face:",
                desc="{0} wants to queue!\n\nQueued for {1} minutes.\n\n"
                "Type **!q** to join".format(player.mention, queueTime),
            )

        await ctx.send("@here Queue has started!")
        return QueueUpdateEmbed(
            title="Queue Started",
            desc="{0} wants to queue!\n\nQueued for {1} minutes.\n\n"
            "Type **!q** to join".format(player.mention, queueTime),
        )

    if (queue_length >= 6):
        return ErrorEmbed(
            title="Queue Already Full",
            desc="Queue is already full, please wait until the current queue is set and try again.",
        )

    if (queue_length == 5):
        Queue.addToQueue(player, queueTime)
        mentionedPlayerList = Queue.getQueueList(mentionPlayers=True)

        await ctx.send("Queue has popped! Get ready!\n" + mentionedPlayerList)
        return QueueUpdateEmbed(
            title="Queue Popped!",
            desc=player.mention + " has been added to the queue for " + str(queueTime) + " minutes.\n\n"
            "**Queue is now full!** \n\n"
            "Type !random for random teams.\n"
            "Type !captains to get picked last."
        )

    Queue.addToQueue(player, queueTime)
    playerList = Queue.getQueueList()

    return QueueUpdateEmbed(
        title="Player Added to Queue",
        desc=player.mention + " has been added to the queue for " + str(queueTime) + " minutes.\n\n"
        "Queue size: " + str(queue_length + 1) + "/6\n\n"
        "Current queue:\n" + playerList
    )


def leave(player: Member) -> Embed:
    """
        Removes author from the Queue.

        Parameters:
            player: discord.Member - The author of the message. The person being removed from the queue.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    username = player.display_name

    if (Queue.queueAlreadyPopped()):
        return ErrorEmbed(
            title="Queue Already Popped",
            desc="TOO LATE! You should've left before captains were picked."
        )

    if (Queue.isPlayerInQueue(player)):

        Queue.removeFromQueue(player)
        playerList = Queue.getQueueList()

        if(Queue.getQueueLength() != 0):
            return QueueUpdateEmbed(
                title="Player Left Queue",
                desc=username + " has left the queue.\n\n"
                "Queue size: " + str(Queue.getQueueLength()) + "/6\n\n"
                "Remaining players:\n" + playerList
            )

        return QueueUpdateEmbed(
            title="Player Left Queue",
            desc=username + " has left the queue.\n\n"
            "Queue is now empty."
        )

    return ErrorEmbed(
        title="Not in Queue",
        desc="You are not in the queue, type **!q** to join"
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


def listQueue(player: Member):
    """
        Lists the players currently in the queue with timestamps. Will show captains if captains are set.

        Parameters:
            player: dicord.Member - The author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (Queue.getQueueLength() == 0):
        return QueueUpdateEmbed(
            title="Queue is Empty",
            desc="Join the queue by typing **!q**"
        )
    if (Queue.queueAlreadyPopped()):
        return captains(player)

    playerList = Queue.getQueueList()
    return QueueUpdateEmbed(
        title="Current Queue",
        desc="Queue size: " + str(Queue.getQueueLength()) + "/6\n\n" + "Current queue:\n" + playerList
    )


def captains(player: Member):
    """
        Pops the queue and randomly assigns two captains. Will show captains if captains are already set.

        Parameters:
            player: dicord.Member - The author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (Queue.getQueueLength() != 6):
        return ErrorEmbed(
            title="Queue is Not Full",
            desc="You cannot pop a queue until is full."
        )

    if (not Queue.isPlayerInQueue(player)):
        return ErrorEmbed(
            title="Not in Queue",
            desc="You are not in the queue, therefore you cannot pop the queue."
        )

    blueCap, orangeCap = Queue.captainsPop()
    playerList = Queue.getQueueList(includeTimes=False)

    if (Queue.queueAlreadyPopped()):
        blueTeam, _ = Queue.getTeamList()

        return CaptainsAlreadySetEmbed(
            blueCap,
            orangeCap,
            Team.BLUE if len(blueTeam) == 1 else Team.ORANGE,
            playerList
        )

    return CaptainsPopEmbed(
        blueCap,
        orangeCap,
        playerList
    )


def random(player: Member):
    """
        Pops the queue and randomly assigns players to teams.

        Parameters:
            player: dicord.Member - The author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (Queue.queueAlreadyPopped()):
        return ErrorEmbed(
            title="Captains Already Chosen",
            desc="You cannot change your mind once you pick captains."
        )

    if (Queue.getQueueLength() != 6):
        return ErrorEmbed(
            title="Queue is Not Full",
            desc="You cannot pop a queue until is full."
        )

    if (not Queue.isPlayerInQueue(player)):
        return ErrorEmbed(
            title="Not in Queue",
            desc="You are not in the queue, therefore you cannot pop the queue."
        )

    blueTeam, orangeTeam = Queue.randomPop()
    Leaderboard.startMatch(blueTeam, orangeTeam)
    return PlayersSetEmbed(blueTeam, orangeTeam)
