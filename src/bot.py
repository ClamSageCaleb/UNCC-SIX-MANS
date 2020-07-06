__author__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__license__ = "MIT"
__version__ = "4.1.1"
__maintainer__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__email__ = "caleb.benjamin9799@gmail.com"
__status__ = "Production"


import asyncio
import CheckForUpdates
import discord
from discord.ext.commands import Bot, CommandNotFound
from EmbedHelper import ErrorEmbed, QueueUpdateEmbed, AdminEmbed, InfoEmbed
from FilePaths import checkProgramFiles
import JSONMethod as Jason
import Leaderboard
import os
from pathlib import Path
import random
import time

# Bot prefix and Discord Bot token
BOT_PREFIX = ("!")

# Creates the Bot with name 'client'
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

pikaO = 1

# Channel ID's
QUEUE_CH_ID = 538166641226416162
TEST_QUEUE_CH_ID = 629502331259584559
MATCH_REPORT_CH_ID = 622786720328581133
LEADERBOARD_CH_ID = 718998601790914591
TUX_TEST_SERVER_CH_ID = 716358749912039429

'''
    Discord Events
'''


@client.event
async def on_message(message):
    allowedChannels = [QUEUE_CH_ID, TEST_QUEUE_CH_ID, MATCH_REPORT_CH_ID, LEADERBOARD_CH_ID, TUX_TEST_SERVER_CH_ID]

    if (message.author != client.user and message.channel.id in allowedChannels):
        await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="6 mans"))
    print("Logged in as " + client.user.name + " version " + __version__)

    channel = client.get_channel(QUEUE_CH_ID)
    await channel.send(embed=AdminEmbed(
        title="Norm Started",
        desc="Current version: v{0}".format(__version__)
    ))


async def list_servers():

    await client.wait_until_ready()
    channel = client.get_channel(QUEUE_CH_ID)

    while True:

        if (Jason.getQueueTime() >= 6 and Jason.getQueueLength() != 0):
            Jason.clearQueue()
            embed = InfoEmbed(
                title="Stale Queue Update",
                desc="The queue has been inactive for 1 hr and has now been reset."
            )

            try:
                await channel.send(embed=embed)
            except Exception:
                print("! Norm does not have access to post in the queue channel.")
                return

        elif (Jason.getQueueTime() != 0):
            timeSpent = Jason.getQueueTime() * 10
            timeLeft = 60 - timeSpent

            if(timeLeft == 30 or timeLeft == 10):
                embed = InfoEmbed(
                    title="Stale Queue Update",
                    desc="Inactive for " + str(timeSpent) + " min. Queue will clear in " + str(timeLeft) + " min."
                )

            try:
                await channel.send(embed=embed)
            except Exception:
                print("! Norm does not have access to post in the queue channel.")
                return

        if (Jason.getQueueLength() != 0):
            Jason.incrementTimer()

        await asyncio.sleep(600)

'''
    Discord Commands - Queue Commands
'''


@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(ctx, quiet=False):
    queue_length = Jason.getQueueLength()
    player = ctx.message.author

    if (Jason.queueAlreadyPopped()):
        embed = ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Please wait until current lobby has been set.",
        )

    elif(Jason.isPlayerInQueue(player)):
        embed = ErrorEmbed(
            title="Already in Queue",
            desc="You are already in the queue, dummy.",
        )

    elif (Leaderboard.isPlayerInActiveMatch(str(player))):
        embed = ErrorEmbed(
            title="Match Still Active",
            desc="Your previous match has not been reported yet."
            " Report your match in <#{0}> and try again.".format(MATCH_REPORT_CH_ID),
        )

    elif(queue_length == 0):
        Jason.addToQueue(player)

        if (quiet):
            embed = QueueUpdateEmbed(
                title="Queue has Started :shushing_face:",
                desc="{0} wants to queue!\n\nType **!q** to join".format(player.mention),
            )
        else:
            embed = QueueUpdateEmbed(
                title="Queue has Started!",
                desc="@here\n\n{0} wants to queue!\n\nType **!q** to join".format(player.mention),
            )

    elif(queue_length >= 6):
        embed = ErrorEmbed(
            title="Queue Already Full",
            desc="Queue is already full, please wait until the current queue is set and try again.",
        )

    elif(queue_length == 5):
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        embed = QueueUpdateEmbed(
            title="Queue Popped!",
            desc=player.mention + " added to the queue!" + "\n\n"
            "Queue size: " + str(queue_length + 1) + "/6\n\n"
            "Current queue:\n" + playerList + "\n\n"
            "**Queue is now full!** \n\n"
            "Type !random for random teams.\n"
            "Type !captains to get picked last."
        )

    else:
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        embed = QueueUpdateEmbed(
            title="Player Added to Queue",
            desc=player.mention + " has been added to the queue!\n\n"
            "Queue size: " + str(queue_length + 1) + "/6\n\n"
            "Current queue:\n" + playerList
        )

    await ctx.send(embed=embed)


@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(ctx):
    await q(ctx, quiet=True)


@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(ctx):
    player = ctx.message.author
    username = player.display_name

    if (Jason.queueAlreadyPopped()):
        embed = ErrorEmbed(
            title="Queue Already Popped",
            desc="TOO LATE! You should've left before captains were picked."
        )

    elif(Jason.isPlayerInQueue(player)):

        Jason.removeFromQueue(player)
        playerList = Jason.getQueueList()

        if(Jason.getQueueLength() != 0):
            embed = QueueUpdateEmbed(
                title="Player Left Queue",
                desc=username + " has left the queue.\n\n"
                "Queue size: " + str(Jason.getQueueLength()) + "/6\n\n"
                "Remaining players:\n" + playerList
            )
        else:
            embed = QueueUpdateEmbed(
                title="Player Left Queue",
                desc=username + " has left the queue.\n\n"
                "Queue is now empty."
            )
    else:
        embed = ErrorEmbed(
            title="Not in Queue",
            desc="You are not in the queue, type **!q** to join"
        )

    await ctx.send(embed=embed)


@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(ctx):
    player = ctx.message.mentions[0]

    if (not Jason.isBotAdmin(ctx.message.author.roles)):
        embed = ErrorEmbed(
            title="Permission Denied",
            desc="You do not have the leg strength to kick other players."
        )

    elif (len(ctx.message.mentions) != 1):
        embed = ErrorEmbed(
            title="Did Not Mention a Player",
            desc="Please mention a player in the queue to kick."
        )

    elif (Jason.queueAlreadyPopped()):
        embed = ErrorEmbed(
            title="Queue Already Popped",
            desc="Can't kick players while picking teams."
        )

    elif(Jason.getQueueLength() == 0):
        embed = ErrorEmbed(
            title="Queue is Empty",
            desc="The queue is empty, what are you doing?"
        )

    if (Jason.isPlayerInQueue(player)):
        Jason.removeFromQueue(player)
        embed = AdminEmbed(
            title="Kicked Player",
            desc="Removed " + player.display_name + " from the queue"
        )

    else:
        embed = ErrorEmbed(
            title="User Not in Queue",
            desc="To see who is in current queue, type: **!list**"
        )

    await ctx.send(embed=embed)


@client.command(name='flip', aliases=['coinflip', 'chance', 'coin'], pass_context=True)
async def coinFlip(ctx):
    if (random.randint(1, 2) == 1):
        await q(ctx, quiet=False)
    else:
        await leave(ctx)


@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status', 'showmethefknqueue', '<:who:599055076639899648>'], pass_context=True)  # noqa
async def listq(ctx):
    if (Jason.getQueueLength() == 0):
        embed = QueueUpdateEmbed(
            title="Queue is Empty",
            desc="Join the queue by typing **!q**"
        )
    elif (Jason.queueAlreadyPopped()):
        await captains(ctx)
        return
    else:
        playerList = Jason.getQueueList()
        embed = QueueUpdateEmbed(
            title="Current Queue",
            desc="Queue size: " + str(Jason.getQueueLength()) + "/6\n\n" + "Current queue:\n" + playerList
        )

    await ctx.send(embed=embed)


@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(ctx):
    if (Jason.queueAlreadyPopped()):
        embed = ErrorEmbed(
            title="Captains Already Chosen",
            desc="You cannot change your mind once you pick captains."
        )
    elif(Jason.getQueueLength() != 6):
        embed = ErrorEmbed(
            title="Queue is Not Full",
            desc="You cannot pop a queue until is full."
        )
    else:
        blueTeam, orangeTeam = Jason.randomPop()
        Leaderboard.startMatch(blueTeam, orangeTeam)

        embed = QueueUpdateEmbed(
            title="Teams are Set!",
            desc=""
        ).add_field(
            name="🔷 BLUE TEAM 🔷",
            value="\n".join([player.mention for player in blueTeam]),
            inline=False
        ).add_field(
            name="🔶 ORANGE TEAM 🔶",
            value="\n".join([player.mention for player in orangeTeam]),
            inline=False
        )

    await ctx.send(embed=embed)


@client.command(name='captains', aliases=['cap', 'iwanttopickteams', 'Captains', 'captain', 'Captain', 'Cap'], pass_context=True)  # noqa
async def captains(ctx):
    if (Jason.queueAlreadyPopped()):
        blueCap, orangeCap = Jason.captainsPop()
        playerList = Jason.getQueueList()
        blueTeam, _ = Jason.getTeamList()

        embed = InfoEmbed(
            title="Captains Already Set",
            desc="🔷 BLUE Team Captain 🔷: " + blueCap.mention +
            "\n\n🔶 ORANGE Team Captain 🔶: " + orangeCap.mention
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        )

        if (len(blueTeam) == 1):
            embed.add_field(
                name="It is 🔷 BLUE Team's 🔷 turn to pick",
                value="Type **!pick** and mention a player from the queue below.",
                inline=False
            )
        else:
            embed.add_field(
                name="It is 🔶 ORANGE Team's 🔶 turn to pick",
                value="Please pick two players.\nEx: `!pick @Twan @Tux`",
                inline=False
            )

        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="Available picks",
            value=playerList,
            inline=False
        )
    elif (Jason.getQueueLength() != 6):
        embed = ErrorEmbed(
            title="Queue is Not Full",
            desc="You cannot pop a queue until is full."
        )
    else:
        blueCap, orangeCap = Jason.captainsPop()
        playerList = Jason.getQueueList()

        embed = QueueUpdateEmbed(
            title="Captains",
            desc="🔷 BLUE Team Captain 🔷: " + blueCap.mention +
            "\n\n🔶 ORANGE Team Captain 🔶: " + orangeCap.mention
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="🔷 BLUE Team 🔷 picks first",
            value="Type **!pick** and mention a player from the queue below.",
            inline=False
        ).add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        ).add_field(
            name="Available picks",
            value=playerList,
            inline=False
        )

    await ctx.send(embed=embed)


def blueTeamPick(ctx):
    """
    Helper function for the !pick command when blue team is picking.

    Parameters:
        ctx (Discord Context): The ctx passed into the !pick command.

    Returns:
        Discord.Embed: An embedded message to send.

    """
    if len(ctx.message.mentions) == 0:
        embed = ErrorEmbed(
            title="No Mentioned Player",
            desc="No one was mentioned, please pick an available player."
        )
    elif len(ctx.message.mentions) != 1:
        embed = ErrorEmbed(
            title="Too Many Mentioned Players",
            desc="More than one player mentioned, please pick just one player."
        )
    else:

        errorMsg = Jason.pick(ctx.message.mentions[0])

        if (errorMsg == ""):
            playerList = Jason.getQueueList()

            embed = QueueUpdateEmbed(
                title="Player Added to Team",
                desc=ctx.message.mentions[0].mention + " was added to 🔷 BLUE TEAM 🔷"
            ).add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            ).add_field(
                name="🔶 ORANGE team 🔶 please pick TWO players.",
                value="Ex: `!pick @Twan @Tux`",
                inline=False
            ).add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            ).add_field(
                name="Available picks",
                value=playerList,
                inline=False
            )
        else:
            embed = ErrorEmbed(
                title="Player Not in Queue",
                desc=errorMsg
            )

    return embed


async def orangeTeamPick(ctx):
    """
    Helper function for the !pick command when orange team is picking.

    Parameters:
        ctx (Discord Context): The ctx passed into the !pick command.

    Returns:
        Discord.Embed: An embedded message to send.

    """
    if len(ctx.message.mentions) == 0:
        embed = ErrorEmbed(
            title="No Mentioned Player",
            desc="No one was mentioned, please pick an available player."
        )

    elif len(ctx.message.mentions) != 2:
        embed = ErrorEmbed(
            title="Incorrect Format",
            desc="Use format: `!pick @player1 @player2`"
        )
        # this was where you could just pick one player at a time, but it seemed to break
        # so I just removed it for now

    else:

        errorMsg = Jason.pick(ctx.message.mentions[0], ctx.message.mentions[1])

        if (errorMsg == ""):
            [player1, player2] = ctx.message.mentions
            blueTeam, orangeTeam = Jason.getTeamList()

            embed = QueueUpdateEmbed(
                title="Final Players Added",
                desc="🔶 ORANGE TEAM 🔶 picked " + player1.mention + " & " + player2.mention +
                "\n\nLast player added to 🔷 BLUE TEAM 🔷"
            )

            await ctx.send(embed=embed)

            embed = QueueUpdateEmbed(
                title="Teams are Set!",
                desc=""
            ).add_field(
                name="🔷 BLUE TEAM 🔷",
                value="\n".join([player.mention for player in blueTeam]),
                inline=False
            ).add_field(
                name="🔶 ORANGE TEAM 🔶",
                value="\n".join([player.mention for player in orangeTeam]),
                inline=False
            )

            Leaderboard.startMatch(blueTeam, orangeTeam)
            Jason.clearQueue()
        else:
            embed = ErrorEmbed(
                title="Player(s) Not Found",
                desc="Either one or both of the players you mentioned is not in the queue. Try again."
            )

    return embed


@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(ctx):
    if (not Jason.queueAlreadyPopped()):
        embed = ErrorEmbed(
            title="Captains Not Set",
            desc="If queue is full, please type **!captains**"
        )

    elif(Jason.validateBluePick(ctx.message.author)):
        embed = blueTeamPick(ctx)

    elif(Jason.validateOrangePick(ctx.message.author)):
        embed = await orangeTeamPick(ctx)

    else:
        blueCap, orangeCap = Jason.captainsPop()
        blueTeam, _ = Jason.getTeamList()
        if (len(blueTeam) == 1):
            embed = ErrorEmbed(
                title="Not the Blue Captain",
                desc="You are not 🔷 BLUE Team Captain 🔷\n\n"
                "🔷 BLUE Team Captain 🔷 is: " + blueCap.mention
            )
        else:
            embed = ErrorEmbed(
                title="Not the Orange Captain",
                desc="You are not 🔶 ORANGE Team Captain 🔶 \n\n"
                "🔶 ORANGE Team Captain 🔶 is: " + orangeCap.mention
            )

    await ctx.send(embed=embed)


@client.command(name="report", pass_contex=True)
async def reportMatch(ctx, *arg):
    player_reporting = str(ctx.message.author)

    if (
        ctx.message.channel.id != MATCH_REPORT_CH_ID
        and ctx.message.channel.id != QUEUE_CH_ID
        and not Jason.isBotAdmin(ctx.message.author.roles)
    ):
        embed = ErrorEmbed(
            title="Can't Do That Here",
            desc="You can only report matches in the <#{0}> and <#{1}> channels.".format(
                MATCH_REPORT_CH_ID, QUEUE_CH_ID
            )
        )

    elif (len(arg) == 1 and (str(arg[0]).lower() == "blue" or str(arg[0]).lower() == "orange")):
        msg = Leaderboard.reportMatch(player_reporting, arg[0])

        if (":x:" in msg):
            embed = ErrorEmbed(
                title="Match Not Found",
                desc=msg[4:]
            )
        elif (":white_check_mark:" in msg):
            embed = QueueUpdateEmbed(
                title="Match Reported",
                desc=msg[19:]
            )

            try:
                # if match was reported successfully, update leaderboard channel
                await updateLeaderboardChannel()
            except Exception:
                print("! Norm does not have access to update the leaderboard.")
        else:
            embed = InfoEmbed(
                title="Match Reported, Needs Confirmation",
                desc=msg
            )
    else:
        embed = ErrorEmbed(
            title="Incorrect Report Format",
            desc="Report only accepts 'blue' or 'orange' as the winner of the match.\n\n"
            "Use the format: `!report blue`"
        )

    await ctx.send(embed=embed)


@client.command(name="leaderboard", aliases=["standings", "rank", "rankings", "stonks"], pass_contex=True)
async def showLeaderboard(ctx, *arg):

    playerMentioned: bool = len(ctx.message.mentions) == 1
    selfRank: bool = len(arg) == 1 and arg[0] == "me"

    if (playerMentioned or selfRank):

        if (playerMentioned):
            player_name = str(ctx.message.mentions[0])
        else:
            player_name = str(ctx.message.author)
        players_rank = Leaderboard.showLeaderboard(player_name)

        if (type(players_rank) == str):
            embed = InfoEmbed(
                title="Leaderboard Placement for {0}".format(player_name),
                desc=players_rank
            )
        else:
            embed = ErrorEmbed(
                title="Not Enough Matches Played",
                desc="{0} has played {1}/5 matches needed to be"
                " on the leaderboard.".format(players_rank[0], players_rank[1])
            )

    elif (len(arg) == 0 and len(ctx.message.mentions) == 0):
        embed = InfoEmbed(
            title="UNCC 6 Mans | Top 5",
            desc=Leaderboard.showLeaderboard(limit=5) +
            "\nTo see the full leaderboard, visit <#{0}>.".format(LEADERBOARD_CH_ID)
        )
    else:
        embed = ErrorEmbed(
            title="Leaderboard Command Help",
            desc="Mention someone to see their rank, use 'me' to see your rank,"
            " include nothing to see the top 5 on the leaderboard."
        )

    await ctx.send(embed=embed)


async def updateLeaderboardChannel():
    """Deletes the old leaderboard and posts the updated one."""
    channel = client.get_channel(LEADERBOARD_CH_ID)
    prev_msg = await channel.fetch_message(channel.last_message_id)
    await channel.delete_messages([prev_msg])
    embed = InfoEmbed(
        title="UNCC 6 Mans | Full Leaderboard",
        desc=Leaderboard.showLeaderboard()
    )
    await channel.send(embed=embed)


@client.command(name="brokenq", aliases=["requeue", "re-q"], pass_contex=True)
async def removeLastPoppedQueue(ctx):
    player = str(ctx.message.author)
    msg = Leaderboard.brokenQueue(player)

    if (":white_check_mark:" in msg):
        embed = QueueUpdateEmbed(
            title="Popped Queue Removed",
            desc="The popped queue has been removed from active matches. You may now re-queue."
        )
    else:
        embed = ErrorEmbed(
            title="Could Not Remove Queue",
            desc=msg
        )

    await ctx.send(embed=embed)


@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(ctx):
    if(Jason.isBotAdmin(ctx.message.author.roles)):
        Jason.clearQueue()
        embed = AdminEmbed(
            title="Queue Cleared",
            desc="The queue has been cleared by an admin.  <:UNCCfeelsgood:538182514091491338>"
        )
    else:
        embed = ErrorEmbed(
            title="Permission Denied",
            desc="You do not have permission to clear the queue."
        )

    await ctx.send(embed=embed)


# Disabling command as it does not work with the new executable.
# TODO: Find a new way to restart Norm since he is now an executable
@client.command(name='restart', aliases=['restartbot'], pass_context=True)
async def restart(ctx):
    await ctx.send(embed=AdminEmbed(
        title="Command Diasbled",
        desc="This command is temporarily disabled."
    ))

    # if(Jason.isBotAdmin(ctx.message.author.roles)):
    #     await ctx.send("Bot restarting...hopefully this fixes everything <:UNCCfeelsgood:538182514091491338>")
    #     os.remove("./data/queue.json")
    #     print("Restarting...")
    #     subprocess.call(["python", ".\\src\\bot.py"])
    #     sys.exit()
    # else:
    #     await ctx.send("You do not have permission to restart me.")


@client.command(name='update', pass_context=True)
async def update(ctx):

    if(Jason.isBotAdmin(ctx.message.author.roles)):
        await ctx.send(embed=AdminEmbed(
            title="Checking For Updates",
            desc="Please hang tight."
        ))
        CheckForUpdates.updateBot()
        await ctx.send(embed=AdminEmbed(
            title="Already Up to Date",
            desc="Current version: v{0}".format(__version__)
        ))
    else:
        await ctx.send(embed=AdminEmbed(
            title="Permission Denied",
            desc="You do not have permission to check for updates."
        ))


'''
    Discord Commands - Easter Eggs
'''


@client.command(name='twan', aliases=['<:twantheswan:540327706076905472>'], pass_context=True)
async def twan(ctx):
    await ctx.send(
        "<:twantheswan:540327706076905472> twantheswan is probably the greatest Rocket League (tm) player to have"
        " ever walked the face of this planet. When he tries, no one ever beats him. If you beat him in a game, he"
        " was letting you win just to make you feel better. ur fkn trash at rl unless u r twantheswan. sub to him on"
        " twitch <:twantheswan:540327706076905472>"
    )


@client.command(name='sad', aliases=[':('], pass_context=True)
async def sad(ctx):
    await ctx.send("This is so sad :frowning: in the chat pls")


@client.command(name='smh', aliases=['myhead'], pass_context=True)
async def smh(ctx):
    randNum = [1, 4, 5, 7, 9, 13, 22, 10, 1, 20, 4, 3, 5, 60,
               7, 8, 90, 2, 1, 2, 3, 1, 5, 4, 3, 2, 3, 1, 2, 3, 4, 5]
    output = "smh"
    output = output + (random.choice(randNum) * " my head")
    await ctx.send(output)


@client.command(name='turhols', aliases=['<:IncognitoTurhol:540327644089155639>'], pass_context=True)
async def turhols(ctx):
    await ctx.send(
        "<:IncognitoTurhol:540327644089155639> turhols in the chat please <:IncognitoTurhol:540327644089155639>"
    )


@client.command(name='pika', aliases=['<:pika:538182616965447706>'], pass_context=True)
async def pika(ctx):
    global pikaO
    output = '<:pika:538182616965447706>' * pikaO
    await ctx.send(output)
    pikaO = pikaO + 1


@client.command(name='zappa', aliases=['zapp', 'zac', '<:zappa:632813684678197268>', '<:zapp:632813709579911179>'], pass_context=True)  # noqa
async def zappa(ctx):
    await ctx.send(
        "<:zappa:632813684678197268> <:zapp:632813709579911179> brainyzac more like brainyWACK amirite...that is"
        " until you get absolutely destroyed by him in 6mans and all the self resprct you had for yourself flies out"
        " the window. Not even sykes can beat him in a 1v1, so what makes you think you can? Do you have 2 emotes in"
        " this server? I didnt think so idiot, so <:zappa:632813684678197268> and <:zapp:632813709579911179> outta"
        " here cuz you're the whack one here <:zappa:632813684678197268> <:zapp:632813709579911179>"
    )


@client.command(name='duis', pass_context=True)
async def duis(ctx):
    await ctx.send(
        "Papa Duis, mor like God Duis. Don't even think about queueing up against him because he will ruin you."
        " You think you're good?\n\nyou think you're good at RL??!?!?!?!?!?!?!?!?!?!?\nfuck no\nyou aren't good.\n"
        "you are shit\nur fkn washed\n You don't even come close to Duis. He will absolutely ruin you without even"
        " looking. His monitor is off 90 percent of the time, eyes closed too. Never doubt the Duis, bitch"
    )


@client.command(name='normq', pass_context=True)
async def normq(ctx):
    playerList = Jason.getQueueList()
    queueSize = Jason.getQueueLength()

    await ctx.send("Duis says I am not supposed to queue, but I don't listen to players worse than me...")
    await ctx.send("!q")

    if (Jason.queueAlreadyPopped() or queueSize == 6):
        embed = ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Whoa there Norm! You can't queue until the current queue has finished popping."
        )
    elif (len(playerList) == 0):
        embed = QueueUpdateEmbed(
            title="Norm has Started the Queue!",
            desc="<@629502587963572225> wants to queue!\n\nType **!q** to join",
        )
    else:
        embed = QueueUpdateEmbed(
            title="Norm Added to Queue",
            desc="<@629502587963572225> has been added to the queue!\n\n"
            "Queue size: " + str(queueSize + 1) + "/6\n\n"
            "Current queue:\nNorm" + (" " if len(playerList) == 0 else ", ") + playerList
        )

    await ctx.send(embed=embed)


@client.command(name='teams', aliases=['uncc'], pass_context=True)
async def teams(ctx):
    await ctx.send(
        "it goes like this:\n"
        "A team: doesn't practice but somehow is good"
        "\nB team: everyone hates how their teamates play but don't talk it out to resolve issues"
        "\nC team: who?"
        "\nD team: best team"
        "\nE team: surprisingly solid"
        "\nF team: how many fkn teams do we have"
        "\nGG team: originally g team"
    )


@client.command(name='8ball', aliases=['norm', 'asknorm', 'eight_ball', 'eightball', '8-ball'], pass_context=True)
async def eight_ball(ctx):
    """
    :param ctx: The question the user is wanting to ask
    :return: Answer to the question
    """
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Ask papa Duis',
        'As I see it, yes',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don’t count on it',
        'It is certain',
        'It is decidedly so',
        'Most likely',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Reply hazy try again',
        'Signs point to yes',
        'Very doubtful',
        'Without a doubt',
        'Yes',
        'Yes, definitely',
        'You may rely on it',
        'shut up',
        'Some questions are best left unanswered...',
        'no',
        'Absolutely not',
    ]
    await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(ctx):
    await ctx.send("u")


@client.command(name="help", pass_context=True)
async def help(ctx):
    msg = discord.Embed(
        title='__**Server Commands**__',
        description="",
        color=0x38761D
    )
    msg.add_field(
        name="!q",
        value="Adds you to the queue",
        inline=False
    )
    msg.add_field(
        name="!qq",
        value="Same as !q but with no ping :)",
        inline=False
    )
    msg.add_field(
        name="!leave",
        value="Removes you from the queue",
        inline=False
    )
    msg.add_field(
        name="!kick",
        value="Kicks someone from the queue, will require a vote",
        inline=False
    )
    msg.add_field(
        name="!list",
        value="Lists the current queue",
        inline=False
    )
    msg.add_field(
        name="!random",
        value="Randomly picks teams",
        inline=False
    )
    msg.add_field(
        name="!captains",
        value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two",
        inline=False
    )
    msg.add_field(
        name="!report",
        value="Reports the result of your queue. Use this command followed by the color of the winning team.",
        inline=False
    )
    msg.add_field(
        name="!leaderboard",
        value="Shows the top 5 players on the leaderboard.",
        inline=False
    )
    msg.add_field(
        name="!leaderboard me",
        value="Shows your rank on the leaderboard.",
        inline=False
    )
    msg.add_field(
        name='!norm, !asknorm, or !8ball',
        value='Will respond to a yes/no question. Good for predictions',
        inline=False
    )
    msg.add_field(
        name="!help",
        value="This command :O",
        inline=False
    )
    msg.set_thumbnail(url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/49ers.png")
    msg.set_footer(text="Developed by Twan, Clam, and Tux")
    await ctx.send(embed=msg)


'''
    Main function
'''


def main():
    checkProgramFiles()
    client.loop.create_task(list_servers())
    token = Jason.getDiscordToken()

    if (token == ""):
        token = Jason.updateDiscordToken(
            input("No Discord Bot token found. Paste your Discord Bot token below and hit ENTER.\ntoken: ")
        )

    # clear screen to hide token
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print(
            "! There was an error with the token you provided. Please verify your bot token and try again.\n"
            "If you need help locating the token for your bot, visit https://www.writebots.com/discord-bot-token/"
        )
        os.remove("{0}/SixMans/config.json".format(Path.home()))
        time.sleep(5)
    except Exception:
        pass


if __name__ == "__main__":
    main()
