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
3. Double click the file to start Norm. Windows may warn you that Norm is unsafe since he is an executable. You can select `More Info` and then `Run anyway` to run Norm normally. 
4. A console window will appear and it will say something to the effect of 
   > No Discord Bot token found. Paste your Discord Bot token below and hit ENTER.  
token: 
   
   Paste your Bot token from step 1 into the console window and hit enter.
5. Assuming your token was valid Norm is now ready to be used!

### In the Background
When you run Norm for the first time, all files are created automatically in a folder called `SixMans` in your home directory. When you paste your Discord Bot token in the console window your token is written to the `config.json` file located in this directory. If you ever need to make changes to your token or any other fields simply edit the file, save, and restart Norm.

Your config file should look something like this:
   ```
   {
     // if you want to upload a backup of your leaderboard to a S3 bucket in AWS, here is where you input those credentials.
     "aws_access_key_id": "", // (optional)
     "aws_secret_access_key": "", // (optional)
     "aws_object_name": "", // (required only if using AWS) - The name you want for the leaderboard in AWS
     "token": "", // (required) - Your bot token
     "queue_channels": [], // (optional) - A list of the channel IDs that users can queue in
     "report_channels": [], // (optional) - A list of the channel IDs that users can report matches in
     "leaderboard_channel": -1 // (optional) - The ID of the channel to post the full leaderboard
   }
   ```
If you leave `"queue_channels"` and `"report_channels"` as they are users will be able to queue and report in any channel in the server that Norm has access to. Leaving `"leaderboard_channel"` as default will disable the full leaderbaord feature.

### Troubleshooting
If the console windows closes suddenly when running the executable, there was likely an exception. To figure out what the exception was, open a Powershell window and navigate to the Norm executable. Run the command `./Norm_the_6_Mans_Bot_v#.#.#.exe`. The exception should then print in the Powershell window. If there is an issue you do not know how to resolve you can create an issue [here](https://github.com/ClamSageCaleb/UNCC-SIX-MANS/issues) and we will get back to you when possible.

## Running the Source Code
1. Clone the repository (```git clone https://github.com/clamsagecaleb/UNCC-SIX-MANS.git```)
2. Install requirements (```pip install -r requirements.txt```)
3. Run `src/bot.py` in the root directory of the project.
4. Follow steps 4-5 in *Running the Executable*.

## How it All Works
Norm uses the [Discord.py](https://pypi.org/project/discord.py/) wrapper for the official [Discord Bot API](https://discordbots.org/api/docs) to read and send messages sent in the designated Discord server.

Current queue, active matches, and the leaderboard are stored in a file called `data.json`. This file is leveraged using a python package called [TinyDB](https://github.com/msiemens/tinydb). The config and data files are kept in the user's home path under a folder named `SixMans`. This folder and associated files are created automatically when Norm runs for the first time. Each file is stored in `JSON` format.

Norm uses AWS to backup the leaderboard remotely with versioning in case the leaderboard ever becomes corrupt. The remote leaderboard is read every time Norm starts, and replaces the remote leaderboard with every newly reported match.

### To see what commands Norm understands and more, visit our [official webpage](https://clamsagecaleb.github.io/UNCC-SIX-MANS/).
---
