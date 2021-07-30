import asyncio

from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Register(commands.Cog):
    """
    Cog for the register command
    Registers users as a clan member
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="clan_register", description="Register for the clan", guild_ids=[850593645009698836])
    async def _clan_register(self, ctx: SlashContext, game: str, username: str, tier: int):
        if ctx.author.id != 764415588873273345:
            return await ctx.send("You are not authorised to use this command")
        await ctx.send("Ok, details recieved")


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
