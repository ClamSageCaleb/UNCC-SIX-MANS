__author__ = "Caleb Smith / Twan"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Caleb Smith / Twan"
__email__ = "caleb.benjamin9799@gmail.com"
__status__ = "Production"


import asyncio
import aiohttp
import json
import random
import discord
from discord import Game
from discord.ext.commands import Bot

# Bot prefix and Discord Bot token
BOT_PREFIX = ("!")
# Add token here
TOKEN = ""

# Creates the Bot with name 'client'
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

#initialize queue
queue = list()

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
        msg = discord.Embed(title='__**Server Commands**__', description="", color=0x38761D)
        msg.add_field(name="!q", value="Adds you to the queue",inline=False)
        msg.add_field(name="!qq", value="Same as !q but with no ping :)",inline=False)
        msg.add_field(name="!leave", value="Removes you from the queue",inline=False)
        msg.add_field(name="!kick", value="Kicks someone from the queue, will require a vote",inline=False)
        msg.add_field(name="!list", value="Lists the current queue",inline=False)
        msg.add_field(name="!Random", value="Randomly picks teams",inline=False)
        msg.add_field(name="!Captains - not working yet", value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two",inline=False)
        msg.add_field(name='!8ball', value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O",inline=False)
        msg.set_thumbnail(url="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/blob/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)

@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(context):
    #numOfMentions = len(context.message.mentions)
    player = context.message.mentions[0]
    if(len(queue) ==0):
        await client.say("User not in the queue because the queue is empty. Is cre8 not in the queue?")
    elif(player in queue):
        queue.remove(player)
        await client.say("Removed " + player.display_name + " from the queue")
    else:
        await client.say("User not in queue. To see who is in current queue, type: !list")

    
@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue'], pass_context=True)
async def listq():
    
    if(len(queue) == 0):
        await client.say("Queue is empty, you should @ here so everyone gets mad at you")
    else:
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say("Current queue:\n" + ", ".join(playerList))

@client.command(name='captains', aliases=['cap', 'iwanttopickteams'], pass_context=True)
async def captains(context):
    await client.say("fuck captains")

@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(context):
    await client.say("u")

@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(context):
    if(len(queue) != 6):
        await client.say("Queue is not full")
    else:
        orange = random.sample(queue, 3)
        for orangeTeam in orange:
            queue.remove(orangeTeam)
        blue = queue
        await client.say("🔶 TEAM 1 🔶: {}".format(", ".join([player.mention for player in orange])))
        await client.say("🔷 TEAM 2 🔷: {}".format(", ".join([player2.mention for player2 in blue])))
        queue.clear()
        
        
@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(context):
    player = context.message.author
    username = player.display_name
    if(player in queue):
        await client.say("Removing player: " + username)
        queue.remove(player)
    else:
        await client.say("You are not in the queue, type !q to queue :)")

@client.command(name='q', aliases=['addmepapanorm', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(context):
    player = context.message.author
    #if(player in queue):
    #    await client.say(context.message.author.mention + " already in queue, dummy")
    if(len(queue) == 0):
        queue.append(player)
        #commented below for testing, no need to ping everytime we test...
        #replaced with line under
        #await client.say("@here, " + context.message.author.mention + " wants to queue!")
        await client.say("@ here, " + context.message.author.mention + " wants to queue!")
        y = str(queue[0])
        y = y.split("#")
        await client.say("\nCurrent queue:")
        await client.say(y[0])
    elif(len(queue) >= 6):
        await client.say("Queue full, wait until teams are picked.")
    elif(len(queue) == 5):
        queue.append(player)
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!" + "\nCurrent queue:\n" + ", ".join(playerList)+"\nQueue full: \nType !random for random teams.\nType !captains to get picked last.")
    else:
        queue.append(player)
        await client.say(player.mention + " added to the queue!")
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say("Current queue:\n" + ", ".join(playerList))

@client.command(name='qq', aliases=['quietq', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(context):
    #if(player in queue):
    #    await client.say(context.message.author.mention + " already in queue, dummy")
    if(len(queue) == 0):
        queue.append(player)
        await client.say(context.message.author.mention + " wants to queue!")
        y = str(queue[0])
        y = y.split("#")
        await client.say("\nCurrent queue:")
        await client.say(y[0])
    elif(len(queue) >= 6):
        await client.say("Queue full, wait until teams are picked.")
    elif(len(queue) == 5):
        queue.append(player)
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!" + "\nCurrent queue:\n" + ", ".join(playerList)+"\nQueue full: \nType !random for random teams.\nType !captains to get picked last.")
    else:
        queue.append(player)
        await client.say(player.mention + " added to the queue!")
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say("Current queue:\n" + ", ".join(playerList))

@client.command(name='8ball', aliases=['eight_ball', 'eightball', '8-ball'], pass_context=True)
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
