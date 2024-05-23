""" fangulese module """
from random import choice, randint

from discord import Color, Embed, Member  # , Status
from discord.ext import commands


class Fangulese(commands.Cog):
    """ Fangulese & c0n-adjacent commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

    @commands.command(aliases=['btoborg', 'btoborg1'])
    async def bronson(self, ctx):
        """
        Sends a mug shot of the original Bronson

        Usage: <prefix>bronson
        Aliases: btoborg, btoborg1
        """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('bronson'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['itb'])
    async def bufu(self, ctx: commands.Context,
                   users: commands.Greedy[Member]):
        """bufu user(s)"""
        bufu_users = await self.gen.format_users(users)
        embed = Embed(
            description=(
                f"oKaY YeA {bufu_users} YeW aRe oH FiSHaLLy BeiNg BuFu'd "
                "LoL oKaY YeA oKaY iN tHe MoTHeRFucKiN' BuTT oKaY TeA "
                "LoL iTb iTb HAh HE hE OHo HO LoL!!! oKaY dO NoT tRy 2 "
                "ReSiSt pL UeA iN tHe MoTHeRFuCkiN' aSSHoLe OkKaAyYYyYy "
                f"BuYYYY!!!! EyE'm GuNnA GiTcHa {bufu_users} oKaY YeA EyE "
                "YaM GuNnA BuFu YeW LoL!!!!!!!!! oKaY YeA KoN YeW r GiTTiN "
                "BuFu'd LoL!!!!!!!!!! oKaAaaYYyYY BuYyYYy!!!!!"
            ), color=Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def hack(self, ctx, users: commands.Greedy[Member]):
        """ hack @user(s) """
        has_have = 'HaZ' if len(users) == 1 else 'HaVe'
        hacked_users = await self.gen.format_users(users)

        embed = Embed(
            title='SMMPHA', description=(
                f'{hacked_users} {has_have} BeEn HaCKeD!!! LoL!!!!! '
                'oKaY KoN eYe HaVe HaKkEd YeR CoMp LoL oKaY YeaH oKaY LoL '
                'YeW HaVe BeEn r0oTeD LoL!!!\n\n'

                'eYe HaVe SucKSeSsFuLLy HiT YeW WitH tHe SeQUeNTiaL '
                'MuLTi-MaTRiX PiNCeR HaK aTTacK!!! hAh HEhe hOh oKaYyYYyY '
                'BuYYy!!!'
            ), color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('hack.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ha(self, ctx):
        """ Sends a ha he ho message """
        msg = [
            'AH haH HEhEH ehh HO o ho Ho Ho OHO!!!!!'
            'HAhA HEH hEHeh he HEHE ho Ho HO HAhAH HEheh eh OH ohOHO!!!!!!',
            'hA HEHHEHAhAH HEh HAH HE hE oHOh o ho hOh OHO!!!!!!!!',
            'HAhAHaHhe hEH hO ohO Ho HAhAH ehhEh eh HOhoHoHo!!!',
            'Ahah HEHhaHAhehH ho hOH oh Oh OAhHAH heh ehe hOH oHOHOoO!!!',
            'HAhAhAhAHHEh hEHE hEHHE Ho o HOAhAHH hEHEHEH hohOhOhOhOHO!!!!!!!',
            'HAhAhHHE hHE HeHE hHE o ho Ho HOHahHAhhHE h HHehH hOhO Hoh oO!!!',
            'HAhah AH haH AhEHh Hehhe HOH oHO h OHAhaHah hEHEHEH hHo H HoHO!!',
            'hAhAhHEH ehEH EH h oh oh o H AHhAHAH heh HEHEHh Oh OH OhOO!!!!!',
            'AHAHhAHHAhAHH Hehe HEHEH hOhOhOHOh aHaHhhAhh hHEheh HOOhOhOoO!!!'
        ]
        embed = Embed(
            description=f'{choice(msg)} {choice(msg)}', color=Color.random()
        )
        await ctx.send(embed=embed)

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
        embed = Embed(description=response, color=Color.random())
        await ctx.send(embed=embed)

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

        embed = Embed(
            description=self._get_alt_caps(f'{oo}k{aa}{yy} {pp}owerslam{ex}'),
            color=Color.random()
        )
        await ctx.send(embed=embed)

    @commands.is_nsfw()
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
        await ctx.send(':poop: **WARNING** :poop:', file=sludge_bin)

    @commands.command()
    async def tohd(self, ctx, users: commands.Greedy[Member]):
        """
        Hits @user(s) with the touch of hurtness distance

        Usage: <prefix>tohd @user(s)
        """
        tohd_users = await self.gen.format_users(users)
        embed = Embed(
            description=(f'TUCH OV HERTNISS DISSTINTS ON U {tohd_users} '
                         'IYAHHHHHHHHHH!!!!11'),
            color=Color.random()
        )
        await ctx.send(embed=embed)

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

        embed = Embed(
            description=f'{tee}\n{heee}\n{heeee}', color=Color.random()
        )
        await ctx.send(embed=embed)

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

        embed = Embed(
            description=(f'Y{ee}H{aa}{ww}{ex}\n'
                         f"RIDIN' A MOTHERFUCKIN' COWBOY{ex * 2} :cowboy:"),
            color=Color.random()
        )
        await ctx.send(embed=embed)

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
        if isinstance(error, commands.CheckFailure):
            await ctx.reply(
                '**Error**: This command can only be used in channels tagged '
                'as **NSFW**.'
            )
        else:
            await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Fangulese(bot))
