""" mom module """
from json import loads

from aiohttp import ClientSession
from discord.ext import commands

class Mom(commands.Cog):
    """ mom class """
    @commands.command(name='mom')
    async def mom(self, ctx):
        """
        Sends a fact about @user's mom

        Returns a random yo mama joke from the yomama-jokes.com API
        targeted at a specific user.
        
        Usage: <prefix>mom @user
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
            html = await self._get_html(
                'https://www.yomama-jokes.com/api/v1/jokes/random/')
        except Exception as e:
            raise commands.CommandError('Could not get HTML.') from e

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

    async def _get_html(self, url):
        """ HTML grabber """
        #gets the HTML of URL specified
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @mom.error
    async def yomama_error(self, ctx, error):
        """ mom error handling """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Mom(bot))
