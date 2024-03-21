""" Bronson """
#!/usr/bin/env python3

from os import getenv
from sys import exit as quit_bot

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = getenv('DISCORD_TOKEN')
BOT_PREFIX = getenv('BOT_PREFIX')

if (DISCORD_TOKEN is None) or (BOT_PREFIX is None):
    print('Could not get environment variables from .env file.')
    quit_bot()

class DiscordBot(commands.Bot):
    """ main bot class """
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(BOT_PREFIX),
            intents=intents,
        )

    async def load_cogs(self):
        """ load cogs """
        #always load assets first
        await self.load_extension('cogs.assets')

        await self.load_extension('cogs.brayne')
        await self.load_extension('cogs.comics')
        await self.load_extension('cogs.facts')
        await self.load_extension('cogs.fangulese')
        await self.load_extension('cogs.novelty')
        await self.load_extension('cogs.voice')

    async def setup_hook(self):
        await self.load_cogs()

bot = DiscordBot()
bot.run(DISCORD_TOKEN)
