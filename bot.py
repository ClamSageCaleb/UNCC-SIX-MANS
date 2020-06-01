__author__ = "Caleb Smith / Twan"
__copyright__ = "Copyright 2019, MIT License"
__credits__ = "Caleb Smith / Twan"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Caleb Smith / Twan"
__email__ = "caleb.benjamin9799@gmail.com"
__status__ = "Production"


import asyncio
import os
import sys
import subprocess
import random
import discord
from discord import Game
from discord.ext.commands import Bot
from datetime import datetime
from dotenv import load_dotenv
import JSONMethod as Jason

# Bot prefix and Discord Bot token
BOT_PREFIX = ("!")

# Creates the Bot with name 'client'
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

pikaO = 1

'''
    Discord Events
'''

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
        msg.set_footer(text="Developed by Twan, Clam, and Tux")
        await message.channel.send(embed=msg)
    await client.process_commands(message)


@client.event
async def on_ready():
    # await client.change_presence(Game(name="6mans"))
    print("Logged in as " + client.user.name)


async def list_servers():

    channel = discord.Object(id='538166641226416162')
    await client.wait_until_ready()
    while not client.is_closed:

        if (Jason.getQueueTime() >= 6 and Jason.getQueueLength() != 0):
            await client.send_message(channel, "Inactive for 1 hr. Queue reset")
            Jason.clearQueue()

        elif (Jason.getQueueTime() != 0):
            timeSpent = Jason.getQueueTime() * 10
            timeLeft = 60 - timeSpent

            if(timeLeft == 30):
                await client.send_message(channel,
                                          "Inactive for " +
                                          str(timeSpent) + " min. Queue will clear in " +
                                          str(timeLeft) + " min."
                                          )

            if(timeLeft == 10):
                await client.send_message(channel,
                                          "Inactive for " +
                                          str(timeSpent) + " min. Queue will clear in " +
                                          str(timeLeft) + " min."
                                          )

        if (Jason.getQueueLength() != 0):
            Jason.incrementTimer()

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

'''
    Discord Commands - Queue Commands
'''


@client.command(name='q', aliases=['addmepapanorm', 'Q', 'addmebitch', 'queue', 'join'], pass_context=True)
async def q(ctx):
    queue_length = Jason.getQueueLength()

    if (Jason.queueAlreadyPopped()):
        await ctx.send(":x: Please wait until current lobby has been set.")
        return

    player = ctx.message.author

    if(Jason.isPlayerInQueue(player)):
        await ctx.send(":x: " + player.mention + " already in queue, dummy")
        return

    if(queue_length == 0):
        Jason.addToQueue(player)

        await ctx.send(
            "@here\n\n" +
            player.mention + " wants to queue!\n\n" +
            "Type **!q** to join"
        )

    elif(queue_length >= 6):
        await ctx.send(":x: Queue full, wait until teams are picked.")

    elif(queue_length == 5):
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        await ctx.send(
            player.mention + " added to the queue!" + "\n\n" +
            "Queue size: " + str(Jason.getQueueLength()) + "/6 \n" +
            "Current queue:\n" + playerList+"\n\n" +
            "**Queue is now full!** \n\n" +
            "Type !random for random teams.\n" +
            "Type !captains to get picked last."
        )

    else:
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        await ctx.send(
            player.mention + " added to the queue!\n\n" +
            "Queue size: " + str(Jason.getQueueLength()) + "/6\n\n" +
            "Current queue:\n" + playerList
        )


@client.command(name='qq', aliases=['quietq', 'QQ', 'quietqueue', 'shh', 'dontping'], pass_context=True)
async def qq(ctx):
    queue_length = Jason.getQueueLength()

    if (Jason.queueAlreadyPopped()):
        await ctx.send(":x: Please wait until current lobby has been set")
        return

    player = ctx.message.author

    if(Jason.isPlayerInQueue(player)):
        await ctx.send(":x: " + player.mention + " already in queue, dummy")
        return

    if(queue_length == 0):
        Jason.addToQueue(player)

        await ctx.send(
            "-Silent Queue-\n\n" +
            player.mention + " wants to queue!\n\n" +
            "Type **!q** to join"
        )

    elif(queue_length >= 6):
        await ctx.send(":x: Queue full, wait until teams are picked.")

    elif(queue_length == 5):
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        await ctx.send(
            player.mention + " added to the queue!" + "\n\n" +
            "Queue size: " + str(Jason.getQueueLength()) + "/6 \n" +
            "Current queue:\n" + playerList+"\n\n" +
            "**Queue is now full!** \n\n" +
            "Type !random for random teams.\n" +
            "Type !captains to get picked last."
        )

    else:
        Jason.addToQueue(player)
        playerList = Jason.getQueueList()

        await ctx.send(
            player.mention + " added to the queue!\n\n" +
            "Queue size: " + str(Jason.getQueueLength()) + "/6\n\n" +
            "Current queue:\n" + playerList
        )


@client.command(name='leave', aliases=['yoink', 'gtfo', 'getmethefuckouttahere'], pass_context=True)
async def leave(ctx):

    if (Jason.queueAlreadyPopped()):
        await ctx.send("TOO LATE! You should've left before captains were picked.")
        return

    player = ctx.message.author
    username = player.display_name

    if(Jason.isPlayerInQueue(player)):

        Jason.removeFromQueue(player)
        playerList = Jason.getQueueList()

        if(Jason.getQueueLength() != 0):
            await ctx.send(
                "Removing player: " + username + "\n\n" +
                "Queue size: " + str(Jason.getQueueLength()) + "/6\n\n" +
                "Remaining players: " + playerList
            )
        else:
            await ctx.send(
                "Removing player: " + username + "\n\n" +
                "Queue is now empty."
            )
    else:
        await ctx.send(":x: You are not in the queue, type **!q** to join")


@client.command(name='kick', aliases=['remove', 'yeet'], pass_context=True)
async def kick(ctx):
    if (Jason.queueAlreadyPopped()):
        await ctx.send(":x: Can't kick players while picking teams.")
        return

    player = ctx.message.mentions[0]

    if(Jason.getQueueLength() == 0):
        await ctx.send(":x: The queue is empty, what are you doing?")

    elif (Jason.isPlayerInQueue(player)):
        Jason.removeFromQueue(player)
        await ctx.send(":exclamation: Removed " + player.display_name + " from the queue")

    else:
        await ctx.send(":x: User not in queue. To see who is in current queue, type: **!list**")


@client.command(name='listq', aliases=['list', 'listqueue', 'show', 'showq', 'showqueue', 'inq', 'sq', 'lq', 'status', 'showmethefknqueue', '<:who:599055076639899648>'], pass_context=True)
async def listq(ctx):
    if (Jason.getQueueLength() == 0):
        await ctx.send("Queue is empty, join the queue by typing **!q**")
    elif (Jason.queueAlreadyPopped()):
        await captains(ctx)
    else:
        playerList = Jason.getQueueList()
        await ctx.send("Current queue: " + str(Jason.getQueueLength()) + "/6 \n" + playerList)


@client.command(name='rnd', aliases=['random', 'idontwanttopickteams', 'fuckcaptains'], pass_context=True)
async def rnd(ctx):

    if(Jason.getQueueLength() != 6):
        await ctx.send(":x: Queue is not full")

    else:
        blueTeam, orangeTeam = Jason.randomPop()

        await ctx.send(
            "**Teams are set!**\n\n" +
            "🔶 TEAM 1 🔶 \n\t{}".format("\n\t".join([Jason.mentionPlayer(player) for player in orangeTeam])) + "\n\n" +
            "🔷 TEAM 2 🔷 \n\t{}".format("\n\t".join([Jason.mentionPlayer(player) for player in blueTeam]))
        )


@client.command(name='captains', aliases=['cap', 'iwanttopickteams', 'Captains', 'captain', 'Captain', 'Cap'], pass_context=True)
async def captains(ctx):

    if (Jason.queueAlreadyPopped()):
        blueCap, orangeCap = Jason.captainsPop()
        playerList = Jason.getQueueList()
        await ctx.send(
            "Captains already set\n\n" +
            "Captains:\n" +
            "🔶 TEAM 1 🔶: " + Jason.mentionPlayer(orangeCap) + "\n" +
            "🔷 TEAM 2 🔷: " + Jason.mentionPlayer(blueCap) + "\n\n" +
            "Available picks:\n" + playerList
        )
        return

    elif (Jason.getQueueLength() != 6):
        await ctx.send(":x: Queue is not full. STOP")
        return

    else:
        blueCap, orangeCap = Jason.captainsPop()
        playerList = Jason.getQueueList()

        await ctx.send(
            "Captains:\n" +
            "🔶 TEAM 1 Captain 🔶: " + Jason.mentionPlayer(orangeCap) + "\n" +
            "🔷 TEAM 2 Captain 🔷: " + Jason.mentionPlayer(blueCap) + "\n\n" +
            "🔶 " + Jason.mentionPlayer(orangeCap) + " 🔶 picks first.\n" + 
            "Type **!pick** and mention a player from the queue below.\n\n" +
            "Available picks:\n" + playerList
        )


@client.command(name='pick', aliases=['add', 'choose', '<:pick:628999871554387969>'], pass_context=True)
async def pick(ctx):

    if (not Jason.queueAlreadyPopped()):
        await ctx.send(":x: Captains not set. If queue is full, please type **!captains**")

    elif(Jason.validateOrangePick(ctx.message.author)):

        # orange captain picks one player
        if len(ctx.message.mentions) == 0:
            await ctx.send(":x: No one was mentioned, please pick an available player.")
            return
        elif len(ctx.message.mentions) != 1:
            await ctx.send(":x: More than one player mentioned, please pick just one player.")
            return
        else:

            errorMsg = Jason.pick(ctx.message.mentions[0])

            if (errorMsg == ""):
                blueCap, orangeCap = Jason.captainsPop()
                playerList = Jason.getQueueList()
                await ctx.send(
                    ctx.message.mentions[0].mention + " was added to 🔶 TEAM 1 🔶\n\n" +
                    "🔷 " + Jason.mentionPlayer(blueCap) + " 🔷 please pick TWO players.\n" +
                    "Ex: `!pick @Twan @Tux`\n\n" +
                    "Available picks:\n" + playerList
                )
            else:
                await ctx.send(":x: " + errorMsg)
                return

    elif(Jason.validateBluePick(ctx.message.author)):

        if len(ctx.message.mentions) == 0:
            await ctx.send(":x: No one was mentioned, please pick a player.")

        elif len(ctx.message.mentions) == 1:
            await ctx.send(":x: Use format: `!pick @player1 @player2`")
            # this was where you could just pick one player at a time, but it seemed to break
            # so I just removed it for now

        elif len(ctx.message.mentions) == 2:

            errorMsg = Jason.pick(ctx.message.mentions[0], ctx.message.mentions[1])

            if (errorMsg == ""):
                blueCap, orangeCap = Jason.captainsPop()
                blueTeam, orangeTeam = Jason.getTeamList()
                await ctx.send(
                    ctx.message.mentions[0].mention + " & " + ctx.message.mentions[1].mention + " added to 🔷 TEAM 2 🔷\n" +
                    "Last player added to 🔶 TEAM 1 🔶\n\n" +
                    "**Teams are set!**\n\n" +
                    "🔶 TEAM 1 🔶 \n\t{}".format("\n\t".join([Jason.mentionPlayer(player) for player in orangeTeam])) + "\n\n" +
                    "🔷 TEAM 2 🔷 \n\t{}".format("\n\t".join([Jason.mentionPlayer(player) for player in blueTeam]))
                )
                Jason.clearQueue()
            else:
                await ctx.send("Either one or both of the players you mentioned is not in the queue. Try again")
                return

    else:
        blueCap, orangeCap = Jason.captainsPop()
        blueTeam, orangeTeam = Jason.getTeamList()
        if (len(orangeTeam) == 1):
            await ctx.send(
                "You are not 🔶 TEAM 1 Captain 🔶\n\n" +
                "🔶 TEAM 1 Captain 🔶 is: " + Jason.mentionPlayer(orangeCap)
            )
        else:
            await ctx.send(
                "You are not 🔷 TEAM 2 Captain 🔷 \n\n" +
                "🔷 TEAM 2 Captain 🔷 is: " + Jason.mentionPlayer(blueCap)
            )


@client.command(name='clear', aliases=['clr', 'reset'], pass_context=True)
async def clear(ctx):
    for x in ctx.message.author.roles:
        if(x.name == "Bot Admin"):
            Jason.clearQueue()

            await ctx.send("Queue cleared <:UNCCfeelsgood:538182514091491338>")
            return

    await ctx.send("You do not have permission to clear the queue.")


@client.command(name='restart', aliases=['restartbot'], pass_context=True)
async def restart(ctx):
    for x in ctx.message.author.roles:
        if(x.name == "Bot Admin"):
            await ctx.send("Bot restarting...hopefully this fixes everything <:UNCCfeelsgood:538182514091491338>")
            os.remove("queue.json")
            subprocess.call([r'runBot.bat'])
            sys.exit(0)
            return

    await ctx.send("You do not have permission to restart me.")


'''
    Discord Commands - Easter Eggs
'''


@client.command(name='twan', aliases=['<:twantheswan:540327706076905472>'], pass_context=True)
async def twan(ctx):
    await ctx.send("<:twantheswan:540327706076905472> twantheswan is probably the greatest Rocket League (tm) player to have ever walked the face of this planet. When he tries, no one ever beats him. If you beat him in a game, he was letting you win just to make you feel better. ur fkn trash at rl unless u r twantheswan. sub to him on twitch <:twantheswan:540327706076905472>")


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
    await ctx.send("<:IncognitoTurhol:540327644089155639> turhols in the chat please <:IncognitoTurhol:540327644089155639>")


@client.command(name='pika', aliases=['<:pika:538182616965447706>'], pass_context=True)
async def pika(ctx):
    global pikaO
    output = '<:pika:538182616965447706>' * pikaO
    await ctx.send(output)
    pikaO = pikaO + 1


@client.command(name='zappa', aliases=['zapp', 'zac', '<:zappa:632813684678197268>', '<:zapp:632813709579911179>'], pass_context=True)
async def zappa(ctx):
    await ctx.send("<:zappa:632813684678197268> <:zapp:632813709579911179> brainyzac more like brainyWACK amirite...that is until you get absolutely destroyed by him" +
                   "in 6mans and all the self resprct you had for yourself flies out the window. Not even sykes can beat him in a 1v1, so what makes you think you can?" +
                   " Do you have 2 emotes in this server? I didnt think so idiot, so <:zappa:632813684678197268> and <:zapp:632813709579911179> outta here cuz you're the whack one here <:zappa:632813684678197268> <:zapp:632813709579911179>")


@client.command(name='duis', pass_context=True)
async def duis(ctx):
    await ctx.send("Papa Duis, mor like God Duis. Don't even think about queueing up against him because he will ruin you. You think you're good?\n\nyou think you're good at RL??!?!?!?!?!?!?!?!?!?!?\nfuck no\nyou aren't good.\nyou are shit\nur fkn washed\n You don't even come close to Duis. He will absolutely ruin you without even looking. His monitor is off 90 percent of the time, eyes closed too. Never doubt the Duis, bitch ")


@client.command(name='normq', pass_context=True)
async def normq(ctx):
    await ctx.send("!q")
    playerList = Jason.getQueueList()

    await ctx.send(
        "\nNorm has been added to the queue! \n\n" +
        "Queue size: " + str(Jason.getQueueLength() + 1) + "/6 \n" +
        "Current queue:\nNorm V3, " + playerList
    )


@client.command(name='teams', aliases=['uncc'], pass_context=True)
async def teams(ctx):
    await ctx.send("it goes like this:\nA team: doesn't practice but somehow is good" +
                   "\nB team: everyone hates how their teamates play but don't talk it out to resolve issues" +
                   "\nC team: who?" +
                   "\nD team: best team" +
                   "\nE team: surprisingly solid" +
                   "\nF team: how many fkn teams do we have" +
                   "\nGG team: originally g team")


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

'''
    Main function
'''


def main():
    Jason.checkQueueFile()

    client.loop.create_task(list_servers())

    # Add token here
    load_dotenv()
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
