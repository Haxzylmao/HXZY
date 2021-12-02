import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import *
import asyncio
from discord_components import *
import datetime
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import time

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @cog_ext.cog_slash(name = 'avatar', description = 'Get a users avatar/profile picture', guild_ids = [901832876256026734])
    async def avatar(self, ctx, target : discord.Member = None):
        if target is None:
            target = ctx.author

        em = discord.Embed(description = f"{target.mention} profile picture", color = 0x9E1ADF)
        em.set_image(url = target.avatar_url)
        em.set_author(name = f'Requested by {ctx.author.name}', icon_url = ctx.author.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em, hidden = True)



    @cog_ext.cog_slash(name = 'kick', description = 'Kick a member', guild_ids = [901832876256026734])
    async def kick(self, ctx, target : discord.Member, *, reason = None):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send('You cannot kick members since you do not have the required permissions!', hidden = True)
        else:
            await target.kick(reason = reason)
            em = discord.Embed(description = f'{ctx.author.mention} kicked {target.mention}', color = 0x9E1ADF)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = target.name, icon_url = target.avatar_url)
            await ctx.send(embed = em)


    @cog_ext.cog_slash(name = 'ban', description = 'Ban a member', guild_ids = [901832876256026734])
    async def ban(self, ctx, target : discord.Member, *, reason = None):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send('You cannot ban members since you do not have the required permissions!', hidden = True)
        else:
            await target.ban(reason = reason)
            em = discord.Embed(description = f'{ctx.author.mention} banned {target.mention}', color = 0x9E1ADF)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = target.name, icon_url = target.avatar_url)
            await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Slash(bot))