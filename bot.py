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
import os
import sys
import subprocess
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
global queue
queue = list()
#initialize captain mode: 0 for normal, 1 if picking orange team, 2 for picking blue team
global botMode
botMode = 0
global orangeCap, blueCap, orangeTeam, blueTeam, pikaO, whoO
whoO = 1
pikaO = 1
orangeTeam = list()
blueTeam = list()
#orangeCap = discord.member.Member(),
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
        msg.add_field(name='!norm,!asknorm, or !8ball', value='Will respond to a yes/no question. Good for preditions', inline=False)
        msg.add_field(name="!help", value="This command :O",inline=False)
        msg.set_thumbnail(url="https://github.com/ClamSageCaleb/UNCC-SIX-MANS/blob/master/49ers.png")
        msg.set_footer(text="Developed by Clam and Twan")
        await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)

@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(context):
    global botMode, queue
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

    
@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status','showmethefknqueue','<:who:599055076639899648>'], pass_context=True)
async def listq():
    global queue
    if(len(queue) == 0):
        await client.say("Queue is empty, you should @ here so everyone gets mad at you")
    else:
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say("Current queue: " + str(len(queue)) + "/6\n" + ", ".join(playerList))


@client.command(name='fuck', aliases=['f', 'frick'], pass_context=True)
async def fuck(context):
    await client.say("u")

@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(context):
    global orangeTeam, blueTeam, queue
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

@client.command(name='captains', aliases=['cap', 'iwanttopickteams', 'Captains','captain','Captain','Cap'], pass_context=True)
async def captains(context):
    global botMode, orangeTeam, blueTeam, orangeCap, blueCap, queue
    if botMode!=0:
        await client.say("Captains already set\nCaptains:\n🔶 TEAM 1 🔶: " + orangeCap.mention + "\n🔷 TEAM 2 🔷: " + blueCap.mention)
        return
    elif len(queue) != 6:
        await client.say("Queue is not full. STOP")
    else:
        botMode = 1
        orangeCap = random.choice(queue)
        queue.remove(orangeCap)
        orangeTeam.append(orangeCap)
        blueCap = random.choice(queue)
        blueTeam.append(blueCap)
        queue.remove(blueCap)
        if len(queue) != 4:
            print("WTF")
            if blueCap in queue:
                queue.remove(blueCap)
                print("removed blue again...")
        playerList = []
        for x in queue:
                y = str(x)
                y = y.split("#")
                playerList.append(y[0])
        await client.say("Captains mode picked. Picking captains...\nCaptains:\n🔶 TEAM 1 Captain 🔶: " + orangeCap.mention + "\n🔷 TEAM 2 Captain 🔷: " + 
            blueCap.mention + "\n\n🔶 " + orangeCap.mention + 
            " 🔶 picks first. Type **!pick** and mention a player from the queue below.\nAvailable picks:\n" + ", ".join(playerList))
        

@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(context):
    global botMode, orangeTeam, blueTeam, orangeCap, blueCap, queue
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
                await client.say(player.mention + " added to 🔷 TEAM 2 🔷. \nLast player,  added to to 🔶 TEAM 1 🔶\nTEAMS ARE SET:\n" +
                    "🔶 TEAM 1 🔶: {}".format(", ".join([player1.mention for player1 in orangeTeam]))+"\n🔷 TEAM 2 🔷: {}".format(", ".join([player2.mention for player2 in blueTeam])))
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
            orangeTeam.append(queue[0])
            await client.say(player1.mention + " & " + player2.mention+ " added to 🔷 TEAM 2 🔷\nLast player added to to 🔶 TEAM 1 🔶\n\n\nTEAMS ARE SET:\n" +
                "🔶 TEAM 1 🔶: {}".format(", ".join([player.mention for player in orangeTeam]))+"\n🔷 TEAM 2 🔷: {}".format(", ".join([player3.mention for player3 in blueTeam])) )
            queue.clear()
            blueTeam.clear()
            orangeTeam.clear()
            botMode = 0
            
            
    else:
        if  botMode == 1:
            await client.say("You are not 🔶 TEAM 1 Captain 🔶\n🔶 TEAM 1 Captain 🔶 is: " + orangeCap.mention)
        else:
            await client.say("You are not 🔷 TEAM 2 Captain 🔷 \n🔷 TEAM 2 Captain 🔷 is: " + blueCap.mention)

@client.command(name='restart', aliases=[ 'restartbot'], pass_context=True)
async def restart(context):
    global botMode, pikaO
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
    randNum = [1,4,5,7,9,13,22,10,1,20,4,3,5,60,7,8,90,2,1,2,3,1,5,4,3,2,3,1,2,3,4,5]
    output = "smh"
    output = output + (random.choice(randNum) * " my head")
    await client.say(output)

@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(context):
    #print(context.message.author.roles[0])
    global orangeTeam, blueTeam, orangeCap, blueCap, pikaO, whoO, queue
    for x in context.message.author.roles:
        if(x.name == "Bot Admin"):
            queue.clear()
            botMode = 0
            orangeTeam.clear()
            blueTeam.clear()
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
    global botMode, queue
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
        if(len(queue)!=0):
            await client.say("Removing player: " + username + "\n\nQueue size: "+str(len(queue)) + "/6\nRemaining players: " + ", ".join(playerList))
        else:
            await client.say("Removing player: " + username + "\n\nQueue is now empty.")
    else:
        await client.say("You are not in the queue, type !q to queue :)")

@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(context):
    global queue
    if  botMode!=0:
        await client.say("Please wait until current lobby has been set")
        return
    player = context.message.author
    if(player in queue):
        await client.say(context.message.author.mention + " already in queue, dummy")
        return
    if(len(queue) == 0):
        queue.append(player)
        await client.say("@here\n" +context.message.author.mention + " wants to queue!\nType **!q** to join")
        y = str(queue[0])
        y = y.split("#")
        await client.say("\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:")
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
        await client.say(player.mention + " added to the queue!" + "\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:\n" + ", ".join(playerList)+"\nQueue is now full! \nType !random for random teams.\nType !captains to get picked last.")
    else:
        queue.append(player)
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:\n" + ", ".join(playerList))

@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(context):
    global queue
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
        await client.say("-Silent queue-\n"+context.message.author.mention + " wants to queue!\nType **!q** to join!")
        y = str(queue[0])
        y = y.split("#")
        await client.say("\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:")
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
        await client.say(player.mention + " added to the queue!" + "\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:\n" + ", ".join(playerList)+"\nQueue is now full! \nType !random for random teams.\nType !captains to get picked last.")
    else:
        queue.append(player)
        playerList = []
        for x in queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        await client.say(player.mention + " added to the queue!\n\nQueue size: "+str(len(queue))+"/6\nCurrent queue:\n" + ", ".join(playerList))


@client.command(name='pika', aliases=['<:pika:538182616965447706>'],pass_context=True)
async def pika(context):
    global pikaO
    output = '<:pika:538182616965447706>' * pikaO * pikaO
    await client.say(output)
    pikaO = pikaO + 1



@client.command(name='duis', pass_context=True)
async def duis(context):
    await client.say("Papa Duis, mor like God Duis. Don't even think about queueing up against him because he will ruin you. You think you're good?\n\nyou think you're good at RL??!?!?!?!?!?!?!?!?!?!?\nfuck no\nyou aren't good.\nyou are shit\nur fkn washed\n You don't even come close to Duis. He will absolutely ruin you without even looking. His monitor is off 90 percent of the time, eyes closed too. Never doubt the Duis, bitch ")

@client.command(name='normq', pass_context=True)
async def normq(context):
    await client.say("!q")
    playerList = []
    for x in queue:
        y = str(x)
        y = y.split("#")
        playerList.append(y[0])

    await client.say("\nNorm has been added to the queue! \n\nQueue size: "+str(len(queue) + 1)+"/6\nCurrent queue:\nNorm V3, " + ", ".join(playerList))

@client.command(name='teams',aliases=['uncc'], pass_context=True)
async def teams(context):
    await client.say("it goes like this:\nA team: doesn't practice but somehow is good"+
        "\nB team: everyone hates how their teamates play but don't talk it out to resolve issues"+
        "\nC team: who?" +
        "\nD team: best team" +
        "\nE team: surprisingly solid" +
        "\nF team: how many fkn teams do we have" +
        "\nGG team: originally g team")




@client.command(name='8ball', aliases=['norm', 'asknorm','eight_ball', 'eightball', '8-ball'], pass_context=True)
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
