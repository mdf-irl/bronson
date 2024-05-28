"""owner module"""
from sys import exit as quit_bot

from discord.ext import commands


async def setup(bot):
    """add class to bot's cog system"""
    await bot.add_cog(Owner(bot))


class Owner(commands.Cog):
    """
    Owner only commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx: commands.Context, *, message: str):
        """Bronson says specified text"""
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx: commands.Context):
        """Quit bot"""
        await ctx.send('oKaAaAAyYy BuYyyY!!! :wave:')
        self.bot.close()
        quit_bot()
