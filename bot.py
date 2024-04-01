""" Bronson """
#!/usr/bin/env python3

from os import getenv, listdir
from sys import exit as quit_bot

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = getenv('DISCORD_TOKEN')
BOT_PREFIX = getenv('BOT_PREFIX')
CLOUD_NAME = getenv('CLOUD_NAME')

if DISCORD_TOKEN is None:
    print("Couldn't get DISCORD_TOKEN from .env file")
    quit_bot()
elif BOT_PREFIX is None:
    print("Couldn't get BOT_PREFIX from .env file. Defaulting to '!'")
    BOT_PREFIX = '!'
elif CLOUD_NAME is None:
    print("Couldn't get CLOUD_NAME from .env file.")
    quit_bot()


class DiscordBot(commands.Bot):
    """ main bot class """

    def __init__(self):
        intents = discord.Intents.default()
        # these following 2 are special privs u need 2 turn on in the
        # discord developer portal
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(BOT_PREFIX),
            intents=intents,
            help_command=None,
        )

    async def load_cogs(self):
        """ load cogs """
        # always load utils first
        await self.load_extension('utils.assets')
        await self.load_extension('utils.general')

        cogs = listdir('./cogs')
        for cog in cogs:
            if cog.endswith('.py'):
                await self.load_extension(f'cogs.{cog[:-3]}')

    async def setup_hook(self):
        await self.load_cogs()

bot = DiscordBot()
bot.run(DISCORD_TOKEN)
