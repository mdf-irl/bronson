""" 8ball module """
from random import choice

from discord import Color, Embed, File
from discord.ext import commands

class Eightball(commands.Cog):
    """ Eightball class """
    @commands.command(name='8ball')
    async def eightball(self, ctx, *, question):
        """
        Ask a question, get an answer
        
        Just your average Magic 8ball.
        Ask it a question and get an answer.

        Currently uses the standard responses from Wikipedia:
        https://en.wikipedia.org/wiki/Magic_8_Ball

        Usage: <prefix>8ball question
        """
        #get 8ball response
        response = self._get_8ball_response()

        #format question to turn mentions into display names
        mentioned_users = ctx.message.mentions

        for user in mentioned_users:
            question = question.replace(user.mention, user.display_name)

        #build embed
        embed = Embed(title=f'{question}',
                      description=f'{response}', color=Color.blue())
        embed.set_author(name="Bronson's Magic 8ball",
                         icon_url='attachment://images_common_bbb.jpg')
        embed.set_thumbnail(url='attachment://images_eightball_eightball.png')

        #attach embedded files & send
        try:
            with open('./images/common/bbb.jpg', 'rb') as icon, \
                 open('./images/eightball/eightball.png', 'rb') as thumbnail:
                await ctx.reply(embed=embed, files=[File(icon),
                                                        File(thumbnail)])
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    def _get_8ball_response(self):
        """ 8ball responses """
        #get random magic 8ball response
        #formatted for ease of adding/removing more responses
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes, definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        return f'{choice(responses)}'

    @eightball.error
    async def eightball_error(self, ctx, error):
        """ 8ball error handler """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('**Error**: You did not ask a question.')
        else:
            await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Eightball(bot))
