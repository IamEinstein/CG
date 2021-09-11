from discord.ext import commands
from ..bot import ClusterBot
import asyncio
import asyncpg
import discord

# TODO: Add sql commands


class Postgres(commands.Cog):
    def __init__(self, bot: ClusterBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        guild = message.guild
        guild_id = guild.id
        bot = self.bot
        bot.get_table(guild_id=guild_id)
