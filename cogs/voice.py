""" voice module """
from discord import Embed, Color, Member
from discord.ext import commands


class Voice(commands.Cog):
    """ voice chat commands """
    # only 1 cmd rn. will be further expanded upon later.

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    @commands.command()
    async def vc(self, ctx, users: commands.Greedy[Member]):
        """
        Sends a voice chat invitation to @user(s)

        This command issues a voice chat invitation to @mentioned
        server members. It can be used by a server member only when
        they are in one of the server's voice channels.

        Usage: <prefix>vc @user(s)
        """

        # check for command errors
        if ctx.author.voice is None:
            raise commands.CommandError("You aren't in a voice channel.")
        if not users:
            raise commands.CommandError("You didn't @mention any user(s).")

        # get a list of the mentioned users separated by commas
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
        embed = Embed(description=inv_msg, color=Color.purple())
        embed.set_author(
            name="Bronson's Voice Chat Invitation",
            icon_url=await self.ass.get_url('bbb')
        )
        embed.set_thumbnail(url=await self.ass.get_url('quill'))
        embed.set_image(url=await self.ass.get_url('rsvp'))
        embed.set_footer(
            text='Please RSVP at your earliest convenience, oKaY BuY.'
        )

        await ctx.reply(embed=embed)

    @vc.error
    async def vc_error(self, ctx, error):
        """ vc err handler """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Voice(bot))
