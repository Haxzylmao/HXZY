import discord
from discord.ext import commands
import random
import datetime
import time


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, message):
        responses = ['Why did you mention me?', 'Dude i am trying to sleep...', 'My prefix is `*`', 'What do you want this timeeeeee']

        response = random.choice(responses)

        if self.bot.user in message.mentions:
            await message.channel.send(response)


def setup(bot):
    bot.add_cog(Message(bot))