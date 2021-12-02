import discord
from discord.ext import commands
from discord_components import *
import time
import datetime
from discord_components import Button, ButtonStyle

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name = 'help')
    @commands.guild_only()
    async def help(self, ctx):
        desc = """
```
Home -> 🏠

General commands -> 🔮

Moderation commands -> 🔨

Music commands -> 🎶
```
"""
        em = discord.Embed(description = desc, color = 0x9E1ADF)
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text = 'HXZY', icon_url = self.bot.user.avatar_url)
        await ctx.send(
            embed = em,
            components = [
                [
                    Button(style = ButtonStyle.blue, emoji = '🏠', id = 'home'),
                    Button(style = ButtonStyle.blue, emoji = '🔮', id = 'general'),
                    Button(style = ButtonStyle.blue, emoji = '🔨', id = 'mod'),
                    Button(style = ButtonStyle.blue, emoji = '🎶', id = 'music'),
                    Button(style = ButtonStyle.red, emoji = '🗑', id = 'del'),
                ]
            ]
        )





    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        desc1 = """
• `*avatar` `*ping` `*8ball` `*say` `*spotify` 
• `*bio` `*setbio` `*whois` `*meme`
"""



        desc2 = """
• `*kick` `*ban` `*mute` `*unmute` `*clear` 
• `*slowmode` `*lock` `*unlock`
"""

        desc3 = """
• `*play` `*stop` `*pause` `*resume` `*volume`
• `*join`        
"""
        if interaction.component.id == 'general':
            generalem = discord.Embed(description = desc1, color = 0x9E1ADF)
            generalem.timestamp = datetime.datetime.utcnow()
            generalem.set_author(name = interaction.author.name, icon_url = interaction.author.avatar_url)
            generalem.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            await interaction.respond(type = 7, embed = generalem)


        if interaction.component.id == 'mod':
            modem = discord.Embed(description = desc2, color = 0x9E1ADF)
            modem.timestamp = datetime.datetime.utcnow()
            modem.set_author(name = interaction.author.name, icon_url = interaction.author.avatar_url)
            modem.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            await interaction.respond(type = 7, embed = modem)

        if interaction.component.id == 'music':
            musicem = discord.Embed(description = desc3, color = 0x9E1ADF)
            musicem.timestamp = datetime.datetime.utcnow()
            musicem.set_author(name = interaction.author.name, icon_url = interaction.author.avatar_url)
            musicem.set_footer(text = self.bot.user.name, icon_url = self.bot.user.avatar_url)
            await interaction.respond(type = 7, embed = musicem)

        if interaction.component.id == 'del':
            await interaction.respond(type =7, content = '**Deleting**')
            await interaction.message.delete()

        if interaction.component.id == 'home':
            desc = """
```
Home -> 🏠

General commands -> 🔮

Moderation commands -> 🔨

Music commands -> 🎶
```
"""
            em = discord.Embed(description = desc, color = 0x9E1ADF)
            em.set_author(name = interaction.author.name, icon_url = interaction.author.avatar_url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_footer(text = 'HXZY', icon_url = self.bot.user.avatar_url)
            await interaction.respond(
                type = 7,
                embed = em)


def setup(bot):
    bot.add_cog(Help(bot))