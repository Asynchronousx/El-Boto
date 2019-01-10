# Discord-Bot: a fun, useful utility to Discord.

## Release

Currently available on: [Bot OnDiscord!](https://bots.ondiscord.xyz/bots/518750364363784207 "El boto!")<br>
Approved on Discordbots: https://discordbots.org/bot/518750364363784207

[![Discord Bots](https://discordbots.org/api/widget/518750364363784207.svg)](https://discordbots.org/bot/518750364363784207)<br>
[![El Boto](https://bots.ondiscord.xyz/bots/518750364363784207/embed)](https://bots.ondiscord.xyz/bots/518750364363784207)<br>

## Commands and help

Want to know about Commands help? type **$help** into Discord to show the commands table.<br>
Also, typing **$help 'command name'** will show more about a command.

## Description
This Discord Bot is hosted on Heroku via real time cloud to make the bot run 24/7.<br>
This repo there contains the configuration file and environ necessary to Heroku to let<br> 
the bot work properly.<br>

This simple discord bot will help and aid in basic features like:

 - BOT BASICS<br>
   Join: simple as it seems: make the bot join the channel. -> $join<br>
   Leave: you won't believe: make the bot leave the channel. -> $leave<br>

 - MUSIC<br>
   Play and search songs from youtube: -> $play 'songname'<br>
   Song's queue management (adding songs while one's currently playing will add to the queue)<br>
   Skip song functionality: bored of the songs played by other? skip it! -> $skip<br>
   Queue status for checking which song it's actually queued -> $qstatus<br>
   Stop function to make the player stop playing -> $stop<br>
   Volume adjust function to adjust the volume -> $volume 'volume number'<br>

 - SEARCHING<br>
   Why open a browser when you comfortably do this on your discord channel?<br>
   Searching features include(TEXT PAGE by default):<br>
   Searching page by name (returns: most-top occurrence) -> $src 'something'<br>
   Searching a video, returning the most-top occurrence of that video on youtube -> $src 'something 'video'<br>

  - MODERATION<br>
   Moderation tool that allows an Admin to perform roles and kicks action. To use this functionality, the server creator must create a role named LORD with admin features, and add this role to himself.<br>
   Set default role: whenever a new user will join your channel, a default role will be assigned. -> $setdefrole 'ROLE NAME' (Note:    everytime your bot will leave your server, you'll need to do that again.<br>
   Addrole: add an existing role to one of the member of the server. -> $addrole @member 'ROLE NAME'<br>
   Removerole: remove an existing role from one of the member of the server. -> $removerole @member 'ROLE NAME'<br>
   Print roles: want to show everyone how creative you are? print your roles into che channel! -> $printroles<br>
   Kick: the ol' nice kick. Kick someone from the server! -> $kick @someone<br>
  - UTILITY
    Offend people with the command $offence, and take a laugh. -> $offence 'Someone'<br>
    Dice roll isn't only on World of Warcraft: win dispute with your friend launching your dice! -> $droll 'diceface' (default dice: 6, diceface can be any number).<br>
    Test Bot: well, you want to check if your bot is alive, don't you? -> $test 'echotest'<br>
    Info: get info about the creator (That's me!)-> $info<br>

 - ### MORE TO COME!<br>

## Dependencies 

This bot requires internal and external dependencies in order to work.<br>
If you'd like to compile ant test it locally, you'll need this the following dependencies:

 ### Runtime enviroinment: 
 -**Python 3.6.7**

 ### Internal Dependencies:
 -**discord.py lib**<br>
 -**youtube_dl lib**<br>
 -**google - specifically googlesearch- lib**<br>
 
 ### External Dependencies
 -**PyNaCL**<br>
 -**FFMPEG/AVCONV to make the bot translate and play youtube audio into the channel**<br>
 
 ### Token
 - Also, don't forget to change the occurrence 'YOUR TOKEN' into the DiscordBot.py file with the token of your bot (available once you created your new bot and went into developer section to check it).
 
 ## Installation
 
 For installing and running this bot in local, make sure to have all the dependencies listed there, and then download
 the DiscordBot.py.<br>
 Once done, type 
 
 ```bash
 cd /path/to/bot
 python DiscordBot.py 
 ```
 into your terminal to make the bot starting his job.
 
 Alternatively you can deploy this bot on Heroku, forking this repo and change the token with yours.<br>
 **Dependencies buildpacks on Heroku:**
 - Python 
 - heroku-buildpack-ffmpeg-latest.
 - AWS APT (heroku-community/apt).
