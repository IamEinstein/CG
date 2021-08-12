import pymongo
from dotenv import load_dotenv
import os
from discord.ext import commands
from utils.tz import IST, datetime_from_utc_to_local
from datetime import datetime
from umongo import Document, fields
from umongo.frameworks import PyMongoInstance
load_dotenv()

# !umongo
#  Basic setup
db = pymongo.MongoClient(os.getenv("DATABASE_URI"))['chronic']

instance = PyMongoInstance(db)
collection = db['data']
polls = db['polls']
registrations = db['registrations']
# User model


@instance.register
class ChronicGamer(Document):
    """
    Model for each gamer
    """
    username = fields.StringField(required=True)
    discord_id = fields.IntegerField(unique=True, required=True)
    games = fields.ListField(fields.StringField(), default=[])
    tier = fields.IntegerField(required=True)

    class Meta:
        collection_name = "data"

    async def is_registered(self=None, id=None):
        if id is None:
            return "Invalid ID"
        else:
            collection = db['data']
            number = collection.count_documents({"discord_id": id})
            return number >= 1



async def register(name, id):
    if await ChronicGamer.is_registered(id=id):
        return False
    cg = ChronicGamer(name=name, discord_id=id)
    ChronicGamer.commit()
    return True


async def remove_user(id):
    if await ChronicGamer.is_registered(id=id):
        collection.delete_one({"discord_id": id})
        return True
    return False

# Poll Model


@instance.register
class PollModel(Document):
    """
    MongoDB model for a poll
    """
    class Meta:
        collection_name = "polls"

    title = fields.StringField(unique=False)
    reactions = fields.ListField(fields.StringField())
    channel_id = fields.IntegerField(required=True)
    start_time = fields.DateTimeField(required=True)
    end_time = fields.DateTimeField(required=True)
    content = fields.StringField(required=True)
    poll_id = fields.IntegerField(required=True, unique=True)
    ended = fields.BooleanField(default=False)
    winner = fields.StringField(unique=False, default="None")
    winner_reaction_count = fields.IntegerField(default=0)
    tie = fields.BooleanField(default=False)
    tie_reaction_list = fields.ListField(fields.StringField(), default=[])

    async def check_ended_polls(self=None):
        for poll in polls.find({'ended': False}):
            ended_list = []
            if IST.localize(datetime_from_utc_to_local(poll['end_time'])) <= datetime.now(tz=IST):
                ended_list.append(poll)
                polls.find_and_modify(query={"_id": poll['_id']}, update={
                    '$set': {'ended': True}})
            return ended_list
            
        return None

# Registration Model


@instance.register
class RegistrationGamer(Document):
    class Meta:
        collection_name = "registrations"
    tier = fields.IntegerField(required=True)
    attachment_url = fields.UrlField(required=True)
    games = fields.ListField(fields.StringField(), default=[])
    username = fields.StringField(required=True, unique=False)
    dm_msg_id = fields.IntegerField(required=False)
    time_registered = fields.DateTimeField(default=datetime.now(tz=IST))
    discord_id = fields.IntegerField(required=True, unique=True)
    approved = fields.BooleanField(default=False)

    async def register(self=None, user=None):
        if self is not None:
            if self.approved is True:
                return "User already is registered"
            gamer = ChronicGamer(username=self.username, tier=self.tier,
                                 games=self.games, discord_id=self.discord_id)
            gamer.commit()
        elif self is None:
            if user['approved'] is True:
                return "User already is registered"
            gamer = ChronicGamer(username=user['username'], tier=user['tier'],
                                 games=user['games'], discord_id=user['discord_id'])
            gamer.commit()
        return gamer

    async def check_approved(self=None, bot: commands.Bot = None):
        for user in registrations.find({}):
            admin = bot.get_user(594093066839654418)
            msg_id = int(user['dm_msg_id'])
            msg = await admin.fetch_message(msg_id)
            for reaction in msg.reactions:
                if reaction.emoji == "✅":
                    user['approved'] is True
                    gamer = await self.register(user)
                    registrations.delete_one({"discord_id": user['id']})
                    print(f"{user}")
                    return gamer
