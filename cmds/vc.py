""" vc module """
from discord import Embed, Color, File
from discord.ext import commands

class Vc(commands.Cog):
    """ vc class """
    @commands.command()
    async def vc(self, ctx):
        """
        Sends a voice chat invitation to @user(s)
        
        This command issues a voice chat invitation to @mentioned
        server members. It can be used by a server member only when
        they are in one of the server's voice channels.

        Usage: <prefix>vc @user(s)
        """
        mentioned_users = ctx.message.mentions
        invitees = ''

        #check for command errors
        if ctx.author.voice is None:
            raise commands.CommandError('You are not in a voice channel.')
        if not mentioned_users:
            raise commands.CommandError('You did not mention any users.')

        #get a list of the mentioned users separated by commas
        for user in mentioned_users:
            invitees = invitees + f'{user.mention}, '

        #build invite message
        inv_msg = (
            f'Dearest {invitees}\n\n'
             'It is my sincere pleasure to extend to you a cordial invitation '
             'to our esteemed voice chat session, currently taking place in '
             'voice communications channel: '
            f'"**{ctx.author.voice.channel.name}**."\n\n'

             'Your insights and contributions are highly valued, and we '
             'believe that your participation would greatly enhance the depth '
             'and breadth of our discussion.\n\n'
            f'Kind regards,\n<@{ctx.author.id}>'
        )

        #build embed with invite message & file references
        embed = Embed(description=inv_msg, color=Color.purple())
        embed.set_author(name="Bronson's Voice Chat Invitation",
                         icon_url='attachment://images_common_bbb.jpg')
        embed.set_thumbnail(url='attachment://images_vc_quill.jpg')
        embed.set_image(url='attachment://images_vc_rsvp.jpg')
        embed.set_footer(text='Please RSVP at your earliest convenience, '
                              'oKaY BuY.')

        #attach embedded files & send
        try:
            with open('./images/common/bbb.jpg', 'rb') as icon, \
                 open('./images/vc/quill.jpg', 'rb') as thumbnail, \
                 open('./images/vc/rsvp.jpg', 'rb') as rsvp_img:

                await ctx.reply(embed=embed, files=[File(icon),
                                                    File(thumbnail),
                                                    File(rsvp_img)])
        except FileNotFoundError as e:
            raise commands.CommandError('Asset not found.') from e

    @vc.error
    async def vc_error(self, ctx, error):
        """ vc err handler """
        await ctx.reply(f'**Error**: {error}')

async def setup(bot):
    """ add command to bot's cog system """
    await bot.add_cog(Vc(bot))
