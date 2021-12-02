import discord
from discord.ext import commands
from discord import *
import datetime
import time
import json
import os
import random
from PIL import Image, ImageFont, ImageDraw
import requests
import aiohttp
import dateutil.parser

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = 'ping')
    @commands.guild_only()
    async def ping(self, ctx):
        em = discord.Embed(description = f'Pinging in **{round(self.bot.latency * 1000)}**ms 🔮', color = 0x9E1ADF)
        em.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)


    @commands.command(name = '8ball')
    @commands.guild_only()
    async def ball(self, ctx, *, question):
        awnsers = ['Yes', 'No', 'Most likely not', 'Probably', '100%', 'Will never happen', '**No**, what were you expecting...']
        choice = random.choice(awnsers)
        em = discord.Embed(description = "My answer is: " + choice, color = 0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)


    @commands.command(name = 'avatar', aliases = ['pfp', 'av'])
    @commands.guild_only()
    async def avatar(self, ctx, *, target : discord.Member = None):
        if target is None:
            target = ctx.author

        em = discord.Embed(description = f"{target.mention} profile picture", color = 0x9E1ADF)
        em.set_image(url = target.avatar_url)
        em.set_author(name = f'Requested by {ctx.author.name}', icon_url = ctx.author.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)




    @commands.command(name = 'say')
    @commands.guild_only()
    async def say(self, ctx, *, content = None):
        if content is None:
            await ctx.send('Thats not how this command words... You need to provide something for me to say!', delete_after = 3)
        if not ctx.author.guild_permissions.ban_members and content == '@everyone':
            await ctx.message.delete()
            await ctx.send('Did you just try to mention everyone without ban members permissions :skull:')
        else:
            await ctx.message.delete()
            await ctx.send(f'{content}')


    @commands.command(name = 'spotify')
    @commands.guild_only()
    async def spotify(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if spotify_result is None:
            await ctx.send(f'{user.name} is not listening to Spotify.')

        track_background_image = Image.open('assets/spotify_template.png')
        album_image = Image.open(requests.get(spotify_result.album_cover_url, stream=True).raw).convert('RGBA')
        title_font = ImageFont.truetype('fonts/theboldfont.ttf', 16)
        artist_font = ImageFont.truetype('fonts/theboldfont.ttf', 14)
        album_font = ImageFont.truetype('fonts/theboldfont.ttf', 14)
        start_duration_font = ImageFont.truetype('fonts/theboldfont.ttf', 12)
        end_duration_font = ImageFont.truetype('fonts/theboldfont.ttf', 12)
        title_text_position = 150, 30
        artist_text_position = 150, 60
        album_text_position = 150, 80
        start_duration_text_position = 150, 122
        end_duration_text_position = 515, 122
        draw_on_image = ImageDraw.Draw(track_background_image)
        draw_on_image.text(title_text_position, spotify_result.title, 'white', font=title_font)
        draw_on_image.text(artist_text_position, f'by {spotify_result.artist}', 'white', font=artist_font)
        draw_on_image.text(album_text_position, spotify_result.album, 'white', font=album_font)
        draw_on_image.text(start_duration_text_position, '0:00', 'white', font=start_duration_font)
        draw_on_image.text(end_duration_text_position,
                           f"{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}",
                           'white', font=end_duration_font)
        album_color = album_image.getpixel((250, 100))
        background_image_color = Image.new('RGBA', track_background_image.size, album_color)
        background_image_color.paste(track_background_image, (0, 0), track_background_image)
        album_image_resize = album_image.resize((140, 160))
        background_image_color.paste(album_image_resize, (0, 0), album_image_resize)
        background_image_color.convert('RGB').save('spotify.jpg', 'JPEG')
        f = discord.File('spotify.jpg')
        em = discord.Embed(color = 0x9E1ADF)
        em.set_author(name = f"{user.name}'s spotify status", icon_url = user.avatar_url)
        em.set_image(url = 'attachment://spotify.jpg')
        await ctx.send(embed = em, file = f)



    @commands.command(name = 'setbio', description = 'Set a short bio for yourself!')
    @commands.guild_only()
    async def setbio(self, ctx, *, bio = None):
        if bio is None:
            with open('storage/bio.json', 'r') as f:
                data = json.load(f)

            del data[str(ctx.author.id)]

            with open('storage/bio.json', 'w') as f:
                json.dump(data, f)


            em1 = discord.Embed(description = 'Your bio has been removed!', color = 0x9E1ADF)
            em1.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em1)


        else:
            with open('storage/bio.json', 'r') as f:
                data = json.load(f)

            data[str(ctx.author.id)] = bio

            with open('storage/bio.json', 'w') as f:
                json.dump(data, f)

            em = discord.Embed(description = f'Your bio is now: **{bio}**', color = 0x9E1ADF)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @commands.command(name = 'bio', description = 'Check your or another users bio!')
    @commands.guild_only()
    async def bio(self, ctx, user : discord.Member = None):
        if user is None:
            user = ctx.author

        with open('storage/bio.json', 'r') as f:
            data = json.load(f)


        data[str(user.id)]

        if data is None:
            await ctx.send('This user does not have a bio!')
        else:
            em = discord.Embed(description = f'{user.mention} bio: **{data[str(user.id)]}**', color = 0x9E1ADF)
            em.set_author(name = user.name, icon_url = user.avatar_url)
            await ctx.send(embed = em)





    @commands.command(name = 'whois', aliases = ['userinfo'], description = 'Get info about a user!')
    @commands.guild_only()
    async def whois(self, ctx, target : discord.Member = None):
        if target is None:
            target = ctx.author


        desc = f"""
Name: `{target.name}`

ID: `{target.id}`

Discriminator: `#{target.discriminator}`

Joined at: `{target.joined_at.strftime("%A, %B %d %Y at %H:%M:%S %p")}`

Created at: `{target.created_at.strftime("%A, %B %d %Y at %H:%M:%S %p")}`

Boosting: `{bool(target.premium_since)}`
"""

        em = discord.Embed(description = desc, color = 0x9E1ADF)
        em.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text = 'Requested by ' + ctx.author.name, icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = target.avatar_url)
        await ctx.send(embed = em)







    @commands.command(name = 'meme', description = 'Just a random meme')
    @commands.guild_only()
    async def meme(self, ctx):

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                title = res['data']['children'][random.randint(0,25)]["data"]["title"]
                embed = discord.Embed(color =0x9E1ADF)
                embed.set_author(name = title, icon_url = ctx.author.avatar_url)
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
        



def setup(bot):
    bot.add_cog(General(bot))