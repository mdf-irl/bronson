""" yogabs module """
from os import listdir
from random import choice

from discord import File
from discord.ext import commands

class Yogabs(commands.Cog):
    """ yogabs class """
    @commands.command(aliases=['yo'])
    async def yogabs(self, ctx):
        """
        Sends a random 'yo gabs' meme
        
        Sends a random 'yo gabs' meme image from the
        ./images/yogabs/ local directory. So wholesome.
        
        Usage: <prefix>yogabs
        Aliases: yo
        """
        try:
            #populate list of yo gabs images
            yg_files = listdir('./images/yogabs/')

            #attach file & send
            with open(f'./images/yogabs/{choice(yg_files)}', 'rb') as yg_img:
                await ctx.reply(file=File(yg_img))
        except Exception as e:
            raise commands.CommandError('Asset not found.') from e

    @yogabs.error
    async def yogabs_error(self, ctx, error):
        """ yogabs err handler """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Yogabs(bot))
