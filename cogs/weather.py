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

        load_dotenv()
        self.openweathermap_api_key = getenv('OPENWEATHERMAP_API_KEY')

    async def _weather_geolocate(self, zipcode: int):
        """geolocate zipcode"""
        try:
            json_data = await self.ass.get_url_data(
                f'http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}'
                f'&appid={self.openweathermap_api_key}', get_type='json'
            )
        except Exception as e:
            raise commands.CommandError(
                "You didn't provide a valid zipcode."
            ) from e
        return json_data['name'], json_data['lat'], json_data['lon']

    @commands.command(aliases=['w'])
    async def weather(self, ctx: commands.Context, zipcode: int = None):
        """weather command"""
        if not zipcode:
            raise commands.CommandError("You didn't provide a zipcode.")

        city, lat, lon = await self._weather_geolocate(zipcode)
        weather_data = await self._weather_get_data(lat, lon)
        await ctx.send(embed=await self._weather_get_embed(city, weather_data))

    async def _weather_get_embed(self, city: str, weather_data: list):
        """get weather embed"""
        embed = Embed(title=city, color=Color.random())
        embed.set_thumbnail(
            url='http://openweathermap.org/img/wn/'
                f"{weather_data['weather'][0]['icon']}@2x.png"
        )
        embed.add_field(
            name='**Status**:',
            value=weather_data['weather'][0]['description'],
            inline=True
        )
        try:
            embed.add_field(
                name='**Rainfall**:',
                value=f"{await self._weather_mm_to_in(
                    weather_data['rain']['1h']):.2f} in/hr",
                inline=True
            )
        except KeyError:
            pass
        try:
            embed.add_field(
                name='**Snowfall**:',
                value=f"{await self._weather_mm_to_in(
                    weather_data['snow']['1h']):.2f} in/hr",
                inline=True
            )
        except KeyError:
            pass
        embed.add_field(
            name='**Temperature**:',
            value=f"{weather_data['main']['temp']} °F",
            inline=True
        )
        embed.add_field(
            name='**Feels like**:',
            value=f"{weather_data['main']['feels_like']} °F",
            inline=True
        )
        embed.add_field(
            name='**Wind speed**:',
            value=f"{weather_data['wind']['speed']} mph",
            inline=True
        )
        embed.add_field(
            name='**Cloud coverage**:',
            value=f"{weather_data['clouds']['all']}%",
            inline=True
        )
        embed.add_field(
            name='**Relative humidity**:',
            value=f"{weather_data['main']['humidity']}%",
            inline=True
        )
        return embed

    async def _weather_get_data(self, lat: float, lon: float):
        """get weather data"""
        try:
            json_data = await self.ass.get_url_data(
                'https://api.openweathermap.org/data/2.5/weather?units=imperial'
                f'&lat={lat}&lon={lon}&appid={self.openweathermap_api_key}',
                get_type='json'
            )
        except Exception as e:
            raise commands.CommandError(
                "Couldn't retrieve weather data."
            ) from e
        return json_data

    async def _weather_mm_to_in(self, mm: float):
        """mm to in"""
        return mm * 0.0393701

    async def cog_command_error(self, ctx: commands.Context, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Weather(bot))
