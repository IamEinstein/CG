from bot import ClusterBot
import discord
import os
from dotenv import load_dotenv
load_dotenv()
bot = ClusterBot(intents=discord.Intents.all(), token=os.getenv('BOT_TOKEN'))
