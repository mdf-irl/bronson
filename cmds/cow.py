""" cow module """
from cowsay import get_output_string
from discord.ext import commands

class Cowsay(commands.Cog):
    """ cowsay commands """
    @commands.command(aliases=['cow'])
    async def cowsay(self, ctx, *, message):
        """
        Sends an ASCII art cow saying your message
        
        Usage: <prefix>cow message
        Aliases: cowsay
        """
        #apparently there's a bunch of options we can use other than
        #'cow' but I don't feel like experimenting at this point...
        #probably later on though it'd be a good command to build upon
        cow = get_output_string('cow', message)
        await ctx.reply(f'```{cow}```')

    @cowsay.error
    async def cowsay_error(self, ctx, error):
        """ cowsay error handler """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('**Error**: You did not specify a message.')
        else:
            await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Cowsay(bot))
