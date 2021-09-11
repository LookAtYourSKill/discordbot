import asyncio
import datetime
import sys
import discord
import pytz
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def getRoles(roles):
        roles.reverse()
        roles = [f'{role.mention}' for role in roles if not role.is_default()]
        thing = ''

        for role in roles:
            if len(thing + str(role)) > 970:
                thing += '...'
                break
            thing += f'{role} '

        else:
            return thing

    @commands.command(name='user', aliases=['userinfo', 'info'])
    async def user(self, ctx, member: discord.Member):
        if not member:
            member = ctx.author
        de = pytz.timezone('Europe/Berlin')
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        roles = self.getRoles(member.roles)
        if not member:
            member = ctx.author
        embed = discord.Embed(title=f'> Userinfo für {member.display_name}',
                              description='',
                              color=0x4cd137,
                              timestamp=datetime.datetime.utcnow().astimezone(tz=de))

        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.add_field(name='**Name**',
                        value=f'```Name: {member.name}#{member.discriminator}\n'
                              f'ID: {member.id}\n'
                              f'Nick: {(member.nick if member.nick else "Nein")}\n```',
                        inline=False)
        embed.add_field(name='**Account**',
                        value=f'```Discord Beigetreten: {member.created_at.strftime("%d.%m.%Y")}\n'
                              f'Bot : {("Ja" if member.bot else "Nein")}\n'
                              f'Farbe : {member.color}\n'
                              f'Status : {member.status}\n'
                              f'Join Position : {str(members.index(member)+1)}```',
                        inline=False)
        embed.add_field(name='**Server**',
                        value=f'```Server Beigetreten : {member.joined_at.strftime("%d.%m.%Y")}\n'
                              f'Booster: {("Ja" if member.premium_since else "Nein")}```',
                        inline=False)
        embed.add_field(name='**Rollen**',
                        value=f'{roles}'
                              f'```Rollen des Users: {len(member.roles) - 1}\n'
                              f'Höchste Rolle: {member.top_role.name}```',
                        inline=False)
        embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='server', aliases=['serverinfo', 'guild'])
    async def server(self, ctx):
        de = pytz.timezone('Europe/Berlin')
        roles = self.getRoles(ctx.guild.roles)
        days = (datetime.datetime.utcnow() - ctx.guild.created_at).days
        role_count = len(ctx.guild.roles)
        embed = discord.Embed(title=f' ',
                              description=' ',
                              color=0x4cd137,
                              timestamp=datetime.datetime.utcnow().astimezone(tz=de))

        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'> Info für {ctx.guild.name}',
                        value=f'```Name : {ctx.guild.name}\n'
                              f'ID : {ctx.guild.id}\n'
                              f'Owner ID : {ctx.guild.owner_id}\n'
                              f'Region : {ctx.guild.region}```',
                        inline=False)
        embed.add_field(name='**Daten**',
                        value=f'```Erstellt: {ctx.guild.created_at.strftime("%d.%m.%Y")}\n'
                              f'Vor {days} Tagen Erstellt\n'
                              f'Boost Status : {ctx.guild.premium_subscription_count}/30```',
                        inline=False)
        embed.add_field(name='**Channel**',
                        value=f'```Insgesamt : {len(ctx.guild.channels)}\n'
                              f'Textchannel : {len(ctx.guild.text_channels)}\n'
                              f'Voicechannel : {len(ctx.guild.voice_channels)}\n'
                              f'Kategorien : {len(ctx.guild.categories)}```')
        embed.add_field(name='**Member**',
                        value=f'```{ctx.guild.member_count}```',
                        inline=False)
        embed.add_field(name='**Rollen**',
                        value=f'{roles}',
                        inline=False)
        embed.add_field(name='**Rollen**',
                        value=f'```Default Role : {ctx.guild.default_role}\n'
                              f'Alle Rollen : {str(role_count)}```',
                        inline=False)
        embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='member')
    async def members(self, ctx):
        embed = discord.Embed(title='**Member Count**',
                              description=f'Auf diesem Server sind `{ctx.guild.member_count}` Mitglieder!')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def join_position(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        await ctx.send(f'`Join Position : {str(members.index(member) + 1)}`')

    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed = discord.Embed(title='**Member joined**',
                              description=f'You joined at the `{ctx.author.joined_at.strftime("%d.%m.%Y")}`\n'
                                          f'Join Position : `{str(members.index(member) + 1)}`')
        await ctx.send(embed=embed)

    @commands.command(name='bot', aliases=['botinfo'])
    async def bot(self, ctx):
        BOT_VERSION = 'v1.1'
        PREFIX = '?'
        de = pytz.timezone('Europe/Berlin')
        python_version = '{}.{}.{}'.format(*sys.version_info[:3])
        embed = discord.Embed(title=f'> Bot Info ',
                              description='',
                              color=0x4cd137,
                              timestamp=datetime.datetime.utcnow().astimezone(tz=de))

        embed.add_field(name='**Besitzer**',
                        value='```LookAtYourSkill#0001\nID: 493370963807830016```',
                        inline=True)
        embed.add_field(name='Versionen',
                        value=f'```Python: {python_version}\nDiscord: {discord.__version__}```',
                        inline=True)
        embed.add_field(name='**Other**',
                        value=f'```Bot Version: {BOT_VERSION}\nBot Prefix: {PREFIX}```',
                        inline=True)
        embed.set_footer(text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}',
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        icon = member.avatar_url
        embed = discord.Embed(title='',
                              color=0x123456,
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'{member.name}#{member.discriminator}',
                         icon_url=icon)
        embed.set_image(url=icon)
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'Angefordert von {ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot)
                )
