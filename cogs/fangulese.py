""" fangulese module """
from random import randint

from discord import Member
from discord.ext import commands


class Fangulese(commands.Cog):
    """ Fangulese & c0n-adjacent commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    @commands.command(aliases=['btoborg', 'btoborg1'])
    async def bronson(self, ctx):
        """
        Sends a mug shot of the original Bronson

        Usage: <prefix>bronson
        Aliases: btoborg, btoborg1
        """
        await ctx.reply(await self.ass.get_url('bronson'))

    @commands.command(aliases=['hey', 'hi'])
    async def hello(self, ctx):
        """
        Sends the infamous Bronson 'almost a beard' hello

        Usage: <prefix>hello
        Aliases: hey, hi
        """
        response = (
            f'hello <@{ctx.author.id}> my name is bronson i am 15 years old '
            'and i have almost i ha a beard, but i should not have a beard '
            'because I am too young tough you know genetics lol. i like '
            'loud music and making games for byond.com. And my teachers are '
            'amazed that I practicly never have home work.'
        )
        await ctx.send(response)

    @commands.command(aliases=['ps', 'pslam'])
    async def powerslam(self, ctx):
        """
        Sends a powerslam

        Alternating caps.
        Emphasized/extended letters O, A, Y, P (and also !)

        Usage: <prefix>powerslam
        Aliases: ps, pslam
        """
        oo = f"{'o' * randint(5, 10)}"
        aa = f"{'a' * randint(5, 10)}"
        yy = f"{'y' * randint(5, 10)}"

        pp = f"{'p' * randint(11, 15)}"
        ex = f"{'!' * randint(11, 15)}"

        await ctx.send(self._get_alt_caps(f'{oo}k{aa}{yy} {pp}owerslam{ex}'))

    @commands.command(aliases=['sludgedump'])
    async def sludge(self, ctx):
        """
        Sends a random sludge dump

        The absolute pinnacle of technological innovation.

        Returns at random one of the finest sludge dumps scraped from
        /r/ratemypoo's top rated of all-time.

        Usage: <prefix>sludge
        Aliases: sludgedump
        """
        # attaching because discord doesn't play nicely with using
        # spoiler tags around an image URL
        sludge_url = await self.ass.get_url('sludge', tag=True)
        sludge_bin = await self.ass.get_discord_file(
            sludge_url, 'sludge.jpg', spoiler=True
        )

        await ctx.send(file=sludge_bin)

    @commands.command()
    async def tohd(self, ctx, users: commands.Greedy[Member]):
        """
        Hits @user(s) with the touch of hurtness distance

        Usage: <prefix>tohd @user(s)
        """
        if not users:
            raise commands.CommandError("You didn't @mention any user(s).")

        tohd_users = ', '.join(user.mention for user in users)

        await ctx.send(
            f'TUCH OV HERTNISS DISSTINTS ON U {tohd_users} '
            'IYAHHHHHHHHHH!!!!11'
        )

    @commands.command(aliases=['tehehe', 'teeheehee'])
    async def thh(self, ctx):
        """
        Sends Equ4L]ZeR0['s legendary tee heee heeee

        Each segment longer the last. Es extended.

        Usage: <prefix>thh
        Aliases: tehehe, teeheehee
        """
        tee = f"T{'E' * randint(10, 20)}"
        heee = f"H{'E' * randint(21, 30)}"
        heeee = f"H{'E' * randint(31, 40)}"

        await ctx.send(f'{tee}\n{heee}\n{heeee}')

    @commands.command(aliases=['yh'])
    async def yeehaw(self, ctx):
        """
        Sends a yeehaw

        E, A, W, ! extended.

        Usage: <prefix>yeehaw
        Aliases: yh
        """
        ee = f"{'E' * randint(5, 10)}"
        aa = f"{'A' * randint(5, 10)}"
        ww = f"{'W' * randint(5, 10)}"
        ex = f"{'!' * randint(5, 10)}"

        await ctx.send(
            f'Y{ee}H{aa}{ww}{ex}\n'
            f"RIDIN' A MOTHERFUCKIN' COWBOY{ex * 2} :cowboy:"
        )

    def _get_alt_caps(self, message):
        """
        Takes a message and returns it with alternating caps.
        """
        output_message = ''

        for i, char in enumerate(message):
            if i % 2 == 0:
                output_message += char.upper()
            else:
                output_message += char.lower()
        return output_message

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Fangulese(bot))
