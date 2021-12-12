import discord
import time
import os
from discord.ext import commands
import sys
from .messages.embeds import ready_embed, edit_msg, del_msg, dm_join_embed, leave_embed
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv

class Bot(commands.Cog):
    """
    Basic bot setup
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_hook = discord.Webhook.from_url(url=os.getenv("LOG_WEBHOOK"),
                                           adapter=RequestsWebhookAdapter())
        self.purge_hook= discord.Webhook.from_url(url=os.getenv("PURGE_WEBHOOK"),
                                           adapter=RequestsWebhookAdapter())

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
        if before.guild.id == 804047321276743680:

            channel = self.bot.get_channel(856767714520465459)
            if int(
                    before.channel.id
            ) == 856767714520465459 or before.author.bot is True or before.content == after.content:
                pass
            else:

                self.log_hook.send(embed=edit_msg(before, after))
        else:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.guild.id == 804047321276743680:
            channel = self.bot.get_channel(856767714520465459)
            if int(message.channel.id) == 856767714520465459:
                pass
            else:
                self.log_hook.send(embed=del_msg(message))
        else:
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NotOwner):
            return await ctx.send(
                f"{ctx.author.mention}, you are not the owner of this bot")
        return await ctx.send(str(error))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == 850593645009698836:
            return
        return await member.send(
            embed=dm_join_embed(self.bot.get_channel(820292134715916298)))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == 850593645009698836:
            return
        channel = self.bot.get_channel(840509242300694559)

        return await channel.send(embed=leave_embed(member))

    @commands.command()
    async def invite(self, ctx):
        if ctx.author.id == 764415588873273345:
            return await ctx.author.send(os.getenv("BOT_LINK"))
        return await ctx.send("You are not authorised to use this command")
      
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for message in messages:
            # try:
            #   e = message.embed
            #   self.purge_hook.send("Message with embed deleted",embed=message.embed)  
            # except AttributeError:
            #   pass
            self.purge_hook.send(embed=del_msg(message))
          

def setup(bot):
    bot.add_cog(Bot(bot))
