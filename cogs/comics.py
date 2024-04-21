""" comics module """
from re import findall
from random import randint

from discord import Color, Embed
from discord.ext import commands


class Comics(commands.Cog):
    """
    Retrieve & view comic strips from GoComics.com & others

    Can *very* easily be expanded to process any comic strip found
    on this list: https://www.gocomics.com/comics/a-to-z
    """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

    @commands.command()
    async def gmg(self, ctx):
        """
        Sends a random Garfield Minus Garfield comic

        Usage: <prefix>gmg
        """
        # not a gocomics comic, files are stored in cloud
        embed = Embed(
            title='Garfield Minus Garfield', color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('gmg', tag=True))
        await ctx.send(embed=embed)

    @commands.command()
    async def xkcd(self, ctx):
        """ gets a random comic from xkcd """
        # official API doesn't support random, so we parse the main site
        # first to get the ID # of the latest comic for our random choice
        html = await self.ass.get_url_data('https://xkcd.com')
        max_num = findall(r'(?<=xkcd\.com\/)\d+', html)

        if not max_num:
            raise commands.CommandError("Couldn't extract highest comic ID.")

        random_id = randint(1, int(max_num[0]))
        json_data = await self.ass.get_url_data(
            f'https://xkcd.com/{random_id}/info.0.json', get_type='json'
        )
        embed = Embed(
            title=(
                f"XKCD: {json_data['safe_title']} "
                f"({json_data['month']}/{json_data['day']}"
                f"/{json_data['year']})"
            ),
            # description=f"*{json_data['alt']}*",
            color=Color.random()
        )
        embed.set_image(url=json_data['img'])
        embed.set_footer(text=json_data['alt'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['bd'])
    async def boondocks(self, ctx):
        """
        Sends a random Boondocks comic

        Usage: <prefix>boondocks
        Aliases: bd
        """
        await self._handle_gocomics_comic(ctx, 'boondocks', 'The Boondocks')

    @commands.command(aliases=['c&h'])
    async def cah(self, ctx):
        """
        Sends a random Calvin & Hobbes comic

        Usage: <prefix>cah
        Aliases: c&h
        """
        await self._handle_gocomics_comic(
            ctx, 'calvinandhobbes', 'Calvin & Hobbes'
        )

    @commands.command(aliases=['gf'])
    async def garfield(self, ctx):
        """
        Sends a random Garfield comic

        Usage: <prefix>garfield
        Aliases: gf
        """
        await self._handle_gocomics_comic(ctx, 'garfield', 'Garfield')

    @commands.command(aliases=['p'])
    async def peanuts(self, ctx):
        """
        Sends a random Peanuts comic

        Usage: <prefix>peanuts
        Aliases: p
        """
        await self._handle_gocomics_comic(ctx, 'peanuts', 'Peanuts')

    @commands.command(aliases=['pb'])
    async def peanutsb(self, ctx):
        """
        Sends a random Peanuts Begins comic

        Usage: <prefix>peanutsb
        Aliases: pb
        """
        await self._handle_gocomics_comic(
            ctx, 'peanuts-begins', 'Peanuts Begins')

    @commands.command(aliases=['scribbles', 'ss'])
    async def sarah(self, ctx):
        """
        Sends a random Sarah's Scribbles comic

        Usage: <prefix>sarah
        Aliases: pb
        """
        await self._handle_gocomics_comic(
            ctx, 'sarahs-scribbles', "Sarah's Scribbles"
        )

    async def _handle_gocomics_comic(self, ctx, url_id, name):
        """
        This gets the HTML of the URL of the comic using the url_id
        that was passed over. It then grabs the date the comic appeared
        & the comic's image to send.
        """
        html = await self.ass.get_url_data(
            f'https://www.gocomics.com/random/{url_id}')

        # I should probably be using bs4 for this for
        # performance reasons
        date = findall(r'(?<=formatted-date=").+?(?=")', html)
        image_url = findall(r'(?<=data-image=").+?(?=")', html)

        if not date:
            raise commands.CommandError("Couldn't extract date.")
        if not image_url:
            raise commands.CommandError("Couldn't extract image URL.")

        embed = Embed(
            title=f'{name}: {date[0]}', color=Color.random()
        )
        embed.set_image(url='attachment://comic.gif')

        # attaching because discord shows attached images larger than
        # URL images for some reason. also no idea why GoComics is using
        # .gif format for their images, but they are
        comic = await self.ass.get_discord_file(image_url[0], 'comic.gif')
        await ctx.send(embed=embed, file=comic)

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system"""
    await bot.add_cog(Comics(bot))
