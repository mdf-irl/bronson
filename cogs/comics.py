"""comics module"""
from datetime import datetime
from pathlib import Path
from re import findall
from random import randint

from discord import Color, Embed, File
from discord.ext import commands
from PIL import Image


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Comics(bot))


class Comics(commands.Cog):
    """
    Commands for retrieving & viewing comic strips from GoComics.com & others
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    async def _get_today(self):
        """get today's date"""
        today = datetime.today()
        return today.strftime('%Y/%m/%d')

    async def _get_proper_date(self, cmd_name: str, date: str):
        """get date in proper format"""
        try:
            dt_obj = datetime.strptime(date, '%m/%d/%Y')
            comic_date = dt_obj.strftime('%Y/%m/%d')
            return comic_date
        except ValueError:
            try:
                dt_obj = datetime.strptime(date, '%m/%d/%y')
                comic_date = dt_obj.strftime('%Y/%m/%d')
                return comic_date
            except ValueError as exc:
                raise commands.CommandError(
                    "You didn't provide a valid date "
                    f"(example: **!{cmd_name} 7/4/23**)."
                ) from exc

    @commands.command(aliases=['bd'])
    async def boondocks(self, ctx: commands.Context, arg: str=None):
        """Sends a random Boondocks comic"""
        await self._handle_gocomics_comic(
            ctx, 'boondocks', 'The Boondocks', arg
        )

    @commands.command(aliases=['c&h'])
    async def cah(self, ctx: commands.Context, arg: str=None):
        """Sends a random Calvin & Hobbes comic"""
        await self._handle_gocomics_comic(
            ctx, 'calvinandhobbes', 'Calvin & Hobbes', arg
        )

    @commands.command()
    async def garfield(self, ctx: commands.Context, arg: str=None):
        """Sends a random Garfield comic"""
        await self._handle_gocomics_comic(ctx, 'garfield', 'Garfield', arg)

    @commands.command(aliases=['p'])
    async def peanuts(self, ctx: commands.Context, arg: str=None):
        """Sends a random Peanuts comic"""
        await self._handle_gocomics_comic(ctx, 'peanuts', 'Peanuts', arg)

    @commands.command(aliases=['pb'])
    async def peanutsb(self, ctx: commands.Context, arg: str=None):
        """Sends a random Peanuts Begins comic"""
        await self._handle_gocomics_comic(
            ctx, 'peanuts-begins', 'Peanuts Begins', arg)

    async def _handle_gocomics_comic(
            self,
            ctx: commands.Context,
            url_id: str,
            name: str,
            arg: str=None
    ):
        """Gets & sends GoComics.com comics"""
        if arg is not None:
            if arg in ['-r', '-random']:
                comic_url = f'https://www.gocomics.com/random/{url_id}'
            else:
                comic_date = await self._get_proper_date(url_id, arg)
                comic_url = f'https://www.gocomics.com/{url_id}/{comic_date}'
        else:
            comic_url = (
                f'https://www.gocomics.com/{url_id}/{await self._get_today()}'
            )

        html = await self.ass.get_url_data(comic_url)

        if 'Sorry but there was no' in html:
            raise commands.CommandError(
                f"There is no {name} comic for that date."
            )
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

    @commands.command()
    async def gmg(self, ctx: commands.Context):
        """Sends a random Garfield Minus Garfield comic"""
        # not a gocomics comic, files are stored in cloud
        embed = Embed(
            title='Garfield Minus Garfield',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('gmg', tag=True))
        await ctx.send(embed=embed)

    @commands.command()
    async def rcg(self, ctx: commands.Context):
        """Sends randomly generated comic from Explosm"""
        panels, comic_id, comic_url = await self._rcg_get_panel_data()
        temp_dir = await self._rcg_download_panels(comic_id, panels)

        await self._rcg_combine_images(
            [temp_dir / f'{comic_id}_{i}.png' for i in range(3)],
            temp_dir / f'{comic_id}.png'
        )
        await self._rcg_send_embed(ctx, comic_url, comic_id, temp_dir)
        await self._rcg_del_temp(temp_dir, comic_id)

    async def _rcg_combine_images(self, img_names: list[str], filename: str):
        """combine RCG panels into one image"""
        images = [Image.open(name) for name in img_names]
        c_img_width = sum(image.size[0] for image in images) + 20
        c_img_height = max(image.size[1] for image in images) + 20
        c_img = Image.new(
            "RGB",
            (c_img_width, c_img_height),
            color=(255, 255, 255)
        )
        x_offset, y_offset = 10, 10
        for image in images:
            c_img.paste(image, (x_offset, y_offset))
            x_offset += image.size[0]
        c_img.save(filename, format="PNG")

    async def _rcg_del_temp(self, temp_dir: str, comic_id: str):
        """delete temp files"""
        for file in temp_dir.glob(f'{comic_id}_*.png'):
            file.unlink()
        (temp_dir / f'{comic_id}.png').unlink()

    async def _rcg_download_panels(self, comic_id: str, panels: list):
        """create temp dir & download panel images"""
        temp_dir = Path('./tmp')
        temp_dir.mkdir(exist_ok=True)

        for i, item in enumerate(panels):
            panel_bin = await self.ass.get_url_data(item, get_type='binary')
            with open(temp_dir / f'{comic_id}_{i}.png', 'wb') as file:
                file.write(panel_bin)
        return temp_dir

    async def _rcg_get_panel_data(self):
        """get panel data for rcg"""
        json_data = await self.ass.get_url_data(
            'https://explosm.net/api/get-random-panels', get_type='json'
        )
        prefix = 'https://rcg-cdn.explosm.net/panels/'
        panels = [f"{prefix}{panel['filename']}" for panel in
                  json_data.get('panels', [])]

        comic_id = ''.join(panel['slug'] for panel in
                           json_data.get('panels', []))
        comic_url = f'https://explosm.net/rcg/{comic_id.lower()}'
        return panels, comic_id, comic_url

    async def _rcg_send_embed(
            self,
            ctx: commands.Context,
            comic_url: str,
            comic_id: str,
            temp_dir: str
    ):
        """send combined panel embed"""
        embed = Embed(
            title="Joking Hazard's Random Comic Generator",
            description=(
                f'[Explosm.net](https://explosm.net/) permalink: {comic_url}'
            ),
            color=Color.random()
        )
        embed.set_image(url=f'attachment://{comic_id}.png')

        with open(temp_dir / f'{comic_id}.png', 'rb') as file:
            comic_file = File(file, f'{comic_id}.png')
            await ctx.send(embed=embed, file=comic_file)

    @commands.command()
    async def xkcd(self, ctx: commands.Context):
        """Sends a random comic from XKCD"""
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
            color=Color.random()
        )
        embed.set_image(url=json_data['img'])
        embed.set_footer(text=json_data['alt'])
        await ctx.send(embed=embed)
