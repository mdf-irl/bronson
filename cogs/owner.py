"""owner module"""
from sys import exit as quit_bot

from discord.ext import commands


class Owner(commands.Cog):
    """owner class"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx: commands.Context):
        """quit bot"""
        await ctx.send('oKaAaAAyYy BuYyyY!!! :wave:')
        self.bot.close()
        quit_bot()

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx: commands.Context, *, message: str):
        """say command"""
        await ctx.send(message)

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Owner(bot))
