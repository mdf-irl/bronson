""" aspies module """
from discord import Color, Embed, Member
from discord.ext import commands


class Aspies(commands.Cog):
    """ aspies & aspies-adjacent commands """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.gen = self.bot.get_cog('General')

    @commands.command(name='49ers')
    async def helly_49ers(self, ctx: commands.Context):
        """Sends HeLLy 49ers gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('helly_49ers'))
        await ctx.send(embed=embed)

    @commands.command()
    async def ckhello(self, ctx: commands.Context):
        """Sends Cool-Knight's hello message"""
        msg = (
            'Hello i am Bronson from StarCraft Broodwar.\n'
            'A gamer, a websiter. And i am Arana Friend.\n'
            'And ofc Cool knight in shiny armor.\n'
            ':slight_smile:'
        )
        embed = Embed(description=msg, color=Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def deploy(self, ctx: commands.Context):
        """Sends deploy c0n image"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('deploy_c0n'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['fucknewby'])
    async def fnewby(self, ctx: commands.Context):
        """Sends the classic fucknewby gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('fucknewby.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['stabby', 'stabbygabby'])
    async def gabby(self, ctx: commands.Context):
        """Sends the stabby gabby gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('gabby.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def homework(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]
    ):
        """Asks @user(s) if they need help with their homework"""
        hw_users = await self.gen.format_users(users)

        embed = Embed(
            description=f'{hw_users} do u need help with ur homework jw',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('homework.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def idk(self, ctx: commands.Context):
        """Sends IDK LOL ASCII art"""
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
        """Sends moo crew gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('moocrew_optimized.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['snitch'])
    async def randall(self, ctx: commands.Context):
        """Sends Randall/snitch gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('randall.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def sdm(self, ctx: commands.Context):
        """Sends #sDm ASCII art"""
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
            description=f'{poop}```{sdm}```{poop}',
            color=Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def spray(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member]
    ):
        """Sprays @user(s) with water bottle (it' hot water.)"""
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
    async def trumpet(self, ctx: commands.Context):
        """Sends a video of Hawk's beautiful trumpet performance"""
        trumpet_url = await self.ass.get_url('trumpet', res_type='video')
        trumpet_vid = await self.ass.get_discord_file(
            trumpet_url, 'trumpet.mov'
        )
        await ctx.send(file=trumpet_vid)

    async def _yo_get_id_list(self):
        """get list of yo gabs photo IDs"""
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
        gabs = ctx.guild.get_member(235906772504805377)
        gabs_mention = '' if gabs is None else '<@235906772504805377>'
        return gabs_mention

    @commands.command(aliases=['yogabs'])
    async def yo(self, ctx: commands.Context, arg: str = None):
        """
        Sends a random yo gabs meme. Optional argument -list shows a list of
        picture IDs that can be used to show a specific meme
        (!yo gordon OR !yo -gordon, etc.)
        """
        if arg is None:
            gabs_img = await self.ass.get_url('yogabs', tag=True)
            # gabs_id = gabs_img.split('/')[-1]

            embed = Embed(color=Color.random())
            embed.set_image(url=gabs_img)
            await ctx.send(await self._yo_get_gabs_mention(ctx), embed=embed)
            return

        public_id_list = await self._yo_get_id_list()

        if arg in ['-list', '-l']:
            public_ids = ', '.join(sorted(public_id_list))
            embed = Embed(
                title='Yo Gabs Meme IDs',
                description=public_ids,
                color=Color.random()
            )
            embed.set_footer(
                text='Example usage: !yo -gordon',
                icon_url=await self.ass.get_url('bbb')
            )
            await ctx.send(embed=embed)
            return

        arg = arg.lstrip('-')

        if arg in public_id_list:
            embed = Embed(color=Color.random())
            embed.set_image(url=await self.ass.get_url(f'yogabs/{arg}'))
            await ctx.send(await self._yo_get_gabs_mention(ctx), embed=embed)
        else:
            raise commands.CommandError(
                f'wow ya "{arg}" is not a valid me me eye D u fkn retard. '
                 'u must b RLY DUMB LOL!!!!! idk maybe try using !yo -list '
                 '2 show sum ackshual valid ones LOL!'
            )


    async def cog_command_error(self, ctx: commands.Context, error):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """add class to bot's cog system"""
    await bot.add_cog(Aspies(bot))
