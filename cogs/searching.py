import re
import discord
import urllib.parse
import urllib.request
from discord.ext import commands
from googlesearch import search

"""Search query on google."""

class Searching():
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

    #adding GOOGLE search to our bot
    @commands.command(pass_context=True)
    async def src(self, ctx, *, message, kind="text"):
        """<name>: search a text page on google."""
        #search text page 
        for url in search(message):
            await self.DiscordBot.say(url)
            break
                
    #end of gsearch
    
    @commands.command(pass_context=True)
    async def srcvideo(self, ctx, *, message, kind="video"):
        """<name>: search a video on youtube."""
        #search video page
        url = self.get_yturl(message)
        await self.DiscordBot.say(url)
    #end of gsearch

def setup(DiscordBot):
DiscordBot.add_cog(Searching(DiscordBot))
