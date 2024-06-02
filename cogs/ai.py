"""ai module"""
from os import getenv

from discord import Color, Embed
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Ai(bot))


class Ai(commands.Cog):
    """
    AI commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

        load_dotenv()
        self.gemini_api_key = getenv('GEMINI_API_KEY')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def ai(self, ctx: commands.Context, *, prompt: str=None):
        """ai"""
        if prompt is None:
            raise commands.CommandError(
                "You didn't provide a prompt "
                "(example: **!ai why do cows moo?**)."
            )
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=(
                'Model provides moderate length answers in an informal tone '
                'with a large dose of personality and a touch of humor.'
            )
        )
        try:
            response = await model.generate_content_async(prompt)
        except Exception as exc:
            raise commands.CommandError(
                f"Unexpected error while generating content: {exc}."
            )
        try:
            answer = response.text
        except ValueError as exc:
            raise commands.CommandError(
                f'Your request ("{prompt}") was denied.'
            ) from exc

        embed = Embed(
            title=f'Gemini: "{prompt}"',
            description=answer,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('robot'))
        await ctx.send(embed=embed)
