__author__ = "Caleb Smith / Twan"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Caleb Smith / Twan"
__email__ = "caleb.benjamin9799@gmail.com"
__status__ = "Production"

import random
import asyncio
import aiohttp
import json
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
        msg.add_field(name="!q - not working yet", value="Adds you to the queue",inline=False)
        msg.add_field(name="!leave", value="Removes you from the queue",inline=False)
        msg.add_field(name="!kick - not working yet", value="Kicks someone from the queue, will require a vote",inline=False)
        msg.add_field(name="!list - not working yet", value="Lists the current queue",inline=False)
        msg.add_field(name="!Random - not working yet", value="Randomly picks teams",inline=False)
        msg.add_field(name="!Captains - not working yet", value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two",inline=False)
        msg.add_field(name='!8ball', value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O",inline=False)
        msg.set_thumbnail(url="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/blob/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)

@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue'], pass_context=True)
async def listq():
    await client.say("Current queue:")
    if(len(queue) == 0):
        await client.say("Queue is f****** empty, you should @ here so everyone gets mad at you")
    else:
        for x in queue:
            y = str(x)
            y = y.split("#")
            await client.say(y[0])

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
    if(len(queue) == 0):
        queue.append(player)
        await client.say(context.message.author.mention + " added to the queue!")
    elif(len(queue) == 6):
        await client.say("Queue full, wait until teams are picked.")
    elif(player in queue):
        await client.say(context.message.author.mention + " already in queue, dummy")
    else:
        queue.append(player)
        await client.say(player.mention + " added to the queue!")
        #returnedQueue = queue.pop()
        await client.say("\nCurrent queue:")
        for x in queue:
            await client.say(x)


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
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
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
