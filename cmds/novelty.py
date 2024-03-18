""" novelty module """
from random import choice

from discord import Color, Embed, File
from discord.ext import commands

class Novelty(commands.Cog):
    """ Novelty commands """
    @commands.command(aliases=['coin', 'flip', 'flipcoin'])
    async def coinflip(self, ctx):
        """
        Bronson flips a coin for you

        Chooses & sends heads or tails coin at random
        
        Usage: <prefix>coinflip
        Aliases: coin, flip, flipcoin
        """
        coin_state = ['./images/coinflip/heads.png',
                      './images/coinflip/tails.png']

        try:
            with open(choice(coin_state), 'rb') as coin_image:
                await ctx.reply(file=File(coin_image))
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @commands.command()
    async def curse(self, ctx):
        """
        Inflict a very nice, very evil curse upon @user
        
        Usage: <prefix>curse @user
        """
        mentioned_users = ctx.message.mentions
        mentions = ''

        if not mentioned_users:
            raise commands.CommandError('You did not mention any users.')

        #determine the grammar if you're cursing 1 or 1+ user(s)
        if len(mentioned_users) == 1:
            has_have = 'has'
        else:
            has_have = 'have'

        for user in mentioned_users:
            mentions += f'{user.mention}, '

        mentions = mentions[:-2]

        #build embed
        embed = Embed(
            description=f'{mentions} {has_have} '
                         'been **CURSED** by Danhausen.', color=Color.red())
        embed.set_author(name="Danhausen's Curse",
                         icon_url='attachment://images_common_bbb.jpg')
        embed.set_image(url='attachment://images_curse_curse.gif')

        #attach local files & send
        try:
            with open('./images/common/bbb.jpg', 'rb') as icon, \
                 open('./images/curse/curse.gif', 'rb') as img_curse:
                await ctx.reply(embed=embed, files=[File(icon),
                                                    File(img_curse)])
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @commands.command()
    async def sausage(self, ctx):
        """
        Ask @user if they would like some sausage
        
        PRO TIP: HeLLy *REALLY* likes sausage. 
                 You should ask him if he wants some.
        
        Usage: <prefix>sausage @user
        """
        mentioned_users = ctx.message.mentions
        mentions = ''

        if not mentioned_users:
            raise commands.CommandError('You did not mention any users.')

        for user in mentioned_users:
            mentions = mentions + f'{user.mention}, '

        #trim the trailing ", " after we've looped through all mentions
        mentions = mentions[:-2]

        response = (
            f'{mentions} would you like some sausage?\n'
            f'{mentions} would you like some sausages?\n'
            f'{mentions} would you like some sausage?\n'
            f'{mentions} would you like some sausages?'
        )

        #attach & send local sausage gif along with the response
        #we just built
        try:
            with open('./images/sausage/sausage.gif', 'rb') as sausage_gif:
                await ctx.reply(response, file=File(sausage_gif))
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        """ coinflip err handler """
        await ctx.reply(f'**Error**: {error}')

    @curse.error
    async def curse_error(self, ctx, error):
        """ curse err handler """
        await ctx.reply(f'**Error**: {error}')

    @sausage.error
    async def sausage_error(self, ctx, error):
        """ sausage err handler """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Novelty(bot))
