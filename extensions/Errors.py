import discord
from discord.ext import commands
import time
import datetime



class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(f"`❌` **{ctx.command.name}** cannot be used in direct messages! `❌`")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'`❌` **{ctx.command.name}** requires you to have certain permissions to use it! `❌`')



def setup(bot):
    bot.add_cog(Errors(bot))