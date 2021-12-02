import discord
from discord.ext import commands
import time
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'lock', description = 'Lock a channel!')
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description = f'Locked {channel.mention}', color = 0x9E1ADF)
        em.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = em)



    @commands.command(name = 'unlock', description = 'Unlock a channel!')
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description = f'Unlocked {channel.mention}', color = 0x9E1ADF)
        em.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = em)
    
    @commands.command(name = 'kick')
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, target : discord.Member = None, *, reason = None):
        if target is None:
            await ctx.send('Please provide a member to **kick**')

        if target == ctx.author:
            await ctx.send('You cannot **kick** yourself')

        if target == self.bot.user:
            await ctx.send('I cannot **kick** myself')
        else:
            await target.kick(reason = reason)
            em = discord.Embed(description = f'{ctx.author.mention} kicked {target.mention}', color = 0x9E1ADF)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = target.name, icon_url = target.avatar_url)
            await ctx.send(embed = em)



    @commands.command(name = 'ban')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, target : discord.Member = None, *, reason = None):
        if target is None:
            await ctx.send('Please provide a member to **ban**')

        if target == ctx.author:
            await ctx.send('You cannot **ban** yourself')

        if target == self.bot.user:
            await ctx.send('I cannot **ban** myself')

        else:
            await target.ban(reason = reason)
            em = discord.Embed(description = f'{ctx.author.mention} banned {target.mention}', color = 0x9E1ADF)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = target.name, icon_url = target.avatar_url)
            await ctx.send(embed = em)



    @commands.command(name = 'mute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, target : discord.Member = None, *, reason = None):
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role not in ctx.guild.roles:
            await ctx.send('A **mute** role does not exist!')

        if role in target.roles:
            await ctx.send('This member is already **muted** the command you may be looking for is **unmute**')

        else:
            await target.add_roles(role)
            em = discord.Embed(description = f'{ctx.author.mention} muted {target.mention}', color = 0x9E1ADF)
            em.set_author(name = target.name, icon_url = target.avatar_url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = em)





    @commands.command(name = 'unmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, target : discord.Member = None, *, reason = None):
        role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if role not in target.roles:
            await ctx.send('This member is already **unmuted** the command you may be looking for is **mute**')

        else:
            await target.remove_roles(role)
            em = discord.Embed(description = f'{ctx.author.mention} unmuted {target.mention}', color = 0x9E1ADF)
            em.set_author(name = target.name, icon_url = target.avatar_url)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = em)


    @commands.command(name = 'clear', aliases = ['purge'])
    @commands.guild_only()
    async def clear(self, ctx, amount : int = None):
            if amount is None:
                await ctx.send('Please provide a `number` of messages to **purge**')
            if amount >= 99:
                await ctx.send('Please delete less than **99** messages')
            else:
                await ctx.channel.purge(limit = amount)
                await ctx.send(f'Purged `{amount}` messages', delete_after = 3)



    @commands.command(name = 'slowmode')
    @commands.guild_only()
    async def slowmode(self, ctx, seconds : int = 0):
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay = 0)
            await ctx.send('Removed **slowmode delay**')
        else:
            await ctx.channel.edit(slowmode_delay = seconds)
            await ctx.send(f'Slowmode set to **{seconds}**')



def setup(bot):
    bot.add_cog(Moderation(bot))