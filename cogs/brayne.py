"""brayne module"""
from datetime import datetime
from os import name as os_name
from platform import platform, python_version, system

from discord import Color, CustomActivity, Embed, Member, __version__
from discord.ext import commands
from gpiozero import CPUTemperature
from psutil import (
    boot_time, cpu_count, cpu_freq, cpu_percent, disk_usage, virtual_memory
)


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Brayne(bot))


class Brayne(commands.Cog):
    """
    Commands that deal with information about the bot, users, or servers.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.connected_time = 0

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.Cog.listener()
    async def on_ready(self):
        """called when the bot is online & ready"""
        self.connected_time = datetime.now()
        await self.bot.change_presence(
            activity=CustomActivity(name='420.69-1.10.1 - !help')
        )

    @commands.command()
    async def avatar(self, ctx: commands.Context, user: Member = None):
        """Sends @user's avatar"""
        if user is None:
            raise commands.CommandError(
                "You didn't provide a user "
                f"(example: **!avatar {ctx.author.mention}**)."
            )
        embed = Embed(
            title=f"{user.display_name}'s Avatar",
            description=f'```{user.display_avatar.url}```',
            color=Color.random()
        )
        embed.set_image(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['about', 'info', 'ver', 'version'])
    async def brayne(self, ctx: commands.Context):
        """Sends information about Bronson's BrAyNe"""
        embed = Embed(
            title='Bronson',
            description=self._brayne_get_platform_info(),
            color=Color.random()
        )
        embed.add_field(
            name='__CPU__:',
            value=self._brayne_get_cpu_info(),
            inline=True
        )
        embed.add_field(
            name='__Memory__:',
            value=self._brayne_get_memory_info(),
            inline=True
        )
        embed.add_field(
            name='__Disk__:',
            value=self._brayne_get_disk_info(),
            inline=True
        )
        embed.set_thumbnail(url=await self.ass.get_url('brayne'))
        embed.set_footer(text=f'Ping: {round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

    def _brayne_get_cpu_info(self) -> str:
        """get cpu info"""
        # get cpu temp if on linux (raspberry pi)
        if system().lower() == "linux":
            cpu_temp = CPUTemperature()
            cpu_temp_c = f'{cpu_temp.temperature:.2f} °C'
        else:
            cpu_temp_c = 'N/A'

        cpu_info = (
            f'**Usage**: {cpu_percent(interval=1):.2f}%\n'
            f'**Core/Freq**: {cpu_count(logical=False)}x @ '
            f'{cpu_freq().current / 1000:.2f} GHz '
            f'(***max*** *{cpu_freq().max / 1000:.2f} GHz*)\n'
            f'**Temperature**: {cpu_temp_c}'
        )
        return cpu_info

    def _brayne_get_disk_info(self) -> str:
        """get disk info"""
        disk_info = (
            f'**Used**: {disk_usage('/').used / (1024 ** 3):.2f} GB\n'
            f'**Total**: {disk_usage('/').total / (1024 ** 3):.2f} GB\n'
            f'({disk_usage('/').percent:.2f}%)'
        )
        return disk_info

    def _brayne_get_memory_info(self) -> str:
        """get memory info"""
        memory_info = (
            f'**Used**: {virtual_memory().used / (1024 ** 3):.2f} GB\n'
            f'**Total**: {virtual_memory().total / (1024 ** 3):.2f} GB\n'
            f'({virtual_memory().percent:.2f}%)'
        )
        return memory_info

    def _brayne_get_platform_info(self) -> str:
        """get platform info"""
        booted_time = datetime.fromtimestamp(boot_time())

        platform_info = (
            '**Bot version**: 420.69-1.10.1\n'
            '**GitHub**: '
            '[/mdf-gh/bronson](https://www.github.com/mdf-gh/bronson)\n\n'

            f'**Python version**: {python_version()}\n'
            f'**discord.py API version**: {__version__}\n\n'

            f'**OS**: {platform()} ({os_name})\n\n'

            f'**Bot uptime**: {self._brayne_get_uptime(self.connected_time)}\n'
            f'**System uptime**: {self._brayne_get_uptime(booted_time)}'
        )
        return platform_info

    def _brayne_get_uptime(self, start_time: datetime) -> str:
        """get uptime info for bot or system"""
        delta = datetime.now() - start_time

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'{days}d, {hours}h, {minutes}m, {seconds}s'

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Sends help message"""
        embed = Embed(
            title='You need help? LOL!!!',
            description=(
                'Please visit [my GitHub page]'
                '(https://github.com/mdf-gh/bronson) to find my command '
                'list, help, documentation, & source code.'
            ),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('cow_capri'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Sends bot's current ping"""
        ping_ms = round(self.bot.latency * 1000)
        embed = Embed(
            title='Pong! :ping_pong: LOL!!!',
            description=f'My current ping is {ping_ms}ms.',
            color=Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['guild'])
    async def server(self, ctx: commands.Context):
        """Sends current server info"""
        embed = Embed(
            title=ctx.guild.name,
            color=Color.random()
        )
        embed.add_field(
            name='**Owner**:',
            value=ctx.guild.owner,
            inline=True
        )
        embed.add_field(
            name='**Created**:',
            value=ctx.guild.created_at.strftime('%m/%d/%Y'),
            inline=True
        )
        embed.add_field(
            name='**Members**:',
            value=ctx.guild.member_count,
            inline=True
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text='This will be expanded upon in a future update.')
        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx: commands.Context, user: Member = None):
        """Sends @user info"""
        if user is None:
            raise commands.CommandError(
                "You didn't provide a user "
                f"(example: **!user {ctx.author.mention}**)."
            )
        embed = Embed(
            title=f'{user.display_name} ({user.name})',
            color=Color.random()
        )
        embed.add_field(
            name='**Server join date**:',
            value=user.joined_at.strftime('%m/%d/%Y')
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text='This will be expanded upon in a future update.')
        await ctx.send(embed=embed)
