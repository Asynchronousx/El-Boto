import discord
from discord.ext import commands
from random import randint

"""Fun and useful!"""

class Utilities():
    def __init__(self, DiscordBot):
        self.DiscordBot = DiscordBot

    #adding TEST command to our bot
    @commands.command(pass_context=True)
    async def test(self, ctx, *, message):
        """<echo argument>: Test the bot."""
        try:
            await self.DiscordBot.say("This is a ECHO test: {} from: {}".format(message, ctx.message.author))
        except:
            await self.DiscordBot.say("Missing echoing argument.")
    #end test

    #adding OFFENCE command to our bot
    @commands.command(pass_context=True)
    async def offence(self, ctx, *, name):
        """<name>: Make the bot offence someone."""
        offences = ["You suck shit", "Go fuck a pokemon", "You nab scum", "Unfeathered mostruosity"
                    "Suck my fart", "GIT GUD", "Your mom asshole is bigger than your mom pussy", "YOU FUCKER",
                    "You love watching gay dog porn don't you", "Donkey ass niBBa", "Banana sucker", "Jerker nab",
                    "shove your grandma's panties down your own throat", "shut you fucking mouth"]
    
        x = randint(0, len(offences))

        try:
            await self.DiscordBot.say("{}, {}".format(offences[x], name))
        except:
            await self.DiscordBot.say("Missing name argument.")
    #end offence

    @commands.command(pass_context=True)
    async def droll(self, ctx, limit=None):
        """Make a dice roll (1-6). Passing a number change num limit."""
        if not limit:
            x = randint(1, 6)
        else: 
            x = randint(1, int(limit))

        await self.DiscordBot.say("You rolled: {} :game_die:".format(x))
    #end droll

    #get info about the creator
    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Get bot credit infos."""
        await self.DiscordBot.say(":dollar: `Creator: Asynchronousx#9475` :dollar:\n:dollar: `Current Version: 1.0` :dollar:\n:dollar: Github: https://github.com/Asynchronousx :dollar:")
    #end of info


def setup(DiscordBot):
DiscordBot.add_cog(Utilities(DiscordBot))
