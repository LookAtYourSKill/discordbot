import asyncio
import json
import discord
from discord.ext import commands


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bladd', aliases=['blacklistadd'])
    @commands.has_permissions(manage_messages=True)
    async def blacklist_add(self, ctx, text):
        with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json", "r") as f:
            data = json.load(f)
            if text in data["blacklist"]:
                embed = discord.Embed(title='<:close:864599591692009513> **ERROR**',
                                      description=f'`Das Wort ({text})` ist **bereits in der Blacklist!**')
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
                return
            else:
                data["blacklist"].append(text)
        with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json", "w") as file:
            json.dump(data, file, indent=4)
            embed = discord.Embed(title='',
                                  description='')
            embed.add_field(name='<:open:869959941321011260> **Blacklist Add**',
                            value=f'Hinzugefügtes Wort:\n'
                                  f'`{text}`',
                            inline=False)
            await ctx.send(embed=embed, delete_after=5)
            await ctx.message.delete()

    @commands.command(name='blrm', aliases=['blacklistremove'])
    @commands.has_permissions(manage_messages=True)
    async def blacklist_remove(self, ctx, text):
        with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json", "r") as f:
            data = json.load(f)
            if text not in data["blacklist"]:
                embed = discord.Embed(title='<:close:864599591692009513> **ERROR**',
                                      description=f'`Das Wort ({text})` ist **nicht in der Blacklist!**')
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
                return
            else:
                data["blacklist"].remove(text)
        with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json", "w") as file:
            json.dump(data, file, indent=4)
            embed = discord.Embed(title='',
                                  description='')
            embed.add_field(name='<:open:869959941321011260> **Blacklist Remove**',
                            value=f'**Entferntes Wort:**\n'
                                  f'`{text}`',
                            inline=False)
            await ctx.send(embed=embed, delete_after=5)
            await ctx.message.delete()

    @commands.command(name='blshow', aliases=['blacklistshow'])
    @commands.has_permissions(manage_messages=True)
    async def blacklist_show(self, ctx):
        with open('C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json', 'r') as f:
            data = json.load(f)
            blacklist = 'C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json'
            empty = []
            if blacklist == empty:
                embed = discord.Embed(title='',
                                      description='')
                embed.add_field(name='<:close:864599591692009513> **ERROR**',
                                value='`Die Blacklist ist leer!`',
                                inline=False)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
            else:
                embed = discord.Embed(title='',
                                      description='')
                embed.add_field(name='**Blacklist Words**',
                                value=f'`{data["blacklist"]}`',
                                inline=False)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.author.send(embed=embed)
                await ctx.message.delete()

    @commands.command(name='blclear', aliases=['blacklistclear'])
    @commands.has_permissions(manage_messages=True)
    async def blacklist_clear(self, ctx):
        with open('C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json', 'r') as f:
            data = json.load(f)
            blacklist = 'C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/blacklist.json'
            if not blacklist:
                embed = discord.Embed(title='',
                                      description='')
                embed.add_field(name='<:close:864599591692009513> **ERROR**',
                                value='`Die Blacklist ist bereits leer!`',
                                inline=False)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
            else:
                with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/spam-detection.json", "r+") as file:
                    await asyncio.sleep(1)
                    file.truncate(0)
                with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json/spam-detection.json", "r+") as file:
                    json.dump(file, data, indent=4)
                embed = discord.Embed(title='',
                                      description='')
                embed.add_field(name='<:open:869959941321011260> **Deleted All Blacklisted Words**',
                                value=f'Deleted Words: `{data}`',
                                inline=False)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()

def setup(bot):
    bot.add_cog(Automod(bot))
