import discord
from discord.ext import commands, tasks

import requests
import random

from main import mongo_cluster, fetch_guild_prefix
from cogs.rule34Cog.rule34_database import Rule34MongoDatabase


class Rule34Post:
    def __init__(self, post: dict):
        self.id = post["id"]
        self.tags = post["tags"]
        self.file_url = post["file_url"]

    def get_output_string(self):
        if len(self.tags) >= 1800:
            self.tags = self.tags[0:1801] + "...(exceeds character limit)"

        output = f"`Post from https://rule34.xxx`\n\n`ID` - `{self.id}`\n\n`Tags` : `{self.tags}`\n\n`URL` : {self.file_url}"
        return output


class Rule34API:
    def __init__(self):
        self.API_URL = (
            "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1"
        )
        self.cache = {}

    # Cache Methods
    def retrieve_from_cache(
        self, search_query: str, remove: bool = True
    ) -> Rule34Post | None:
        if search_query not in self.cache.keys():
            return
        elif len(self.cache[search_query]) == 0:
            self.cache.pop(search_query)
            return

        index = random.randint(0, len(self.cache[search_query]) - 1)
        post: Rule34Post = self.cache[search_query][index]
        if remove:
            self.cache[search_query].pop(index)
        return post

    def push_to_cache(self, search_query: str, posts: list) -> None:
        self.cache[search_query] = posts
        return

    # API Methods
    def search(self, search_query: str) -> Rule34Post | None:
        if self.retrieve_from_cache(search_query=search_query, remove=False) is None:
            try:
                json_response: list = requests.get(
                    f"{self.API_URL}&tags={search_query}&limit=1000"
                ).json()
            except:
                return
            to_cache = [Rule34Post(post) for post in json_response]
            self.push_to_cache(search_query=search_query, posts=to_cache)
        return self.retrieve_from_cache(search_query=search_query, remove=True)

    def latest(self) -> Rule34Post:
        return Rule34Post(requests.get(f"{self.API_URL}&limit=1").json()[0])


class Rule34Cog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.mongo_database = Rule34MongoDatabase(mongo_cluster=mongo_cluster)
        self.rule34_api = Rule34API()
        self.RULE34_GREEN = 0xAAE5A4
        self.clear_cache.start()

    # Clears cache every hour
    @tasks.loop(seconds=3600)
    async def clear_cache(self):
        self.rule34_api.cache = {}

    # Utility Functions
    def convert_to_list(self, tag_string: str):
        tag_list = tag_string.strip().lower().replace(",", " ").split(" ")
        tag_list = list(set([tag for tag in tag_list if tag != ""]))
        return tag_list

    def convert_to_string(self, tag_list: str, blacklist: bool = False):
        tag_string = ""
        for tag in tag_list:
            if blacklist:
                tag_string += f"-{tag} "
            else:
                tag_string += f"{tag} "
        return tag_string

    @commands.group(aliases=["r34"])
    @commands.is_nsfw()
    async def rule34(self, ctx: commands.Context):
        pass

    @rule34.group(aliases=["blist"])
    async def blacklist(self, ctx: commands.Context):
        pass

    @blacklist.command()
    async def view(self, ctx: commands.Context):
        blacklist = self.mongo_database.fetch_blacklist(user_id=ctx.author.id)
        blacklist_string = " ".join(blacklist) if blacklist != [] else "Empty"
        blacklist_enabled = self.mongo_database.blacklist_enabled(user_id=ctx.author.id)
        blacklist_enabled_string = "Enabled" if blacklist_enabled else "Disabled"

        blacklist_embed = discord.Embed(
            title=f"Rule34 Blacklist",
            description=f"`Blacklist` - `{blacklist_string}`\n\n`Blacklist is {blacklist_enabled_string}`",
            timestamp=ctx.message.created_at,
            color=self.RULE34_GREEN,
        )
        blacklist_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )

        await ctx.reply(embed=blacklist_embed)
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @blacklist.command()
    async def add(self, ctx: commands.Context, *, tags: str):
        tag_list = self.convert_to_list(tag_string=tags)

        blacklist = self.mongo_database.fetch_blacklist(user_id=ctx.author.id)
        absent_tags = []
        for tag in tag_list:
            if tag not in blacklist:
                absent_tags.append(tag)

        self.mongo_database.add_to_blacklist(user_id=ctx.author.id, tags=absent_tags)

        response_message = "> **Given tag(s) have been added to your blacklist.**"
        if len(absent_tags) != len(tag_list):
            response_message = f"> **The following tag(s) have been added to your blacklist:**`{' '.join(absent_tags)}`**, the rest were duplicates.**"

        await ctx.reply(content=response_message)
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @blacklist.command()
    async def remove(self, ctx: commands.Context, *, tags: str):
        tag_list = self.convert_to_list(tag_string=tags)
        blacklist = self.mongo_database.fetch_blacklist(user_id=ctx.author.id)
        present_tags = []
        for tag in tag_list:
            if tag in blacklist:
                present_tags.append(tag)

        self.mongo_database.remove_from_blacklist(
            user_id=ctx.author.id, tags=present_tags
        )

        response_message = (
            "> **Given tag(s) have been removed from your blacklist.**   "
        )
        if len(present_tags) != len(tag_list):
            response_message = f"> **The following tag(s) have been removed from your blacklist:**`{' '.join(present_tags)}`**, the rest were not in your blacklist:**"

        await ctx.reply(content=response_message)
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @blacklist.command()
    async def clear(self, ctx: commands.Context, confirmation: str = ""):
        if confirmation != ctx.author.display_name:
            warning_embed = discord.Embed(
                title="⚠️ CLEARING YOUR BLACKLIST ⚠️",
                description=f"This action will clear your blacklist. This action is irreversible.\n\nRun the command `{fetch_guild_prefix(self.client, ctx.message)}rule34 blacklist clear {ctx.author.display_name}` to clear your blacklist permanently.",
                timestamp=ctx.message.created_at,
                color=discord.Color.red(),
            )
            warning_embed.set_footer(
                text=ctx.author.display_name, icon_url=ctx.author.display_avatar
            )

            await ctx.reply(embed=warning_embed)
            return
        else:
            self.mongo_database.clear_blacklist(user_id=ctx.author.id)
            await ctx.reply("> **Your blacklist has been cleared.**")
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @blacklist.command()
    async def enable(self, ctx: commands.Context):
        blacklist_enabled = self.mongo_database.blacklist_enabled(user_id=ctx.author.id)

        if blacklist_enabled:
            await ctx.reply(f"> **Your blacklist is already enabled.**")
            return
        self.mongo_database.toggle_blacklist(user_id=ctx.author.id)
        await ctx.reply(f"> **Blacklist has been enabled.**")
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @blacklist.command()
    async def disable(self, ctx: commands.Context):
        blacklist_enabled = self.mongo_database.blacklist_enabled(user_id=ctx.author.id)

        if not blacklist_enabled:
            await ctx.reply(f"> **Your blacklist is already disabled.**")
            return
        self.mongo_database.toggle_blacklist(user_id=ctx.author.id)
        await ctx.reply(f"> **Blacklist has been disabled.**")
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @rule34.command()
    async def latest(self, ctx: commands.Context):
        await ctx.reply(self.rule34_api.latest().get_output_string())
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @rule34.command()
    async def random(self, ctx: commands.Context):
        blacklist = self.mongo_database.fetch_blacklist(user_id=ctx.author.id)
        blacklist_enabled = self.mongo_database.blacklist_enabled(user_id=ctx.author.id)
        blacklist_string = (
            self.convert_to_string(tag_list=blacklist, blacklist=True)
            if blacklist_enabled
            else ""
        )

        post = self.rule34_api.search(blacklist_string)
        if post is None:
            await ctx.reply(
                f"> **An unforseen Error has occured. Please contact walmartPhilosopher immediately.**"
            )
            return
        await ctx.reply(post.get_output_string())
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @rule34.command()
    async def search(self, ctx: commands.Context, *, tags: str):
        tag_list = self.convert_to_list(tag_string=tags)
        tag_string = self.convert_to_string(tag_list=tag_list, blacklist=False)

        blacklist = self.mongo_database.fetch_blacklist(user_id=ctx.author.id)
        blacklist_enabled = self.mongo_database.blacklist_enabled(user_id=ctx.author.id)
        blacklist_string = (
            self.convert_to_string(tag_list=blacklist, blacklist=True)
            if blacklist_enabled
            else ""
        )

        if blacklist_enabled:
            conflict_tags = []
            for tag in tag_list:
                if tag in blacklist:
                    conflict_tags.append(tag)

            if len(conflict_tags) >= 1:
                await ctx.reply(
                    f"> **Error: Conflicting Tag(s). The following tag(s) are in your blacklist and search query at the same time:** `{' '.join(conflict_tags)}`**. Remove them from your blacklist or disable your blacklist to search for them.**"
                )
                return

        search_query = (tag_string + blacklist_string).lstrip()
        post = self.rule34_api.search(search_query=search_query)
        if post is None:
            await ctx.reply(f"> **Error: Zero posts found for search query.**")
            return
        await ctx.reply(post.get_output_string())
        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    # Error Handling

    @rule34.error
    async def rule34_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.reply(
                f"> **Error: Command can only be run on channels marked NSFW.**"
            )


def setup(client: commands.Bot):
    client.add_cog(Rule34Cog(client=client))
