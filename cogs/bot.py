import discord
import datetime
from discord import Color
from discord.ext import commands
import sys
from .embeds import bot
from datetime import datetime
from utils.tz import IST


class Bot(commands.Cog):
    """
    Basic bot setup
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        "Tells when the bot is ready"
        print("Bot is ready")
        channel = self.bot.get_channel(840509242300694559)
        other_channel = self.bot.get_channel(869132416130891796)
        await channel.send(embed=bot.ready_embed(sys.platform))
        await other_channel.send(embed=bot.ready_embed(sys.platform))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        "Identifies and reports edited messages"
        channel = self.bot.get_channel(856767714520465459)
        if int(before.channel.id) == 856767714520465459 or before.author.bot == True or before.content == after.content:
            pass
        else:
            await channel.send(embed=bot.edit_msg(before, after))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(856767714520465459)
        if int(message.channel.id) == 856767714520465459:
            pass
        else:
            await channel.send(embed=bot.del_msg(message))

    @commands.command()
    async def help(self, ctx: commands.Context, *args, **kwargs):
        """
        Help command for the bot
        """
        embed = discord.Embed(color=Color.blue(), url="https://github.com/IamEinstein/CG",
                              title=f"Chronic Gamers Bot help,\n here are the list of commands", timestamp=datetime.now(tz=IST))
        embed.add_field(name="cg!register",
                        value="Type cg!register if you want to get registered as an ChronicGamer ", inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NotOwner):
            return await ctx.send(f"{ctx.author.mention}, you are not the owner of this bot")
        return await ctx.send(str(error))


def setup(bot):
    bot.add_cog(Bot(bot))