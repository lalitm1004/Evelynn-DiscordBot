from pymongo import MongoClient


class GuildMongoDatabase:
    def __init__(self, cluster: MongoClient):
        self.guildDatabase = cluster["guildDatabase"]
        self.guild_profiles = self.guildDatabase["guild_profiles"]

    # Guild Methods
    def create_guild_profile(self, guild_id: int) -> None:
        self.guild_profiles.insert_one(
            {
                "_id": guild_id,
                "command_prefix": ">>",
                "channel_data": {},
            }
        )
        return

    def fetch_guild_profile(self, guild_id: int) -> dict:
        if self.guild_profiles.find_one({"_id": guild_id}) is None:
            self.create_guild_profile(guild_id=guild_id)
        return self.guild_profiles.find_one({"_id": guild_id})

    def fetch_guild_prefix(self, guild_id: int) -> str:
        return self.fetch_guild_profile(guild_id=guild_id)["command_prefix"]

    def update_guild_prefix(self, guild_id: int, new_prefix: str) -> None:
        self.guild_profiles.update_one(
            {"_id": guild_id}, {"$set": {"command_prefix": new_prefix}}
        )
