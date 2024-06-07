"""image aliases module"""
from datetime import datetime

from aiohttp import ClientSession, InvalidURL
from discord import Color, Embed, Message
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Aliases(Base):
    """sqlalchemy"""
    __tablename__ = "aliases"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    url = Column(String, unique=False)
    author_id = Column(Integer, unique=False)
    server_id = Column(Integer, unique=False)
    datetime = Column(String, unique=False)
    usage_count = Column(Integer, unique=False)


engine = create_engine("sqlite:///./etc/image_aliases.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


async def setup(bot: commands.Bot):
    """add to bot"s cog system"""
    await bot.add_cog(ImageAliases(bot))


class ImageAliases(commands.Cog):
    """
    Image commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: str):
        """handle cog errors"""
        await ctx.reply(f"**Error**: {error}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """triggered on message"""
        if message.content.startswith(self.bot.prefix):
            arg = message.content[1:]
            db_command = session.query(Aliases).filter_by(name=arg).first()

            if db_command:
                db_command.usage_count += 1
                session.commit()
                await message.channel.send(db_command.url)

    @commands.command()
    async def image(self, ctx: commands.Context, *, args: str = None):
        """image command"""
        if args is None:
            await self._image_help(ctx)
            return

        split_args = args.split(" ")
        sub_command = split_args[0]

        if sub_command in ["-list", "list"]:
            await self._image_list(ctx)

        elif sub_command in ["-add", "add"]:
            await self._image_add(ctx, args)

        elif sub_command in ["-del", "del", "-rem", "rem"]:
            await self._image_del(ctx, args)

        elif sub_command in ["-info", "info"]:
            await self._image_info(ctx, args)

        elif sub_command in ["-rename", "rename"]:
            await self._image_rename(ctx, args)

        elif sub_command in ["-help", "help"]:
            await self._image_help(ctx)

        else:
            raise commands.CommandError(
                f"Invalid argument(s): `{args}`. Use `{self.bot.prefix}"
                f"{ctx.command.name} -help` if you need help using this "
                "feature."
            )

    async def _image_list(self, ctx: commands.Context):
        """list images"""
        names = session.query(Aliases.name).all()
        if not names:
            raise commands.CommandError(
                "The scripted image command database is empty."
            )
        name_list = sorted([name[0] for name in names])

        embed = Embed(
            title="Scripted Image Commands",
            description=", ".join(name_list),
            color=Color.random()
        )
        await ctx.send(embed=embed)

    async def _image_add(self, ctx: commands.Context, args: str):
        """add image"""
        await self._check_if_wrong_args(ctx, args)

        split_args = args.split(" ")
        cmd_name, cmd_url = split_args[1], split_args[2]

        await self._check_if_exists(cmd_name)
        await self._check_if_internal(cmd_name)
        await self._check_if_url_used(cmd_url)
        await self._check_if_valid_url(cmd_url)

        db_command = Aliases(name=cmd_name)
        db_command.url = cmd_url
        db_command.author_id = ctx.author.id
        db_command.server_id = ctx.guild.id
        db_command.datetime = datetime.now()
        db_command.usage_count = 0
        session.add(db_command)
        session.commit()

        await ctx.send(
            f"Added `{cmd_name}` to the scripted image command database."
        )

    async def _image_del(self, ctx: commands.Context, args: str):
        """del image"""
        await self._check_if_wrong_args(ctx, args)

        split_args = args.split(" ")
        cmd_name = split_args[1]

        await self._check_if_exists(cmd_name, True)
        await self._check_if_permitted(cmd_name, ctx.author.id)

        db_command = session.query(Aliases).filter_by(name=cmd_name).first()
        session.delete(db_command)
        session.commit()

        await ctx.send(
            f"Deleted `{cmd_name}` from the scripted image command database."
        )

    async def _image_info(self, ctx: commands.Context, args: str):
        """show info about specified command"""
        await self._check_if_wrong_args(ctx, args)

        split_args = args.split(" ")
        cmd_name = split_args[1]

        await self._check_if_exists(cmd_name, True)

        db_command = session.query(Aliases).filter_by(name=cmd_name).first()
        author = self.bot.get_user(db_command.author_id).display_name
        added_on = db_command.datetime

        await ctx.send(db_command.url)
        await ctx.send(
            f"`{db_command.name}` was added by `{author}` on `{added_on}`. "
            f"It has been used a total of `{db_command.usage_count}` times."
        )

    async def _image_rename(self, ctx: commands.Context, args: str):
        """rename image"""
        await self._check_if_wrong_args(ctx, args)

        split_args = args.split(" ")
        old_name, new_name = split_args[1], split_args[2]

        await self._check_if_exists(new_name)
        await self._check_if_internal(new_name)
        await self._check_if_exists(old_name, True)
        await self._check_if_permitted(old_name, ctx.author.id)

        db_command = session.query(Aliases).filter_by(name=old_name).first()
        db_command.name = new_name
        session.commit()

        await ctx.send(
            f"Renamed `{old_name}` to `{new_name}` in the scripted image "
            "command database."
        )

    async def _check_if_valid_url(self, url: str):
        """check if url is valid"""
        try:
            async with ClientSession() as http:
                async with http.get(url, timeout=5) as response:
                    if response.status == 200:
                        pass
                    else:
                        raise commands.CommandError(
                            f"`{url}` is not a valid URL."
                        )
        except TimeoutError as exc:
            raise commands.CommandError(
                "URL validation reached timeout threshold of 5 seconds. "
                "Please try again."
            ) from exc
        except InvalidURL as exc:
            raise commands.CommandError(
                f"`{url}` is not a valid URL."
            ) from exc

    async def _check_if_wrong_args(self, ctx: commands.Context, args: str):
        """check for wrong # of arguments used"""
        split_args = args.split(" ")
        sub_command = split_args[0]

        if sub_command in ["-add", "add"]:
            arg_count = 3
            example = "-add <name> <URL>"

        if sub_command in ["-del", "del", "-rem", "rem"]:
            arg_count = 2
            example = "-del <name>"

        elif sub_command in ["-info", "info"]:
            arg_count = 2
            example = "-info <name>"

        elif sub_command in ["-rename", "rename"]:
            arg_count = 3
            example = "-rename <old_name> <new_name>"

        if len(split_args) != arg_count:
            raise commands.CommandError(
                f"Command takes {arg_count - 1} arguments "
                f"(`{self.bot.prefix}{ctx.command.name} {example}`)."
            )

    async def _check_if_internal(self, cmd_name: str):
        """check if command already exists internally"""
        if cmd_name in self.bot.all_commands:
            raise commands.CommandError(
                f"`{cmd_name}` can't be used as a scripted image command as "
                "it's already reserved by an internal command."
            )

    async def _check_if_url_used(self, url: str):
        """check if url has already been used by another command"""
        db_command = session.query(Aliases).filter_by(url=url).first()
        if db_command:
            raise commands.CommandError(
                f"Provided URL is already tied to the scripted image "
                f"command `{db_command.name}`."
            )

    async def _check_if_exists(self, cmd_name: str, doesnt: bool = False):
        """check if command name already exists"""
        db_command = session.query(Aliases).filter_by(name=cmd_name).first()
        if (db_command) and (not doesnt):
            raise commands.CommandError(
                f"`{cmd_name}` is already being used by another scripted "
                "image command."
            )
        if (not db_command) and (doesnt):
            raise commands.CommandError(
                f"`{cmd_name}` does not exist as a scripted image command."
            )

    async def _check_if_permitted(self, cmd_name: str, user_id: int):
        """check if user has permission"""
        owner_id = (await self.bot.application_info()).owner.id

        db_command = session.query(Aliases).filter_by(name=cmd_name).first()
        if not user_id in (owner_id, db_command.author_id):
            raise commands.CommandError(
                "You're not permitted to do that. Scripted image commands can "
                "only be modified by the command's author or the bot owner."
            )

    async def _image_help(self, ctx: commands.Context):
        """show image cmd help embed"""
        p = f"{self.bot.prefix}{ctx.command.name}"

        embed = Embed(
            title=f"{self.bot.prefix}{ctx.command.name} Usage:",
            description=(
                f"`{self.bot.prefix}<name>`\n"
                "Shows scripted image command `<name>`.\n\n"

                f"`{p} -list`\n"
                "Shows list of all scripted image commands.\n\n"

                f"`{p} -add <name> <URL>`\n"
                "Adds command `<name>` from image at `<URL>`.\n\n"

                f"`{p} -del <name>`\n"
                "Deletes command `<name>`.\n"
                "Must be command's author or bot owner.\n\n"

                f"`{p} -rename <old_name> <new_name>`\n"
                "Renames command `<old_name>` to `<new_name>`.\n"
                "Must be command's author or bot owner.\n\n"

                f"`{p} -info <name>`\n"
                "Shows info and stats about command `<name>`.\n\n"

                f"`{p} -help`\n"
                "Shows this helpful embed. :wink:"
            ),
            color=Color.random()
        )
        await ctx.send(embed=embed)
