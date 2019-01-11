import discord
from discord.ext import commands
from discord.utils import get

"""Tools for managing the channel."""

class Moderation():
    def __init__(self, DiscordBot):
        self.DiscordBot = DiscordBot
        
    #add role to user
    @commands.command(pass_context=True)
    @commands.has_role("LORD")
    async def addrole(self, ctx, userName: discord.Member, *, roleName):
        """<user> <role>: Add a role to an user."""
        author = ctx.message.author
        role = get(author.server.roles, name=roleName)
        await self.DiscordBot.add_roles(userName, role)
    #end addrole

    #remove role from user
    @commands.command(pass_context=True)
    @commands.has_role("LORD")
    async def removerole(self, ctx, userName: discord.Member, *, roleName):
        """<user> <role>: Remove a role from an user."""
        author = ctx.message.author
        role = get(author.server.roles, name=roleName)
        await self.DiscordBot.remove_roles(userName, role)
    #end removerole
 
    @commands.command(pass_context=True)
    async def printroles(self, ctx):
        """Print all the current defined roles in the server."""
        server = ctx.message.server
        roles_list =  []
        for role in server.roles:
            roles_list.append("`" + role.name + "`" + " :hammer_pick:")
    
        await self.DiscordBot.say("\n".join(roles_list))   
    #end of display role

    #kick an user.
    @commands.command(pass_context = True)
    @commands.has_role("LORD")
    async def kick(self, ctx, userName: discord.User):
        """<user>: Kick an user from the server."""
        await self.DiscordBot.kick(userName)
    #end kick

def setup(DiscordBot):
DiscordBot.add_cog(Moderation(DiscordBot))
