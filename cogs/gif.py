"""gif module"""
from os import getenv

from discord import ButtonStyle, Color, Embed
from discord.ext import commands
from dotenv import load_dotenv
from reactionmenu import ViewMenu, ViewButton


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Gif(bot))


class Gif(commands.Cog):
    """gif commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.tenor_api_key = getenv('TENOR_API_KEY')
        self.tenor_client_key = getenv('TENOR_CLIENT_KEY')
        self.giphy_api_key = getenv('GIPHY_API_KEY')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command(aliases=['img'])
    async def gif(self, ctx: commands.Context, *, query: str=None):
        """
        !gif name -> sends 1st Tenor result for "name"
        !gif name -menu -> sends menu of Tenor results for "name"
        !gif name -# -> Sends Tenor result for "name" at position "#"

        !gif name -g -> sends 1st GIPHY result for "name"
        !gif name -gmenu -> sends menu of GIPHY results for "name"
        !gif name -g# -> Sends GIPHY result for "name" at position "#"
        """
        if query is None:
            raise commands.CommandError(
                "You didn't provide a search query "
                "(example: **!gif cow**)."
            )

        args = query.split(' ')
        gif_index = 0
        giphy = False

        #!gif <query> -g
        if args[-1] == '-g':
            query = query[:-3]
            giphy = True

        #!gif <query> -m / -menu
        if args[-1] in ['-m', '-menu']:
            query = query[:-3] if args[-1] == '-m' else query[:-6]
            gif_index = -1
        #!gif <query> -gm / -gmenu
        elif args[-1] in ['-gm', '-gmenu']:
            query = query[:-4] if args[-1] == '-gm' else query[:-7]
            gif_index = -1
            giphy = True

        #!gif <query> -#
        if args[-1].startswith('-') and args[-1][1:].isdigit():
            query = query[:-(len(args[-1]) + 1)]
            gif_index = int(args[-1][1:]) - 1
        #!gif <query> -g#
        elif args[-1].startswith('-g') and args[-1][2:].isdigit():
            query = query[:-(len(args[-1]) + 1)]
            gif_index = int(args[-1][2:]) - 1
            giphy = True

        # get search results
        json_data = await self._gif_get_json_data(query, giphy)

        if (giphy or json_data['results']) and \
                (not giphy or json_data['data']):
            await self._gif_handle_results(ctx, json_data, gif_index, giphy)
        else:
            raise commands.CommandError('No results found.')

    async def _gif_get_json_data(self, query: str, giphy: bool) -> list:
        """get json data from tenor or giphy"""
        if giphy:
            json_data = await self.ass.get_url_data(
                f'http://api.giphy.com/v1/gifs/search?q={query}&limit=50'
                f'&api_key={self.giphy_api_key}', get_type='json'
            )
        else:
            json_data = await self.ass.get_url_data(
                f'https://tenor.googleapis.com/v2/search?q={query}'
                f'&key={self.tenor_api_key}&client_key={self.tenor_client_key}'
                '&limit=50', get_type='json'
            )
        return json_data

    async def _gif_handle_results(
            self,
            ctx: commands.Context,
            json_data: list,
            gif_index: int,
            giphy: bool
    ):
        """handle gif results"""
        if gif_index == 0:
            gif_url = json_data['data'][0]['images']['original']['url'] if \
                giphy else \
                json_data['results'][0]['media_formats']['gif']['url']

            embed = Embed(color=Color.random())
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)

        elif gif_index == -1:
            gif_embeds = await self._gif_populate_embeds(json_data, giphy)
            await self._gif_show_gifs(ctx, gif_embeds)

        else:
            gif_embeds = await self._gif_populate_embeds(json_data, giphy)
            try:
                await ctx.send(embed=gif_embeds[gif_index])
            except IndexError as exc:
                raise commands.CommandError(
                    f'"{gif_index + 1}" is not a valid #.'
                ) from exc

    async def _gif_populate_embeds(self, json_data: list, giphy: bool) -> list:
        """populate gif embeds"""
        gif_embeds = []
        json_key = 'data' if giphy else 'results'

        for gif in json_data[json_key]:
            embed = Embed(color=Color.random())
            if giphy:
                embed.set_image(url=gif['images']['original']['url'])
            else:
                embed.set_image(url=gif['media_formats']['gif']['url'])
            gif_embeds.append(embed)
        return gif_embeds

    async def _gif_show_gifs(self, ctx: commands.Context, embeds: list):
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
