import random


class SixMans:
    def __init__(self):
        self.queue = list()
        self.blueTeam = list()
        self.orangeTeam = list()
        self.blueCaptain = ""
        self.orangeCaptain = ""
        self.botMode = 0

    '''
     addToQueue - Adds a player to the queue
     params - player: the player to add; quiet: whether to include ping or not
     returns - status message
    '''

    def addToQueue(self, player, quiet):
        if (self.botMode != 0):
            return "Please wait until current lobby has been set"

        if (player in self.queue):
            return player.mention + " already in queue, dummy"

        if (len(self.queue) == 6):
            return "Queue full, wait until teams are picked."

        self.queue.append(player)

        if (len(self.queue) == 6):
            return player.mention + " added to the queue!" + self.listQueue() + "\nQueue is now full! \nType !random for random teams.\nType !captains to get picked last."

        if (len(self.queue) == 1 and not quiet):
            return "@here\n" + player.mention + " wants to queue!\nType **!q** to join"

        if (len(self.queue) == 1 and quiet):
            return "-Silent queue-\n" + player.mention + " wants to queue!\nType **!q** to join!"

        return player.mention + " added to the queue!" + self.listQueue()

    '''
     removeFromQueue - Removes a player from the queue
     params - player: the player to remove
     returns - status message
    '''

    def removeFromQueue(self, player):
        if (botMode != 0):
            return "Too late! No changes while picking teams."

        if (player in self.queue):
            self.queue.remove(player)
            return "Removed " + player.display_name + " from the queue" + self.listQueue()
        else:
            return "User not in queue. To see who is in current queue, type: !list"

    '''
     addToTeam - Adds a player to a team
     params - team_color: the team to add the player to; player: the player to add
     returns - status message
    '''

    def addToTeam(self, team_color, player):
        if (player in queue):
            status = self.removeFromQueue(player)
            if (status != -1):
                if (team_color == 'blue'):
                    self.blueTeam.append(player)
                else:
                    self.orangeTeam.append(player)
        return -1

    '''
     listQueue - Returns a formatted list of the players in the queue
     params - none
     returns - status message
    '''

    def listQueue(self):
        if(len(self.queue) == 0):
            return "Current queue is empty"

        playerList = []
        for x in self.queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        return "\n\nCurrent queue: " + str(len(queue)) + "/6\n" + ", ".join(playerList)

    '''
     getQueue - Returns the players in the queue
     params - none
     returns - player list
    '''

    def getQueue(self):
        playerList = []
        for x in self.queue:
            y = str(x)
            y = y.split("#")
            playerList.append(y[0])
        return playerList

    '''
     randomPickTeams - Randomly adds players to teams
     params - none
     returns - picked teams
    '''

    def randomPickTeams(self):
        if (len(self.queue) != 6):
            return "Queue is not full"

        for p in random.sample(queue, 3):
            self.addToTeam('blue', p)
            self.removeFromQueue(p)

        for p in self.queue:
            self.addToTeam('orange', p)

        self.queue.clear()

        msg1 = "🔶 TEAM 1 🔶: {}".format(
            ", ".join([player.mention for player in orangeTeam]))
        msg2 = "\n🔷 TEAM 2 🔷: {}".format(
            ", ".join([player2.mention for player2 in blueTeam]))

        return msg1 + msg2

    '''
     pickCaptains - Randomly picks captains
     params - none
     returns - status message
    '''

    def pickCaptains(self):

        if (self.botMode != 0):
            return "Captains already set\nCaptains:\n🔶 TEAM 1 🔶: " + self.orangeCap.mention + "\n🔷 TEAM 2 🔷: " + self.blueCap.mention

        if (len(self.queue) != 6):
            return "Queue is not full. STOP"

        self.botMode = 1
        self.blueCaptain = random.sample(self.queue, 1)
        self.addToTeam('blue', self.blueCaptain)
        self.removeFromQueue(self.blueCaptain)

        self.orangeCaptain = random.sample(self.queue, 1)
        self.addToTeam('orange', self.orangeCaptain)
        self.removeFromQueue(self.orangeCaptain)

        return "Captains mode picked. Picking captains...\nCaptains:\n🔶 TEAM 1 Captain 🔶: " + self.orangeCap.mention + "\n🔷 TEAM 2 Captain 🔷: " + self.blueCap.mention + "\n\n🔶 " + self.orangeCap.mention + " 🔶 picks first. Type **!pick** and mention a player from the queue below.\nAvailable picks:\n" + ", ".join(self.queue)

    '''
     getCaptains - Returns the current captains
     params - none
     returns - captains
    '''

    def getCaptains(self):
        if (self.orangeCaptain == "" or self.blueCaptain == ""):
            return -1

        return self.blueCaptain, self.orangeCaptain

    '''
     pickTeams - Handles when captains pick
     params - the captain color and the players picked
     returns - status message
    '''

    def pickTeams(self, captain, players):
        if (self.botMode == 0):
            return "Captains not set. If queue is full, please type !captains"
        if (self.botMode == 1 and captain == 'orange'):
            if (len(players) == 0):
                return "No one was mentioned, please pick an available player."
            if (len(players) != 1):
                return "More than one player mentioned, please pick just one player."
            self.addToTeam('orange', players[0])

            playerList = self.getQueue()
            self.botMode = 2
            return players[0].mention + " was added to 🔶 TEAM 1 🔶\n\n🔷 TEAM 2 Captain 🔷 will now pick TWO players\n🔷 " + self.blueCap.mention + " 🔷 please pick two players.\n\nAvailable picks:\n" + ", ".join(playerList)

        if (self.botMode == 2 and captain == 'blue'):
            if (len(players) == 0):
                return "No one was mentioned, please pick an available player."
            if (len(players) != 2):
                return "Please pick two people in the queue."
            for p in players:
                self.addToTeam('blue', p)

            self.addToTeam('orange', self.queue[0])
            self.clearAll()

            return players[0].mention + " & " + players[1].mention + " added to 🔷 TEAM 2 🔷\nLast player added to to 🔶 TEAM 1 🔶\n\n\nTEAMS ARE SET:\n" + "🔶 TEAM 1 🔶: {}".format(", ".join([p.mention for p in orangeTeam]))+"\n🔷 TEAM 2 🔷: {}".format(", ".join([p.mention for p in blueTeam]))

        if (captain == ''):
            return "You are not 🔶 TEAM 1 Captain 🔶\n🔶 TEAM 1 Captain 🔶 is: " + self.orangeCap.mention if botMode == 1 else "You are not 🔷 TEAM 2 Captain 🔷 \n🔷 TEAM 2 Captain 🔷 is: " + self.blueCap.mention

    '''
     clearAll - Clears all variables - should be done after a queue is properly setup
     params - none
     returns - none
    '''

    def clearAll(self):
        self.queue.clear()
        self.blueTeam.clear()
        self.orangeTeam.clear()
        self.blueCaptain = ""
        self.orangeCaptain = ""
        botMode = 0
