""" novelty module """
from io import BytesIO
from json import loads
from random import choice

from cowsay import get_output_string
from discord import Color, Embed, File
from discord.ext import commands

class Novelty(commands.Cog):
    """ Novelty commands """
    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

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
        #get response from cloud
        responses_url = self.ass.get_cloud_url(
            '8ball_responses.txt', res_type='raw')
        responses_text = await self.ass.get_text(responses_url)
        responses = responses_text.splitlines()
        response = choice(responses)

        #format question to turn mentions into display names
        #we do this because an embed title won't properly display
        #mentions
        mentioned_users = ctx.message.mentions

        for user in mentioned_users:
            question = question.replace(user.mention, user.display_name)

        embed = Embed(title=f'{question}',
                      description=f'{response}', color=Color.blue())
        embed.set_author(name="Bronson's Magic 8ball",
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_thumbnail(url=self.ass.get_cloud_url('8ball'))

        await ctx.reply(embed=embed)

    @commands.command(aliases=['coin', 'flip', 'flipcoin'])
    async def coinflip(self, ctx):
        """
        Bronson flips a coin for you

        Chooses & sends heads or tails coin at random

        Usage: <prefix>coinflip
        Aliases: coin, flip, flipcoin
        """
        coin_state = [self.ass.get_cloud_url('heads'),
                      self.ass.get_cloud_url('tails')]
        await ctx.reply(choice(coin_state))

    @commands.command(aliases=['cow'])
    async def cowsay(self, ctx, *, message):
        """
        Sends an ASCII art cow saying your message

        Usage: <prefix>cow message
        Aliases: cowsay
        """
        #there's a bunch of options we can use other than 'cow'
        #will expand on this at a later time
        cow = get_output_string('cow', message)
        await ctx.reply(f'```{cow}```')

    @commands.command()
    async def curse(self, ctx):
        """
        Inflict a very nice, very evil curse upon @user(s)

        Usage: <prefix>curse @user(s)
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
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_image(url=f'{self.ass.get_cloud_url('curse')}.gif')

        await ctx.reply(embed=embed)

    @commands.command()
    async def dadjoke(self, ctx):
        """
        Sends a random dad joke

        Usage: <prefix>dadjoke
        """
        resp = await self.ass.get_text('https://icanhazdadjoke.com/slack')
        data = loads(resp)
        joke = data['attachments'][0]['text']

        embed = Embed(description=joke, color=Color.red())
        embed.set_author(name="Bronson's Dad Jokes",
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_thumbnail(url=self.ass.get_cloud_url('dad'))
        await ctx.reply(embed=embed)

    @commands.command(aliases=['fucknewby'])
    async def fnewby(self, ctx):
        """
        Sends fuck newby gif

        Usage: <prefix>fnewby
        Aliases: fucknewby
        """
        await ctx.reply(f'{self.ass.get_cloud_url('fucknewby')}.gif')

    @commands.command()
    async def insult(self, ctx):
        """
        Insult @user

        Usage: <prefix>insult @user
        """
        mentioned_users = ctx.message.mentions

        if not mentioned_users:
            raise commands.CommandError("You didn't mention a user.")
        if len(mentioned_users) > 1:
            raise commands.CommandError('You can only mention one user for '
                                        'this command.')

        insult = await self.ass.get_text(
            'https://insult.mattbas.org/api/insult.txt')
        insult = insult.replace("You ", "you ", 1)
        response = f'{mentioned_users[0].mention}, {insult.rstrip()}.'

        embed = Embed(description=response, color=Color.red())
        embed.set_author(name="Bronson's Insults",
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_thumbnail(url=self.ass.get_cloud_url('insult'))

        await ctx.reply(embed=embed)

    @commands.command()
    async def sausage(self, ctx):
        """
        Ask @user(s) if they would like some sausage

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
        #attaching because discord doesn't play nicely with loading
        #content URLs in a multi-line message
        sausage_url = self.ass.get_cloud_url('sausage')
        sausage_bin = File(BytesIO(await self.ass.get_binary(sausage_url)),
                           filename='sausage.gif')
        await ctx.reply(response, file=sausage_bin)

    @commands.command(aliases=['yo'])
    async def yogabs(self, ctx):
        """
        Sends a random 'yo gabs' meme

        Sends a random 'yo gabs' meme image from the
        ./images/yogabs/ local directory. So wholesome.

        Usage: <prefix>yogabs
        Aliases: yo
        """
        await ctx.reply(await self.ass.get_random_cloud_url('yogabs'))

    @eightball.error
    async def eightball_error(self, ctx, error):
        """ 8ball error handler """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('**Error**: You did not ask a question.')
        else:
            await ctx.reply(f'**Error**: {error}')

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        """ coinflip err handler """
        await ctx.reply(f'**Error**: {error}')

    @cowsay.error
    async def cowsay_error(self, ctx, error):
        """ cowsay error handler """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('**Error**: You did not specify a message.')
        else:
            await ctx.reply(f'**Error**: {error}')

    @curse.error
    async def curse_error(self, ctx, error):
        """ curse err handler """
        await ctx.reply(f'**Error**: {error}')

    @fnewby.error
    async def fnewby_error(self, ctx, error):
        """ fnewby err handler """
        await ctx.reply(f'**Error**: {error}')

    @insult.error
    async def insult_error(self, ctx, error):
        """ insult err handler """
        await ctx.reply(f'**Error**: {error}')

    @sausage.error
    async def sausage_error(self, ctx, error):
        """ sausage err handler """
        await ctx.reply(f'**Error**: {error}')

    @yogabs.error
    async def yogabs_error(self, ctx, error):
        """ yogabs err handler """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Novelty(bot))
