import discord
from discord.ext import commands
import asyncio


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(AFK(bot))