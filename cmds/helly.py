""" helly module """
from random import choice

from discord import Color, Embed, File
from discord.ext import commands

class Helly(commands.Cog):
    """ helly class """
    @commands.command(aliases=['fact', 'hellyfact'])
    async def helly(self, ctx):
        """
        Sends a random fact about HeLLy
        
        Returns a random fact about HeLLy, pulled from a local
        text file of recycled Chuck Norris jokes. This originally
        used the Chuck Norris joke API @ api.chucknorris.io, but
        half of the jokes were in broken English or made no
        fucking sense whatsoever.
        
        Usage: <prefix>helly
        Aliases: fact, hellyfact
        """
        try:
            #populate list of facts
            with open('./other/helly_facts.txt', 'r', encoding='utf-8') as f:
                facts = f.readlines()
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

        #choose a fact at random & get its index
        fact = choice(facts)
        fact_num = facts.index(fact)

        #build embed
        embed = Embed(title=f'HeLLy fact {fact_num} of {len(facts)}:',
                      description=f'{fact}', color=Color.red())
        embed.set_author(name="Bronson's HeLLy Facts",
                         icon_url='attachment://images_common_bbb.jpg')
        embed.set_thumbnail(url='attachment://images_helly_sherlock.png')

        try:
            #attach local images & send embed
            with open('./images/common/bbb.jpg', 'rb') as img_bronson, \
                 open('./images/helly/sherlock.png', 'rb') as img_helly:
                await ctx.reply(embed=embed, files=[File(img_bronson),
                                                    File(img_helly)])
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @helly.error
    async def helly_error(self, ctx, error):
        """ helly error handling """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Helly(bot))
