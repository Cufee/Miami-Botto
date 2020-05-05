import discord
from discord.ext import commands, tasks
import os
import csv
from cogs.core_logger.logger import Logger
logger = Logger()


def add_poll_channel(guild_id, channel_id):
    with open(f'{os.getcwd()}/cogs/cmd_poll_channels/guild_settings.csv') as settings:
        readCSV = csv.reader(settings)
        raw_settings = settings


def remove_poll_channel(guild_id, channel_id):
    pass


class poll_channels(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'[Beta] poll_channels cog is ready.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        pass

    # Commands
    @commands.command(hidden=True)
    async def msgremove(self, ctx, option=None):
        pass


def setup(client):
    client.add_cog(poll_channels(client))
