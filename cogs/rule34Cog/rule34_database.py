from pymongo import MongoClient


class Rule34MongoDatabase:
    def __init__(self, mongo_cluster: MongoClient):
        self.userDatabase = mongo_cluster["userDatabase"]
        self.rule34_profiles = self.userDatabase["rule34_profiles"]

    def create_user_profile(self, user_id: int) -> None:
        self.rule34_profiles.insert_one(
            {
                "_id": user_id,
                "blacklist": [],
                "blacklist_enabled": True,
                "commands_run": {},
            }
        )
        return

    def fetch_user_profile(self, user_id: int) -> dict:
        if self.rule34_profiles.find_one({"_id": user_id}) is None:
            self.create_user_profile(user_id=user_id)
        return self.rule34_profiles.find_one({"_id": user_id})

    def increment_commands_run(self, user_id: int, guild_id: int) -> None:
        user_profile = self.fetch_user_profile(user_id=user_id)
        commands_run: dict = user_profile["commands_run"]
        if str(guild_id) in commands_run.keys():
            commands_run[str(guild_id)] += 1
        else:
            commands_run[str(guild_id)] = 1

        self.rule34_profiles.update_one(
            {"_id": user_id}, {"$set": {"commands_run": commands_run}}
        )
        return

    def fetch_blacklist(self, user_id: int) -> list:
        user_profile = self.fetch_user_profile(user_id=user_id)
        return user_profile["blacklist"]

    def add_to_blacklist(self, user_id: int, tags: list) -> None:
        if len(tags) == 0:
            return
        user_profile = self.fetch_user_profile(user_id=user_id)
        blacklist: list = user_profile["blacklist"]
        for tag in tags:
            blacklist.append(tag)
        self.rule34_profiles.update_one(
            {"_id": user_id}, {"$set": {"blacklist": sorted(blacklist)}}
        )
        return

    def remove_from_blacklist(self, user_id: int, tags: list) -> None:
        if len(tags) == 0:
            return
        user_profile = self.fetch_user_profile(user_id=user_id)
        blacklist: list = user_profile["blacklist"]
        updated_blacklist = [tag for tag in blacklist if tag not in tags]
        self.rule34_profiles.update_one(
            {"_id": user_id}, {"$set": {"blacklist": sorted(updated_blacklist)}}
        )
        return

    def clear_blacklist(self, user_id: int):
        user_profile = self.fetch_user_profile(user_id=user_id)
        self.rule34_profiles.update_one({"_id": user_id}, {"$set": {"blacklist": []}})

    def blacklist_enabled(self, user_id: int) -> bool:
        user_profile = self.fetch_user_profile(user_id=user_id)
        return user_profile["blacklist_enabled"]

    def toggle_blacklist(self, user_id: int) -> None:
        user_profile = self.fetch_user_profile(user_id=user_id)
        self.rule34_profiles.update_one(
            {"_id": user_id},
            {"$set": {"blacklist_enabled": not user_profile["blacklist_enabled"]}},
        )
        return
