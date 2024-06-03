"""facts module"""
from datetime import datetime
from os import getenv
from random import choice

from discord import Color, Embed, Member
from discord.ext import commands
from dotenv import load_dotenv

async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Facts(bot))


class Facts(commands.Cog):
    """Commands to send various facts."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.rapid_api_key = getenv('RAPID_API_KEY')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def cat(self, ctx: commands.Context):
        """Sends a random cat fact"""
        json_data = await self.ass.get_url_data(
            'https://catfact.ninja/fact', get_type='json'
        )
        embed = Embed(
            title='Cat Facts',
            description=json_data['fact'],
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('billy_c'))
        await ctx.send(embed=embed)

    @commands.command()
    async def cow(self, ctx: commands.Context):
        """Sends a random cow fact"""
        cow_url = await self.ass.get_url('cow_facts.txt', res_type='raw')
        cow_txt = await self.ass.get_url_data(cow_url)
        cow_facts = cow_txt.splitlines()

        embed = Embed(
            title='Cow Facts',
            description=choice(cow_facts),
            color=Color.random()
        )
        embed.set_thumbnail(
            url=await self.ass.get_url('stock_photo_autistic_man')
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx: commands.Context):
        """Sends a random dog fact"""
        json_data = await self.ass.get_url_data(
            'https://dogapi.dog/api/v2/facts', get_type='json'
        )
        embed = Embed(
            title='Dog Facts',
            description=json_data['data'][0]['attributes']['body'],
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('duchess_c'))
        await ctx.send(embed=embed)

    @commands.command()
    async def foiegras(self, ctx: commands.Context):
        """Sends a random fact about foie gras"""
        fg_url = await self.ass.get_url('foie_facts.txt', res_type='raw')
        fg_txt = await self.ass.get_url_data(fg_url)
        fg_facts = fg_txt.splitlines()

        embed = Embed(
            title="HeLLy's Foie Gras Fun Facts",
            description=choice(fg_facts),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('foie_gras'))
        await ctx.send(embed=embed)

    @commands.command()
    async def helly(self, ctx: commands.Context):
        """Sends a random fact about HeLLy"""
        facts_url = await self.ass.get_url('helly_facts.txt', res_type='raw')
        facts_text = await self.ass.get_url_data(facts_url)
        facts = facts_text.splitlines()

        embed = Embed(
            title='HeLLy Facts',
            description=choice(facts),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('sherlock'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['yomama'])
    async def mom(self, ctx: commands.Context, user: Member = None):
        """Sends a fact about @user's mom"""
        if user is None:
            raise commands.CommandError(
                "You didn't provide a user "
                f"(example: **!mom {ctx.author.mention}**)."
            )
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
            title='Mom Facts',
            description=joke,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('your_mom_md'))
        await ctx.send(embed=embed)

    @commands.command()
    async def today(self, ctx: commands.Context):
        """Sends a fact about this day in history"""
        date = datetime.today().strftime('%m/%d')
        headers = {
            'x-rapidapi-key': self.rapid_api_key,
            'x-rapidapi-host': 'numbersapi.p.rapidapi.com'
        }
        today_fact = await self.ass.get_url_data(
            f'https://numbersapi.p.rapidapi.com/{date}/date',
            headers=headers
        )
        embed = Embed(
            title=f'{date} in history:',
            description=today_fact,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('calendar'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['interesting'])
    async def useless(self, ctx: commands.Context):
        """Sends useless/interesting facts"""
        json_data = await self.ass.get_url_data(
            'https://uselessfacts.jsph.pl/api/v2/facts/random?language=en',
            get_type='json'
        )
        embed = Embed(
            title='Useless & Interesting Facts',
            description=json_data['text'],
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('bulb'))
        await ctx.send(embed=embed)
