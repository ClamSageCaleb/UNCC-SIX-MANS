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
        msg.add_field(name="!leave - not working yet", value="Removes you from the queue",inline=False)
        msg.add_field(name="!kick - not working yet", value="Kicks someone from the queue, will require a vote",inline=False)
        msg.add_field(name="!Random - not working yet", value="Randomly picks teams",inline=False)
        msg.add_field(name="!Captains - not working yet", value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two",inline=False)
        msg.add_field(name='!8ball', value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O",inline=False)
        #msg.set_thumbnail(url="https://en.wikipedia.org/wiki/Charlotte_49ers#/media/File:Charlotte_49ers_logo.svg")
        msg.set_thumbnail(url="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/blob/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)


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

@client.command()
async def square(number):
    """
    :param number: The number the user is wanting to square
    :return: Squared Number
    """
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    """
    :return: Price of bitcoin
    """
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command()
async def ggez(name):
    msg = '''░░░░░░░░░░░░░░░░░░░░░░░░░
░░░█▀▀▀░█▀▀▀░░█▀▀░▀▀█░░░░
░░░█░▀█░█░▀█░░█▀▀░▄▀░░░░░
░░░▀▀▀▀░▀▀▀▀░░▀▀▀░▀▀▀░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░'''
    await client.say(msg + "\n" + name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
