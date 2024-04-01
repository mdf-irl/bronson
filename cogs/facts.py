""" facts module """
from random import choice

from discord import Color, Embed
from discord.ext import commands


class Facts(commands.Cog):
    """ Fact-related commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    @commands.command()
    async def cat(self, ctx):
        """
        Sends a random cat fact

        Usage: <prefix>cat
        """
        json_data = await self.ass.get_url_data(
            'https://catfact.ninja/fact', get_type='json')
        fact = json_data['fact']

        embed = Embed(description=fact, color=Color.red())
        embed.set_author(
            name="Bronson's Cat Facts", icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('billy_c'))

        await ctx.reply(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        """
        Sends a random dog fact

        Usage: <prefix>dog
        """
        json_data = await self.ass.get_url_data(
            'https://dogapi.dog/api/v2/facts', get_type='json'
        )
        fact = json_data['data'][0]['attributes']['body']

        embed = Embed(description=fact, color=Color.red())
        embed.set_author(
            name="Bronson's Dog Facts", icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('duchess_c'))

        await ctx.reply(embed=embed)

    @commands.command()
    async def helly(self, ctx):
        """
        Sends a random fact about HeLLy

        Usage: <prefix>helly
        """
        facts_url = await self.ass.get_url('helly_facts.txt', res_type='raw')
        facts_text = await self.ass.get_url_data(facts_url)
        facts = facts_text.splitlines()

        embed = Embed(description=choice(facts), color=Color.red())
        embed.set_author(
            name="Bronson's HeLLy Facts",
            icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('sherlock'))

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

        # check to make sure a single user was mentioned
        if not mentioned_users:
            raise commands.CommandError("You didn't mention a user.")
        if len(mentioned_users) > 1:
            raise commands.CommandError(
                'You can only mention one user for this command.'
        )

        json_data = await self.ass.get_url_data(
            'https://www.yomama-jokes.com/api/v1/jokes/random/',
            get_type='json'
        )
        joke = json_data['joke']

        # make sure the joke is in valid format, then swap out
        # "yo mama" for @user's MOM
        if joke.lower().startswith('yo mama'):
            joke = f"{mentioned_users[0].mention}'s **MOM** {joke[7:]}"
        else:
            raise commands.CommandError('Malformed joke.')

        embed = Embed(description=joke, color=Color.red())
        embed.set_author(
            name="Bronson's Mom Facts", icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('your_mom'))

        await ctx.reply(embed=embed)

    @commands.command()
    async def useless(self, ctx):
        """
        Sends a random useless fact

        Usage: <prefix>useless
        Aliases: uf
        """
        json_data = await self.ass.get_url_data(
            'https://uselessfacts.jsph.pl/api/v2/facts/random?language=en',
            get_type='json'
        )
        fact = json_data['text']

        embed = Embed(description=fact, color=Color.red())
        embed.set_author(
            name="Bronson's Useless Facts",
            icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('useless'))

        await ctx.reply(embed=embed)

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Facts(bot))
