""" assets module """
from io import BytesIO
from os import getenv
from random import choice

from aiohttp import ClientSession
from cloudinary import config, utils
from discord import File
from discord.ext import commands
from dotenv import load_dotenv

class Assets(commands.Cog):
    """ Assets class """

    def __init__(self, bot):
        self.bot = bot # just to shut pylint up
        load_dotenv()
        self.cloud_name = getenv('CLOUD_NAME')

    async def get_url(self, public_id, res_type='image', tag=False):
        """ get cloud url """
        config(cloud_name=self.cloud_name)

        if not tag:
            return utils.cloudinary_url(
                f'bronson/{public_id}', resource_type=res_type)[0]

        json_data = await self.get_url_data(
            f'http://res.cloudinary.com/'
            f'{self.cloud_name}/image/list/{public_id}.json', get_type='json')
        chosen_public_id = choice(
            [resource['public_id'] for resource in json_data['resources']]
        )
        return utils.cloudinary_url(
            chosen_public_id, resource_type=res_type)[0]

    async def get_url_data(self, url, get_type='text', timeout=5):
        """ GET """
        try:
            async with ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 200:
                        if get_type == 'text':
                            return await response.text()
                        if get_type == 'json':
                            return await response.json()
                        if get_type == 'binary':
                            return await response.read()
                    else:
                        raise commands.CommandError(
                            f'Fetch attempt on "{url}" failed with error code '
                            f'{response.status}.')
        except TimeoutError as e:
            raise commands.CommandError(
                f'Timeout threshold of {timeout} seconds reached while '
                f'attempting to fetch data from "{url}."') from e

    async def get_discord_file(self, url, filename, spoiler=False):
        """ get discord File() """
        binary = await self.get_url_data(url, get_type='binary')
        return File(BytesIO(binary), filename=filename, spoiler=spoiler)


async def setup(bot):
    """ add class to bot's cog system """
    await bot.add_cog(Assets(bot))
