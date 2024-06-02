"""novelty module"""
from random import choice, choices, sample
from string import ascii_lowercase, digits

from cowsay import get_output_string
from discord import ButtonStyle, Color, Embed, File, Member
from discord.ext import commands
from gtts import gTTS
from reactionmenu import ViewMenu, ViewButton

async def setup(bot: commands.Bot):
    """add to bot's cog system"""
    await bot.add_cog(Novelty(bot))


class Novelty(commands.Cog):
    """
    Novelty commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f'**Error**: {error}')

    @commands.command(name='8ball')
    async def eightball(self, ctx: commands.Context, *, question: str=None):
        """Magic 8ball"""
        if question is None:
            raise commands.CommandError(
                "You didn't provide a question "
                "(example: **!8ball is HeLLy tha kewlest?**)."
            )
        resp_url = await self.ass.get_url('8ball_2.txt', res_type='raw')
        resp_text = await self.ass.get_url_data(resp_url)
        responses = resp_text.splitlines()

        if not question.endswith('?'):
            question = f'{question}?'

        embed = Embed(
            title='Magic 8ball',
            description=(
                f'*{question}*\n'
                f'**Answer**: {choice(responses)}'
            ),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('8ball_new'))
        await ctx.send(embed=embed)

    @commands.command()
    async def achtung(self, ctx: commands.Context, *, message: str=None):
        """Sends an achtung with your message"""
        if message is None:
            raise commands.CommandError(
                "You didn't provide a message "
                "(example: **!achtung HeLLy farted**)."
            )
        embed = Embed(
            title='ACHTUNG!',
            description=message,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('ach_siren'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['choice'])
    async def choose(self, ctx: commands.Context, *, args: str=None):
        """choose between things"""
        if args is None:
            raise commands.CommandError(
                "You didn't list anything to choose from "
                "(example: **!choose ketchup, mustard, mayo**)."
            )
        split_args = args.split(', ')
        my_choice = choice(split_args)

        embed = Embed(
            title=f'From {args}...',
            description=f'I choose **{my_choice}**. :blush:',
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('thinking'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['cn'])
    async def citation(self, ctx: commands.Context):
        """citation needed"""
        embed = Embed(color=Color.random())
        embed.set_image(url=await self.ass.get_url('citation'))
        await ctx.send(embed=embed)

    @commands.command()
    async def coin(self, ctx: commands.Context):
        """Bronson flips a coin for you"""
        coin_state = choice(['heads', 'tails'])
        embed = Embed(
            title='And...',
            description=f'{coin_state.title()} it is!',
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url(coin_state))
        await ctx.send(embed=embed)

    @commands.command()
    async def cowsay(self, ctx: commands.Context, *, message: str=None):
        """Sends an ASCII art cow saying your message"""
        # there's a bunch of options we can use other than 'cow'
        # will expand on this at a later time
        if message is None:
            raise commands.CommandError(
                "You didn't provide a message "
                "(example: **!cowsay MOO LOL**)."
            )
        await ctx.reply(f'```{get_output_string('cow', message)}```')

    @commands.command()
    async def dadjoke(self, ctx: commands.Context):
        """Sends a random dad joke"""
        resp = await self.ass.get_url_data(
            'https://icanhazdadjoke.com/slack', get_type='json'
        )
        embed = Embed(
            title='Dad Jokes',
            description=resp['attachments'][0]['text'],
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('dad'))
        await ctx.send(embed=embed)

    @commands.command()
    async def fortune(self, ctx: commands.Context, user: Member = None):
        """Sends fortune"""
        resp_url = await self.ass.get_url('fortunes.txt', res_type='raw')
        resp_txt = await self.ass.get_url_data(resp_url)
        responses = resp_txt.splitlines()

        who = f"{user.display_name}'s" if user else 'Your'
        embed = Embed(
            title=f'{who} fortune is...',
            description=choice(responses),
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('fortune'))
        await ctx.send(embed=embed)

    @commands.command()
    async def humpty(self, ctx: commands.Context):
        """Sends humpty 101 instructions"""
        humpty_url = await self.ass.get_url('humpty.txt', res_type='raw')
        humpty_txt = await self.ass.get_url_data(humpty_url)
        humpty_parts = humpty_txt.split('%')

        humpty_embeds = []
        for humpty_part in humpty_parts:
            embed = Embed(
                title='Humpty 101',
                description=humpty_part,
                color=Color.random()
            )
            embed.set_thumbnail(url=await self.ass.get_url('humpty25.gif'))
            humpty_embeds.append(embed)
        await self._humpty_show(ctx, humpty_embeds)

    async def _humpty_show(self, ctx: commands.Context, embeds: list):
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
    async def insult(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None,
        *, arg: str=None
    ):
        """
        !insult @user(s) -> mild insult
        !insult @user(s) -spicy -> spicy insult
        """
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!insult {ctx.author.mention}**)."
            )
        insultees = ', '.join(user.display_name for user in users)

        if arg is None:
            insult = await self.ass.get_url_data(
                'https://insult.mattbas.org/api/insult.txt'
            )
            thumbnail = 'insult_mild'
            response = f'{insult.rstrip()}.'
        elif arg in ['-spicy', '-s']:
            words_txt = await self.ass.get_url_data(
                await self.ass.get_url('insult_words.txt', res_type='raw')
            )
            words_list = words_txt.splitlines()
            words_chosen_list = sample(words_list, 10)
            words = ' '.join(words_chosen_list)
            a_an = 'an' if words[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'

            thumbnail = 'insult_spicy'
            response = f'You are {a_an} {words}.'
        else:
            raise commands.CommandError(
                "You didn't provide a valid argument "
                f"(example: **!insult {ctx.author.mention} -spicy**)."
            )
        embed = Embed(
            title=f'{insultees}...',
            description=response,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url(thumbnail))
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx: commands.Context):
        """Sends a random joke"""
        joke = await self.ass.get_url_data(
            'https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Spooky'
            '?blacklistFlags=racist,sexist&format=txt'
        )
        embed = Embed(
            title='RLY FUN-E JOKES LOL!!! :hand_splayed::skull:',
            description=joke,
            color=Color.random()
        )
        embed.set_thumbnail(url=await self.ass.get_url('cow_lol'))
        await ctx.send(embed=embed)

    @commands.command()
    async def sausage(
        self,
        ctx: commands.Context,
        users: commands.Greedy[Member] = None
    ):
        """Ask @user(s) if they would like some sausage"""
        if users is None:
            raise commands.CommandError(
                "You didn't provide any user(s) "
                f"(example: **!sausage {ctx.author.mention}**)."
            )
        hungry_users = ', '.join(user.mention for user in users)

        response = (
            f'{hungry_users} would you like some sausage?\n'
            f'{hungry_users} would you like some sausages?\n'
            f'{hungry_users} would you like some sausage?\n'
            f'{hungry_users} would you like some sausages?'
        )
        embed = Embed(description=response, color=Color.random())
        embed.set_image(url=await self.ass.get_url('sausage.gif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def tts(self, ctx: commands.Context, *, message: str=None):
        """Sends wav file of text to speech message"""
        if message is None:
            raise commands.CommandError(
                "You didn't provide a message "
                "(example: **!tts r u kon?**)."
            )
        filename = await self._tts_get_filename()
        tts = gTTS(text=message, lang='en')
        tts.save(f'./tmp/Bronson_{filename}.mp3')
        await ctx.send(file=File(f'./tmp/Bronson_{filename}.mp3'))

    async def _tts_get_filename(self) -> str:
        """get random filename"""
        filename = ''.join(choices(ascii_lowercase + digits, k=20))
        return filename

    @commands.command()
    async def vapor(self, ctx: commands.Context):
        """Sends a chart image of the vaporization points
        of various cannabinoids"""
        embed = Embed(
            title='Cannabinoid Vaporization Temperatures',
            color=Color.random()
        )
        embed.set_image(url=await self.ass.get_url('vapor'))
        await ctx.send(embed=embed)
