""" wrestling module """

from discord import Color, Embed, Member
from discord.ext import commands


class Wrestling(commands.Cog):
    """ wrestling-related commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

    @commands.command()
    async def curse(self, ctx, users: commands.Greedy[Member]):
        """
        Inflict a very nice, very evil curse upon @user(s)

        Usage: <prefix>curse @user(s)
        """

        has_have = 'has' if len(users) == 1 else 'have'
        cursed_users = await self.gen.format_users(users)

        embed = Embed(
            description=(
                f'{cursed_users} {has_have} been **CURSED** by Danhausen.'),
            color=Color.random()
        )
        # embed.set_author(
        #     name="Danhausen's Curse", icon_url=await self.ass.get_url('bbb')
        # )
        embed.set_image(url=f'{await self.ass.get_url('curse')}.gif')
        await ctx.send(embed=embed)

    @commands.command(aliases=['deeznuts', 'redeem'])
    async def deez(self, ctx, users: commands.Greedy[Member]):
        """
        Ask @user(s) to redeem deez nuts

        Usage: <prefix>deez @user(s)
        Aliases: deeznuts, redeem
        """
        deez_users = await self.gen.format_users(users)

        embed = Embed(
            description=f'{deez_users} **REDEEM DEEZ NUTS!!!**',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('deez.gif'))
        await ctx.send(embed=embed)

        # deez_url = await self.ass.get_url('deez.gif')
        # deez_bin = await self.ass.get_discord_file(deez_url, 'deez.gif')

        # await ctx.send(f'{deez_users} **REDEEM DEEZ NUTS!!!**', file=deez_bin)

    @commands.command(aliases=['del'])
    async def delete(self, ctx, users: commands.Greedy[Member]):
        """
        Tells @user(s) they will be deleted

        Usage: <prefix>delete @user(s)
        Aliases: del
        """
        del_users = await self.gen.format_users(users)

        embed=Embed(
            description=f'{del_users} will be **DELETED**!!!',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('mh_delete.gif'))
        await ctx.send(embed=embed)
        # del_url = await self.ass.get_url('mh_delete.gif')
        # del_bin = await self.ass.get_discord_file(del_url, 'mh_delete.gif')

        # await ctx.send(f'{del_users} will be **DELETED**!!!', file=del_bin)

    @commands.command()
    async def eviluno(self, ctx):
        """
        Sends Evil Uno 'farts a lot' meme

        Usage: <prefix>eviluno
        """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('evil_uno'))
        await ctx.send(embed=embed)
        # await ctx.reply(await self.ass.get_url('evil_uno'))

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Wrestling(bot))
