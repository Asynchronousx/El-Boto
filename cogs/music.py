import re
import discord
import youtube_dl
import urllib.parse
import urllib.request

from discord.ext import commands

"""Play your music on the channel!"""

#global variables: discord bot
voice = None
player = None
voice_channel = None

#global variables: useful var
song_list = []
is_paused = False


class Music():
    def __init__(self, DiscordBot):
        self.DiscordBot = DiscordBot

    #defining function for getting the url
    def get_yturl(self, songName):
        #do query
        query_string = urllib.parse.urlencode({"search_query" : songName})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        #fetch the first url 
        return "http://www.youtube.com/watch?v=" + search_results[0]
    #end of function

    #defining the command JOIN: this command must be ran before every other action.
    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Let the bot join the session."""
        #doing init actions
    
        #global calling
        global voice
        global voice_channel
    
        #joining channel
        voice_channel = ctx.message.author.voice_channel
        voice = await self.DiscordBot.join_voice_channel(voice_channel)

        #TODO: other action here

        await self.DiscordBot.say(":b::o2::regional_indicator_t: joined the session :alien:")
    #end of join 

    #make bot leave the channel.
    @commands.command(pass_context=True)
    async def leave(self,ctx):
        """Let the bot leave the session."""
        #global calling
        global voice
        global voice_channel
        global player
        global song_list
        global is_paused
    
        #setting nulls
        voice = None
        voice_channel = None
        player = None
        song_list = []
        is_paused = False
    
        #leaving
        server = ctx.message.server
        voice_client = self.DiscordBot.voice_client_in(server)
        await voice_client.disconnect()
    #end of leave

    #adding PLAY song functionality
    @commands.command(pass_context=True)
    async def play(self, ctx, *, songName):
        """<songname>: Play the desired song."""
        #global calling
        global voice
        global player
        global song_list
    
        #bot is not joined into the channel
        if not voice:
            #communicate it and return
            await self.DiscordBot.say("You need to `invite` me first to play songs.\nType `$join`!")
            return

        await self.DiscordBot.say(":mag_right: `Searching the Song..` :mag_right:\n\n")
  
        #fetch the url
        play_url = self.get_yturl(songName)

        #check if there is a current player streaming
        if not player:
            #create the player
            player = await voice.create_ytdl_player(play_url)

            #display the video on channel
            await self.DiscordBot.say(":loud_sound: :loud_sound: `Song found!` :loud_sound: :loud_sound:\n")
            await self.DiscordBot.say(play_url)
        
            #adjust the volume and start
            player.volume = 0.5
            player.start()

        else:
            #appen the list to queue and notify
            song_list.append(play_url)
            await self.DiscordBot.say("`Currently playing! Song added to the queue.` :track_next: :track_next: ")

    #end of play

    #add pause function to our bot
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pause the current song."""
    
        #global calling
        global player
        global is_paused
    
        if player and player.is_playing():
            player.pause()
            is_paused = True
            await self.DiscordBot.say("`Song paused!` :sound: :sound:")
        else:
            await self.DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
    #end of pause

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        """Resume the current song."""
    
        #global calling
        global player
        global is_paused
    
        if player and is_paused:
            player.resume()
            is_paused = False
            await self.DiscordBot.say("`Song resumed!` :loud_sound: :loud_sound:")
        else:
            if not player:
                await self.DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
            else: 
                await self.DiscordBot.say("`Nothing on pause. GIT GUD.` :angry:")   
    #end resume

    def next_song(self, ctx, *, songName):
        #global calling
        global player
        global song_list

        #reset the player
        player = None

        #implement next song

    #end next song

    #adding STOP funcionality to our bot
    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stop the currently playing song."""
        global player 

        #if current player is alive
        if player and player.is_playing():
            #stop the music
            player.stop()
            player = None
        else:
            await self.DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
    #end of stop

    #adding SKIP funcionality to our bot
    @commands.command(pass_context=True)
    async def skip(self, ctx):
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
            await self.DiscordBot.say("`Song found!` :loud_sound: :loud_sound:\n")
            await self.DiscordBot.say(dequeued_url)

            #create and start
            player = await voice.create_ytdl_player(dequeued_url)
            player.volume = 0.5
            player.start()
        else:
            await self.DiscordBot.say("`No song found into the list` :back:. For `stopping` the audio, try $stop :robot: ")  
    #end skip

    #adding VOLUME functionality to our bot
    @commands.command(pass_context=True)
    async def volume(self, ctx, volume):
        """<volume number>: Adjust current song's volume."""

        #global calling
        global player

        if player:
            player.volume = int(volume)/100
        else: 
            await self.DiscordBot.say("`Nothing on play. GIT GUD.` :angry:")
    #end volume


    #adding QUEUE STATUS funcionality to our bot
    @commands.command(pass_context=True)
    async def qstatus(self, ctx):
        """Get song's queue status."""
        #global calling
        global song_list

        counter = 1
    
        if not song_list:
            await self.DiscordBot.say("`No song found into the queue.` :alien:")
        else:
            for song in song_list:
                await self.DiscordBot.say("{}. {}".format(counter, song))
                counter += 1
    #end qstatus


def setup(DiscordBot):
DiscordBot.add_cog(Music(DiscordBot))
