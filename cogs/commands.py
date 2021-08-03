import itertools
import asyncio
from discord.ext import commands
from mongo import *
from .messages.embeds import create_team_emded
from .messages.dms import *
from .messages.poll import timeout_message
from .descriptions import maketeams_description


class CGCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["mt"], description=maketeams_description)
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
