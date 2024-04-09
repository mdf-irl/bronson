""" quotes module """
from random import choice

from discord import Color, Embed
from discord.ext import commands


class Quotes(commands.Cog):
    """ quotes class """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    @commands.command()
    async def kanye(self, ctx):
        """ gets a kanye quote """
        quote = await self.ass.get_url_data('https://api.kanye.rest/text')
        embed = Embed(
            title='Kanye West Quotes', description=quote, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('kanye_f'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ralph(self, ctx):
        """ Sends a Ralph Wiggum quote """
        ralph_url = await self.ass.get_url('ralph_wiggum.txt', res_type='raw')
        ralph_txt = await self.ass.get_url_data(ralph_url)
        ralph_quotes = ralph_txt.split('%')

        embed = Embed(
            title='Ralph Wiggum Quotes',
            description=choice(ralph_quotes), color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('ralph_25'))
        await ctx.send(embed=embed)

    @commands.command()
    async def zen(self, ctx):
        """ gets a random zen quote """
        json_data = await self.ass.get_url_data(
            'https://zenquotes.io/api/random', get_type='json'
        )
        msg = (
            f'{json_data[0]['q']}\n\n'
            f'-- {json_data[0]['a']}, inspired by HeLLy'
        )
        embed = Embed(
            title='Zen Quotes', description=msg, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('zen'))
        await ctx.send(embed=embed)

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
    await bot.add_cog(Quotes(bot))
