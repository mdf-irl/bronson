""" comics module """
from io import BytesIO
from re import findall

from discord import Color, Embed, File
from discord.ext import commands

class Comics(commands.Cog):
    """
    Retrieve & view comic strips from GoComics.com

    Can *very* easily be expanded to process any comic strip found
    on this list: https://www.gocomics.com/comics/a-to-z
    """
    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    @commands.command(aliases=['c&h'])
    async def cah(self, ctx):
        """
        Sends a random Calvin & Hobbes comic

        Usage: <prefix>cah
        Aliases: c&h
        """
        await self._handle_gocomics_comic(ctx, 'calvinandhobbes',
                                          'Calvin & Hobbes')

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
        await self._handle_gocomics_comic(ctx, 'peanuts-begins',
                                          'Peanuts Begins')

    async def _handle_gocomics_comic(self, ctx, url_id, name):
        """
        This gets the HTML of the URL of the comic using the url_id
        that was passed over. It then grabs the date the comic appeared
        & the comic's image to send.
        """
        try:
            html = await self.ass.get_text(
                f'https://www.gocomics.com/random/{url_id}')
        except Exception:
            await ctx.reply("**Error**: Couldn't get HTML.")
            raise

        #I should probably be using bs4 for this for
        #performance reasons
        date = findall('(?<=formatted-date=").+?(?=")', html)
        image_url = findall('(?<=data-image=").+?(?=")', html)

        if (not date) or (not image_url):
            await ctx.reply("**Error**: Couldn't extract date or image URL.")
            raise ValueError("Couldn't extract date or image URL.")

        embed = Embed(title=f'{name}: {date[0]}', color=Color.yellow())
        embed.set_author(name="Bronson's Comics",
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_image(url='attachment://comic.gif')

        #attaching because discord shows attached images larger than
        #URL images for some reason. also no idea why GoComics is using
        #.gif format for their images, but they are
        comic = File(BytesIO(await self.ass.get_binary(image_url[0])),
                     filename='comic.gif')
        await ctx.reply(embed=embed, file=comic)

async def setup(bot):
    """ add class to bot's cog system"""
    await bot.add_cog(Comics(bot))
