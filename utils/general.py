""" general module """
from discord import Member
from discord.ext import commands


class General(commands.Cog):
    """ General class """

    def __init__(self, bot):
        self.bot = bot

    async def format_users(
            self,
            users: commands.Greedy[Member],
            mention: bool=True
    ):
        """format users"""
        if not users:
            raise commands.CommandError("You didn't @mention any user(s).")

        if mention:
            users_f = ', '.join(user.mention for user in users)
        else:
            users_f = ', '.join(user.display_name for user in users)
        return users_f


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(General(bot))
