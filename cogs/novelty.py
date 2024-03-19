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
        response = self._get_8ball_response()

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
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_image(url=f'{self.ass.get_cloud_url('curse')}.gif')

        await ctx.reply(embed=embed)

    @commands.command(aliases=['fact', 'hellyfact'])
    async def helly(self, ctx):
        """
        Sends a random fact about HeLLy

        Usage: <prefix>helly
        Aliases: fact, hellyfact
        """
        #get facts
        facts_url = self.ass.get_cloud_url('helly_facts.txt', res_type='raw')
        facts_text = await self.ass.get_text(facts_url)
        facts = facts_text.splitlines()

        #choose a fact at random & get its index
        fact = choice(facts)
        fact_num = facts.index(fact)

        embed = Embed(title=f'HeLLy fact #{fact_num}:',
                      description=f'{fact}', color=Color.red())
        embed.set_author(name="Bronson's HeLLy Facts",
                         icon_url=self.ass.get_cloud_url('bbb'))
        embed.set_thumbnail(url=self.ass.get_cloud_url('sherlock'))

        await ctx.reply(embed=embed)

    @commands.command(aliases=['yomama'])
    async def mom(self, ctx):
        """
        Sends a fact about @user's mom

        Returns a random yo mama joke from the yomama-jokes.com API
        targeted at a specific user.

        Usage: <prefix>mom @user
        Aliases: yomama
        """
        mentioned_users = ctx.message.mentions

        #check to make sure a single user was mentioned
        if not mentioned_users:
            raise commands.CommandError('You did not mention a user.')
        if len(mentioned_users) > 1:
            raise commands.CommandError('You can only mention one user '
                                        'for this command.')

        #get content from the API URL
        try:
            html = await self.ass.get_text(
                'https://www.yomama-jokes.com/api/v1/jokes/random/')
        except Exception as e:
            raise commands.CommandError("Couldn't get HTML.") from e

        #get the joke from the JSON returned
        data = loads(html)
        joke = data['joke']

        #make sure the joke is in valid format, then swap out
        #"yo mama" for @user's MOM
        if joke.lower().startswith('yo mama'):
            await ctx.reply(f"{mentioned_users[0].mention}'s "
                             "**MOM**" + joke[7:])
        else:
            raise commands.CommandError('Malformed joke.')

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

    def _get_8ball_response(self):
        """ 8ball responses """
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

    @helly.error
    async def helly_error(self, ctx, error):
        """ helly err handler """
        await ctx.reply(f'**Error**: {error}')

    @mom.error
    async def mom_error(self, ctx, error):
        """ mom err handler """
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
    """ add command to bot's cog system """
    await bot.add_cog(Novelty(bot))
