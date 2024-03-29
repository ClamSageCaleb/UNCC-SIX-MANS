from discord import Embed, Member, channel as Channel
import Queue
import Leaderboard
from typing import List, Literal
from math import ceil
from EmbedHelper import \
    ErrorEmbed,\
    QueueUpdateEmbed,\
    InfoEmbed,\
    CaptainsPopEmbed,\
    PlayersSetEmbed,\
    CaptainsRandomHelpEmbed
from Commands.Utils import updateLeaderboardChannel, orangeTeamPick, blueTeamPick


def playerQueue(player: Member, *arg, quiet: bool = False) -> List[str or Embed]:
    """
        Adds the author to the Queue for the specified amount of time.

        Parameters:
            player: discord.Member - The author of the message. The person being removed from the queue.
            *arg: tuple - The args passed into the client function.
            quiet: bool (optional, default is False) - Specifies whether to include @here ping in channel.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    queue_length = Queue.getQueueLength()

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
        return [ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Please wait until current lobby has been set.",
        )]

    if (Queue.isPlayerInQueue(player) and Queue.getQueueLength() != 6):
        Queue.resetPlayerQueueTime(player, queueTime)
        playerList = Queue.getQueueList()
        return [QueueUpdateEmbed(
            title="Already in Queue, Queue Time Reset",
            desc="You're already in the queue, but your queue time has been reset to {0} minutes.".format(queueTime),
        ).add_field(
            name="Current Queue (" + str(queue_length) + "/6)",
            value=playerList
        )]

    if (Queue.isPlayerInQueue(player) and Queue.getQueueLength() == 6):
        Queue.resetPlayerQueueTime(player, queueTime)
        playerList = Queue.getQueueList()
        return [QueueUpdateEmbed(
            title="Already in Queue, Queue Time Reset",
            desc="You're already in the queue, but your queue time has been reset to {0} minutes.".format(queueTime),
        ).add_field(
            name="Queue Popped!",
            value="**React to the \U0001F1E8 or \U0001F1F7 for captains or random.**\n\n"
            "**Current Queue (" + str(queue_length) + "/6)**\n" + playerList,
            inline=False
        )]

    if (Leaderboard.getActiveMatch(player) is not None):
        return [ErrorEmbed(
            title="Your previous match has not been reported yet.",
            desc="React to the 🔷 or 🔶 to report the match.\n"
            "One player from each team must report the match.\n"
            "You will not be able to queue again until the match has been reported!"
        ).add_field(
            name="React to the 💔 to broken queue.",
            value="There must be at least 4️⃣ players that want to broken queue.",
            inline=False
        )]

    if(queue_length == 0):
        Queue.addToQueue(player, queueTime)

        if (quiet):
            return [QueueUpdateEmbed(
                title="Queue has Started :shushing_face:",
                desc="{0} wants to queue!\n\nQueued for {1} minutes.\n\n"
                "React to the ✅ to join".format(player.mention, queueTime),
            )]

        return ["@here Queue has started!",
                QueueUpdateEmbed(
                    title="Queue Started",
                    desc="{0} wants to queue!\n\nQueued for {1} minutes.\n\n"
                    "React to the ✅ to join".format(player.mention, queueTime),
                )]

    if (queue_length >= 6):
        playerList = Queue.getQueueList()
        return [ErrorEmbed(
            title="Queue Already Full",
            desc="Queue is already full, please wait until the current queue is set and try again.",
        ).add_field(
            name="Queue Popped!",
            value="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
            inline=False
        ).add_field(
            name="Current Queue " + str(queue_length) + "/6",
            value=playerList
        )]

    if (queue_length == 5):
        Queue.addToQueue(player, queueTime)
        playerList = Queue.getQueueList()
        mentionedPlayerList = Queue.getQueueList(mentionPlayers=True, separator=", ")

        return [QueueUpdateEmbed(
            title="Queue Popped!",
            desc=player.mention + " has been added to the queue for " + str(queueTime) + " minutes.\n\n"
            "**Queue is now full!** \n\n"
            "React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n"
        ).add_field(
            name="Current Queue " + str(queue_length + 1) + "/6",
            value=playerList
        ),
            "Queue has popped! Get ready!\n" + mentionedPlayerList]

    Queue.addToQueue(player, queueTime)
    playerList = Queue.getQueueList()

    return [QueueUpdateEmbed(
        title="Player Added to Queue",
        desc=player.mention + " has been added to the queue for " + str(queueTime) + " minutes."
    ).add_field(
        name="Current Queue " + str(queue_length + 1) + "/6",
        value=playerList
    )]


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
                desc=username + " has left the queue."
            ).add_field(
                name="Remaining Players (" + str(Queue.getQueueLength()) + "/6)",
                value=playerList
            )
        return QueueUpdateEmbed(
            title="Player Left Queue",
            desc=username + " has left the queue.\n\n"
            "Queue is now empty.\n\n"
            "Join the queue by reacting to the ✅.\n"
        )

    playerList = Queue.getQueueList()
    embed = ErrorEmbed(
        title="Not in Queue",
        desc="You are not in the queue, react to the ✅ to join if there is space.\n"
    )
    if (Queue.getQueueLength() == 6):
        embed.add_field(
            name="Queue Popped!",
            value="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
            inline=False
        )
    embed.add_field(
        name="Queued Players (" + str(Queue.getQueueLength()) + "/6)",
        value="Queue is empty." if playerList == "" else playerList
    )

    return embed


def listQueue(player: Member) -> Embed:
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
            desc="Join the queue by reacting to the ✅.\n"
        )
    if (Queue.queueAlreadyPopped()):
        return captains(player)
    if (Queue.getQueueLength() == 6):
        return QueueUpdateEmbed(
            title="Current Queue (" + str(Queue.getQueueLength()) + "/6)\n\n"
            "Queue Popped!",
            desc=""
        ).add_field(
            name="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
            value=Queue.getQueueList()
        )

    playerList = Queue.getQueueList()
    return QueueUpdateEmbed(
        title="Current Queue (" + str(Queue.getQueueLength()) + "/6)",
        desc=playerList
    )


def captains(player: Member) -> Embed:
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
        ).add_field(
            name="Queue Popped!",
            value="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
            inline=False
        ).add_field(
            name="Current Queue " + str(Queue.getQueueLength()) + "/6",
            value=Queue.getQueueList(),
            inline=False
        )

    blueCap, orangeCap = Queue.captainsPop()
    playerList = Queue.getQueueList(includeTimes=False, includeLetters=True)

    if (Queue.queueAlreadyPopped()):
        blueTeam, _ = Queue.getTeamList()

        return CaptainsPopEmbed(
            blueCap,
            orangeCap,
            playerList
        )

    return CaptainsPopEmbed(
        blueCap,
        orangeCap,
        playerList
    )


def random(player: Member) -> Embed:
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
        ).add_field(
            name="Queue Popped!",
            value="React to the \U0001F1E8 or \U0001F1F7 for captains or random.\n",
            inline=False
        ).add_field(
            name="Current Queue " + str(Queue.getQueueLength()) + "/6",
            value=Queue.getQueueList(),
            inline=False
        )

    blueTeam, orangeTeam = Queue.randomPop()
    Leaderboard.startMatch(blueTeam, orangeTeam)
    return PlayersSetEmbed(blueTeam, orangeTeam)


def brokenQueue(player: Member) -> Embed:
    """
        Removes the active match that the author is in.

        Parameters:
            player: dicord.Member - The author of the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    msg = Leaderboard.brokenQueue(player)
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


def leaderboard(author: Member, mentions: str, lbChannelId: int, *arg) -> Embed:
    """
        Shows the leaderboard. Shows top 5 if no one mentioned. Shows player stats if mentioned or used keyword "me".

        Parameters:
            author: discord.Member - The author of the message
            mentions: str - The content in the message.
            *arg - The rest of the args in the message.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    playerMentioned: bool = False
    selfRank: bool = False
    if (len(arg) > 0):
        if ("<@!" in arg[0]):
            split = mentions.split("<@!")
            player_id = split[1][:-1]
            if (player_id.isdigit()):
                playerMentioned = True
        elif (arg[0] == "me"):
            selfRank = True

    blueTeam, orangeTeam = Queue.getTeamList()
    blueCap, orangeCap = Queue.getCaptains()

    if (playerMentioned or selfRank):
        player = player_id if playerMentioned else str(author.id)
        players_rank = Leaderboard.showLeaderboard(player)
        member = Leaderboard.getBallChaser(player)

        if (type(players_rank) == str and member):
            embed = InfoEmbed(
                title="Leaderboard Placement for {0}".format(member["Name"].split("#")[0]),
                desc=players_rank
            )
            edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
            return edited_embed

        embed = ErrorEmbed(
            title="No Matches Played",
            desc="{0} hasn't played any matches and won't show up on the leaderboard.".format(arg[0])
        )
        edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
        return edited_embed

    elif (len(arg) == 0 and playerMentioned == False):
        if (Leaderboard.countLeaderboard() >= 6):
            viewFullLb = "\nTo see the full leaderboard, visit <#{0}>.".format(lbChannelId) if (lbChannelId != -1) else "" # noqa
            embed = InfoEmbed(
                title="UNCC 6 Mans | Top 5",
                desc=Leaderboard.showLeaderboard(limit=5) + viewFullLb
            )
            edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
            return edited_embed
        else:
            embed = ErrorEmbed(
                title="No Leaderboard!",
                desc="There are currently no leaderboard statistics!"
            )
            edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
            return edited_embed

    else:
        embed = ErrorEmbed(
            title="Leaderboard Command Help",
            desc="Mention someone to see their rank, use 'me' to see your rank,"
            " include nothing to see the top 5 on the leaderboard."
        )
        edited_embed = CaptainsRandomHelpEmbed(embed, blueTeam, orangeTeam, blueCap, orangeCap)
        return edited_embed


async def report(player: Member, lbChannel: Channel, winningTeam: Literal["blue", "orange"]) -> bool or None:
    """
        Used to report the winning team of the series.

        Parameters:
            player: discord.Member - The author of the message.
            lbChannel: discord.Channel - The specified leaderboard channel object
            winningTeam: str - The reported winning team

        Returns:
            dicord.Embed - The embedded message to respond with or sends nothing.
    """
    match_reported = Leaderboard.reportMatch(player, winningTeam)

    if (match_reported):
        try:
            # if match was reported successfully, update leaderboard channel
            await updateLeaderboardChannel(lbChannel)
        except Exception as e:
            print("! Norm does not have access to update the leaderboard.", e)

        return match_reported

    else:
        return None


def pick(player: Member, reactionNumber: int) -> Embed:
    """
        Assigns picked players to their respective teams.

        Parameters:
            player: discord.Member - The author of the message
            reactionNumber: int - The picked player by reaction.

        Returns:
            dicord.Embed - The embedded message to respond with.
    """
    if (not Queue.queueAlreadyPopped()):
        return ErrorEmbed(
            title="Captains Not Set",
            desc="If queue is full, please react to the \U0001F1E8 or \U0001F1F7"  # noqa | regional indicator C / regional indicator R
        )

    blueCap, orangeCap = Queue.captainsPop()

    blueTeam, orangeTeam = Queue.getTeamList()

    if (Queue.isPlayerInQueue(player)):
        if (Queue.validateBluePick(player)):
            availablePicks = Queue.getAvailablePicks()
            return blueTeamPick(availablePicks[reactionNumber - 1], blueCap, orangeCap)
        if (len(blueTeam) == 1):
            if (not Queue.validateBluePick(player)):
                return ErrorEmbed(
                    title="Not the Blue Captain",
                    desc="You are not 🔷 BLUE Team Captain 🔷\n\n"
                    "🔷 BLUE Team Captain 🔷 is: " + blueCap.mention
                ).add_field(
                    name="🔷 " + blueCap.name.split("#")[0] + " 🔷 picks first. \n"
                    "🔶 ORANGE Team Captain 🔶 is: " + orangeCap.name.split("#")[0],
                    value="Pick a player from the list below by reacting to the numbers.\n",
                    inline=False
                ).add_field(
                    name="\u200b",
                    value="\u200b",
                    inline=False
                ).add_field(
                    name="Available picks",
                    value=Queue.getQueueList(includeTimes=False, includeLetters=True),
                    inline=False
                )

        if (Queue.validateOrangePick(player)):
            availablePicks = Queue.getAvailablePicks()
            return orangeTeamPick(availablePicks[reactionNumber - 1], orangeTeam, blueCap, orangeCap)
        if (len(blueTeam) == 2):
            if (not Queue.validateOrangePick(player)):
                return ErrorEmbed(
                    title="Not the Orange Captain",
                    desc="You are not 🔶 ORANGE Team Captain 🔶 \n\n"
                    "🔶 ORANGE Team Captain 🔶 is: " + orangeCap.mention
                ).add_field(
                    name="🔶 " + orangeCap.name.split("#")[0] + " 🔶 picks second. \n"
                    "🔷 BLUE Team Captain 🔷 is: " + blueCap.name.split("#")[0],
                    value="Pick a player from the list below by reacting to the numbers.\n",
                    inline=False
                ).add_field(
                    name="\u200b",
                    value="\u200b",
                    inline=False
                ).add_field(
                    name="Available picks",
                    value=Queue.getQueueList(includeTimes=False, includeLetters=True),
                    inline=False
                )
    else:
        if (len(blueTeam) == 1):
            return ErrorEmbed(
                title="Not in Queue",
                desc="You are not in the queue!\n",
            ).add_field(
                name="🔷 " + blueCap.name.split("#")[0] + " 🔷 picks first. \n"
                "🔶 ORANGE Team Captain 🔶 is: " + orangeCap.name.split("#")[0],
                value="Pick a player from the list below by reacting to the numbers.\n",
                inline=False
            ).add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            ).add_field(
                name="Available picks",
                value=Queue.getQueueList(includeTimes=False, includeLetters=True),
                inline=False
            )
        if (len(blueTeam) == 2):
            return ErrorEmbed(
                title="Not in Queue",
                desc="You are not in the queue!\n",
            ).add_field(
                name="🔶 " + orangeCap.name.split("#")[0] + " 🔶 picks second. \n"
                "🔷 BLUE Team Captain 🔷 is: " + blueCap.name.split("#")[0],
                value="Pick a player from the list below by reacting to the numbers.\n",
                inline=False
            ).add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            ).add_field(
                name="Available picks",
                value=Queue.getQueueList(includeTimes=False, includeLetters=True),
                inline=False
            )


def checkQueueTimes() -> List[Embed] or None:
    """
        Checks the queue times for each player and returns warning or removal embeds if applicable

        Parameters:
            None.

        Returns:
            List[Embed] or None - A list of embeds to send or nothing
    """
    if (Queue.getQueueLength() == 0 or Queue.queueAlreadyPopped()):
        return None

    warn_players, removed_players = Queue.checkQueueTimes()

    if (len(warn_players) == 0 and len(removed_players) == 0):
        return None

    embeds = []

    if (len(warn_players) > 0):
        warn_str = ",".join([player.mention for player in warn_players])
        embeds.append(InfoEmbed(
            title="Stale Player Queue Warning",
            desc=warn_str + " will be removed from the queue in 5 minutes.\n\n"
            "To stay in the queue, react to the ✅"
        ).add_field(
            name="Current Queue",
            value=Queue.getQueueList(),
            inline=False
        ))

    if (len(removed_players) > 0):
        rem_str = ",".join([player.mention for player in removed_players])
        playerList = Queue.getQueueList()
        if(Queue.getQueueLength() != 0):
            embeds.append(QueueUpdateEmbed(
                title="Queue Stale Players Removed",
                desc=rem_str + " have been removed from the queue."
            ).add_field(
                name="Remaining Players (" + str(Queue.getQueueLength()) + "/6)",
                value=playerList
            ))
        else:
            embeds.append(QueueUpdateEmbed(
                title="Queue Stale Players Removed",
                desc=rem_str + " have been removed from the queue.\n\n" + "Queue is now empty."
            ))

    return embeds
