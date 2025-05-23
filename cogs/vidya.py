"""vidya module"""
from datetime import datetime
from os import getenv

from discord import Color, Embed
from discord.ext import commands
from dotenv import load_dotenv


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Vidya(bot))


class Vidya(commands.Cog):
    """
    Vidya game related commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.rapid_api_key = getenv('RAPID_API_KEY')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def epic(self, ctx: commands.Context, args: str=None):
        """
        !epic -> sends epic game store's free games of the week
        !epic -upcoming -> sends epic game store's upcoming free games
        """
        headers = {
            'X-RapidAPI-Key': self.rapid_api_key,
            'X-RapidAPI-Host': 'free-epic-games.p.rapidapi.com'
        }
        json_data = await self.ass.get_url_data(
            'https://free-epic-games.p.rapidapi.com/free',
            get_type='json', headers=headers
        )
        if args in ['-u', '-upcoming']:
            game_key = 'upcoming'
            promo_key = 'upcomingPromotionalOffers'
            embed_title = "Epic Game Store's Upcoming Free Games"
            thumbnail = 'controller2'
        else:
            game_key = 'current'
            promo_key = 'promotionalOffers'
            embed_title = "Epic Game Store's Free Games of the Week"
            thumbnail = 'controller'

        game_data = json_data['freeGames'][game_key]
        body = ''
        for i, game in enumerate(game_data, start=1):
            body += (
                f"{i}. [**{game['title']}**]"
                f"({await self._epic_get_game_url(game)}) "
                f"({await self._epic_get_game_type(game)})\n"
                f"*{await self._epic_get_date(
                    game_data, 'startDate', promo_key, i - 1)} -> "
                f"{await self._epic_get_date(
                    game_data, 'endDate', promo_key, i - 1)}*\n\n"
                f"{game['description']}\n\n"
            )
        embed = Embed(
            title=embed_title,
            description=body,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url(thumbnail))
        await ctx.send(embed=embed)

    async def _epic_convert_timestamp(self, timestamp: str) -> str:
        """convert timestamp from json into mm/dd/yyyy format"""
        dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = dt_object.strftime("%m/%d/%Y")
        return formatted_date

    async def _epic_get_date(
            self,
            game_data: list,
            get_type: str,
            promo_key: str,
            index: int
    ) -> str:
        """get start or end date of free epic games"""
        try:
            get_date = (
                game_data[index]['promotions'][promo_key]
                [0]['promotionalOffers'][0][get_type]
            )
            get_date = await self._epic_convert_timestamp(get_date)
        except (KeyError, IndexError):
            get_date = '(unknown)'
        return get_date

    async def _epic_get_game_type(self, game: list) -> str:
        """get game type"""
        game_type = game['offerType'].replace('BASE_GAME', 'base game') \
                                     .replace('ADD_ON', 'add-on') \
                                     .replace('OTHERS', 'other')
        return game_type

    async def _epic_get_game_url(self, game: list) -> str:
        """get game's url"""
        try:
            game_url = (
                f"https://store.epicgames.com/en-US/p/"
                f"{game['catalogNs']['mappings'][0]['pageSlug']}"
            )
        except (KeyError, IndexError):
            game_url = 'https://store.epicgames.com/en-US/free-games'
        return game_url
