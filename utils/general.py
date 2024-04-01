""" general module """
from discord import Member
from discord.ext import commands

class General(commands.Cog):
    """ General class """

    def __init__(self, bot):
        self.bot = bot

    async def format_users(self, users: commands.Greedy[Member]):
        """ format users """
        if not users:
            raise commands.CommandError("You didn't @mention any user(s).")

        users_f = ', '.join(user.mention for user in users)
        return users_f

async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(General(bot))
