"""urbandictionary module"""
from discord import ButtonStyle, Color, Embed
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton

async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(UrbanDictionary(bot))

class UrbanDictionary(commands.Cog):
    """
    Urban Dictionary commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def ud(self, ctx: commands.Context, *, query: str=None):
        """urban dictionary command"""
        if query is None:
            raise commands.CommandError(
                "You didn't provide a search query "
                "(example: **!ud blumpkin**)."
            )
        json_data = await self.ass.get_url_data(
            f'http://api.urbandictionary.com/v0/define?term={query}',
              get_type='json'
        )
        if json_data['list']:
            def_embeds = []
            for def_ in json_data['list']:
                result = def_['definition'].replace('[', '').replace(']', '')
                example = def_['example'].replace('[', '').replace(']', '')

                embed = Embed(
                    title=f'Urban Dictionary definitions for "{query}":',
                    description=f'{result}\n\n*{example}*',
                    color=Color.random()
                )
                embed.set_thumbnail(url=await self.ass.get_url('ud'))
                def_embeds.append(embed)
            await self._ud_show_embeds(ctx, def_embeds)
        else:
            raise commands.CommandError(f'No definitions found for "{query}".')

    async def _ud_show_embeds(self, ctx: commands.Context, embeds: list):
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
