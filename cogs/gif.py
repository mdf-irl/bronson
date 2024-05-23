"""gif module"""
from os import getenv

from discord import ButtonStyle, Color, Embed
from discord.ext import commands
from dotenv import load_dotenv
from reactionmenu import ViewMenu, ViewButton

# aliases = {
#     "cowlick": "https://media.tenor.com/fTy4MGK0QRsAAAAC/lick-tongue.gif",
#     "cowdance": "https://media.tenor.com/micwEWa24ZcAAAAC/cow-pole.gif",
# }


class Gif(commands.Cog):
    """gif commands"""
    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.tenor_api_key = getenv('TENOR_API_KEY')
        self.tenor_client_key = getenv('TENOR_CLIENT_KEY')
        self.giphy_api_key = getenv('GIPHY_API_KEY')

    # async def _handle_list(self, ctx: commands.Context):
    #     """list all aliases"""
    #     #pass

    # async def _handle_alias(self, ctx: commands.Context, query: str):
    #     """send gif by alias"""
    #     if query in aliases:
    #         await ctx.send(aliases[query])
    #     else:
    #         raise commands.CommandError(f'"{query}" is not a valid alias.')

    async def _populate_embeds(self, json_data: list, giphy: bool):
        """populate gif embeds"""
        gif_embeds = []
        json_key = 'data' if giphy else 'results'
        embed_footer = 'Source: GIPHY' if giphy else 'Source: Tenor'

        for gif in json_data[json_key]:
            embed = Embed(color=Color.random())
            if giphy:
                embed.set_image(url=gif['images']['original']['url'])
            else:
                embed.set_image(url=gif['media_formats']['gif']['url'])
            embed.set_footer(text=embed_footer)
            gif_embeds.append(embed)

        return gif_embeds

    async def _handle_results(self, ctx: commands.Context, json_data: list,
                              gif_index: int, giphy: bool):
        """handle gif results"""
        if gif_index == 0:
            embed_footer = 'Source: GIPHY' if giphy else 'Source: Tenor'

            gif_url = json_data['data'][0]['images']['original']['url'] if \
            giphy else json_data['results'][0]['media_formats']['gif']['url']

            embed = Embed(color=Color.random())
            embed.set_image(url=gif_url)
            embed.set_footer(text=embed_footer)
            await ctx.send(embed=embed)

        elif gif_index == -1:
            gif_embeds = []
            gif_embeds = await self._populate_embeds(json_data, giphy)
            await self._show_gifs(ctx, gif_embeds)

        else:
            gif_embeds = []
            gif_embeds = await self._populate_embeds(json_data, giphy)
            try:
                await ctx.send(embed=gif_embeds[gif_index])
            except IndexError as exc:
                raise commands.CommandError(
                    f'"{gif_index + 1}" is not a valid #.'
                ) from exc

    async def _get_json_data(self, query: str, giphy: bool):
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

    @commands.command(aliases=['img'])
    async def gif(self, ctx: commands.Context, *, query: str = None):
        """!gif command"""
        if query is None:
            raise commands.CommandError("You didn't supply a query.")

        args = query.split(' ')
        gif_index = 0
        giphy = False

        # #!gif -list
        # if args[-1] in ['-l', '-list']:
        #     await self._handle_list(ctx)
        #     return

        # #!gif -<name>
        # if args[-1].startswith('-') and len(args) == 1:
        #     await self._handle_alias(ctx, args[-1][1:])
        #     return

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

        #get search results
        json_data = await self._get_json_data(query, giphy)

        if (giphy or json_data['results']) and \
        (not giphy or json_data['data']):
            await self._handle_results(ctx, json_data, gif_index, giphy)
        else:
            raise commands.CommandError('No results found.')

    async def _show_gifs(self, ctx: commands.Context, embeds: list):
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
    await bot.add_cog(Gif(bot))
