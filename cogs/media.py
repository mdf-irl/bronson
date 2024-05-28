"""media module"""
from os import getenv

from discord import ButtonStyle, Color, Embed
from discord.ext import commands
from dotenv import load_dotenv
from reactionmenu import ViewMenu, ViewButton


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Media(bot))


class Media(commands.Cog):
    """
    Movie & TV show commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.omdb_api_key = getenv('OMDB_API_KEY')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def movie(self, ctx: commands.Context, *, query: str = None):
        """Sends info about specified movie"""
        if query is None:
            raise commands.CommandError(
                "You didn't provide a search query "
                "(example: **!movie Hellraiser**)."
            )

        if query.startswith('tt'):
            await ctx.send(embed=await self._get_embed_by_tt(query, 'movie'))
        else:
            movie_ids = await self._get_ids(query, 'movie')
            movie_ids = movie_ids[:5]

            movie_embeds = await self._populate_embeds(movie_ids, 'movie')
            await self._show_media(ctx, movie_embeds)

    @commands.command()
    async def tv(self, ctx: commands.Context, *, query: str = None):
        """Sends info about specified TV series"""
        if query is None:
            raise commands.CommandError(
                "You didn't provide a search query "
                "(example: **!tv Breaking Bad**)."
            )
        if query.startswith('tt'):
            await ctx.send(embed=await self._get_embed_by_tt(query, 'series'))
        else:
            tv_ids = await self._get_ids(query, 'series')
            tv_ids = tv_ids[:5]

            tv_embeds = await self._populate_embeds(tv_ids, 'series')
            await self._show_media(ctx, tv_embeds)

    async def _format_ratings(self, ratings_list: list) -> str:
        """format ratings from json to string"""
        ratings = []
        for rating in ratings_list:
            ratings.append(f"{rating['Value']} (**{rating['Source']}**)")

        ratings_f = ', '.join(ratings)
        ratings_f = ratings_f.replace('Internet Movie Database', 'IMDb')
        ratings_f = ratings_f.replace('Rotten Tomatoes', 'RT')
        return ratings_f

    async def _format_search_title(self, title: str) -> str:
        """format title into a searchable format"""
        search_title = title.replace(' ', '+')
        return search_title

    async def _get_ids(self, query: str, media_type: str) -> list:
        json_data = await self.ass.get_url_data(
            f'https://www.omdbapi.com/?apikey={self.omdb_api_key}&s={query}'
            f'&type={media_type}', get_type='json'
        )
        if json_data['Response'] == 'False':
            raise commands.CommandError('No results found.')

        ids = []
        for search_result in json_data['Search']:
            # only get IDs from results with posters
            if search_result['Poster'] != 'N/A':
                ids.append(search_result['imdbID'])
        return ids

    async def _get_embed_by_tt(self, tt: str, media_type: str) -> Embed:
        """get embed by IMDb ID"""
        json_data = await self.ass.get_url_data(
            f'https://www.omdbapi.com/?apikey={self.omdb_api_key}&i={tt}'
            f'&plot=short', get_type='json'
        )
        if json_data['Ratings']:
            ratings = await self._format_ratings(json_data['Ratings'])
        else:
            ratings = 'N/A'

        search_title = await self._format_search_title(json_data['Title'])
        m_id = '5000' if media_type == 'series' else '2000'

        body = f"{json_data['Plot']}\n\n"
        body += f"**Seasons**: {json_data['totalSeasons']}\n" if \
            media_type == 'series' else ''
        body += (
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
            f"(https://drunkenslug.com/search/{search_title}?t={m_id}), "
            "[NZBFinder]"
            f"(https://nzbfinder.ws/search?search={search_title}&t={m_id}), "
            "[NZBGeek]"
            "(https://nzbgeek.info/geekseek.php?moviesgeekseek=1"
            f"&c={m_id}&browseincludewords={search_title}), "
        )
        if media_type == 'movie':
            body += (
                "[PTP]"
                "(https://passthepopcorn.me/torrents.php?order_by=relevance"
                f"&searchstr={search_title})"
            )
        elif media_type == 'series':
            body += (
                "[BTN]"
                "(https://broadcasthe.net/torrents.php?"
                f"searchstr={search_title})"
            )
        embed = Embed(
            title=f"{json_data['Title']} ({json_data['Year']})",
            description=body, color=Color.random()
        )
        embed.set_thumbnail(url=json_data['Poster'])
        return embed

    async def _populate_embeds(self, media_ids: list, media_type: str) -> list:
        """populate embed list"""
        embeds = []
        for result_id in media_ids:
            embeds.append(await self._get_embed_by_tt(result_id, media_type))
        return embeds

    async def _show_media(self, ctx: commands.Context, embeds: list):
        """show embeds"""
        menu = ViewMenu(
            ctx, menu_type=ViewMenu.TypeEmbed,
            timeout=None, all_can_click=True
        )

        for media_embed in embeds:
            menu.add_page(media_embed)

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
