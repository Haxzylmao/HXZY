import discord
from discord.ext import commands
import datetime
import time
from discord_slash import cog_ext
from discord_slash import *


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('I am online!')
        await self.bot.change_presence(activity = discord.Game('*help'))



def setup(bot):
    bot.add_cog(Ready(bot))