"""voice module"""
from discord import Color, Embed, Member
from discord.ext import commands


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Voice(bot))


class Voice(commands.Cog):
    """
    Voice chat commands.
    """
    # only 1 cmd rn. will be further expanded upon later.

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command()
    async def vc(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """Sends a voice chat invitation to @user(s)"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!vc {ctx.author.mention}**)."
            )
        # check for command errors
        if ctx.author.voice is None:
            raise commands.CommandError("You aren't in a voice channel.")

        invitees = ', '.join(user.mention for user in users)
        # build invite message
        inv_msg = (
            f'Dearest {invitees},\n\n'
            'It is my sincere pleasure to extend to you a cordial invitation '
            'to our esteemed voice chat session, currently taking place in '
            'voice communications channel: '
            f'"**{ctx.author.voice.channel.name}**."\n\n'

            'Your insights and contributions are highly valued, and we '
            'believe that your participation would greatly enhance the depth '
            'and breadth of our discussion.\n\n'
            f'Kind regards,\n<@{ctx.author.id}>'
        )
        # build embed with invite message & file references
        embed = Embed(description=inv_msg, color=Color.random())
        embed.set_thumbnail(url=await self.ass.get_url('quill'))
        embed.set_image(url=await self.ass.get_url('rsvp'))
        embed.set_footer(
            text='Please RSVP at your earliest convenience, oKaY BuY.'
        )
        await ctx.send(embed=embed)
