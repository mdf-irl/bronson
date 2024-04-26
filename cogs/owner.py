"""owner module"""
from os import listdir, remove
from sys import exit as quit_bot

from discord.ext import commands


class Owner(commands.Cog):
    """owner class"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def deltmp(self, ctx):
        """clear tmp files"""
        files = listdir('./tmp')
        files_count = len(files)

        for file in files:
            remove(f'./tmp/{file}')

        await ctx.send(f'Deleted {files_count} files from ./tmp')

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        """quit bot"""
        await ctx.send('oKaAaAAyYy BuYyyY!!! :wave:')
        self.bot.close()
        quit_bot()

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, message: str):
        """say command"""
        await ctx.send(message)

    # @commands.command()
    # @commands.is_owner()
    # async def update(self, ctx):
    #     """update bot"""


    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Owner(bot))
