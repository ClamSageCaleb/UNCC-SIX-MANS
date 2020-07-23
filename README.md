<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/media/norm.gif" alt="Character Selector" width="200">
  <br>
    UNCC SIX MANS
  <br>
</h1>

<h4 align="center">UNCC SIX MANS OFFICIAL DISCORD BOT.</h4>
<br>

![Build](https://github.com/ClamSageCaleb/UNCC-SIX-MANS/workflows/Build%20Norm%20Executable/badge.svg)

## Norm the 6 Mans Bot
This repository contains the code for the official 6 mans Discord bot for the UNC Charlotte Rocket League community. A typical Rocket League match consists of two teams with three players on each team. This 6 mans bot makes it easier for players to get together, choose teams, play, and record each player's performance from match to match.

### Norm is responsible for:
 - Keeping track of who is in the queue
 - Clearing the queue when it has not been active for over an hour
 - Assigning players to teams when the queue is full (reachers 6 players)
   - Teams are assigned either randomly or chosen by randomly selected captains
 - Recording which team won the match as reported by the players
 - Recording the result for each individual player to the leaderboard in terms of:
   - Wins
   - Losses
   - Matches Played
   - Win Percentage
 
Norm is a Python based Discord bot that is compiled into a single executable. This makes it easy for anyone who is interested in adopting Norm to get started rather quickly.

## Running the Executable
1. Go to the latest release [here](https://github.com/ClamSageCaleb/UNCC-SIX-MANS/releases/tag/v4.2.1) and download `Norm_the_6_Mans_Bot_v#.#.#.exe`.
2. Double click the file to start Norm. Windows may warn you that Norm is unsafe since he is an executable. You can select `More Info` and then `Run anyway` to run Norm normally.
3. A window should appear. This is the Admin Console for Norm. Here you can edit the current queue, edit active matches, view the leaderboard, and edit Norm's configuration settings.
4. For this next step you will need a valid Discord Bot Token. 
   1. Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create your bot application.
      - This includes adding your new bot to the server you wish to use this application in.
   2. Click on `Bot` on the left side of the page. 
   3. Click on `Copy` underneath where it says `Token`. 
   4. Paste this token into the `Discord Bot Token` field under the `Config` section in the Norm Admin Console. 
   5. Click Save Changes.
5. Click the `Start Norm` button in the top left corner of the Admin Console.

## Running the Source Code
1. Clone the repository (```git clone https://github.com/clamsagecaleb/UNCC-SIX-MANS.git```)
2. Install requirements (```pip install -r requirements.txt```)
3. Run `src/main.py` in the root directory of the project.
4. Follow steps 3-5 in *Running the Norm Executable*.

## How it All Works
Norm uses the [Discord.py](https://pypi.org/project/discord.py/) wrapper for the official [Discord Bot API](https://discordbots.org/api/docs) to read and send messages sent in the designated Discord server.

Current queue, active matches, the leaderboard, and the config are kept in the user's home path under a folder named `SixMans`. This folder and associated files are created automatically when Norm runs for the first time. Each file is stored in `JSON` format.

Norm uses AWS to backup the leaderboard remotely with versioning in case the leaderboard ever becomes corrupt. The remote leaderboard is read every time Norm starts, and replaces the remote leaderboard with every newly reported match.

The Admin Console is built using [Eel](https://pypi.org/project/Eel/). All source code is packaged using `pyinstaller` which is installed along with Eel.

### To see what commands Norm understands and more, visit our [official webpage](https://clamsagecaleb.github.io/UNCC-SIX-MANS/).
---
