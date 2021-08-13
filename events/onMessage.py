import discord
from discord.ext import commands


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json_files/spam-detection.json',
              'r+') as file:
        file.truncate(0)

    @commands.Cog.listener()
    async def on_message(self, message):
        counter = 0
        with open("C:/Users/simon/PycharmProjects/pythonProject/Discord Bot/utils/json_files/spam-detection.json",
                  "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            file.writelines(f"{str(message.author.id)}\n")
            if counter > 15:
                await message.guild.kick(message.author, reason="spam")
                channel = message.guild.get_channel(872945922743619657)
                embed = discord.Embed(title='',
                                      description='',
                                      color=discord.Color.random())
                embed.add_field(name='**Spam Detection Kick**',
                                value=f'Kicked User : `{message.author.name}#{message.author.discriminator}`\n'
                                      f'User ID : `{message.author.id}`\n'
                                      f'Gekickt von : `Ich seh dich#0264`')
                await channel.send(embed=embed)

        if message.content.startswith('<@790965419670241281>'):
            embed = discord.Embed(title="Prefix", color=0xff00c8)
            embed.add_field(name="Wowowow a Ping",
                            value=f"Mein Prefix: **?**\n"
                                  f"Mit ?help kannst du dir alle command anschauen!",
                            inline=False)
            await message.author.send(embed=embed)


def setup(bot):
    bot.add_cog(onMessage(bot))
