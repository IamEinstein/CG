from discord.ext import commands
import re


class Register(commands.Cog):
    """
    Cog for the register command
    Registers users as a clan member
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def clan_register(self, ctx: commands.Context):
        if ctx.author.id != 850589370569195541:
            return await ctx.send("You are not authorised to use this command")
        msg_format = r"""
Game: .{32}
Username: .{64}
Tier: \d{1:4}
        """
        if re.match(msg_format, ctx.message.content):
            if ctx.message.attachments != None and len(ctx.message.attachments != 0):
                url = ctx.message.attachments[0].url
            else:
                await ctx.send("There is no attachment in this message, kindly attach a visual proof for registration")
        else:
            await ctx.send(f"Your format is not correct, the correct format is `{str(msg_format)}`")


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
