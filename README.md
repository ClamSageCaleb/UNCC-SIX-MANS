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
 - Assigning players to teams when the queue is full (reaches 6 players)
   - Teams are assigned either randomly or chosen by randomly selected captains
 - Recording which team won the match as reported by the players
 - Recording the result for each individual player to the leaderboard in terms of:
   - Wins
   - Losses
   - Matches Played
   - Win Percentage
 
Norm is a Python based Discord bot that is compiled into a single executable. This makes it easy for anyone who is interested in adopting Norm to get started rather quickly.

## Running the Executable
1. First things first you will need a valid Discord Bot Token. 
   1. Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create your bot application.
      - This includes adding your new bot to the server you wish to use this application in.
   2. Click on `Bot` on the left side of the page. 
   3. Click on `Copy` underneath where it says `Token`. 
2. Go to the latest Norm release [here](https://github.com/ClamSageCaleb/UNCC-SIX-MANS/releases/latest) and download `Norm_the_6_Mans_Bot_v#.#.#.exe`.
3. Double click the file to start Norm. Windows may warn you that Norm is unsafe since he is an executable. You can select `More Info` and then `Run anyway` to run Norm normally. A console window will appear and it will say something to the effect of 
   > ! There was an error with the token you provided. Please verify your bot token and try again.

   This is expected. You can close the console window and proceed to the next step.


4. The purpose of executing Norm was to automatically create all of the necessary data files needed for Norm to work correctly. Now that these files have been created, locate the `config.json` file in your home path under the `SixMans` directory. Here's an example path to the config file: `C:\Users\your_username\SixMans\config.json`
5. Open the config file in your favorite text editor. Your config file should look something like this:
   ```
   {
     "aws_access_key_id": "",
     "aws_secret_access_key": "",
     "aws_object_name": "",
     "token": ""
   }
   ```
   The only required field is the `token` option. Copy and paste your Discord API token from step 1 between the two quotation marks next to the `token` field.

6. Once the token field is set, Norm is ready for operation. Locate the Norm executable and double click to run. The console window should reappear and print the version of the application running.

### Troubleshooting
If the console windows closes suddenly when running the executable, there was likely an exception. To figure out what the exception was, open a Powershell window and navigate to the Norm executable. Run the command `./Norm_the_6_Mans_Bot_v#.#.#.exe`. The exception should then print in the Powershell window. If there is an issue, you do not know how to resolve you can create an issue [here](https://github.com/ClamSageCaleb/UNCC-SIX-MANS/issues) and we will get back to you when possible.

## Running the Source Code
1. Clone the repository (```git clone https://github.com/clamsagecaleb/UNCC-SIX-MANS.git```)
2. Install requirements (```pip install -r requirements.txt```)
3. Run `src/bot.py` in the root directory of the project.
4. Follow steps 3-5 in *Running the Executable*.

## How it All Works
Norm uses the [Discord.py](https://pypi.org/project/discord.py/) wrapper for the official [Discord Bot API](https://discordbots.org/api/docs) to read and send messages sent in the designated Discord server.

Current queue, active matches, the leaderboard, and the config are kept in the user's home path under a folder named `SixMans`. This folder and associated files are created automatically when Norm runs for the first time. Each file is stored in `JSON` format.

Norm uses AWS to backup the leaderboard remotely with versioning in case the leaderboard ever becomes corrupt. The remote leaderboard is read every time Norm starts, and replaces the remote leaderboard with every newly reported match.

### To see what commands Norm understands and more, visit our [official webpage](https://clamsagecaleb.github.io/UNCC-SIX-MANS/).
---
