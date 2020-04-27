import discord
import json
from discord.ext import commands, tasks
from cogs.core_logger.logger import Logger
logger = Logger()


class multi_guild(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'multi_guild cog is ready.')

    # @commands.command(aliases=[''])
    # @commands.is_owner()
    # async def command(self):
    #     pass


def setup(client):
    client.add_cog(multi_guild(client))
