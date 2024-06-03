"""wrestling module"""
from discord import Color, Embed, Member
from discord.ext import commands


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Wrestling(bot))


class Wrestling(commands.Cog):
    """
    Wrestling related commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def choppy(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]=None
    ):
        """choppy choppy"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!choppy {ctx.author.mention}**)."
            )
        choppy_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=(
                f'{choppy_users} **I... CHOPPY CHOPPY.. YOUR.. PEE PEE!!!**'
            ),
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('choppy2.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def cry(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]=None
    ):
        """cry me a river"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!cry {ctx.author.mention}**)."
            )
        cry_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=f'{cry_users} **CRY ME A RIVER!**',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('cry.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def curse(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """Inflict a very nice, very evil curse upon @user(s)"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!curse {ctx.author.mention}**)."
            )
        has_have = 'has' if len(users) == 1 else 'have'
        cursed_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=(
                f'{cursed_users} {has_have} been **CURSED** by Danhausen.'),
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('curse.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['deeznuts', 'redeem'])
    async def deez(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]=None
    ):
        """Ask @user(s) to redeem deez nuts"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!deez {ctx.author.mention}**)."
            )
        deez_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=f'{deez_users} **REDEEM DEEZ NUTS!!!**',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('deez.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['del'])
    async def delete(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """Tells @user(s) they will be deleted"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!delete {ctx.author.mention}**)."
            )
        del_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=f'{del_users} will be **DELETED**!!!',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('mh_delete.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def eviluno(self, ctx: commands.Context):
        """Sends Evil Uno 'farts a lot' meme"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('evil_uno'))
        await ctx.send(embed=embed)

    @commands.command()
    async def hotrain(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]=None
    ):
        """Asks user(s) to come aboard the ho train"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!hotrain {ctx.author.mention}**)."
            )
        ho_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=(
                f"IT'S TIME, ONCE AGAIN, FOR {ho_users} TO COME "
                "ABOARD THE... **HOOOOOO TRAAAAIIIINNNNN**!!!"
            ),
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('ho_train.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def indeed(self, ctx: commands.Context):
        """sends indeed gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('indeed.gif'))
        await ctx.send(embed=embed)

