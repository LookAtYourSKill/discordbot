import discord
import youtube_dl
from discord.ext import commands
import ffmpeg

client = commands.Bot(intense=discord.Intents.all(), command_prefix='?')


class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title='<:close:864599591692009513> **ERROR**',
                                  description=f'You\'re not in a voice channel!')
            await ctx.send(embed=embed)
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            embed = discord.Embed(title='',
                                  description='Connected to your channel!')
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.move_to(voice_channel)
            embed = discord.Embed(title='',
                                  description=' Moved to your channel!')
            await ctx.send(embed=embed)

    @commands.command(name='leave', aliases=['l'])
    async def disconnect(self, ctx):
        embed = discord.Embed(title='',
                              description='Disconnected the channel!')
        await ctx.send(embed=embed)
        await ctx.voice_client.disconnect()

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, url):
        ctx.voice_client.pause()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 - reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn',
                          'executable': r'C:\ffmpeg\ffmpeg-N-103179-gac0408522a-win64-gpl\bin\ffmpeg.exe'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            embed = discord.Embed(title='',
                                  description='**Started Playing**')
            await ctx.send(embed=embed)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        embed = discord.Embed(title='',
                              description=f'Paused Playing')
        await ctx.send(embed=embed)
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        embed = discord.Embed(title='',
                              description=f'Resumed Playing')
        await ctx.send(embed=embed)
        await ctx.voice_client.resume()

    @commands.command(name='nowplaying', aliases=['np'])
    async def now_playing(self, ctx):
        embed = discord.Embed(title='',
                              description=f'Now playing : `{ctx.voice_client.current()}`')
        await ctx.send(embed=embed)

    @commands.command()
    async def loop(self, ctx):
        embed = discord.Embed(title='',
                              description=f'Loop is activated')
        await ctx.send(embed=embed)
        await ctx.voice_client.loop()

    @commands.command(name='volume')
    async def volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_client.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_client.volume = volume / 100
        await ctx.send(f'Volume of the player set to {volume}%')

    @commands.command()
    async def raft(self, ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title='<:close:864599591692009513> **ERROR**',
                                  description=f'You\'re not in a voice channel!')
            await ctx.send(embed=embed)
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio(
            'C:/Users/simon/Videos/4K Video Downloader/Raft/RAFT 1.01 Official Soundtrack   Full.mp3'))
        embed = discord.Embed(title='',
                              description='Now playing the **Raft theme song!**',
                              color=discord.Color.dark_blue())
        embed.set_image(url='https://cdn.discordapp.com/attachments/864513088396591156/875455286368948235/raftpng.png')
        await ctx.send(embed=embed)
        await ctx.voice_client.loop()


def setup(client):
    client.add_cog(MusicBot(client)
                   )
