import itertools
import asyncio
from discord.ext import commands
from mongo import *
from .messages.embeds import create_team_emded
from .messages.dms import *
from .messages.poll import timeout_message


class CGCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.command()
    # async def register(self, ctx: commands.Context):
    #     author = ctx.author
    #     if await ChronicGamer.is_registered(id=author.id):
    #         return await ctx.send(f"{ctx.author.mention}, You are already registered")
    #     await ctx.send("Please enter your name")

    #     try:
    #         name = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
    #     except asyncio.TimeoutError:
    #         return await ctx.send(f"{ctx.author.mention},The request to register has timed out. Kindly restart the process")
    #     else:
    #         if await register(name=str(name.content), id=ctx.author.id):
    #             await ctx.send(f"{ctx.author.mention}, you have been registered as an ChronicGamer")
    #         else:
    #             await ctx.send(f"{ctx.author.mention}, you are already registered")

    # @commands.command()
    # async def remove(self, ctx: commands.Context):

    #     id = ctx.author.id
    #     if not await ChronicGamer.is_registered(id=id):
    #         return ctx.send("You are not registered")
    #     await ctx.send("Type `yes` if you want to confirm your removal..")
    #     try:
    #         response = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
    #         if response.content.lower() != "yes" and response.content.lower() != "no":
    #             return await ctx.send("You didn't enter a valid response, the process has been cancelled")
    #         elif response.content.lower() == "no":
    #             return await ctx.send("Okay, the process is cancelled")
    #     except asyncio.TimeoutError:
    #         return await ctx.send("No response was recieved, the process has been cancelled")
    #     if await remove_user(id):
    #         await ctx.send(f"{ctx.author.mention}, you have been removed")
    #     else:
    #         await ctx.send("You are not registered")

    # @commands.command()
    # async def nodms(self, ctx: commands.Context):
    #     if ChronicGamer.is_registered(id=ctx.author.id):
    #         await ctx.send("Ok wait")
    #     else:
    #         await ctx.send(f"Oof {ctx.author.mention}!, you need to be registered to run this command.")

    @commands.command(alias="mt")
    async def maketeams(self, ctx: commands.Context):
        if ctx.author.id != 764415588873273345:
            return await ctx.send("You are not authorised to use this command yet")
        await ctx.send("Which game?")
        try:

            game = await self.bot.wait_for("message", check=lambda message: message.author.id == ctx.author.id, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send(timeout_message)
        if game != None:
            await ctx.send("How much time do you want to wait for making the teams (enter in seconds)")
            time = await self.bot.wait_for(
                "message", timeout=30, check=lambda message: message.author.id == ctx.author.id)
            try:
                time = int(time.content)
            except (TypeError, ValueError):
                await ctx.send("Not valid time")
            else:
                users = []
                msg = await ctx.send(embed=create_team_emded(game=game, time=time))
                await msg.add_reaction("👍")
                await asyncio.sleep(int(time))
                reacted_msg = await ctx.channel.fetch_message(msg.id)

                for reaction in reacted_msg.reactions:
                    user_list = await reaction.users().flatten()

                    for user in user_list:
                        print(user)
                        if user.id != 850589370569195541:
                            users.append(user)
                print(users)
                if users != None and users != []:
                    teams = list(itertools.permutations(users, 3))
                    if teams == None:
                        new_teams = list(itertools.permutations(users, 2))
                        if new_teams == None:
                            new_new_teams = teams = list(
                                itertools.permutations(users, 1))
                            ctx.send(new_new_teams)
                        else:
                            ctx.send(new_teams)
                    else:
                        await ctx.send(teams)
                else:
                    await ctx.send("NO one reacted :|")


def setup(bot):
    bot.add_cog(CGCommands(bot))
