import discord
from discord.ext import commands

from main import mongo_cluster
from cogs.guildSetupCog.guildSetup_database import GuildMongoDatabase


class GuildSetupCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.mongo_database = GuildMongoDatabase(cluster=mongo_cluster)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx: commands.Context, new_prefix: str):
        if self.mongo_database.fetch_guild_prefix(guild_id=ctx.guild.id) == new_prefix:
            await ctx.reply("> **Error: New prefix must be different from old one**")
            return

        self.mongo_database.update_guild_prefix(
            guild_id=ctx.guild.id, new_prefix=new_prefix
        )
        await ctx.reply(
            f"> **Prefix for **`{ctx.guild.name}`** is set to **`{new_prefix}`"
        )
        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.mongo_database.fetch_guild_profile(guild_id=guild.id)
        return

    # Error Handling
    @change_prefix.error
    async def change_prefix_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                content="> **Error: Only administrators can run this command**"
            )


def setup(client: commands.Bot):
    client.add_cog(GuildSetupCog(client=client))
