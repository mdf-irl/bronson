""" sludge module """
from os import listdir
from random import choice

from discord import File
from discord.ext import commands

class Sludge(commands.Cog):
    """ sludge class """
    @commands.command(aliases=['sludgedump'])
    async def sludge(self, ctx):
        """
        Sends a random sludge dump
        
        The absolute pinnacle of technological innovation.

        Returns at random one of the finest sludge dumps scraped from
        /r/ratemypoo's top rated of all-time.
               
        Locally sourced because I'm too lazy to figure out how to work
        Selenium right now.
                
        Usage: <prefix>sludge
        Aliases: sludgedump
        """
        try:
            sd_files = listdir('./images/sludge/')

            #we're sending with spoiler tags because some people
            #just don't appreciate a good sludge dump. weirdos.
            with open(f'./images/sludge/{choice(sd_files)}', 'rb') as f:
                await ctx.reply(file=File(f, spoiler=True))
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @sludge.error
    async def sludge_error(self, ctx, error):
        """ sludge err handler """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Sludge(bot))
