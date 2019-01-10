#Bot.py
from random import randint
import urllib.request
import urllib.parse
import asyncio
import re

#External dependencies
import discord
import youtube_dl
from discord.utils import get
from googlesearch import search
from discord.ext import commands

#global variables: discord bot
voice = None
player = None
voice_channel = None
is_paused = False

#global variables: useful var
song_list = []
default_role_to_assign = None

#creating the bot istance
DiscordBot = commands.Bot(command_prefix="$")

#generating the token
TOKEN = 'YOUR TOKEN'


#### EVENT HANDLING ####

#defining our ready event
@DiscordBot.event
async def on_ready():
    print("-----")
    print(DiscordBot.user.name)
    print(DiscordBot.user.id)
    print("-----")
#end on ready event

@DiscordBot.event
async def on_member_join(member):
    #global calling
    global default_role_to_assign;

    #if a default role is not assigned
    if not default_role_to_assign:
        return

    role = get(member.server.roles, name=default_role_to_assign)
    await DiscordBot.add_roles(member, role)

#end on join event

#### JOIN AND LEAVE COMMAND ####

#defining the command JOIN: this command must be ran before every other action.
@DiscordBot.command(pass_context=True)
async def join(ctx):
    """Let the bot join the session."""
    #doing init actions
    
    #global calling
    global voice
    global voice_channel
    
    #joining channel
    voice_channel = ctx.message.author.voice_channel
    voice = await DiscordBot.join_voice_channel(voice_channel)

    #TODO: other action here

    await DiscordBot.say(":b::o2::regional_indicator_t: joined the session :alien:")

#end of join 

#make bot leave the channel.
@DiscordBot.command(pass_context=True)
async def leave(ctx):
    """Let the bot leave the session."""
    #global calling
    global voice
    global voice_channel
    
    #setting voice to null
    voice = None
    voice_channel = None
    
    #leaving
    server = ctx.message.server
    voice_client = DiscordBot.voice_client_in(server)
    await voice_client.disconnect()

#end of leave

#### MODERATION SECTION ####

#add role to user
@DiscordBot.command(pass_context=True)
@commands.has_role("LORD")
async def addrole(ctx, userName: discord.Member, *, roleName):
    """<user> <role>: Add a role to an user."""
    author = ctx.message.author
    role = get(author.server.roles, name=roleName)
    await DiscordBot.add_roles(userName, role)
    
#end addrole

#remove role from user
@DiscordBot.command(pass_context=True)
@commands.has_role("LORD")
async def removerole(ctx, userName: discord.Member, *, roleName):
    """<user> <role>: Remove a role from an user."""
    author = ctx.message.author
    role = get(author.server.roles, name=roleName)
    await DiscordBot.remove_roles(userName, role)

    
#add default role on member join
@DiscordBot.command(pass_context=True)
@commands.has_role("LORD")
async def setdefrole(ctx, *, roleName):
    """<role>: Set a default role for newcomers in the server."""
    #global calling
    global default_role_to_assign
    default_role_to_assign = roleName
        
#end of default role assigning
 
@DiscordBot.command(pass_context=True)
async def printroles(ctx):
    """Print all the current defined roles in the server."""
    server = ctx.message.server
    roles_list =  []
    for role in server.roles:
        roles_list.append("`" + role.name + "`" + " :hammer_pick:")
    
    await DiscordBot.say("\n".join(roles_list))
   
#end of display role
    
    
#kick an user.
@DiscordBot.command(pass_context = True)
@commands.has_role("LORD")
async def kick(ctx, userName: discord.User):
    """<user>: Kick an user from the server."""
    await DiscordBot.kick(userName)

#end kick

#### MUSIC SECTION ####

#adding PLAY song functionality
@DiscordBot.command(pass_context=True)
async def play(ctx, *, songName):
    """<songname>: Play the desired song."""
    #global calling
    global voice
    global player
    global song_list
    
    #bot is not joined into the channel
    if not voice:
        #communicate it and return
        await DiscordBot.say("You need to `invite` me first to play songs.\nType `$join`!")
        return

    await DiscordBot.say(":mag_right: `Searching the Song..` :mag_right:\n\n")
  
    #fetch the url
    play_url = get_yturl(songName)

    #check if there is a current player streaming
    if not player:
        #create the player
        player = await voice.create_ytdl_player(play_url)

        #display the video on channel
        await DiscordBot.say(":loud_sound: :loud_sound: `Song found!` :loud_sound: :loud_sound:\n")
        await DiscordBot.say(play_url)
        
        #adjust the volume and start
        player.volume = 0.5
        player.start()

    else:
        #appen the list to queue and notify
        song_list.append(play_url)
        await DiscordBot.say("`Currently playing! Song added to the queue.` :track_next: :track_next: ")

#end of play

#add pause function to our bot
@DiscordBot.command(pass_context=True)
async def pause(ctx):
    #global calling
    global player
    global is_paused
    
    if player and player.is_playing():
        player.pause()
        is_paused = True
        await DiscordBot.say("`Song paused!` :sound: :sound:")
    else:
        await DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")

#end of pause

@DiscordBot.command(pass_context=True)
async def resume(ctx):
    #global calling
    global player
    global is_paused
    
    if player and is_paused:
        player.resume()
        is_paused = False
        await DiscordBot.say("`Song resumed!` :loud_sound: :loud_sound:")
    else:
        if not player:
            await DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
        else: 
            await DiscordBot.say("`Nothing on pause. GIT GUD.` :angry:")
            
    
#end resume
    


def next_song(ctx, *, songName):
    #global calling
    global player
    global song_list

    #reset the player
    player = None

    #implement next song

#end next song

#adding STOP funcionality to our bot
@DiscordBot.command(pass_context=True)
async def stop(ctx):
    """Stop the currently playing song."""
    global player 

    #if current player is live
    if player and player.is_playing():
        #stop the music
        player.stop()
        player = None
    else:
        await DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
    
#end of stop


#defining function for getting the url
def get_yturl(songName):
    query_string = urllib.parse.urlencode({"search_query" : songName})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

    #fetch the first url 
    return "http://www.youtube.com/watch?v=" + search_results[0]
#end of function

#adding SKIP funcionality to our bot
@DiscordBot.command(pass_context=True)
async def skip(ctx):
    """Skip the currently playing song."""
    #global calling
    global player
    global song_list

    #if something in queue
    if song_list:
        #stop player 
        player.stop()
        player = None

        #dequeue song
        dequeued_url = song_list.pop(0)
        
        #notify the client
        await DiscordBot.say("`Song found!` :loud_sound: :loud_sound:\n")
        await DiscordBot.say(dequeued_url)

        #create and start
        player = await voice.create_ytdl_player(dequeued_url)
        player.volume = 0.5
        player.start()
    else:
        await DiscordBot.say("`No song found into the list` :back:. For `stopping` the audio, try $stop :robot: ")
        
#end skip

#adding VOLUME functionality to our bot
@DiscordBot.command(pass_context=True)
async def volume(ctx, volume):
    """<volume number>: Adjust current song's volume."""

    #global calling
    global player

    if player:
        player.volume = int(volume)/100
    else: 
        await DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")

#end volume


#adding QUEUE STATUS funcionality to our bot
@DiscordBot.command(pass_context=True)
async def qstatus(ctx):
    """Get song's queue status."""
    #global calling
    global song_list

    counter = 1
    
    if not song_list:
        await DiscordBot.say("`No song found into the queue.` :alien:")
    else:
        for song in song_list:
            await DiscordBot.say("{}. {}".format(counter, song))
            counter += 1

#end qstatus

#### SEARCHING SECTION ####

#adding GOOGLE search to our bot
@DiscordBot.command(pass_context=True)
async def src(ctx, *, message, kind="text"):
    """<name> <kind>: Get Google page. <kind=text> or <kind=video>. Text default."""
    #search for the selected object
    if kind == "text":
        for url in search(message):
            await DiscordBot.say(url)
            break
    else:
        url = get_yturl(message)
        await DiscordBot.say(url)

#end of gsearch

#### UTILITIES SECTION ####

#adding TEST command to our bot
@DiscordBot.command(pass_context=True)
async def test(ctx, *, message):
    """<echo argument>: Test the bot."""
    try:
        await DiscordBot.say("This is a ECHO test: {} from: {}".format(message, ctx.message.author))
    except:
        await DiscordBot.say("Missing echoing argument.")
#end test

#adding OFFENCE command to our bot
@DiscordBot.command(pass_context=True)
async def offence(ctx, *, name):
    """<name>: Make the bot offence someone."""
    offences = ["You suck shit", "Go fuck a pokemon", "You nab scum", "Unfeathered mostruosity"
                "Suck my fart", "GIT GUD", "Your mom asshole is bigger than your mom pussy", "YOU FUCKER",
                "You love watching gay dog porn don't you", "Donkey ass niBBa", "Banana sucker", "Jerker nab",
                "shove your grandma's panties down your own throat", "shut you fucking mouth"]
    
    x = randint(0, len(offences))

    try:
        await DiscordBot.say("{}, {}".format(offences[x], name))
    except:
        await DiscordBot.say("Missing name argument.")

#end offence

@DiscordBot.command(pass_context=True)
async def droll(ctx, limit=None):
    """Make a dice roll (1-6). Passing a number change num limit."""
    if not limit:
        x = randint(1, 6)
    else: 
        x = randint(1, int(limit))

    await DiscordBot.say("You rolled: {} :game_die:".format(x))

#end droll

#get info about the creator
@DiscordBot.command(pass_context=True)
async def info(ctx):
    """Get bot credit infos."""
    await DiscordBot.say(":dollar: `Creator: Asynchronousx#9475` :dollar:\n:dollar: `Current Version: 1.0` :dollar:\n:dollar: Github: https://github.com/Asynchronousx :dollar:"); 

#end of info

DiscordBot.run(TOKEN)
