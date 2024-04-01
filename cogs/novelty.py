""" novelty module """
from random import choice

from cowsay import get_output_string
from discord import Color, Embed, Member
from discord.ext import commands


class Novelty(commands.Cog):
    """ Novelty commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

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

        # format question to turn mentions into display names
        # we do this because an embed title won't properly display
        # mentions
        mentioned_users = ctx.message.mentions

        for user in mentioned_users:
            question = question.replace(user.mention, user.display_name)

        embed = Embed(
            title=f'{question}', description=choice(responses),
            color=Color.blue()
        )
        embed.set_author(
            name="Bronson's Magic 8ball",
            icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('8ball'))

        await ctx.reply(embed=embed)

    @commands.command()
    async def achtung(self, ctx, *, message):
        """
        Sends an achtung with your message

        Usage: <prefix>achtung message
        """

        embed = Embed(
            title='ACHTUNG!', description=message, color=Color.red()
        )
        embed.set_thumbnail(url=await self.ass.get_url('siren.gif'))

        await ctx.send(embed=embed)

    @commands.command()
    async def ckhello(self, ctx):
        """
        Sends Cool-Knight's hello message

        Usage: <prefix>ckhello
        """
        await ctx.send(
            'Hello i am Bronson from StarCraft Broodwar.\n'
            'A gamer, a websiter. And i am Arana Friend.\n'
            'And ofc Cool knight in shiny armor.\n'
            ':slight_smile:'
        )

    @commands.command(aliases=['coin', 'flip', 'flipcoin'])
    async def coinflip(self, ctx):
        """
        Bronson flips a coin for you

        Chooses & sends heads or tails coin at random

        Usage: <prefix>coinflip
        Aliases: coin, flip, flipcoin
        """
        coin_state = [
            await self.ass.get_url('heads'), await self.ass.get_url('tails')
        ]

        await ctx.reply(choice(coin_state))

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

        embed = Embed(description=joke, color=Color.red())
        embed.set_author(
            name="Bronson's Dad Jokes", icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('dad'))

        await ctx.reply(embed=embed)

    @commands.command(aliases=['fucknewby'])
    async def fnewby(self, ctx):
        """
        Sends fuck newby gif

        Usage: <prefix>fnewby
        Aliases: fucknewby
        """
        await ctx.reply(f'{await self.ass.get_url('fucknewby')}.gif')

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

        embed = Embed(description=response, color=Color.red())
        embed.set_author(
            name="Bronson's Insults", icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('insult'))

        await ctx.reply(embed=embed)

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
        # attaching because discord doesn't play nicely with loading
        # content URLs in a multi-line message
        sausage_url = await self.ass.get_url('sausage')
        sausage_bin = await self.ass.get_discord_file(
            sausage_url, filename='sausage.gif'
        )

        await ctx.reply(response, file=sausage_bin)

    @commands.command()
    async def spray(self, ctx, users: commands.Greedy[Member]):
        """
        Sprays @user(s) with water bottle

        Usage: <prefix>spray @user(s)
        """
        sprayed_users = await self.gen.format_users(users)

        await ctx.send(
            f'Sprays {sprayed_users} with water bottle\n'
            'There some water for you\n'
            "it' hot water.\n"
            ':wink:'
        )

    @commands.command(aliases=['hawk'])
    async def trumpet(self, ctx):
        """
        Sends Hawk's beautiful trumpet performance

        Usage: <prefix>trumpet
        Aliases: hawk
        """
        trumpet_url = await self.ass.get_url('trumpet', res_type='video')
        trumpet_vid = await self.ass.get_discord_file(
            trumpet_url, 'trumpet.mov'
        )
        await ctx.reply(file=trumpet_vid)

    @commands.command(aliases=['yo'])
    async def yogabs(self, ctx):
        """
        Sends a random 'yo gabs' meme

        Sends a random 'yo gabs' meme image from the
        ./images/yogabs/ local directory. So wholesome.

        Usage: <prefix>yogabs
        Aliases: yo
        """
        await ctx.reply(await self.ass.get_url('yogabs', tag=True))

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
