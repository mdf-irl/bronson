""" Bronson 420.69-2024.03.16-01 """
#!/usr/bin/env python3

from os import getenv, listdir
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
        """ called when class is created """
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(BOT_PREFIX),
            intents=intents,
        )

    async def load_cmds(self):
        """ load commands from cmds folder """
        try:
            for file in listdir('./cmds'):
                if file.endswith('.py'):
                    await self.load_extension(f'cmds.{file[:-3]}')
        except FileNotFoundError:
            print('Error loading command files.')
            quit_bot()

    async def setup_hook(self):
        await self.load_cmds()

bot = DiscordBot()
bot.run(DISCORD_TOKEN)
