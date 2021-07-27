import logging
import discord
from discord.ext import commands
import cogs
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Setup bot
token = os.getenv("BOT_TOKEN")
client = commands.Bot(command_prefix="cg!",
                      activity=discord.Game("Developed by Ash"), intents=discord.Intents.all(), help_command=None)

for i in cogs.cogs:
    client.load_extension(f"cogs.{i}")


if sys.platform == "linux":
    from keep_alive import keep_alive
    keep_alive()
    print('Waiting for bot to get ready')
    client.run(token)
else:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    print('Waiting for bot to get ready')
    client.run(token)