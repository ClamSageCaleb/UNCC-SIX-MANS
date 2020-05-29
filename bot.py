__author__ = "Caleb Smith / Twan"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Caleb Smith / Twan"
__email__ = "caleb.benjamin9799@gmail.com"
__status__ = "Production"


import asyncio
# import aiohttp
import json
import os
import sys
import subprocess
import random
import discord
from discord import Game
from discord.ext.commands import Bot
from dotenv import load_dotenv
import SixMans

# Bot prefix and Discord Bot token
BOT_PREFIX = ("!")
# Add token here
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Creates the Bot with name 'client'
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

# initialize captain mode: 0 for normal, 1 if picking orange team, 2 for picking blue team
botMode = 0
whoO = 1
pikaO = 1
norm = SixMans.SixMans()

# Replaces the basic !help feature, responds with formatted bot commands and usage
@client.event
async def on_message(message):
    """
    :param message: Sent in by the user. Executed by !help
    :return: Formatted command list
    """
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        msg = discord.Embed(title='__**Server Commands**__',
                            description="", color=0x38761D)
        msg.add_field(name="!q", value="Adds you to the queue", inline=False)
        msg.add_field(
            name="!qq", value="Same as !q but with no ping :)", inline=False)
        msg.add_field(
            name="!leave", value="Removes you from the queue", inline=False)
        msg.add_field(
            name="!kick", value="Kicks someone from the queue, will require a vote", inline=False)
        msg.add_field(
            name="!list", value="Lists the current queue", inline=False)
        msg.add_field(name="!random",
                      value="Randomly picks teams", inline=False)
        msg.add_field(
            name="!captains", value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two", inline=False)
        msg.add_field(name='!norm,!asknorm, or !8ball',
                      value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O", inline=False)
        msg.set_thumbnail(
            url="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)


@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(context):
    global norm

    player = context.message.mentions[0]
    return_msg = norm.removeFromQueue(player=player)

    await client.say(return_msg)


@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status', 'showmethefknqueue', '<:who:599055076639899648>'], pass_context=True)
async def listq():
    global norm

    return_msg = norm.listQueue()

    await client.say(return_msg)


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(context):
    await client.say("u")


@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(context):
    global norm

    return_msg = norm.randomPickTeams()

    await client.say(return_msg)


@client.command(name='captains', aliases=['cap', 'iwanttopickteams', 'Captains', 'captain', 'Captain', 'Cap'], pass_context=True)
async def captains(context):
    global norm

    return_msg = norm.pickCaptains()

    await client.say(return_msg)


@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(context):
    global norm

    blueCap, orangeCap = norm.getCaptains()

    team_cap = ''

    if (context.message.author == blueCap):
        team_cap = 'blue'
    elif (context.message.author == orangeCap):
        team_cap = 'orange'

    players = list()
    for p in context.message.mentions:
        players.append(p)

    return_msg = norm.pickTeams(team_cap, players)

    await client.say(return_msg)


@client.command(name='restart', aliases=['restartbot'], pass_context=True)
async def restart(context):
    global pikaO
    for x in context.message.author.roles:
        if(x.name == "Bot Admin"):
            await client.say("Bot restarting...hopefully this fixes everything <:UNCCfeelsgood:538182514091491338>")

            subprocess.call([r'runBot.bat'])
            sys.exit(0)
            return

    await client.say("You do not have permission to restart me.")


@client.command(name='twan', aliases=['<:twantheswan:540327706076905472>'], pass_context=True)
async def twan(context):
    await client.say("<:twantheswan:540327706076905472> twantheswan is probably the greatest Rocket League (tm) player to have ever walked the face of this planet. When he tries, no one ever beats him. If you beat him in a game, he was letting you win just to make you feel better. ur fkn trash at rl unless u r twantheswan. sub to him on twitch <:twantheswan:540327706076905472>")


@client.command(name='sad', aliases=[':('], pass_context=True)
async def sad(context):
    await client.say("This is so sad :frowning: in the chat pls")


@client.command(name='smh', aliases=['myhead'], pass_context=True)
async def smh(context):
    randNum = [1, 4, 5, 7, 9, 13, 22, 10, 1, 20, 4, 3, 5, 60,
               7, 8, 90, 2, 1, 2, 3, 1, 5, 4, 3, 2, 3, 1, 2, 3, 4, 5]
    output = "smh"
    output = output + (random.choice(randNum) * " my head")
    await client.say(output)


@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(context):
    global norm

    for x in context.message.author.roles:
        if(x.name == "Bot Admin"):
            norm.clearAll()
            pikaO = 1
            whoO = 1

            await client.say("Queue cleared <:UNCCfeelsgood:538182514091491338>")
            return

    await client.say("You do not have permission to clear the queue.")


@client.command(name='turhols', aliases=['<:IncognitoTurhol:540327644089155639>'], pass_context=True)
async def turhols(context):
    await client.say("<:IncognitoTurhol:540327644089155639> turhols in the chat please <:IncognitoTurhol:540327644089155639>")


@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(context):
    global norm

    player = context.message.author

    username = player.display_name

    return_msg = norm.removeFromQueue(player=player)

    await client.say(return_msg)


@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(context):

    player = context.message.author

    return_msg = norm.addToQueue(player=player, quiet=False)

    await client.say(return_msg)


@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(context):
    global norm

    player = context.message.author

    return_msg = norm.addToQueue(player=player, quiet=True)

    await client.say(return_msg)


@client.command(name='pika', aliases=['<:pika:538182616965447706>'], pass_context=True)
async def pika(context):
    global pikaO
    output = '<:pika:538182616965447706>' * pikaO
    await client.say(output)
    pikaO = pikaO + 1


@client.command(name='zappa', aliases=['zapp', 'zac', '<:zappa:632813684678197268>', '<:zapp:632813709579911179>'], pass_context=True)
async def zappa(context):
    await client.say("<:zappa:632813684678197268> <:zapp:632813709579911179> brainyzac more like brainyWACK amirite...that is until you get absolutely destroyed by him" +
                     "in 6mans and all the self resprct you had for yourself flies out the window. Not even sykes can beat him in a 1v1, so what makes you think you can?" +
                     " Do you have 2 emotes in this server? I didnt think so idiot, so <:zappa:632813684678197268> and <:zapp:632813709579911179> outta here cuz you're the whack one here <:zappa:632813684678197268> <:zapp:632813709579911179>")


@client.command(name='duis', pass_context=True)
async def duis(context):
    await client.say("Papa Duis, mor like God Duis. Don't even think about queueing up against him because he will ruin you. You think you're good?\n\nyou think you're good at RL??!?!?!?!?!?!?!?!?!?!?\nfuck no\nyou aren't good.\nyou are shit\nur fkn washed\n You don't even come close to Duis. He will absolutely ruin you without even looking. His monitor is off 90 percent of the time, eyes closed too. Never doubt the Duis, bitch ")


@client.command(name='normq', pass_context=True)
async def normq(context):
    global norm

    await client.say("!q")
    playerList = norm.getQueue()

    await client.say("\nNorm has been added to the queue! \n\nQueue size: "+str(len(playerList) + 1)+"/6\nCurrent queue:\nNorm V3, " + ", ".join(playerList))


@client.command(name='teams', aliases=['uncc'], pass_context=True)
async def teams(context):
    await client.say("it goes like this:\nA team: doesn't practice but somehow is good" +
                     "\nB team: everyone hates how their teamates play but don't talk it out to resolve issues" +
                     "\nC team: who?" +
                     "\nD team: best team" +
                     "\nE team: surprisingly solid" +
                     "\nF team: how many fkn teams do we have" +
                     "\nGG team: originally g team")


@client.command(name='8ball', aliases=['norm', 'asknorm', 'eight_ball', 'eightball', '8-ball'], pass_context=True)
async def eight_ball(context):
    """
    :param context: The question the user is wanting to ask
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
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="6mans"))
    print("Logged in as " + client.user.name)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
