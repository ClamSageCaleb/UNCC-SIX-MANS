from discord import Member, Embed
from typing import List
from random import choice
import Queue
from EmbedHelper import ErrorEmbed, QueueUpdateEmbed

pikaO = 0


def EightBall(author: Member):
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
    return choice(possible_responses) + ", " + author.mention


def Teams() -> str:
    return ("it goes like this:\n"
            "A team: doesn't practice but somehow is good"
            "\nB team: everyone hates how their teamates play but don't talk it out to resolve issues"
            "\nC team: who?"
            "\nD team: best team"
            "\nE team: surprisingly solid"
            "\nF team: how many fkn teams do we have"
            "\nGG team: originally g team")


def NormQ() -> List[str or Embed]:
    messages: List[str or Embed] = []
    playerList = Queue.getQueueList()
    queueSize = Queue.getQueueLength()

    messages.append("Duis says I am not supposed to queue, but I don't listen to players worse than me...")
    messages.append("!q")

    if (Queue.queueAlreadyPopped() or queueSize == 6):
        messages.append(ErrorEmbed(
            title="Current Lobby Not Set",
            desc="Whoa there Norm! You can't queue until the current queue has finished popping."
        ))
    elif (len(playerList) == 0):
        messages.append(QueueUpdateEmbed(
            title="Norm has Started the Queue!",
            desc="<@629502587963572225> wants to queue!\n\nQueued for 0 minutes.\n\nType **!q** to join",
        ))
    else:
        messages.append(QueueUpdateEmbed(
            title="Norm Added to Queue",
            desc="<@629502587963572225> has been added to the queue for 0 minutes.\n\n"
            "Queue size: " + str(queueSize + 1) + "/6\n\n"
            "Current queue:\nNorm" + (" " if len(playerList) == 0 else ", ") + playerList
        ))

    return messages


def Duis() -> str:
    return ("Papa Duis, mor like God Duis. Don't even think about queueing up against him because he will ruin you."
            " You think you're good?\nyou think you're good at RL??!?!?!?!?!?!?!?!?!?!?\nfuck no\nyou aren't good.\n"
            "you are shit\nur fkn washed\n You don't even come close to Duis. He will absolutely ruin you without even"
            " looking. His monitor is off 90 percent of the time, eyes closed too. Never doubt the Duis, bitch")


def Zappa() -> str:
    return ("<:zappa:632813684678197268> <:zapp:632813709579911179> brainyzac more like brainyWACK amirite...that is"
            " until you get absolutely destroyed by him in 6mans and all the self resprct you had for yourself flies"
            " out the window. Not even sykes can beat him in a 1v1, so what makes you think you can? Do you have 2"
            " emotes in this server? I didnt think so idiot, so <:zappa:632813684678197268> and"
            " <:zapp:632813709579911179> outta here cuz you're the whack one here <:zappa:632813684678197268>"
            " <:zapp:632813709579911179>")


def Pika() -> str:
    global pikaO
    pikaO += 1
    return '<:pika:538182616965447706>' * pikaO


def Turhols() -> str:
    return "<:IncognitoTurhol:540327644089155639> turhols in the chat please <:IncognitoTurhol:540327644089155639>"


def Smh() -> str:
    randNum = [1, 4, 5, 7, 9, 13, 22, 10, 1, 20, 4, 3, 5, 60,
               7, 8, 90, 2, 1, 2, 3, 1, 5, 4, 3, 2, 3, 1, 2, 3, 4, 5]
    return "smh" + (choice(randNum) * " my head")


def Twan() -> str:
    return ("<:twantheswan:540327706076905472> twantheswan is probably the greatest Rocket League (tm) player to have"
            " ever walked the face of this planet. When he tries, no one ever beats him. If you beat him in a game, he"
            " was letting you win just to make you feel better. ur fkn trash at rl unless u r twantheswan. sub to him"
            " on twitch <:twantheswan:540327706076905472>")


def Sad() -> str:
    return "This is so sad :frowning: in the chat pls"
