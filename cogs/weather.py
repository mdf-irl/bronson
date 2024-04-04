""" weather module """
from os import getenv

from discord import Color, Embed
from discord.ext import commands
from dotenv import load_dotenv


class Weather(commands.Cog):
    """ weather class """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

        load_dotenv()
        self.openweathermap_api_key = getenv('OPENWEATHERMAP_API_KEY')
        # load_dotenv()
        # self.weatherbit_api_key = getenv('WEATHERBIT_API_KEY')

    @commands.command(aliases=['w'])
    async def weather(self, ctx, zipcode):
        """ weather command """
        try:
            json_data = await self.ass.get_url_data(
                f'http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}'
                f'&appid={self.openweathermap_api_key}', get_type='json'
            )
        except Exception as e:
            raise commands.CommandError(
                "You didn't provide a valid postal code."
            ) from e

        await ctx.send(
            embed=await self._get_weather_embed(
                city=json_data['name'],
                lat=json_data['lat'], lon=json_data['lon']
            )
        )

    async def _get_weather_embed(self, city, lat, lon):
        """ build weather embed """
        json_data = await self.ass.get_url_data(
            'https://api.openweathermap.org/data/2.5/weather?units=imperial'
            f'&lat={lat}&lon={lon}&appid={self.openweathermap_api_key}',
            get_type='json'
        )
        body = (
            f'**Right now**: {json_data['weather'][0]['description']}\n'
        )

        try:
            body += (
                f'**Rainfall**: {await self._mm_to_in(
                    json_data['rain']['1h']):.2f} in/hr\n\n'
            )
            rainfall = True
        except KeyError:
            rainfall = False

        try:
            body += (
                f'**Snowfall**: {await self._mm_to_in(
                    json_data['snow']['1h']):.2f} in/hr\n\n'
            )
            snowfall = True
        except KeyError:
            snowfall = False

        if (not rainfall) and (not snowfall):
            body += '\n'

        body += (
            f'**Temperature**: {json_data['main']['temp']} °F\n'
            f'**Feels like**: {json_data['main']['feels_like']} °F\n\n'

            f'**Wind speed**: {json_data['wind']['speed']} mph\n'
            f'**Cloud coverage**: {json_data['clouds']['all']}%\n'
            f'**Relative humidity**: {json_data['main']['humidity']}%'
        )

        embed = Embed(title=city, description=body, color=Color.random())
        # embed.set_author(
        #     name="Bronson's Weather",
        #     icon_url=await self.ass.get_url('bbb')
        # )
        embed.set_thumbnail(
            url='http://openweathermap.org/img/wn/'
                f'{json_data['weather'][0]['icon']}@2x.png'
        )
        return embed

    async def _mm_to_in(self, mm):
        """ mm to in """
        return mm * 0.0393701

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                "**Error**: You didn't provide the necessary argument(s)."
            )
        else:
            await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Weather(bot))
