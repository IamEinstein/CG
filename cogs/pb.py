from discord.ext import commands
import discord
import aiohttp
import io
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("API_KEY")


class PikaBot(commands.Cog):
    """
    Thanks @PichuPikaRai for this code
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def lyrics(self, ctx, *, song):
        pass

    @commands.command()
    async def add(self, ctx, num1: float, num2: float):
        await ctx.send(num1 + num2)

    @commands.command()
    async def subtract(self, ctx, num1: float, num2: int):
        await ctx.send(num1 - num2)

    @commands.command()
    async def divide(self, ctx, num1: float, num2: float):
        await ctx.send(num1 / num2)

    @commands.command()
    async def multiply(self, ctx, num1: float, num2: float):
        await ctx.send(num1 * num2)

    @commands.command()
    @commands.is_owner()
    async def petpet(self, ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author

        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"huh, what u tryna see aye aye ?"
            ) as resp:

                if 300 > resp.status >= 200:
                    fp = io.BytesIO(await resp.read())

                    await ctx.reply(file=discord.File(fp, 'petpet.gif'))
                else:
                    await ctx.reply('Couldnt get image :(')

                await session.close()

    @commands.command()
    async def avatar(ctx, *, member: discord.Member = None):
        await ctx.send(member.avatar_url)

    '''@commands.command()
    async def stupid(ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author

        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f""
            ) as resp:

                if 300 > resp.status >= 200:
                    fp = io.BytesIO(await resp.read())

                    await ctx.reply(file=discord.File(fp, 'stupid.gif'))
                else:
                    await ctx.reply('Couldnt get image :(')

                await session.close()'''

    '''def get_birb():
        #making a GET request to the endpoint.
        resp = requests.get("animal/birb")
        #checking if resp has a healthy status code.
        if 300 > resp.status_code >= 200:
            content = resp.json() #We have a dict now.
        else:
            content = f"Recieved a bad status code of {resp.status_code}."
        #print(content)
    get_birb()'''

    '''@client.event
    async def on_message(message):
    if message.author == client.user:
    return

    if message.content.startswith('pb birb'):
        birb = get_birb()
        await message.channel.send(birb)'''

    '''@client.command()
    async def pikachu(ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author

        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"pokedex?pokemon=pikachu"
            )
            as resp: 

                if 300 > resp.status >= 200:
                    fp = io.BytesIO(await resp.read())

                    await ctx.reply(file=discord.File(fp, 'stupid.gif'))
                else:
                    await ctx.reply('Couldnt get image :(')

                await session.close()'''

    # Kick Command

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.send("You have been kicked from CG | Community, because"+reason)
        await member.kick(reason=reason)
        await ctx.send(f'{member} was kicked.')

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to kick people")

    # Ban Command

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.send("You have been banned from CG | Community, because"+reason)
        await member.ban(reason=reason)
        await ctx.send(f'{member} was banned.')

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to ban people")


def setup(bot: commands.Bot):
    bot.add_cog(PikaBot(bot))
