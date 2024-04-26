""" facts module """
from random import choice

from discord import Color, Embed, Member
from discord.ext import commands


class Facts(commands.Cog):
    """ Fact-related commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

    @commands.command()
    async def cat(self, ctx):
        """
        Sends a random cat fact

        Usage: <prefix>cat
        """
        json_data = await self.ass.get_url_data(
            'https://catfact.ninja/fact', get_type='json'
        )
        fact = json_data['fact']

        embed = Embed(
            title='Cat Facts', description=fact, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('billy_c'))
        await ctx.send(embed=embed)

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

        embed = Embed(
            title='Dog Facts', description=fact, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('duchess_c'))
        await ctx.send(embed=embed)

    @commands.command()
    async def helly(self, ctx):
        """
        Sends a random fact about HeLLy

        Usage: <prefix>helly
        """
        facts_url = await self.ass.get_url('helly_facts.txt', res_type='raw')
        facts_text = await self.ass.get_url_data(facts_url)
        facts = facts_text.splitlines()

        embed = Embed(
            title='HeLLy Facts', description=choice(facts),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('sherlock'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['yomama'])
    async def mom(self, ctx, user: Member):
        """
        Sends a fact about @user's mom

        Returns a random yo mama joke from the yomama-jokes.com API
        targeted at a specific user.

        Usage: <prefix>mom @user
        Aliases: yomama
        """
        #target_users = await self.gen.format_users(users)

        json_data = await self.ass.get_url_data(
            'https://www.yomama-jokes.com/api/v1/jokes/random/',
            get_type='json'
        )
        joke = json_data['joke']

        # make sure the joke is in valid format, then swap out
        # "yo mama" for @user's MOM
        if joke.lower().startswith('yo mama'):
            joke = f"{user.mention}'s **MOM** {joke[7:]}"
        else:
            raise commands.CommandError('Malformed joke.')

        embed = Embed(
            title='Mom Facts', description=joke, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('your_mom'))
        await ctx.send(embed=embed)

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

        embed = Embed(
            title='Useless Facts', description=fact, color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('useless'))
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Facts(bot))
