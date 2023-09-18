import discord
from discord.ext import commands

from main import mongo_cluster
from cogs.funCog.fun_database import FunMongoDatabase

import asyncio
import random
from pathlib import Path

"""
Command List :
- who (who_asked)
- _8ball (8ball)
- megamind
- oogway
- bite
- cry
- hug
- kiss
- pat
- slap
"""


class FunAssets:
    def __init__(self):
        # Paths
        self.temp_dir = Path("cogs/funCog/funAssets")

        # Font Paths
        self.impact_ttf = Path("cogs/funCog/funAssets/impact.ttf")

        # Image Paths
        self.megamind_jpg = Path("cogs/funCog/funAssets/megamind.jpg")
        self.oogway_jpg = Path("cogs/funCog/funAssets/oogway.jpg")

        # GIF Lists
        self.crying = [
            "https://imgur.com/N1NGru9.gif",
            "https://imgur.com/Iz9rmCa.gif",
            "https://imgur.com/6bkhWV3.gif",
            "https://imgur.com/Ys3grqA.gif",
            "https://imgur.com/f76ExfA.gif",
            "https://imgur.com/WA2LS64.gif",
            "https://imgur.com/E29HJwY.gif",
            "https://imgur.com/hkN5dGX.gif",
            "https://imgur.com/f5dzSMB.gif",
            "https://imgur.com/1vZ2DAF.gif",
            "https://imgur.com/tls3uWU.gif",
            "https://imgur.com/8QYrJ0P.gif",
            "https://imgur.com/FLEhlr6.gif",
            "https://imgur.com/xiqkjhV.gif",
            "https://imgur.com/rn6llX0.gif",
            "https://imgur.com/wx2dgJF.gif",
            "https://imgur.com/aAYAe9i.gif",
            "https://imgur.com/G415UjX.gif",
            "https://imgur.com/Nbsl37n.gif",
            "https://imgur.com/mwReVy3.gif",
            "https://imgur.com/aaOHhvg.gif",
            "https://imgur.com/bfJr8r2.gif",
            "https://imgur.com/rN0t1wy.gif",
            "https://imgur.com/aLs9qIX.gif",
            "https://imgur.com/E4l4IGp.gif",
            "https://imgur.com/aLLjGKU.gif",
            "https://imgur.com/iJ2bXb8.gif",
            "https://imgur.com/ce94yy7.gif",
            "https://imgur.com/avk4Bwm.gif",
            "https://imgur.com/WdVLSlj.gif",
        ]

        self.hug = [
            "https://imgur.com/1Uw0ND9.gif",
            "https://imgur.com/YxvTmyc.gif",
            "https://imgur.com/8k5NNUb.gif",
            "https://imgur.com/4TuksAR.gif",
            "https://imgur.com/Bavj850.gif",
            "https://imgur.com/0HXKt2a.gif",
            "https://imgur.com/I8LZHal.gif",
            "https://imgur.com/NjNsGFn.gif",
            "https://imgur.com/UslK0cS.gif",
            "https://imgur.com/l78ohvk.gif",
            "https://imgur.com/4t5uJ2N.gif",
            "https://imgur.com/S0ASo84.gif",
        ]

        self.pat = [
            "https://imgur.com/KAzbNLq.gif",
            "https://imgur.com/4qBalr8.gif",
            "https://imgur.com/jVGaByM.gif",
            "https://imgur.com/9qd3MXD.gif",
            "https://imgur.com/okQ9QrO.gif",
            "https://imgur.com/KyQIY1u.gif",
            "https://imgur.com/UNAaXdN.gif",
            "https://imgur.com/EfxfZUG.gif",
            "https://imgur.com/hF5QWGU.gif",
            "https://imgur.com/FzG4eeh.gif",
            "https://imgur.com/gUQUhFc.gif",
            "https://imgur.com/WSoOjaa.gif",
            "https://imgur.com/0T7H8f7.gif",
            "https://imgur.com/QjzBz51.gif",
            "https://imgur.com/Dy1oifq.gif",
            "https://imgur.com/62ttoDz.gif",
            "https://imgur.com/RX7Nx0C.gif",
            "https://imgur.com/aNzWCzs.gif",
        ]

        self.slap = [
            "https://imgur.com/zKd1pO1.gif",
            "https://imgur.com/ohgZMD9.gif",
            "https://imgur.com/JITUsIV.gif",
            "https://imgur.com/doU1KiI.gif",
            "https://imgur.com/Ilh9bqW.gif",
            "https://imgur.com/E1G5W1P.gif",
            "https://imgur.com/Q4s479V.gif",
            "https://imgur.com/ZWmwYHg.gif",
            "https://imgur.com/t3NzlZK.gif",
            "https://imgur.com/DvVRnyu.gif",
            "https://imgur.com/usSLcMb.gif",
            "https://imgur.com/V5ybKS8.gif",
            "https://imgur.com/vA9IZwe.gif",
            "https://imgur.com/hDtKB8e.gif",
            "https://imgur.com/kKrgq90.gif",
            "https://imgur.com/s4MWZXa.gif",
            "https://imgur.com/3ovGhM2.gif",
            "https://imgur.com/3xKrPYx.gif",
            "https://imgur.com/psoGkoM.gif",
            "https://imgur.com/Ua2PFYo.gif",
            "https://imgur.com/WqFkZTy.gif",
            "https://imgur.com/4frsdM7.gif",
        ]

        self.bite = [
            "https://imgur.com/OgqMrw0.gif",
            "https://imgur.com/EktgFMV.gif",
            "https://imgur.com/PgHynhe.gif",
            "https://imgur.com/IhIY3qM.gif",
            "https://imgur.com/RydRfST.gif",
            "https://imgur.com/UwEfBp1.gif",
            "https://imgur.com/GgsLzxZ.gif",
            "https://imgur.com/JOqds2Q.gif",
            "https://imgur.com/HZ28tFJ.gif",
            "https://imgur.com/x08s87w.gif",
            "https://imgur.com/wkEYTk6.gif",
            "https://imgur.com/aI0QT7x.gif",
            "https://imgur.com/lGxGeb7.gif",
            "https://imgur.com/21kkhnf.gif",
            "https://imgur.com/9yf7q5r.gif",
            "https://imgur.com/X8Z11bB.gif",
        ]

        self.kiss = [
            "https://imgur.com/sohGagM.gif",
            "https://imgur.com/hmIUzco.gif",
            "https://imgur.com/NcSoOE2.gif",
            "https://imgur.com/uG6mFAF.gif",
        ]

        self.scrunkly = ["https://imgur.com/QnHkrYy.gif"]


class FunCommandsCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.assets = FunAssets()
        self.mongo_database = FunMongoDatabase(mongo_cluster=mongo_cluster)

    def fetch_highest_role_color(self, user: discord.Member):
        roles = user.roles
        colored_roles = [
            role for role in roles if role.color != discord.Color.default()
        ]

        return (
            colored_roles[-1].color if colored_roles != [] else discord.Color.default()
        )

    # Text reply commands
    @commands.command(aliases=["who_asked"])
    async def who(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.5)
            await ctx.reply(
                random.choice(
                    [
                        "No one.",
                        "According to my calculations, 0 people asked.",
                        "I used all of NASA's satellites, and still couldnt find who asked",
                        "ERROR - NO ONE FOUND",
                    ]
                )
            )

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx: commands.Context, question: str):
        responses = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes - definitely.",
            "You may rely on it.",
        ]

        await ctx.reply(f"`{random.choice(responses)}`")

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    # GIF Reaction Commands

    @commands.command()
    async def bite(self, ctx: commands.Context, member: discord.Member = ""):
        if member == "" or member == ctx.author:
            member = ctx.author
            embed_title = (
                f"{ctx.author.display_name} bites themselves in their confusion!"
            )
        else:
            embed_title = f"{ctx.author.display_name} bites {member.display_name}!"

        bite_embed = discord.Embed(
            title=embed_title,
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        bite_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        bite_embed.set_image(url=random.choice(self.assets.bite))

        await ctx.reply(embed=bite_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command()
    async def cry(self, ctx: commands.Context):
        member = ctx.author

        crying_embed = discord.Embed(
            title=f"{member.display_name} cries",
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        crying_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        crying_embed.set_image(url=random.choice(self.assets.crying))

        await ctx.reply(embed=crying_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command()
    async def hug(self, ctx: commands.Context, member: discord.Member = ""):
        if member == "" or member == ctx.author:
            member = ctx.author
            embed_title = f"{ctx.author.display_name} hugs themselves! Sad."
        else:
            embed_title = f"{ctx.author.display_name} hugs {member.display_name}!"

        hug_embed = discord.Embed(
            title=embed_title,
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        hug_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        hug_embed.set_image(url=random.choice(self.assets.hug))

        await ctx.reply(embed=hug_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command()
    async def kiss(self, ctx: commands.Context, member: discord.Member = ""):
        if member == "" or member == ctx.author:
            member = ctx.author
            embed_title = f"{ctx.author.display_name} kisses themselves! Sad."
        else:
            embed_title = f"{ctx.author.display_name} kisses {member.display_name}!"

        kiss_embed = discord.Embed(
            title=embed_title,
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        kiss_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        kiss_embed.set_image(url=random.choice(self.assets.kiss))

        await ctx.reply(embed=kiss_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command()
    async def pat(self, ctx: commands.Context, member: discord.Member = ""):
        if member == "" or member == ctx.author:
            member = ctx.author
            embed_title = f"{ctx.author.display_name} pats themselves! Sad."
        else:
            embed_title = f"{ctx.author.display_name} pats {member.display_name}!"

        pat_embed = discord.Embed(
            title=embed_title,
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        pat_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        pat_embed.set_image(url=random.choice(self.assets.pat))

        await ctx.reply(embed=pat_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    @commands.command()
    async def slap(self, ctx: commands.Context, member: discord.Member = ""):
        if member == "" or member == ctx.author:
            member = ctx.author
            embed_title = (
                f"{ctx.author.display_name} slaps themselves in their confusion!"
            )
        else:
            embed_title = f"{ctx.author.display_name} slaps {member.display_name}!"

        slap_embed = discord.Embed(
            title=embed_title,
            timestamp=ctx.message.created_at,
            color=self.fetch_highest_role_color(user=member),
        )
        slap_embed.set_footer(
            text=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        slap_embed.set_image(url=random.choice(self.assets.slap))

        await ctx.reply(embed=slap_embed)

        self.mongo_database.increment_commands_run(
            user_id=ctx.author.id, guild_id=ctx.guild.id
        )

    # Error Handling

    @_8ball.error
    async def _8ball_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("`Error: Missing [question] parameter`")

    @bite.error
    async def bite_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("`Error: User not found`")

    @hug.error
    async def hug_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("`Error: User not found`")

    @kiss.error
    async def kiss_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("`Error: User not found`")

    @pat.error
    async def pat_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("`Error: User not found`")

    @slap.error
    async def slap_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("`Error: User    not found`")


def setup(client: commands.Bot):
    client.add_cog(FunCommandsCog(client))
