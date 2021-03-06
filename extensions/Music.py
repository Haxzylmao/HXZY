import asyncio
import discord
import youtube_dl
from discord.ext import commands
import datetime
import time
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.send('I joined the voice channel!')


    @commands.command(name = 'stream')
    @commands.guild_only()
    async def stream(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        em = discord.Embed(description = f"**Now streaming** `{player.title}`", color = 0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)



    @commands.command(name = 'play', aliases = ['p'])
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        em = discord.Embed(description = f"**Now playing** `{player.title}`", color = 0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)


    @commands.command(name = 'volume')
    @commands.guild_only()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        em = discord.Embed(description = f"Volume changed to `{volume}`", color = 0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)


    @commands.command(name = 'stop')
    @commands.guild_only()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('????')



    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx):
        """Pauses the music"""
        server = ctx.message.guild
        voice_channel = server.voice_client             
        voice_channel.pause()
        em = discord.Embed(description = f"**Paused** Waiting for `*resume`", color=0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed =em)


    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx):
        """Resumes the music"""
        server = ctx.message.guild
        voice_channel = server.voice_client                
        voice_channel.resume()
        em = discord.Embed(description = f"**Resumed**", color = 0x9E1ADF)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed =em)



    @play.before_invoke
    @stream.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))