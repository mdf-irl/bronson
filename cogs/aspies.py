""" aspies module """
from discord import ButtonStyle, Color, Embed, Member
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton


class Aspies(commands.Cog):
    """ aspies & aspies-adjacent commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

        # message.guild.id == 427500277076197376
        # and message.author.id == 333306739187515394

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     """triggered on msg"""
    #     if (
    #         message.guild.id == 427500277076197376
    #         and message.author.id == 333306739187515394
    #         and message.content == 'wow'
    #     ):
    #         await message.channel.send('ya\n:madcow:\nu bitch')

    @commands.command(name='49ers')
    async def helly_49ers(self, ctx):
        """ sends HeLLy 49ers meme image """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('helly_49ers'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ckhello(self, ctx):
        """
        Sends Cool-Knight's hello message

        Usage: <prefix>ckhello
        """
        msg = (
            'Hello i am Bronson from StarCraft Broodwar.\n'
            'A gamer, a websiter. And i am Arana Friend.\n'
            'And ofc Cool knight in shiny armor.\n'
            ':slight_smile:'
        )
        embed = Embed(description=msg, color=Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def deploy(self, ctx):
        """ Sends deploy c0n image """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('deploy_c0n'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['fucknewby'])
    async def fnewby(self, ctx):
        """
        Sends fuck newby gif

        Usage: <prefix>fnewby
        Aliases: fucknewby
        """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('fucknewby.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def gabby(self, ctx):
        """ sends stabby gabby gif """
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('gabby.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def homework(self, ctx: commands.Context,
                       users: commands.Greedy[Member]):
        """homework"""
        hw_users = await self.gen.format_users(users)

        embed = Embed(
            description=f'{hw_users} do u need help with ur homework jw',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('homework.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def humpty(self, ctx: commands.Context):
        """humpty instructions"""
        humpty_url = await self.ass.get_url('humpty.txt', res_type='raw')
        humpty_txt = await self.ass.get_url_data(humpty_url)
        humpty_parts = humpty_txt.split('%')

        humpty_embeds = []
        for humpty_part in humpty_parts:
            embed = Embed(
                title='Humpty 101', description=humpty_part,
                color=Color.random()
            )
            embed.set_thumbnail(url=await self.ass.get_url('humpty25.gif'))
            humpty_embeds.append(embed)
        await self._show_humpty(ctx, humpty_embeds)

    async def _show_humpty(self, ctx: commands.Context, embeds: list):
        """show humpty"""
        menu = ViewMenu(
            ctx, menu_type=ViewMenu.TypeEmbed,
            timeout=None, all_can_click=True
        )

        for humpty_embed in embeds:
            menu.add_page(humpty_embed)

        btn_back = ViewButton(
            style=ButtonStyle.primary, label='<',
            custom_id=ViewButton.ID_PREVIOUS_PAGE
        )
        menu.add_button(btn_back)

        btn_next = ViewButton(
            style=ButtonStyle.primary, label='>',
            custom_id=ViewButton.ID_NEXT_PAGE
        )
        menu.add_button(btn_next)

        await menu.start()

    @commands.command()
    async def idk(self, ctx: commands.Context):
        """idk lol"""
        idk_lol = (
            '#### ########  ##    ##\n'
            ' ##  ##     ## ##   ##\n'
            ' ##  ##     ## ##  ##\n'
            ' ##  ##     ## #####\n'
            ' ##  ##     ## ##  ##\n'
            ' ##  ##     ## ##   ##\n'
            '#### ########  ##    ##\n'
            '\n'
            '##        #######  ##\n'
            '##       ##     ## ##\n'
            '##       ##     ## ##\n'
            '##       ##     ## ##\n'
            '##       ##     ## ##\n'
            '##       ##     ## ##\n'
            '########  #######  ########'
        )
        embed = Embed(description=f'```{idk_lol}```', color=Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def moocrew(self, ctx: commands.Context):
        """moo crew"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('moocrew_optimized.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['snitch'])
    async def randall(self, ctx: commands.Context):
        """randall gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('randall.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def sdm(self, ctx: commands.Context):
        """#sDm"""
        poop = ':poop:' * 15
        sdm = (
            '  # #          ######\n'
            '  # #    ####  #     # #    #\n'
            '####### #      #     # ##  ##\n'
            '  # #    ####  #     # # ## #\n'
            '#######      # #     # #    #\n'
            '  # #   #    # #     # #    #\n'
            '  # #    ####  ######  #    #\n'
        )
        embed = Embed(
            description=f'{poop}```{sdm}```{poop}', color=Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def spray(self, ctx, users: commands.Greedy[Member]):
        """
        Sprays @user(s) with water bottle

        Usage: <prefix>spray @user(s)
        """
        sprayed_users = await self.gen.format_users(users)

        msg = (
            f'Sprays {sprayed_users} with water bottle\n'
            'There some water for you\n'
            "it' hot water.\n"
            ':wink:'
        )
        embed = Embed(description=msg, color=Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=['hawk'])
    async def trumpet(self, ctx):
        """
        Sends Hawk's beautiful trumpet performance

        Usage: <prefix>trumpet
        Aliases: hawk
        """
        trumpet_url = await self.ass.get_url('trumpet', res_type='video')
        trumpet_vid = await self.ass.get_discord_file(
            trumpet_url, 'trumpet.mov'
        )
        await ctx.send(file=trumpet_vid)

    async def _yo_get_id_list(self):
        """get list of yo gabs picture IDs"""
        json_data = await self.ass.get_url_data(
            'https://res.cloudinary.com/mdf-cdn/image/list/yogabs.json',
            get_type='json'
        )
        public_id_list = (
            [resource['public_id'][15:]
                for resource in json_data['resources']]
        )
        return public_id_list

    async def _yo_get_gabs_mention(self, ctx: commands.Context):
        """check for gabs & get @mention"""
        # gabs user id: 235906772504805377
        # check for gabs & @mention her if she's in the server
        gabs = ctx.guild.get_member(235906772504805377)
        gabs_mention = '' if gabs is None else '<@235906772504805377>'
        return gabs_mention

    @commands.command(aliases=['yogabs'])
    async def yo(self, ctx: commands.Context, arg: str = None):
        """yo gabs"""
        if arg is None:
            embed = Embed(color=Color.random())
            embed.set_image(url=await self.ass.get_url('yogabs', tag=True))
            await ctx.send(await self._yo_get_gabs_mention(ctx), embed=embed)
            return

        public_id_list = await self._yo_get_id_list()

        if arg in ['-list', '-l']:
            public_ids = ', '.join(sorted(public_id_list))
            embed = Embed(
                title='Yo Gabs Photo Aliases', description=public_ids,
                color=Color.random()
            )
            embed.set_footer(text='Example usage: !yo -gordon')
            await ctx.send(embed=embed)
            return

        #added to maintain backwards compatability with !yo gordon
        #but also support the new preferred !yo -gordon
        if arg.startswith('-'):
            arg = arg[1:]

        if arg in public_id_list:
            embed = Embed(color=Color.random())
            embed.set_image(url=await self.ass.get_url(f'yogabs/{arg}'))
            await ctx.send(await self._yo_get_gabs_mention(ctx), embed=embed)
        else:
            raise commands.CommandError(
                f'wow ya "{arg}" is not a valid fo toe alias u fkn retard. '
                 'u must b RLY DUMB LOL!!!!!'
            )


    async def cog_command_error(self, ctx, error):
        """ override, handles all cog errors for this class """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                "**Error**: You didn't provide the necessary argument(s)."
            )
        else:
            await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Aspies(bot))
