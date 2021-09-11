import aiohttp
import os
import datetime
from mongo import PollModel
import discord
from discord import Embed
from utils.tz import datetime_from_utc_to_local, format_time, IST
from discord.ext import commands
from utils.colours import give_random_color
import discord
from importlib import reload
import asyncio
from dotenv import load_dotenv
from utils.colours import give_random_color
from discord.ext import commands
import cogs
import utils
import sys
import asyncio
import asyncpg
DEFAULT_DISABLED_MESSAGE = (
    "The bot's currently disabled. It may be refreshing for some quick updates, or down for another reason. "
    "Contact admins for further information"
)

if sys.platform == "linux":
    import uvloop
    uvloop.install()


async def connect_pg():
    """
    Connects and returns postgres database
    """
    load_dotenv()
    conn = await asyncpg.connect(user=os.getenv("PG_USER"), password=os.getenv("PG_PASSWORD"), database=os.getenv("PG_DATABASE"), host=os.getenv("PG_HOST"))
    return conn


async def determine_prefix(bot, message):
    cog = bot.get_cog("Bot")
    return await cog.determine_prefix(message.guild)


def is_enabled(ctx):
    if not ctx.bot.enabled:
        raise commands.CheckFailure(DEFAULT_DISABLED_MESSAGE)
    return True


class ClusterBot(commands.AutoShardedBot):

    class Embed(discord.Embed):
        def __init__(self, **kwargs):
            super().__init__(**kwargs, color=give_random_color())

    def load_dotenv(self):
        load_dotenv()

    def __init__(self, **kwargs):
        self.ready = False
        loop = asyncio.new_event_loop()
        super().__init__(**kwargs, loop=loop, command_prefix=determine_prefix)
        self.load_extension("jishaku")
        for i in cogs.cogs:
            self.load_extension(f"cogs.{i}")

        self.add_check(is_enabled)
        self.activity = discord.Game("Developed by Ash")
        self.http_session = aiohttp.ClientSession()
        self.loop.create_task(self.do_startup_tasks())
        self.run(kwargs["token"])
        self.database = asyncio.run(connect_pg)

    @property
    def log(self):
        return self.get_cog("Logging").log

    async def do_startup_tasks(self):
        self.log.info(
            f"Starting with shards {self.shard_ids} and total {self.shard_count}")
        await self.wait_until_ready()
        self.ready = True
        self.log.info(f"Logged in as {self.user}")

    async def on_ready(self):
        self.log.info(f"Bot is ready")

    async def on_shard_ready(self, shard_id):
        self.log.info(f"Shard {shard_id} ready")

    async def close(self):
        self.log.info("shutting down")
        await super().close()

    async def reload_modules(self):
        self.ready = False

        reload(cogs)

        for i in dir(utils):
            if not i.startswith("_"):
                reload(getattr(utils, i))

        for i in cogs.default:
            self.reload_extension(f"cogs.{i}")

        await self.do_startup_tasks()

    # Methods for creating embeds

    class Embeds():
        def create_team_emded(time: int, game: str):
            embed = Embed(colour=give_random_color(
            ), description=f"Time to play {game.content},react with 👍 if u in", title="Matchmaking")
            embed.set_footer(text=f"Ends in {str(time)} seconds")

            return embed

        def ready_embed(platform):
            """
            Embed for bot's startup message
            """
            embed = discord.Embed(title="Bot has started/restarted",
                                  description="Bot has started running, here are the details", color=give_random_color())
            local_timezone = datetime.datetime.now(
                datetime.timezone.utc).astimezone().tzinfo
            time = datetime.datetime.now()
            utc = datetime.datetime.utcnow()
            if utc > time:
                time_lag = utc-time
            else:
                time_lag = time-utc

            if platform == "linux":
                server = "replit"
            else:
                server = "Ash's computer"
            embed.add_field(name="Running on", value=server, inline=False)
            embed.add_field(name="Server timezone",
                            value=local_timezone, inline=True)
            embed.add_field(name="Sever time", value=f"{time}", inline=True)
            embed.add_field(name="UTC time", value=f"{utc}", inline=True)
            embed.add_field(name="Time lag(according to UTC)",
                            value=str(time_lag), inline=False)
            return embed

        def edit_msg(before, after):
            """
            Embed for edited message reporting
            """
            embed = discord.Embed(
                color=give_random_color(), url=before.jump_url, title=f"{before.author} edited a message", timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.add_field(name="Original Message",
                            value=f'{before.content}', inline=False)
            embed.add_field(name="Edited Message",
                            value=f'{after.content}', inline=True)
            embed.add_field(
                name="Channel", value=f"{before.channel.mention}", inline=True)
            return embed

        def del_msg(message: discord.Message):
            """
            Embed for deleted message reporting
            """
            embed = discord.Embed(
                color=give_random_color(), url=message.jump_url, title=f"{message.author} deleted a message", timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=message.author.avatar_url)

            embed.add_field(name="Message Content",
                            value=f'{message.content}', inline=False)
            embed.add_field(
                name="Channel", value=f"{message.channel.mention}", inline=True)
            return embed

        async def log_poll(poll: PollModel, bot: commands.Bot):
            time_started = format_time(IST.localize(
                datetime_from_utc_to_local(poll['start_time'])))
            time_ended = format_time(IST.localize(
                datetime_from_utc_to_local(poll['end_time'])))
            msg_id = poll['poll_id']
            reaction_count = poll['winner_reaction_count']
            guild = bot.get_channel(int(poll['channel_id'])).guild
            message = await bot.get_channel(int(poll['channel_id'])).fetch_message(msg_id)
            icon_url = guild.icon_url
            guild_name = guild.name
            url = message.jump_url
            embed = discord.Embed(
                title=f"Poll ended in {guild_name}", url=url, thumbnail=icon_url, color=give_random_color())
            embed.add_field(name="Poll topic", value=poll['title'])
            embed.add_field(
                name="Started", value=str(time_started))
            embed.add_field(name="Ended", value=str(time_ended))
            embed.add_field(name="Ended at",
                            value=f"{str(datetime.datetime.now(tz=IST))}")
            embed.add_field(
                name="Winner", value=f"Winner {poll['winner']}, Votes: {reaction_count}")
            return embed

        def dm_join_embed(channel):
            embed = discord.Embed(colour=give_random_color(), title="Welcome to Chronic Gamers",
                                  description=f"Welcome to Chronic Gamers (CG). We are a lively and friendly community built around zombsroyale, minecraft and other games. Kindly check the rules here, {channel.mention}.", timestamp=datetime.datetime.now(IST))
            return embed

        def approved_embed(user):
            embed = discord.embed(color=give_random_color(), title="Registration successful",
                                  description=f"Hi {user.mention}, we are glad to announce that your registration for the chronic members clan has been approved.")
            return embed

        def info_embed(ctx: commands.Context, author: discord.User = None):

            user = ctx.author
            id = user.id
            avatar_url = user.avatar
            time_created = user.created_at
            embed = discord.Embed(colour=give_random_color(
            ), title="User information", timestamp=datetime.datetime.now())
            embed.add_field(name="id", value=id, inline=False)
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Creation Date", value=format_time(
                time_created), inline=False)
            embed.add_field(name="Username",
                            value=f"{user.name}#{user.discriminator}")
            icon = ctx.bot.user.avatar
            embed.set_footer(text="Chronic Gamers", icon_url=icon)
            return embed

        def leave_embed(user: discord.User):
            embed = discord.Embed(colour=give_random_color(
            ), title="A Member has left us.", description=f"{user.name + user.discriminator} has left the server")
            return embed

    class Messages():
        duration_message = '''
How long should the poll last(duration in minutes)
For eg, if you want the poll to be for 2 hours, type 120
'''

        channel_message = "Which channel do you want to the poll to be in?"
        timeout_message = """
Hmm, 
Looks like you took a lot of time and...
timeout
Try faster next time 😉
        """
        react_message = """
Okay, now type the emojis with which u want to react
For eg, if the emojis are 😇 and 😈
Type
`😇 😈`
        """
        topic_msg = "Enter the topic of the poll"

    # Postgres methods
    async def make_table(self, guild: discord.Guild):
        id = guild.id
        conn = self.database
        # levelling user model
        #  Fields= user_id, messages, level(level of user according to number of messages), roles(list for roles of levels),
        await conn.execute(f"CREATE TABLE {id}(USER_ID PRIMARY KEY, LEVEL NUMBER, MESSAGES NUMBER)")

    async def get_table(self, guild_id):
        self.conn.execute(f"SELECT * FROM {guild_id}")
