""" comics module """
from datetime import datetime
from random import choice
from re import findall
from string import ascii_lowercase, digits

from aiohttp import ClientSession
from discord import Color, Embed, File
from discord.ext import commands

class Comics(commands.Cog):
    """
    Retrieve & view comic strips from GoComics.com
    
    It can *very* easily be expanded to process any comic strip found
    on this list: https://www.gocomics.com/comics/a-to-z
    """
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
        & the comic's image URL using simple RegEx on that HTML.
        
        Next, it generates a random file name that will be used to
        store the image locally, downloads it, builds a fancy embed,
        attaches the file, & sends it to the channel.
        """
        #get HTML of the comic's page
        try:
            html = await self._get_html(
                f'https://www.gocomics.com/random/{url_id}')
        except Exception:
            await ctx.reply("**Error**: Couldn't get HTML.")
            raise

        #get date of comic & url of the comic image
        #I should probably be using bs4 for this for
        #performance reasons
        date = findall('(?<=formatted-date=").+?(?=")', html)
        image_url = findall('(?<=data-image=").+?(?=")', html)

        if (not date) or (not image_url):
            await ctx.reply("**Error**: Couldn't extract date or image URL.")
            raise ValueError("Could'nt extract date or image URL.")

        #get random file name for saving comic image as
        file_name = await self._get_random_file_name()

        #download the comic image & save it as file_name
        try:
            await self._download_image(image_url[0],
                                       f'./images/comics/{file_name}')
        except Exception:
            await ctx.reply("**Error**: Couldn't download file.")
            raise

        #build embed
        embed = Embed(title=f'{name}: {date[0]}', color=Color.yellow())
        embed.set_author(name="Bronson's Comics",
                         icon_url='attachment://images_common_bbb.jpg')
        embed.set_image(url=f'attachment://images_comics_{file_name}')

        #attach icon, local comic image & send
        try:
            with open('./images/common/bbb.jpg', 'rb') as icon, \
                 open(f'./images/comics/{file_name}', 'rb') as comic:
                await ctx.reply(embed=embed,
                                     files=[File(icon), File(comic)])
        except FileNotFoundError:
            await ctx.reply("**Error**: Couldn't access local image file.")
            raise

    async def _get_random_file_name(self):
        """ Random file name generator """
        rand_chars = ''
        #get date in YYYYMMDD format to use as prefix for file name
        file_prefix = datetime.now().strftime('%Y%m%d-')

        #generate string of 20 random chars
        for _ in range(20):
            rand_chars += choice(ascii_lowercase + digits)

        #join file name string together & return
        #gocomics.com image files are strangely in .gif format
        return f'{file_prefix}{rand_chars}.gif'

    async def _get_html(self, url):
        """ HTML grabber """
        #gets the HTML of URL specified
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def _download_image(self, url, save_file):
        """ Image downloader """
        #downloads & saves image file specified
        async with ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

                with open(save_file, 'wb') as file:
                    file.write(content)

async def setup(bot):
    """ add class to bot's cog system"""
    await bot.add_cog(Comics(bot))
