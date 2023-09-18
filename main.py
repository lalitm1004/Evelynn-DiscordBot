import discord
from discord.ext import commands

import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Setting up global constants
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUG_CHANNEL_ID = int(os.getenv("DEBUG_CHANNEL_ID"))
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

mongo_cluster = MongoClient(MONGO_DB_URL)


# Loading guild prefixes
def fetch_guild_prefix(client: commands.Bot, message: discord.Message) -> str:
    try:
        return mongo_cluster["guildDatabase"]["guild_profiles"].find_one(
            {"_id": message.guild.id}
        )["command_prefix"]
    except:
        return ">>"


client = commands.Bot(
    command_prefix=fetch_guild_prefix,
    help_command=None,
    intents=discord.Intents.all(),
)


@client.event
async def on_ready():
    debug_channel = await client.fetch_channel(DEBUG_CHANNEL_ID)
    await debug_channel.send(f"## Logged in as {client.user}")
    print(f"Logged in as {client.user}")


# Loading cogs
for folder in os.listdir(Path("./cogs")):
    for filename in os.listdir(Path(f"./cogs/{folder}")):
        if filename.endswith("_cog.py"):
            client.load_extension(f"cogs.{folder}.{filename[:-3]}")

client.run(BOT_TOKEN)
