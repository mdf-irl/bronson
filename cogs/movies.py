"""movies module"""
from os import getenv

from discord import ButtonStyle, Color, Embed
from discord.ext import commands
from dotenv import load_dotenv
from reactionmenu import ViewMenu, ViewButton

class Movies(commands.Cog):
    """movies class"""
    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.omdb_api_key = getenv('OMDB_API_KEY')

        self.movie_embeds = []

    @commands.command()
    async def movie(self, ctx: commands.Context, *, query: str):
        """get movie info"""
        if query.startswith('tt'):
            await ctx.send(embed=await self._get_embed_by_tt(query))
        else:
            movie_ids = []
            movie_ids = await self._get_movie_ids(query)
            movie_ids = movie_ids[:5]

            await self._populate_movie_embeds(movie_ids)
            await self._show_movies(ctx)

    async def _populate_movie_embeds(self, movie_ids: list):
        """populate the class's movie embed list"""
        self.movie_embeds.clear()

        for movie_id in movie_ids:
            self.movie_embeds.append(await self._get_embed_by_tt(movie_id))

    async def _get_movie_ids(self, query: str):
        json_data = await self.ass.get_url_data(
            f'https://www.omdbapi.com/?apikey={self.omdb_api_key}&s={query}'
            '&type=movie', get_type = 'json'
        )
        if json_data['Response'] == 'False':
            raise commands.CommandError('No results found.')

        movie_ids = []
        for search_result in json_data['Search']:
            # only get IDs from results with movie posters
            if search_result['Poster'] != 'N/A':
                movie_ids.append(search_result['imdbID'])

        return movie_ids

    async def _format_ratings(self, ratings_list: list):
        """format movie ratings from json to string"""
        ratings = []
        for rating in ratings_list:
            ratings.append(f"{rating['Value']} (**{rating['Source']}**)")

        ratings_f = ', '.join(ratings)
        ratings_f = ratings_f.replace('Internet Movie Database', 'IMDb')
        ratings_f = ratings_f.replace('Rotten Tomatoes', 'RT')

        return ratings_f

    async def _format_search_title(self, title: str):
        """format movie title into a searchable format"""
        search_title = title.replace(' ', '+')
        return search_title

    async def _get_embed_by_tt(self, tt: str):
        """get movie embed by IMDb ID"""
        json_data = await self.ass.get_url_data(
            f'https://www.omdbapi.com/?apikey={self.omdb_api_key}&i={tt}'
            f'&plot=short', get_type = 'json'
        )
        try:
            ratings = await self._format_ratings(json_data['Ratings'])
        except IndexError:
            ratings = 'N/A'

        search_title = await self._format_search_title(json_data['Title'])

        embed = Embed(
            title=f"{json_data['Title']} ({json_data['Year']})",
            description=(
                f"{json_data['Plot']}\n\n"

                f"**Genre**: {json_data['Genre']}\n"

                f"**Rated**: {json_data['Rated']}, "
                f"**Released**: {json_data['Released']}, "
                f"**Runtime**: {json_data['Runtime']}\n"

                f"**Ratings**: {ratings}\n\n"

                f"**Director(s)**: {json_data['Director']}\n"
                f"**Writer(s)**: {json_data['Writer']}\n"
                f"**Starring**: {json_data['Actors']}\n\n"

                "**Search**: "
                "[DS]"
                f"(https://drunkenslug.com/search/{search_title}?t=2000), "
                "[NZBFinder]"
                f"(https://nzbfinder.ws/search?search={search_title}&t=2000), "
                "[NZBGeek]"
                "(https://nzbgeek.info/geekseek.php?moviesgeekseek=1"
                f"&c=2000&browseincludewords={search_title}), "
                "[PTP]"
                "(https://passthepopcorn.me/torrents.php?order_by=relevance"
                f"&searchstr={search_title})"
            ),
            color=Color.random()
        )
        if json_data['Poster'] != 'N/A':
            embed.set_thumbnail(url=json_data['Poster'])
        return embed

    async def _show_movies(self, ctx: commands.Context):
        """show movies"""
        menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed)

        for movie_embed in self.movie_embeds:
            menu.add_page(movie_embed)

        btn_back = ViewButton(
            style=ButtonStyle.primary, label='<',
            custom_id=ViewButton.ID_PREVIOUS_PAGE
        )
        menu.add_button(btn_back)

        btn_next = ViewButton(
            style=ButtonStyle.primary, label='>',
              custom_id=ViewButton.ID_NEXT_PAGE
        )
        menu.add_button(btn_next)

        await menu.start()

    async def cog_command_error(self, ctx: commands.Context, error):
        """handles cog errors"""
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system"""
    await bot.add_cog(Movies(bot))
