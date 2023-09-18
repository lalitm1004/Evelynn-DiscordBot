import discord
from discord.ext import commands

from datetime import datetime

from main import mongo_cluster, fetch_guild_prefix


class InfoCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def get_highest_role_color(self, user: discord.Member):
        colored_roles = [
            role.color for role in user.roles if role.color != discord.Color.default()
        ]
        return colored_roles[-1] if colored_roles != [] else discord.Color.default()

    @commands.command(aliases=["server"])
    async def guild(self, ctx: commands.Context):
        guild_embed = discord.Embed(
            title=f"{ctx.guild.name}",
            timestamp=ctx.message.created_at,
            color=discord.Color.blurple(),
        )
        guild_embed.add_field(
            name="**Current Owner**", value=ctx.guild.owner.mention, inline=True
        )
        guild_embed.add_field(
            name="**Created On**",
            value=f"{ctx.guild.created_at.strftime('%d-%B-%Y')}",
            inline=True,
        )
        guild_embed.add_field(
            name="**Command Prefix**",
            value=f"`{fetch_guild_prefix(self.client, ctx.message)}`",
            inline=True,
        )
        guild_embed.add_field(
            name="**Member Count**", value=ctx.guild.member_count, inline=True
        )
        guild_embed.add_field(
            name="**Channel Count**", value=len(ctx.guild.channels), inline=True
        )
        guild_embed.add_field(
            name="**Category Count**", value=len(ctx.guild.categories), inline=True
        )

        guild_embed.set_thumbnail(url=ctx.guild.icon)
        guild_embed.set_footer(
            text=f"{ctx.author.display_name}", icon_url=ctx.author.display_avatar
        )

        await ctx.reply(embed=guild_embed)

    @commands.command(aliases=["pfp"])
    async def avatar(self, ctx: commands.Context, user: discord.Member = ""):
        if user == "":
            user = ctx.author

        avatar_embed = discord.Embed(
            title=f"{user.display_name}",
            timestamp=ctx.message.created_at,
            color=self.get_highest_role_color(user=user),
        )
        avatar_embed.set_image(url=user.display_avatar)
        avatar_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )

        await ctx.reply(embed=avatar_embed)

    # Error Handling

    @avatar.error
    async def avatar_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply(f"> **Error: User not found**")


def setup(client: commands.Bot):
    client.add_cog(InfoCog(client=client))
