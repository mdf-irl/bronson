""" novelty module """
from os import getenv
from random import choice

from cowsay import get_output_string
from discord import Color, Embed, Member
from discord.ext import commands
from dotenv import load_dotenv


class Novelty(commands.Cog):
    """ Novelty commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

        load_dotenv()
        # self.giphy_api_key = getenv('GIPHY_API_KEY')
        self.tenor_api_key = getenv('TENOR_API_KEY')

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
        resp_url = await self.ass.get_url(
            '8ball_responses.txt', res_type='raw'
        )
        resp_text = await self.ass.get_url_data(resp_url)
        responses = resp_text.splitlines()

        if not question.endswith('?'):
            question = f'{question}?'

        embed = Embed(
            title='Magic 8ball',
            description=(f'*{question}*\n'
                         f'**Answer**: {choice(responses)}'),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('8ball_ai_f'))
        await ctx.send(embed=embed)

    @commands.command()
    async def achtung(self, ctx, *, message):
        """
        Sends an achtung with your message

        Usage: <prefix>achtung message
        """

        embed = Embed(
            title='ACHTUNG!', description=message, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('siren.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def coin(self, ctx):
        """ Bronson flips a coin for you """
        coin_state = choice(['heads', 'tails'])

        embed = Embed(
            title='And...', description=f'{coin_state.title()} it is!',
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url(coin_state))
        await ctx.send(embed=embed)

    @commands.command(aliases=['cow'])
    async def cowsay(self, ctx, *, message):
        """
        Sends an ASCII art cow saying your message

        Usage: <prefix>cow message
        Aliases: cowsay
        """
        # there's a bunch of options we can use other than 'cow'
        # will expand on this at a later time
        await ctx.reply(f'```{get_output_string('cow', message)}```')

    @commands.command()
    async def dadjoke(self, ctx):
        """
        Sends a random dad joke

        Usage: <prefix>dadjoke
        """
        resp = await self.ass.get_url_data(
            'https://icanhazdadjoke.com/slack', get_type='json'
        )
        joke = resp['attachments'][0]['text']

        embed = Embed(
            title='Dad Jokes', description=joke, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('dad'))
        await ctx.send(embed=embed)

    # @commands.command()
    # async def fortune(self, ctx):
    #     """ get fortune """
    #     resp_url = await self.ass.get_url('fortunes.txt', res_type='raw')
    #     resp_txt = await self.ass.get_url_data(resp_url)
    #     responses = resp_txt.splitlines()

    #     fortune = choice(responses)
    #     await ctx.send(fortune)

    # @commands.command(aliases=['gif'])
    # async def giphy(self, ctx, *, query):
    #     """ get gif from giphy """
    #     json_data = await self.ass.get_url_data(
    #         f'http://api.giphy.com/v1/gifs/search?q={query}&limit=10'
    #         f'&api_key={self.giphy_api_key}', get_type='json'
    #     )
    #     if json_data['data']:
    #         rand_gif = choice(json_data['data'])
    #         rand_url = rand_gif['images']['original']['url']

    #         embed = Embed(color=Color.random())
    #         embed.set_image(url=rand_url)
    #         await ctx.send(embed=embed)
    #     else:
    #         raise commands.CommandError('No results found.')

    @commands.command()
    async def insult(self, ctx, users: commands.Greedy[Member]):
        """
        Insult @user(s)

        Usage: <prefix>insult @user(s)
        """
        insultees = await self.gen.format_users(users)

        insult = await self.ass.get_url_data(
            'https://insult.mattbas.org/api/insult.txt'
        )
        insult = insult.replace("You ", "you ", 1)
        response = f'{insultees}, {insult.rstrip()}.'

        embed = Embed(
            title='Insults', description=response, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('insult'))
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        """ sends a random joke """
        joke = await self.ass.get_url_data(
            'https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Spooky'
            '?blacklistFlags=racist,sexist&format=txt'
        )
        embed = Embed(
            title='RLY FUN-E JOKES LOL!!! :hand_splayed: :skull:',
            description=joke, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('cow_lol'))
        await ctx.send(embed=embed)

    @commands.command()
    async def sausage(self, ctx, users: commands.Greedy[Member]):
        """
        Ask @user(s) if they would like some sausage

        PRO TIP: HeLLy *REALLY* likes sausage.
                 You should ask him if he wants some.

        Usage: <prefix>sausage @user(s)
        """
        hungry_users = await self.gen.format_users(users)

        response = (
            f'{hungry_users} would you like some sausage?\n'
            f'{hungry_users} would you like some sausages?\n'
            f'{hungry_users} would you like some sausage?\n'
            f'{hungry_users} would you like some sausages?'
        )
        embed = Embed(description=response, color=Color.random())
        embed.set_image(url=await self.ass.get_url('sausage.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['gif'])
    async def tenor(self, ctx, *, query):
        """ get tenor gif """
        json_data = await self.ass.get_url_data(
            f'https://tenor.googleapis.com/v2/search?q={query}'
            f'&key={self.tenor_api_key}&client_key=bronson&limit=1',
            get_type='json'
        )
        if json_data['results']:
            gif = json_data['results'][0]['media_formats']['gif']['url']
            embed = Embed(color=Color.random())
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
        else:
            raise commands.CommandError('No results found.')

    @commands.command()
    async def vapor(self, ctx):
        """ sends a chart image of the vaporization points
        of various cannabinoids """
        embed = Embed(
            title='Cannabinoid Vaporization Temperatures',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('vapor'))
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                "**Error**: You didn't provide the necessary argument(s)."
            )
        else:
            await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Novelty(bot))
