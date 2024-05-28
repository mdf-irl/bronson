"""quotes module"""
from random import choice

from discord import Color, Embed
from discord.ext import commands


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Quotes(bot))


class Quotes(commands.Cog):
    """
    Quote commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def kanye(self, ctx: commands.Context):
        """Sends a Kanye quote"""
        quote = await self.ass.get_url_data('https://api.kanye.rest/text')
        embed = Embed(
            title='Kanye West Quotes',
            description=f'{quote}\n\n-- Kanye West, inspired by HeLLy',
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('kanye_f'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ralph(self, ctx: commands.Context):
        """Sends a Ralph Wiggum quote"""
        ralph_url = await self.ass.get_url('ralph_wiggum.txt', res_type='raw')
        ralph_txt = await self.ass.get_url_data(ralph_url)
        ralph_quotes = ralph_txt.split('%')

        ralph_quote = choice(ralph_quotes)
        ralph_quote = ralph_quote.replace(
            '--Ralph Wiggum', '-- Ralph Wiggum, inspired by HeLLy'
        )
        embed = Embed(
            title='Ralph Wiggum Quotes',
            description=ralph_quote,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('ralph_25'))
        await ctx.send(embed=embed)

    @commands.command()
    async def zen(self, ctx: commands.Context):
        """Sends a random zen quote"""
        json_data = await self.ass.get_url_data(
            'https://zenquotes.io/api/random', get_type='json'
        )
        msg = (
            f'{json_data[0]['q']}\n\n'
            f'-- {json_data[0]['a']}, inspired by HeLLy'
        )
        embed = Embed(
            title='Zen Quotes',
            description=msg,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('zen'))
        await ctx.send(embed=embed)
