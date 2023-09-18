from pymongo import MongoClient


class FunMongoDatabase:
    def __init__(self, mongo_cluster: MongoClient):
        self.mongo_cluster = mongo_cluster
        self.userDatabase = self.mongo_cluster["userDatabase"]
        self.fun_profiles = self.userDatabase["fun_profiles"]

    def create_user_profile(self, user_id: int) -> None:
        self.fun_profiles.insert_one({"_id": user_id, "commands_run": {}})

    def fetch_user_profile(self, user_id: int) -> dict:
        if self.fun_profiles.find_one({"_id": user_id}) is None:
            self.create_user_profile(user_id=user_id)
        return self.fun_profiles.find_one({"_id": user_id})

    def increment_commands_run(self, user_id: int, guild_id: int) -> None:
        user_profile = self.fetch_user_profile(user_id=user_id)
        commands_run: dict = user_profile["commands_run"]
        if str(guild_id) in commands_run.keys():
            commands_run[str(guild_id)] += 1
        else:
            commands_run[str(guild_id)] = 1

        self.fun_profiles.update_one(
            {"_id": user_id}, {"$set": {"commands_run": commands_run}}
        )
        return
