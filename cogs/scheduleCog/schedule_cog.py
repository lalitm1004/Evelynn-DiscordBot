import discord
from discord.ext import commands, tasks

from main import mongo_cluster


class ScheduleCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


def setup(client: commands.Bot):
    client.add_cog(ScheduleCog(client=client))
