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
#initialize captain mode: 0 for normal, 1 if picking orange team, 2 for picking blue team
global botMode
botMode = 0
global orangeCap, blueCap, orangeTeam, blueTeam
orangeTeam = list()
blueTeam = list()
#orangeCap = discord.member.Member()
#blueCap = discord.member.Member()
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
        msg.add_field(name="!random", value="Randomly picks teams",inline=False)
        msg.add_field(name="!captains", value="Randomly selects captains. \nFirst captain picks 1 \nSecond captain picks the next two",inline=False)
        msg.add_field(name='!8ball', value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O",inline=False)
        msg.set_thumbnail(url="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/blob/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)

@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(context):
    global botMode
    if botMode!=0:
        await client.say("Can't kick players while picking teams.")
        return
    #numOfMentions = len(context.message.mentions)
    player = context.message.mentions[0]
    if(len(queue) ==0):
        await client.say("User not in the queue because the queue is empty. Is cre8 not in the queue?")
    elif(player in queue):
        queue.remove(player)
        await client.say("Removed " + player.display_name + " from the queue")
    else:
        await client.say("User not in queue. To see who is in current queue, type: !list")

    
@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status'], pass_context=True)
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


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(context):
    await client.say("u")

@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(context):
    global orangeTeam, blueTeam
    if(len(queue) != 6):
        await client.say("Queue is not full")
    else:
        orangeTeam = random.sample(queue, 3)
        for x in orangeTeam:
            queue.remove(x)
        blueTeam = queue
        await client.say("🔶 TEAM 1 🔶: {}".format(", ".join([player.mention for player in orangeTeam])))
        await client.say("🔷 TEAM 2 🔷: {}".format(", ".join([player2.mention for player2 in blueTeam])))
        queue.clear()
        orangeTeam.clear()
        blueTeam.clear()

@client.command(name='captains', aliases=['cap', 'iwanttopickteams'], pass_context=True)
async def captains(context):
    global botMode, orangeTeam, blueTeam, orangeCap, blueCap
    if botMode!=0:
        await client.say("Captains already set\nCaptains:\n🔶 TEAM 1 🔶: " + orangeCap + "\n🔷 TEAM 2 🔷: " + blueCap)
        return
    elif len(queue) != 6:
        await client.say("Queue is not full. STOP")
    else:
        botMode = 1
        orangeCap = random.choice(queue)
        queue.remove(orangeCap)
        orangeTeam.append(orangeCap)
        blueCap = random.choice(queue)
        queue.remove(blueCap)
        blueTeam.append(blueCap)
        playerList = []
        for x in queue:
                y = str(x)
                y = y.split("#")
                playerList.append(y[0])
        await client.say("Captains mode picked. Picking captains...\nCaptains:\n🔶 TEAM 1 Captain 🔶: " + orangeCap.mention + "\n🔷 TEAM 2 Captain 🔷: " + blueCap.mention + "\n\n🔶 " + orangeCap.mention + " 🔶 picks first. Type !pick and mention a player from the queue below.\nAvailable picks:\n" + ", ".join(playerList))
        

@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(context):
    global botMode, orangeTeam, blueTeam, orangeCap, blueCap
    if(botMode == 0):
        await client.say("Captains not set. If queue is full, please type !captains")
    elif( botMode == 1 and context.message.author == orangeCap):
        #orange captain picks one player
        if len(context.message.mentions) == 0:
            await client.say("No one was mentioned, please pick an available player.")
        elif len(context.message.mentions) != 1:
            await client.say("More than one player mentioned, please pick just one player.")
        else:    
            player = context.message.mentions[0]
            queue.remove(player)
            orangeTeam.append(player)
            playerList = []
            for x in queue:
                    y = str(x)
                    y = y.split("#")
                    playerList.append(y[0])
            await client.say(player.mention +" was added to 🔶 TEAM 1 🔶\n\n🔷 TEAM 2 Captain 🔷 will now pick TWO players\n🔷 " + blueCap.mention + " 🔷 please pick two players.\n\nAvailable picks:\n" + ", ".join(playerList))
            botMode = 2
    elif( botMode == 2 and context.message.author == blueCap):
        if len(context.message.mentions) == 0:
            await client.say("No one was mentioned, please pick a player.")
        elif len(context.message.mentions) == 1:
            if len(blueTeam) == 1:
                player = context.message.mentions[0]
                queue.remove(player)
                blueTeam.append(player)
                playerList = []
                for x in queue:
                        y = str(x)
                        y = y.split("#")
                        playerList.append(y[0])
                await client.say(player.mention + " added to 🔷 TEAM 2 🔷 \n🔷 " + blueCap.mention + " 🔷 please pick one more player.\n\nAvailable picks:\n" + ", ".join(playerList))
            elif len(blueTeam) == 2:
                player = context.message.mentions[0]
                queue.remove(player)
                blueTeam.append(player)
                orangeTeam.append(queue[0])
                await client.say(player.mention + " added to 🔷 TEAM 2 🔷. \nLast player added to to 🔶 TEAM 1 🔶\nTEAMS ARE SET:\n🔶 TEAM 1 🔶: {}".format(", ".join([player.mention for player in orangeTeam]))+"\n🔷 TEAM 2 🔷: {}".format(", ".join([player2.mention for player2 in blueTeam])))
                queue.clear()
                orangeTeam.clear()
                blueTeam.clear()
                botMode = 0
        elif len(context.message.mentions) == 2:
            player1 = context.message.mentions[0]
            queue.remove(player1)
            blueTeam.append(player1)
            player2 = context.message.mentions[1]
            queue.remove(player2)
            blueTeam.append(player2)
            botMode = 0
            orangeTeam.append(queue[0])
            queue.clear()
            await client.say(player1.mention + " & " + player2.mention+ " added to 🔷 TEAM 2 🔷\nLast player added to to 🔶 TEAM 1 🔶\n\n\nTEAMS ARE SET:\n🔶 TEAM 1 🔶: {}".format(", ".join([player.mention for player in orangeTeam]))+"\n🔷 TEAM 2 🔷: {}".format(", ".join([player2.mention for player2 in blueTeam])) )
    else:
        if  botMode == 1:
            await client.say("You are not 🔶 TEAM 1 Captain 🔶\n🔶 TEAM 1 Captain 🔶 is: " + orangeCap.mention)
        else:
            await client.say("You are not 🔷 TEAM 2 Captain 🔷 \n🔷 TEAM 2 Captain 🔷 is: " + blueCap.mention)

@client.command(name='restart', aliases=['reset', 'resetbot'], pass_context=True)
async def restart(context):
    for x in context.message.author.roles:
        if(x.name == "Bot Admin"):
            queue.clear()
            orangeTeam.clear()
            blueTeam.clear()
            botMode = 0

            await client.say("Bot reset...hopefully this fixes everything <:UNCCfeelsgood:538182514091491338>")
            return
        
    await client.say("You do not have permission to reset me.")

@client.command(name='sad', aliases=[':('], pass_context=True)
async def sad(context):
    await client.say("This is so sad :frowning: in the chat pls")

@client.command(name='clear', aliases=['clr'], pass_context=True)
async def clear(context):
    #print(context.message.author.roles[0])
    if  botMode!=0:
        await client.say("Can't clear queue while picking teams")
        return
    for x in context.message.author.roles:
        if(x.name == "Bot Admin"):
            queue.clear()
            await client.say("Queue cleared <:UNCCfeelsgood:538182514091491338>")
            return
        
    await client.say("You do not have permission to clear the queue.")

@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(context):
    global botMode
    if  botMode!=0:
        await client.say("TOO LATE! You should've left before captains were picked.")
        return
    player = context.message.author
    username = player.display_name
    if(player in queue):
        queue.remove(player)
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say("Removing player: " + username + "\n\nRemaining players: " + ", ".join(playerList))
    else:
        await client.say("You are not in the queue, type !q to queue :)")

@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(context):
    if  botMode!=0:
        await client.say("Please wait until current lobby has been set")
        return
    player = context.message.author
    if(player in queue):
        await client.say(context.message.author.mention + " already in queue, dummy")
        return
    if(len(queue) == 0):
        queue.append(player)
        #commented below for testing, no need to ping everytime we test...
        #replaced with line under
        #await client.say("@here, " + context.message.author.mention + " wants to queue!")
        await client.say(context.message.author.mention + " wants to queue!\n@here Type !q to join")
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
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!\nCurrent queue:\n" + ", ".join(playerList))

@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(context):
    global botMode
    if  botMode!=0:
        await client.say("Please wait until current lobby has been set")
        return
    player = context.message.author
    if(player in queue):
        await client.say(context.message.author.mention + " already in queue, dummy")
        return
    if(len(queue) == 0):
        queue.append(player)
        await client.say(context.message.author.mention + " wants to queue!\nType !q to join!")
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
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!\nCurrent queue:\n" + ", ".join(playerList))

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
