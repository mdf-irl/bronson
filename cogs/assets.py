""" assets module """
from json import loads
from random import choice

from aiohttp import ClientSession
from cloudinary import config, utils
from discord.ext import commands

class Assets(commands.Cog):
    """ Assets class """
    def get_cloud_url(self, public_id, res_type='image', add_prefix=True):
        """ get resource url from cdn """
        config(cloud_name='mdf-cdn')

        if add_prefix:
            p_id = f'bronson/{public_id}'
        else:
            p_id = public_id
        return utils.cloudinary_url(f'{p_id}',
                                    resource_type=res_type)[0]

    async def get_random_cloud_url(self, tag):
        """ get random image url from cdn files matching tag """
        data = loads(await self.get_text(
            f'http://res.cloudinary.com/mdf-cdn/image/list/{tag}.json'))
        public_ids = [resource['public_id'] for resource in data['resources']]
        return self.get_cloud_url(choice(public_ids), add_prefix=False)

    async def get_text(self, url):
        """ aiohttp text grabber """
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def get_binary(self, url):
        """ aiohttp binary grabber """
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

async def setup(bot):
    """ add class to bot's cog system"""
    await bot.add_cog(Assets(bot))
