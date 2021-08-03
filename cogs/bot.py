import discord
import os
import datetime
from discord import Color
from discord.ext import commands
import sys
from .messages.embeds import ready_embed, edit_msg, del_msg
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
        channel = self.bot.get_channel(869494380770230282)
        other_channel = self.bot.get_channel(869132416130891796)
        await channel.send(embed=ready_embed(sys.platform))
        await other_channel.send(embed=ready_embed(sys.platform))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        "Identifies and reports edited messages"
        channel = self.bot.get_channel(856767714520465459)
        if int(before.channel.id) == 856767714520465459 or before.author.bot == True or before.content == after.content:
            pass
        else:
            await channel.send(embed=edit_msg(before, after))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(856767714520465459)
        if int(message.channel.id) == 856767714520465459:
            pass
        else:
            await channel.send(embed=del_msg(message))

    # @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NotOwner):
            return await ctx.send(f"{ctx.author.mention}, you are not the owner of this bot")
        # return await ctx.send(str(error))

    @commands.command()
    async def invite(self, ctx):
        if ctx.author.id == 764415588873273345:
            return await ctx.author.send(os.getenv("BOT_LINK"))
        else:
            return await ctx.send("You are not authorised to use this command")


def setup(bot):
    bot.add_cog(Bot(bot))
