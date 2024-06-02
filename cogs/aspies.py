"""aspies module"""
from discord import Color, Embed, Member
from discord.ext import commands


async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Aspies(bot))


class Aspies(commands.Cog):
    """
    Commands that are only really relevant to Aspies & Aspies-adjacent servers.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.Cog.listener()
    async def on_message(self, message):
        """triggered on msg"""
        #Sends an image expressing disdain for a certain cow
        if await self._simple_checksum(message.content) == 47616:
            embed = Embed(color=Color.random())
            embed.set_image(url=await self.ass.get_url('autistic_man.gif'))
            await message.channel.send(embed=embed)

    async def _simple_checksum(self, message: str) -> int:
        """simple checksum"""
        checksum_value = 420
        for char in message:
            checksum_value += ord(char) * 69
        return checksum_value

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

    @commands.command(aliases=['stabby', 'stabbygabby'])
    async def gabby(self, ctx: commands.Context):
        """Sends stabby gabby gif"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('gabby.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def homework(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """Asks @user(s) if they need help with their homework"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!homework {ctx.author.mention}**)."
            )
        hw_users = ', '.join(user.mention for user in users)

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

    @commands.command()
    async def poke(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """poke @user(s)"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!poke {ctx.author.mention}**)."
            )
        has_have = 'has' if len(users) == 1 else 'have'
        poked_users = ', '.join(user.mention for user in users)

        embed = Embed(
            description=(
                f':point_right: {poked_users} :point_left: {has_have} been '
                '**POKED**. LOL!!!'
            ),
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('poke.gif'))
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
            '  # #    ####  ######  #    #'
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
        users: commands.Greedy[Member] = None
    ):
        """Sprays @user(s) with water bottle (it' hot water.)"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!spray {ctx.author.mention}**)."
            )
        sprayed_users = ', '.join(user.mention for user in users)

        msg = (
            f'Sprays {sprayed_users} with water bottle\n'
            'There some water for you\n'
            "it' hot water.\n"
            ':wink:'
        )
        embed = Embed(description=msg, color=Color.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def ty(self, ctx: commands.Context, user: Member=None):
        """ty"""
        if user is None:
            raise commands.CommandError(
                "You didn't provide a user "
                f"(example: **!ty {ctx.author.mention}**)."
            )
        embed = Embed(
            description=f'ty 4 the upd8 {user.mention}',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('ty_o.gif'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['hawk'])
    async def trumpet(self, ctx: commands.Context):
        """Sends video of Hawk's beautiful trumpet performance"""
        trumpet_url = await self.ass.get_url('trumpet', res_type='video')
        trumpet_vid = await self.ass.get_discord_file(
            trumpet_url, 'trumpet.mov'
        )
        await ctx.send(file=trumpet_vid)

    @commands.command(aliases=['yogabs'])
    async def yo(self, ctx: commands.Context, *, arg: str=None):
        """
        Sends yo gabs meme:
        !yo -> sends random yo gabs meme
        !yo -list -> sends list of yo gabs meme public IDs
        !yo -name -> sends yo gabs meme with the public ID "name"
        """
        if arg is None:
            gabs_img = await self.ass.get_url('yogabs', tag=True)

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
                f'Yo {ctx.author.mention}, "{arg}" is not a valid argument. '
                'Try using **!yo** by itself for a random meme, or **!yo '
                '-list** to see a list of valid arguments you can use.'
            )

    async def _yo_get_gabs_mention(self, ctx: commands.Context) -> str:
        """check for gabs & get @mention"""
        gabs = ctx.guild.get_member(235906772504805377)
        gabs_mention = '' if gabs is None else '<@235906772504805377>'
        return gabs_mention

    async def _yo_get_id_list(self) -> list:
        """get list of yo gabs photo public IDs"""
        json_data = await self.ass.get_url_data(
            'https://res.cloudinary.com/mdf-cdn/image/list/yogabs.json',
            get_type='json'
        )
        public_id_list = (
            [resource['public_id'][15:] for resource in json_data['resources']]
        )
        return public_id_list
