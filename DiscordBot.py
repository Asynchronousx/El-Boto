#Bot.py
import discord
from discord.ext import commands

#cogs list to be loaded
startup_extensions = ["cogs.moderation", "cogs.music", "cogs.searching", "cogs.utilities"]

#variables
default_role_to_assign = None

#creating the bot istance
DiscordBot = commands.Bot(command_prefix="$")

#generating the token
TOKEN = 'YOUR TOKEN'

### EVENT HANDLING
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
    
    #set role
    role = get(member.server.roles, name=default_role_to_assign)
    await DiscordBot.add_roles(member, role)
#end on member join
    
## EVENT RELATED FUNCTIONS
#add default role on member join .
@DiscordBot.command(pass_context=True)
@commands.has_role("LORD")
async def setdefrole(self, ctx, *, roleName):
    """<role>: Set a default role for newcomers in the server."""
    #global calling
    global default_role_to_assign
    default_role_to_assign = roleName        
#end of default role assigning

#main to recall cogs
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            DiscordBot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

#run bot with token
DiscordBot.run(TOKEN)
