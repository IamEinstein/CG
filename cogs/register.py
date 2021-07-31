import discord
from discord.ext import commands


class Register(commands.Cog):
    """
    Cog for the register command
    Registers users as a clan member
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Registers users in the clan.The format is `cg!register <NameofGame> <Username> <Tier>` .The message should also have an attachment as the proof of their ranking.")
    async def register(self, ctx: commands.Context, game: str, username: str, tier: int):
        """
        Registers you as a clan member
        Format should be:
        `cg!register <NameoftheGame> <Username> <Tier>`
        """
        attachments = ctx.message.attachments
        if len(attachments) > 0:
            await ctx.message.reply("Ok, details recieved")
        else:
            return await ctx.send("No attachments recieved")
        admin = self.bot.get_user(594093066839654418)
        embed = discord.Embed(author=ctx.author.name+ctx.author.discriminator, footer=f"Registration by {ctx.author.mention}",
                              title="New registration for CG Clan", url=ctx.message.jump_url, description=f"Hi {admin.mention}, we got a new registration for the CG Clan.")
        await admin.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
