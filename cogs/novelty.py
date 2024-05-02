""" novelty module """
from os import getenv
from random import choice, sample

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
        self.tenor_api_key = getenv('TENOR_API_KEY')
        self.tenor_client_key = getenv('TENOR_CLIENT_KEY')
        self.giphy_api_key = getenv('GIPHY_API_KEY')
        self.drunkenslug_api_key = getenv('DRUNKENSLUG_API_KEY')

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
        resp_url = await self.ass.get_url('8ball_2.txt', res_type='raw')
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
        embed.set_thumbnail(url=await self.ass.get_url('8ball_new'))
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

    @commands.command()
    async def fortune(self, ctx, user: Member = None):
        """ get fortune """
        resp_url = await self.ass.get_url('fortunes.txt', res_type='raw')
        resp_txt = await self.ass.get_url_data(resp_url)
        responses = resp_txt.splitlines()

        who = f"{user.display_name}'s" if user else 'Your'
        embed = Embed(
            title=f'{who} fortune is...', description=choice(responses),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('fortune'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['gif2'])
    async def giphy(self, ctx, *, query):
        """ get gif from giphy """
        json_data = await self.ass.get_url_data(
            f'http://api.giphy.com/v1/gifs/search?q={query}&limit=1'
            f'&api_key={self.giphy_api_key}', get_type='json'
        )
        if json_data['data']:
            embed = Embed(color=Color.random())
            embed.set_image(
                url=json_data['data'][0]['images']['original']['url']
            )
            await ctx.send(embed=embed)
        else:
            raise commands.CommandError('No results found.')

    @commands.command()
    async def insult(
        self, ctx: commands.Context,
        users: commands.Greedy[Member], *, arg: str = None):
        """insult @user(s)"""
        insultees = await self.gen.format_users(users, False)

        if arg is None:
            insult = await self.ass.get_url_data(
                'https://insult.mattbas.org/api/insult.txt'
            )
            thumbnail = 'insult_mild'
            response = f'{insult.rstrip()}.'
        elif arg == '-spicy':
            words_txt = await self.ass.get_url_data(
                await self.ass.get_url('insult_words.txt', res_type='raw')
            )
            words_list = words_txt.splitlines()
            words_chosen_list = sample(words_list, 10)
            words = ' '.join(words_chosen_list)
            a_an = 'an' if words[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'

            thumbnail = 'insult_spicy'
            response = f'You are {a_an} {words}.'

        embed = Embed(
            title=f'{insultees}...', description=response, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url(thumbnail))
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        """ sends a random joke """
        joke = await self.ass.get_url_data(
            'https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Spooky'
            '?blacklistFlags=racist,sexist&format=txt'
        )
        embed = Embed(
            title='RLY FUN-E JOKES LOL!!! :hand_splayed::skull:',
            description=joke, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('cow_lol'))
        await ctx.send(embed=embed)

    @commands.command()
    async def nzb(self, ctx, *, query):
        """ check drunkenslug for nzbs """
        # this is hacked together and DEFINITELY needs a re-write
        # but... for now it works! LOL!!!!!!!!
        json_data = await self.ass.get_url_data(
            f'https://drunkenslug.com/api?t=search&q={query}&o=json'
            f'&apikey={self.drunkenslug_api_key}', get_type='json'
        )
        try:
            if json_data['item']:
                entry_list = []
                if not isinstance(json_data['item'], list):
                    # we have only 1 result, so 'item' is not a list...
                    # so we process the result here to avoid a KeyError
                    entry_list.append(
                        f"1. [{json_data['item']['title']}]"
                        f"({json_data['item']['guid']['text']})"
                    )
                else:
                    # we have more than 1 result:
                    items = json_data['item'][:5]
                    for i, item in enumerate(items, start=1):
                        entry_list.append(
                            f"{i}. [{item['title']}]({item['guid']['text']})"
                        )
                entries = '\n'.join(entry_list)

                embed = Embed(
                    title='DrunkenSlug Results', description=entries,
                    color=Color.random()
                )
                embed.set_thumbnail(url=await self.ass.get_url('drunk_slug'))
                await ctx.send(embed=embed)
        except KeyError as e:
            # we have 0 results
            raise commands.CommandError('No results found.') from e

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
            f'&key={self.tenor_api_key}&client_key={self.tenor_client_key}'
            '&limit=1', get_type='json'
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
