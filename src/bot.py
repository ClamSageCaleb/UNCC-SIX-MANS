__author__ = "Caleb Smith / Twan / Matt Wells (Tux) / Austin Baker (h)"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan / Matt Wells (Tux) / Austin Baker (h)"
__license__ = "MIT"
__version__ = "7.0.0"
__maintainer__ = "Caleb Smith / Twan / Matt Wells (Tux) / Austin Baker (h)"
__email__ = "caleb.benjamin9799@gmail.com / unavailable / mattwells878@gmail.com / noise.9no@gmail.com"


import AWSHelper as AWS
from DataFiles import getDiscordToken, updateDiscordToken, getChannelIds
from EmbedHelper import AdminEmbed, HelpEmbed
from SendMessageHelper import sendMessage
from asyncio import sleep as asyncsleep
import discord
from discord.ext.commands import Bot, CommandNotFound
from os import name as osName, system as osSystem
from random import randint
from time import sleep
from typing import List
from Commands import EasterEggs, SixMans, Testing, Admin, Utils
from discord.embeds import Embed
import Queue

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

# Valid Command List that has reactions sent upon being called.
valid_commands = [
    "q",
    "addmepapanorm",
    "Q",
    "addmebitch",
    "queue",
    "join",
    "qq",
    "quietq",
    "QQ",
    "quietqueue",
    "shh",
    "dontping",
    "kick",
    "remove",
    "yeet",
    "flip",
    "coinflip",
    "chance",
    "coin",
    "brokenq",
    "requeue",
    "re-q",
    "clear",
    "clr",
    "reset",
    "fill",
    "fillCap",
    "flipCap",
    "flipReport",
    "update",
    "leaderboard",
    "lb",
    "standings",
    "rank",
    "rankings",
    "stonks",
]


@client.event
async def on_message(message: discord.Message):
    if (message.author != client.user):
        if (message.reference is not None):
            replied_to_msg = await message.channel.fetch_message(message.reference.message_id)
            if (any(queue_cmd == message.content.split(" ")[0][1:] for queue_cmd in valid_commands)):
                replied_to_msg_embed = replied_to_msg.embeds
                if (any(embed.title == "Teams are Set!" for embed in replied_to_msg_embed)):
                    await client.process_commands(message)
                    await message.delete()
                else:
                    await replied_to_msg.delete()
                    await client.process_commands(message)
                    await message.delete()
            elif (any(cmd == message.content.split(" ")[0][1:] for cmd in EasterEggs.egg_commands)):
                await client.process_commands(message)
        elif (message.reference is None):
            if (any(cmd == message.content.split(" ")[0][1:] for cmd in EasterEggs.egg_commands)):
                await client.process_commands(message)
                return


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    print(error)


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    global LB_CHANNEL

    if (not user.bot):
        channel = client.get_channel(QUEUE_CH_IDS[0])

        # regional indicator b
        if (reaction.emoji == "\U0001F1E7" and Queue.isBotAdmin(user.roles)):
            await reaction.message.delete()
            await sendMessage(channel, Admin.brokenQueue(user, user.roles), None)
            await sendMessage(channel, SixMans.listQueue(user), "queue")
            return

        elif (reaction.emoji == "🛑" and Queue.isBotAdmin(user.roles)):
            await reaction.message.delete()
            await sendMessage(channel, Admin.clear(user.roles), None)
            await sendMessage(channel, SixMans.listQueue(user), "queue")
            return

        # Check to validate reaction is valid by seeing if Norm also reacted with the same reaction
        reacted_users = await reaction.users().flatten()
        if (not any(reacted_user.id == client.user.id for reacted_user in reacted_users)):
            return

        blueTeam, orangeTeam = Queue.getTeamList()

        if (reaction.emoji == "✅"):
            await reaction.message.delete()
            messages = SixMans.playerQueue(user)
            for msg in messages:
                await sendMessage(
                    channel,
                    msg,
                    "popped" if msg.title == "Queue Popped!" or Queue.getQueueLength() == 6 else "queue"
                )

        elif (reaction.emoji == "❌"):
            await reaction.message.delete()
            await sendMessage(channel, SixMans.leave(user), "queue" if Queue.getQueueLength() < 6 else "popped")

        elif (reaction.emoji == "🤫"):
            await reaction.message.delete()
            messages = SixMans.playerQueue(user, quiet=True)
            for msg in messages:
                await sendMessage(
                    channel,
                    msg,
                    "popped" if msg.title == "Queue Popped!" or Queue.getQueueLength() == 6 else "queue"
                )

        elif (reaction.emoji == "🔢"):
            await reaction.message.delete()
            top_5 = []
            await sendMessage(
                channel,
                SixMans.leaderboard(client.user.name, top_5, LEADERBOARD_CH_ID),
                "popped" if Queue.getQueueLength() == 6 else "queue"
            )

        elif (reaction.emoji == "❓"):
            await reaction.message.delete()
            if (len(blueTeam) >= 1):
                await sendMessage(channel, HelpEmbed(), None)
                await sendMessage(channel, SixMans.listQueue(user), "picks")
            elif (Queue.getQueueLength() == 6 and len(blueTeam) == 0):
                await sendMessage(channel, HelpEmbed(), None)
                await sendMessage(channel, SixMans.listQueue(user), "popped")
            else:
                await sendMessage(channel, HelpEmbed(), None)
                await sendMessage(channel, SixMans.listQueue(user), "queue")

        # regional indicator C
        elif (reaction.emoji == "\U0001F1E8"):
            await reaction.message.delete()
            if (Queue.isPlayerInQueue(user)):
                await sendMessage(channel, SixMans.captains(user), "picks")
            elif (not Queue.isPlayerInQueue(user) and Queue.getQueueLength() == 6):
                await sendMessage(channel, SixMans.captains(user), "popped")
            else:
                await sendMessage(channel, SixMans.listQueue(user), "queue")

        # regional indicator R
        elif (reaction.emoji == "\U0001F1F7"):
            await reaction.message.delete()
            if (Queue.isPlayerInQueue(user)):
                await sendMessage(channel, SixMans.random(user), "active")
                await sendMessage(channel, SixMans.listQueue(user), "queue")
            elif (not Queue.isPlayerInQueue(user) and Queue.getQueueLength() == 6):
                await sendMessage(channel, SixMans.random(user), "popped")
            else:
                await sendMessage(channel, SixMans.listQueue(user), "queue")

        # regional indicator L
        elif (reaction.emoji == "\U0001F1F1"):
            await reaction.message.delete()
            if (len(blueTeam) == 0 and Queue.getQueueLength() != 6):
                await sendMessage(channel, SixMans.listQueue(user), "queue")
            elif (Queue.getQueueLength() == 6 and len(blueTeam) == 0):
                await sendMessage(channel, SixMans.listQueue(user), "popped")
            else:
                await sendMessage(channel, SixMans.listQueue(user), "picks")

        elif (reaction.emoji == "1️⃣"):
            await reaction.message.delete()
            if (len(orangeTeam) == 2 and Queue.validateOrangePick(user)):
                await sendMessage(channel, SixMans.pick(user, 1), "active")
                await sendMessage(channel, SixMans.listQueue(user), "queue")
            else:
                await sendMessage(channel, SixMans.pick(user, 1), "picks")

        elif (reaction.emoji == "2️⃣"):
            if (len(orangeTeam) == 2 and Queue.validateOrangePick(user)):
                await reaction.message.delete()
                await sendMessage(channel, SixMans.pick(user, 2), "active")
                await sendMessage(channel, SixMans.listQueue(user), "queue")
            else:
                await reaction.message.delete()
                await sendMessage(channel, SixMans.pick(user, 2), "picks")

        elif (reaction.emoji == "3️⃣"):
            await reaction.message.delete()
            await sendMessage(channel, SixMans.pick(user, 3), "picks")

        elif (reaction.emoji == "4️⃣"):
            await reaction.message.delete()
            await sendMessage(channel, SixMans.pick(user, 4), "picks")

        elif (reaction.emoji == "🔷"):
            response = await SixMans.report(user, LB_CHANNEL, "blue")
            if (response):
                await reaction.message.add_reaction("👍")

        elif (reaction.emoji == "🔶"):
            response = await SixMans.report(user, LB_CHANNEL, "orange")
            if (response):
                await reaction.message.add_reaction("👍")

        elif (reaction.emoji == "💔" and reaction.count >= 5):  # majority vote is 4 + 1 for the bot reaction
            await sendMessage(channel, SixMans.brokenQueue(user), "queue")


@client.event
async def on_ready():
    global LB_CHANNEL

    await client.change_presence(activity=discord.Game(name="6 mans"))
    print("Logged in as " + client.user.name + " version " + __version__)

    try:
        channel = client.get_channel(QUEUE_CH_IDS[0])
        await sendMessage(channel, AdminEmbed(
            title="Norm Started",
            desc="Current version: v{0}".format(__version__)
        ), None)
        await sendMessage(channel, SixMans.listQueue(client.user.name), "queue")

    except Exception as e:
        print("! Norm does not have access to post in the queue channel.", e)

    try:
        AWS.readRemoteLeaderboard()
        if (LEADERBOARD_CH_ID != -1):
            LB_CHANNEL = client.get_channel(LEADERBOARD_CH_ID)
            # update leaderboard channel when remote leaderboard pulls
            await Utils.updateLeaderboardChannel(LB_CHANNEL)
    except Exception as e:
        # this should only throw an exception if the Leaderboard file does not exist or the credentials are invalid
        print(e)


async def stale_queue_timer():
    await client.wait_until_ready()
    channel = client.get_channel(QUEUE_CH_IDS[0])

    while True:

        embeds = SixMans.checkQueueTimes()

        if (embeds is not None):
            try:
                for embed in embeds:
                    await sendMessage(channel, embed, "queue")
            except Exception as e:
                print("! Norm does not have access to post in the queue channel.", e)
                return

        await asyncsleep(60)  # check queue times every minute

"""
    Discord Commands - Queue Commands
"""


@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(ctx, *arg):
    messages = SixMans.playerQueue(ctx.message.author, *arg)
    for msg in messages:
        if (msg.title == "Queue Popped!"):
            await sendMessage(ctx, msg, "popped")
        else:
            await sendMessage(ctx, msg, "queue")


@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(ctx, *arg):
    messages = SixMans.playerQueue(ctx.message.author, *arg, quiet=True)
    for msg in messages:
        if (msg.title == "Queue Popped!"):
            await sendMessage(ctx, msg, "popped")
        else:
            await sendMessage(ctx, msg, "queue")


@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(ctx, *arg):
    blueTeam, _ = Queue.getTeamList()
    kicking = Admin.kick(ctx.message.content, ctx.message.author.roles, *arg)
    if (len(blueTeam) == 0 and Queue.getQueueLength() != 6):
        await sendMessage(ctx, kicking, "queue")
    elif (Queue.getQueueLength() == 6 and len(blueTeam) == 0):
        await sendMessage(ctx, kicking, "popped")
    elif (len(blueTeam) >= 1):
        await sendMessage(ctx, kicking, "picks")


@client.command(name='flip', aliases=['coinflip', 'chance', 'coin'], pass_context=True)
async def coinFlip(ctx):
    if (randint(1, 2) == 1):
        await q(ctx)
    else:
        await sendMessage(ctx, SixMans.leave(ctx.author), "queue")


@client.command(name="leaderboard", aliases=["lb", "standings", "rank", "rankings", "stonks"], pass_context=True)
async def showLeaderboard(ctx, *arg):
    blueTeam, _ = Queue.getTeamList()
    lb = SixMans.leaderboard(ctx.message.author, ctx.message.content, LEADERBOARD_CH_ID, *arg)
    if (len(blueTeam) == 0 and Queue.getQueueLength() != 6):
        await sendMessage(ctx, lb, "queue")
    elif (Queue.getQueueLength() == 6 and len(blueTeam) == 0):
        await sendMessage(ctx, lb, "popped")
    else:
        await sendMessage(ctx, lb, "picks")


@client.command(name="brokenq", aliases=["requeue", "re-q"], pass_context=True)
async def removeLastPoppedQueue(ctx):
    await sendMessage(ctx, Admin.brokenQueue(ctx.message.author, ctx.message.author.roles), "queue")


@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(ctx):
    await sendMessage(ctx, Admin.clear(ctx.message.author.roles), "queue")


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
    await ctx.send(AdminEmbed(
        title="Checking For Updates",
        desc="Please hang tight."
    ))
    await ctx.send(embed=Admin.update())


"""
    Discord Commands - Easter Eggs
"""


@client.command(name='twan', aliases=['<:twantheswan:540327706076905472>'], pass_context=True)
async def twan(ctx):
    await ctx.reply(EasterEggs.Twan())


@client.command(name='sad', aliases=[':('], pass_context=True)
async def sad(ctx):
    await ctx.reply(EasterEggs.Sad())


@client.command(name='smh', aliases=['myhead'], pass_context=True)
async def smh(ctx):
    await ctx.reply(EasterEggs.Smh())


@client.command(name='turhols', aliases=['<:IncognitoTurhol:540327644089155639>'], pass_context=True)
async def turhols(ctx):
    await ctx.reply(EasterEggs.Turhols())


@client.command(name='pika', aliases=['<:pika:538182616965447706>'], pass_context=True)
async def pika(ctx):
    await ctx.reply(EasterEggs.Pika())


@client.command(name='zappa', aliases=['zapp', 'zac', '<:zappa:632813684678197268>', '<:zapp:632813709579911179>'], pass_context=True)  # noqa
async def zappa(ctx):
    await ctx.reply(EasterEggs.Zappa())


@client.command(name='duis', pass_context=True)
async def duis(ctx):
    await ctx.reply(EasterEggs.Duis())


@client.command(name='furry', pass_context=True)
async def furry(ctx):
    await ctx.reply(EasterEggs.Furry())


@client.command(name='don', pass_context=True)
async def don(ctx):
    await ctx.reply(EasterEggs.Don())


@client.command(name='daffy', pass_context=True)
async def daffy(ctx):
    await ctx.reply(EasterEggs.Daffy())


@client.command(name='giddy', pass_context=True)
async def giddy(ctx):
    await ctx.reply(EasterEggs.Giddy())


@client.command(name='nodought', pass_context=True)
async def nodought(ctx):
    await ctx.reply(EasterEggs.NoDought())


@client.command(name='coolio', pass_context=True)
async def coolio(ctx):
    await ctx.reply(EasterEggs.Coolio())


@client.command(name='normq', pass_context=True)
async def normq(ctx):
    blueTeam, _ = Queue.getTeamList()
    if (len(blueTeam) >= 1):
        await ctx.send("Duis says I am not supposed to queue, but I don't listen to players worse than me...")
        await ctx.send("!q")
        await sendMessage(ctx, EasterEggs.NormQ(), "active")
    else:
        await ctx.send("Duis says I am not supposed to queue, but I don't listen to players worse than me...")
        await ctx.send("!q")
        await sendMessage(ctx, EasterEggs.NormQ(),
                          "queue" if len(blueTeam) == 0 and
                          Queue.getQueueLength() != 6
                          else "popped")


@client.command(name='teams', aliases=['uncc'], pass_context=True)
async def teams(ctx):
    await ctx.reply(EasterEggs.Teams())


@client.command(name='8ball', aliases=['norm', 'asknorm', 'eight_ball', 'eightball', '8-ball'], pass_context=True)
async def eight_ball(ctx):
    await ctx.reply(EasterEggs.EightBall(ctx.message.author))


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(ctx):
    await ctx.reply(EasterEggs.Fuck())


@client.command(name="help", pass_context=True)
async def help(ctx):
    await ctx.send(embed=HelpEmbed())


@client.command(name="oops", pass_context=True)
async def oops(ctx):
    await ctx.reply("I didn't think the queue would pop...")


@client.command(name="h", pass_contex=True)
async def h(ctx):
    await ctx.reply("h")


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
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
