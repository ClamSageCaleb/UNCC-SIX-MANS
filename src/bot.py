__author__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__license__ = "MIT"
__version__ = "6.0.0"
__maintainer__ = "Caleb Smith / Twan / Matt Wells (Tux)"
__email__ = "caleb.benjamin9799@gmail.com / unavailable / mattwells878@gmail.com"


import AWSHelper as AWS
from DataFiles import getDiscordToken, updateDiscordToken, getChannelIds
from EmbedHelper import ErrorEmbed, QueueUpdateEmbed, InfoEmbed, AdminEmbed
import Queue
from asyncio import sleep as asyncsleep
import discord
from discord.ext.commands import Bot, CommandNotFound
from os import name as osName, system as osSystem
from random import choice, randint
from time import sleep

from Commands import EasterEggs, SixMans, Testing, Admin, Utils

# Bot prefix and Discord Bot token
BOT_PREFIX = ("!")

# Creates the Bot with name 'client'
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

pikaO = 1

# Channel ID's
LEADERBOARD_CH_ID = -1
QUEUE_CH_IDS = []
REPORT_CH_IDS = []

# Leaderboard Channel Object
LB_CHANNEL: discord.channel = None

"""
    Discord Events
"""


@client.event
async def on_message(message: discord.Message):
    isReport = "report" in message.content.lower()
    if (message.author != client.user):

        if (
            isReport and
            len(QUEUE_CH_IDS) > 0 and
            message.channel.id in QUEUE_CH_IDS and
            message.channel.id not in REPORT_CH_IDS
        ):
            channel = client.get_channel(message.channel.id)
            await channel.send(embed=ErrorEmbed(
                title="Can't Do That Here",
                desc="You can only report matches in the <#{0}> channel.".format(REPORT_CH_IDS[0])
            ))

        elif (
            not isReport and
            len(REPORT_CH_IDS) > 0 and
            message.channel.id in REPORT_CH_IDS and
            message.channel.id not in QUEUE_CH_IDS
        ):
            channel = client.get_channel(message.channel.id)
            await channel.send(embed=ErrorEmbed(
                title="Can't Do That Here",
                desc="You can only use that command in the <#{0}> channel.".format(QUEUE_CH_IDS[0])
            ))
        else:
            await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    print(error)


@client.event
async def on_ready():
    global LB_CHANNEL

    await client.change_presence(activity=discord.Game(name="6 mans"))
    print("Logged in as " + client.user.name + " version " + __version__)

    try:
        AWS.readRemoteLeaderboard()
        if (LEADERBOARD_CH_ID != -1):
            LB_CHANNEL = client.get_channel(LEADERBOARD_CH_ID)
            await Utils.updateLeaderboardChannel(LB_CHANNEL)  # update leaderboard channel when remote leaderboard pulls
    except Exception as e:
        # this should only throw an exception if the Leaderboard file does not exist or the credentials are invalid
        print(e)

    try:
        channel = client.get_channel(QUEUE_CH_IDS[0])
        await channel.send(embed=AdminEmbed(
            title="Norm Started",
            desc="Current version: v{0}".format(__version__)
        ))
    except Exception as e:
        print("! Norm does not have access to post in the queue channel.", e)


async def stale_queue_timer():

    await client.wait_until_ready()
    channel = client.get_channel(QUEUE_CH_IDS[0])

    while True:

        if (Queue.getQueueLength() > 0 and not Queue.queueAlreadyPopped()):
            warn_players, removed_players = Queue.checkQueueTimes()

            if (len(warn_players) > 0 or len(removed_players) > 0):
                embeds = []

                if (len(warn_players) > 0):
                    warn_str = ",".join([player.mention for player in warn_players])
                    embeds.append(InfoEmbed(
                        title="Stale Player Queue Warning",
                        desc=warn_str + " will be removed from the queue in 5 minutes.\n\n"
                        "To stay in the queue, type **!q**"
                    ))
                if (len(removed_players) > 0):
                    rem_str = ",".join([player.mention for player in removed_players])
                    playerList = Queue.getQueueList()
                    if(Queue.getQueueLength() != 0):
                        embeds.append(QueueUpdateEmbed(
                            title="Queue Stale Players Removed",
                            desc=rem_str + " have been removed from the queue.\n\n" +
                            "Queue size: " + str(Queue.getQueueLength()) + "/6\n\n"
                            "Remaining players:\n" + playerList
                        ))
                    else:
                        embeds.append(QueueUpdateEmbed(
                            title="Queue Stale Players Removed",
                            desc=rem_str + " have been removed from the queue.\n\n" + "Queue is now empty."
                        ))
                try:
                    for embed in embeds:
                        await channel.send(embed=embed)
                except Exception as e:
                    print("! Norm does not have access to post in the queue channel.", e)
                    return

        await asyncsleep(60)  # check queue times every minute

"""
    Discord Commands - Queue Commands
"""


@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(ctx, *arg):
    await ctx.send(embed=await SixMans.playerQueue(ctx, *arg))


@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(ctx, *arg):
    await ctx.send(embed=await SixMans.playerQueue(ctx, *arg, quiet=True))


@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(ctx):
    await ctx.send(embed=SixMans.leave(ctx.message.author))


@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(ctx):
    await ctx.send(embed=SixMans.kick(ctx.message.mentions, ctx.message.author.roles))


@client.command(name='flip', aliases=['coinflip', 'chance', 'coin'], pass_context=True)
async def coinFlip(ctx):
    if (randint(1, 2) == 1):
        await q(ctx, quiet=False)
    else:
        await leave(ctx)


@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status', 'showmethefknqueue', '<:who:599055076639899648>'], pass_context=True)  # noqa
async def listq(ctx):
    await ctx.send(embed=SixMans.listQueue(ctx.message.author))


@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def random(ctx):
    await ctx.send(embed=SixMans.random(ctx.message.author))


@client.command(name='captains', aliases=['cap', 'iwanttopickteams', 'Captains', 'captain', 'Captain', 'Cap'], pass_context=True)  # noqa
async def captains(ctx):
    await ctx.send(embed=SixMans.captains(ctx.message.author))


@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(ctx):
    embeds = SixMans.pick(ctx.message.author, ctx.message.mentions)
    for embed in embeds:
        await ctx.send(embed=embed)


@client.command(name="report", pass_contex=True)
async def reportMatch(ctx, *arg):
    await ctx.send(embed=await SixMans.report(ctx.message.author, LB_CHANNEL, *arg))


@client.command(name="leaderboard", aliases=["lb", "standings", "rank", "rankings", "stonks"], pass_contex=True)
async def showLeaderboard(ctx, *arg):
    await ctx.send(embed=SixMans.leaderboard(ctx.message.author, ctx.message.mentions, *arg))


@client.command(name="brokenq", aliases=["requeue", "re-q"], pass_contex=True)
async def removeLastPoppedQueue(ctx):
    await ctx.send(embed=SixMans.brokenQueue(ctx.message.author))


@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(ctx):
    await ctx.send(embed=Admin.clear(ctx.message.author.roles))


@client.command(name="fill", pass_context=True)
async def fill(ctx):
    if (__debug__):
        await ctx.send(embed=Testing.fill(ctx.message.author.roles))


@client.command(name="fillCap", pass_context=True)
async def fillCap(ctx):
    if (__debug__):
        await ctx.send(embed=Testing.fillCap(ctx.message.author.roles))


@client.command(name="flipCap", pass_context=True)
async def flipCap(ctx):
    if (__debug__):
        await ctx.send(embed=Testing.flipCap(ctx.message.author.roles))


@client.command(name="flipReport", pass_context=True)
async def flipReport(ctx):
    if (__debug__):
        await ctx.send(embed=Testing.flipReport(ctx.message.author.roles))


@client.command(name='restart', aliases=['restartbot'], pass_context=True)
async def restart(ctx):
    await ctx.send(embed=Admin.restart())


@client.command(name='update', pass_context=True)
async def update(ctx):
    await ctx.send(embed=Admin.update())


"""
    Discord Commands - Easter Eggs
"""


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
    output = output + (choice(randNum) * " my head")
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
    playerList = Queue.getQueueList()
    queueSize = Queue.getQueueLength()

    await ctx.send("Duis says I am not supposed to queue, but I don't listen to players worse than me...")
    await ctx.send("!q")

    if (Queue.queueAlreadyPopped() or queueSize == 6):
        embed = ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Whoa there Norm! You can't queue until the current queue has finished popping."
        )
    elif (len(playerList) == 0):
        embed = QueueUpdateEmbed(
            title="Norm has Started the Queue!",
            desc="<@629502587963572225> wants to queue!\n\nQueued for 0 minutes.\n\nType **!q** to join",
        )
    else:
        embed = QueueUpdateEmbed(
            title="Norm Added to Queue",
            desc="<@629502587963572225> has been added to the queue for 0 minutes.\n\n"
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
    await ctx.send(choice(possible_responses) + ", " + ctx.message.author.mention)


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(ctx):
    await ctx.send("u")


@client.command(name="help", pass_context=True)
async def help(ctx):
    await ctx.send(
        embed=discord.Embed(
            title="Norm Commands",
            description="https://clamsagecaleb.github.io/UNCC-SIX-MANS",
            color=0x38761D
        ).add_field(
            name="!q",
            value="Adds you to the queue",
            inline=False
        ).add_field(
            name="!leave",
            value="Removes you from the queue",
            inline=False
        ).add_field(
            name="!list",
            value="Lists the current queue",
            inline=False
        ).add_field(
            name="!random",
            value="Randomly picks teams (Requires 6 players in queue)",
            inline=False
        ).add_field(
            name="!captains",
            value="Randomly selects captains (Requires 6 players in queue)."
            "\nFirst captain picks 1 \nSecond captain picks the next two",
            inline=False
        ).add_field(
            name="!report",
            value="Reports the result of your queue. Use this command followed by the color of the winning team.",
            inline=False
        ).add_field(
            name="!leaderboard",
            value="Shows the top 5 players on the leaderboard.",
            inline=False
        ).add_field(
            name="!leaderboard me",
            value="Shows your rank on the leaderboard.",
            inline=False
        ).add_field(
            name='!norm, !asknorm, or !8ball',
            value='Will respond to a yes/no question. Good for predictions',
            inline=False
        ).add_field(
            name="!help",
            value="This command :O",
            inline=False
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/49ers.png"
        ).set_footer(
            text="Developed by Twan, Clam, and Tux"
        )
    )


"""
    Main function
"""


def main():
    global LEADERBOARD_CH_ID, QUEUE_CH_IDS, REPORT_CH_IDS

    token = getDiscordToken()
    if (token == ""):
        token = updateDiscordToken(
            input("No Discord Bot token found. Paste your Discord Bot token below and hit ENTER.\ntoken: ")
        )

    # clear screen to hide token
    if osName == 'nt':
        _ = osSystem('cls')
    else:
        _ = osSystem('clear')

    AWS.init()

    channels = getChannelIds()
    LEADERBOARD_CH_ID = channels["leaderboard_channel"]
    QUEUE_CH_IDS = channels["queue_channels"]
    REPORT_CH_IDS = channels["report_channels"]

    if (len(QUEUE_CH_IDS) > 0):
        client.loop.create_task(stale_queue_timer())
    else:
        print("Stale queue feature disabled as no queue channel id was specified.")

    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print(
            "! There was an error with the token you provided. Please verify your bot token and try again.\n"
            "If you need help locating the token for your bot, visit https://www.writebots.com/discord-bot-token/"
        )
        sleep(5)
    except Exception:
        pass


if __name__ == "__main__":
    main()
