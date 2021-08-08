import discord
from discord.ext import commands, tasks
from .descriptions import register_description
from .messages.embeds import approved_embed
from mongo import RegistrationGamer


class Register(commands.Cog):
    """
    Cog for the register command
    Registers users as a clan member
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_approved.start()

    @commands.command(description=register_description)
    async def register(self, ctx: commands.Context, game: str, username: str, tier: int):
        """
        Registers you as a clan member
        Format should be:
        `cg!register <NameoftheGame> <Username> <Tier>`
        """
        attachments = ctx.message.attachments
        if len(attachments) > 0:
            await ctx.message.reply("Ok, details recieved. Processing your request.")

        else:
            return await ctx.send("No attachments recieved")
        admin = self.bot.get_user(594093066839654418)
        embed = discord.Embed(author=ctx.author.name+ctx.author.discriminator, footer=f"Registration by {ctx.author.mention}",
                              title="New registration for CG Clan", url=ctx.message.jump_url, description=f"Hi {admin.mention}, we got a new registration for the CG Clan.")
        msg = await admin.send(embed=embed)
        registration = RegistrationGamer(
            username=username, game=game, tier=tier, attachment_url=str(attachments[0]), dm_msg_id=msg.id)

    @tasks.loop(minutes=1)
    async def check_approved(self):
        "Checks for approvals for entering the clan."

        gamer = await RegistrationGamer.check_approved(self=None, bot=self.bot)
        if gamer:
            user = self.bot.get_user(user_id=gamer.discord_id)
            msg = await user.send(embed=approved_embed(user))
            print("Checked for approved registrations, got one")
        else:
            print("Checked for approved registrations")

    @check_approved.before_loop
    async def before_check_approved(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
